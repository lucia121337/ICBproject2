import sys
sys.stdout.reconfigure(encoding="utf-8")
import requests
import sqlite3
import pandas as pd
import time
from pathlib import Path

API_URL = "https://store.kyobobook.co.kr/api/gw/best/v2/best-seller/online"
HEADERS = {
    "host": "store.kyobobook.co.kr",
    "referer": "https://store.kyobobook.co.kr/category/domestic/33/best?page=1&per=50",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "x-api-gw-key": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..i35xkkCOngvXqCRx."
                    "0CqToQel6sj5d0qOS2ftoDu37jRwb0vtQwMBd1e_G1ynl7KUrTrH_qPJnygVpk"
                    "c0tExt4BUX_pJ4RepB5QsxWmKLjC8tEuMELKG8SvRLEVn6ambMnSmDaJ85mLbG"
                    "tHcM-zFiDBzi.3y1-RnxGHFxeLNMK2dWZoQ",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-fetch-dest": "empty",
    "accept": "application/json, text/plain, */*",
}
BASE_PARAMS = {
    "per": 50,
    "saleCmdtClstCode": 33,
    "soldOutExcludeYn": "N",
    "saleCmdtDsplDvsnCode": "KOR",
    "period": "002",
    "dsplDvsnCode": "001",
    "dsplTrgtDvsnCode": "004",
}


def fetch_page(page: int) -> list[dict]:
    params = {**BASE_PARAMS, "page": page}
    r = requests.get(API_URL, params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    data = r.json()
    return data.get("data", {}).get("bestSeller", [])


def parse_book(item: dict) -> dict:
    pi = item.get("product", {}).get("productInfo", {}) or {}
    price_info = item.get("product", {}).get("priceInfo", {}) or {}
    sale_info = item.get("product", {}).get("saleInfo", {}) or {}
    rating_info = item.get("product", {}).get("ratingInfo", {}) or {}
    author_info = item.get("product", {}).get("authorInfo", {}) or {}

    return {
        "현재순위": item.get("prstRnkn"),
        "이전순위": item.get("frmrRnkn"),
        "기간": item.get("ymw"),
        "상품ID": pi.get("saleCmdtid"),
        "ISBN": pi.get("isbn"),
        "EAN": pi.get("cmdtcode"),
        "제목": pi.get("cmdtName"),
        "부제1": pi.get("sbttName1"),
        "부제2": pi.get("sbttName2"),
        "부제3": pi.get("sbttName3"),
        "저자명": pi.get("chrcName"),
        "저자코드": pi.get("chrcCode"),
        "출판사": pi.get("pbcmName"),
        "출시일": pi.get("rlseDate"),
        "카테고리코드": pi.get("saleCmdtClstCode"),
        "카테고리명": pi.get("saleCmdtClstName"),
        "도서구분코드": pi.get("saleCmdtDvsnCode"),
        "도서구분명": pi.get("saleCmdtDvsnCodeName"),
        "중분류": pi.get("cmdtClstName"),
        "상태코드": pi.get("cmdtCdtnCode"),
        "상태명": pi.get("cmdtCdtnCodeName"),
        "판매상태코드": pi.get("saleCdtnCode"),
        "판매상태명": pi.get("saleCdtnCodeName"),
        "연령제한": pi.get("saleLmttAge"),
        "정가": price_info.get("fixedPrice") or price_info.get("offlineFixedPrice"),
        "판매가": price_info.get("salePrice") or price_info.get("onlineSalePrice"),
        "할인율": price_info.get("discntRate") or price_info.get("onlineDiscntRate"),
        "판매여부": sale_info.get("saleYn"),
        "재고여부": sale_info.get("stckYn"),
        "평점": rating_info.get("avgScrPntg") or rating_info.get("mdScore"),
        "리뷰수": rating_info.get("revwCnt"),
        "URL": f"https://store.kyobobook.co.kr/detail/shop/product/{pi.get('saleCmdtid', '')}",
    }


def scrape_all() -> pd.DataFrame:
    all_records = []
    page = 1
    print("[kyobobook] 베스트셀러 수집 시작")

    while True:
        items = fetch_page(page)
        if not items:
            print(f"  {page}페이지: 데이터 없음 — 수집 종료")
            break
        records = [parse_book(item) for item in items]
        all_records.extend(records)
        print(f"  {page}페이지: {len(records)}건 수집 (누적: {len(all_records)}건)")
        page += 1
        time.sleep(0.5)

    return pd.DataFrame(all_records)


def save_to_sqlite(df: pd.DataFrame, db_path: Path):
    conn = sqlite3.connect(db_path)
    df.to_sql("bestseller", conn, if_exists="replace", index=False)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_rank ON bestseller(현재순위)
    """)
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM bestseller").fetchone()[0]
    conn.close()
    print(f"SQLite 저장 완료: {db_path} ({count}건)")


if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)

    # 1페이지 테스트
    print("=== 1페이지 테스트 ===")
    items = fetch_page(1)
    print(f"수집 건수: {len(items)}")
    if items:
        sample = parse_book(items[0])
        print("샘플 (1위):")
        for k, v in list(sample.items())[:10]:
            print(f"  {k}: {v}")

        print("\n=== 전체 수집 시작 ===")
        df = scrape_all()

        # CSV 저장
        csv_path = data_dir / "kyobobook_bestseller.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"CSV 저장: {csv_path} ({len(df)}건)")

        # SQLite 저장
        db_path = data_dir / "kyobobook_bestseller.db"
        save_to_sqlite(df, db_path)

        print(f"\n총 {len(df)}건, 컬럼 {len(df.columns)}개")
        print("컬럼:", list(df.columns))
        print(df.head(5)[["현재순위", "제목", "저자명", "출판사", "판매가", "평점"]].to_string())
    else:
        print("수집 실패 — API 키 만료 또는 구조 변경")
