import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "https://www.yes24.com/Product/Category/BestSeller"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip() if text else ""


def extract_num(text: str) -> str:
    m = re.search(r"[\d.,]+", text)
    return m.group().replace(",", "") if m else ""


def parse_page(html: str, page_no: int) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    items = soup.select("div.item_info")
    records = []

    for rank_offset, item in enumerate(items):
        rank = (page_no - 1) * len(items) + rank_offset + 1

        # 제목 / URL / 상품ID
        name_tag = item.select_one("a.gd_name")
        if not name_tag:
            continue
        title = clean(name_tag.get_text())
        href = name_tag.get("href", "")
        m = re.search(r"/goods/(\d+)", href)
        product_id = m.group(1) if m else ""
        url = f"https://www.yes24.com{href}" if href else ""

        # 분류 ([도서], [외국도서] 등)
        res_tag = item.select_one("span.gd_res")
        category_type = clean(res_tag.get_text()) if res_tag else ""

        # 특이사항 (완결, 초판종료 등)
        features = [clean(f.get_text()) for f in item.select("span.feature")]
        features_str = ", ".join(features)

        # 저자
        auth_tag = item.select_one("span.info_auth")
        author = clean(auth_tag.get_text()) if auth_tag else ""

        # 출판사
        pub_tag = item.select_one("span.info_pub")
        publisher = clean(pub_tag.get_text()) if pub_tag else ""

        # 출판일
        date_tag = item.select_one("span.info_date")
        pub_date = clean(date_tag.get_text()) if date_tag else ""

        # 할인율
        sale_tag = item.select_one("span.txt_sale em.num")
        discount_rate = clean(sale_tag.get_text()) + "%" if sale_tag else "0%"

        # 판매가
        price_tag = item.select_one("strong.txt_num em.yes_b")
        sale_price = clean(price_tag.get_text()) if price_tag else ""

        # 정가
        orig_tag = item.select_one("span.txt_num_original em.yes_b")
        original_price = clean(orig_tag.get_text()) if orig_tag else ""

        # 판매지수
        rating_row = item.select_one("div.info_rating")
        sales_index = ""
        if rating_row:
            m2 = re.search(r"판매지수\s*([\d,]+)", rating_row.get_text())
            sales_index = m2.group(1).replace(",", "") if m2 else ""

        # 평점 (리뷰 총점)
        grade_tag = item.select_one("div.rating_grade") or item.select_one("span.rating_grade")
        rating = ""
        if grade_tag:
            m3 = re.search(r"([\d.]+)$", grade_tag.get_text().strip())
            rating = m3.group(1) if m3 else extract_num(grade_tag.get_text())

        # 리뷰 수
        rv_tag = item.select_one("a.rating_rvCount") or item.select_one("span.rating_rvCount")
        if rv_tag:
            review_count = extract_num(rv_tag.get_text())
        else:
            review_count = "0"

        # 마일리지
        mile_tag = item.select_one("span.gd_mileage") or item.select_one("em.txt_mileage")
        mileage = clean(mile_tag.get_text()) if mile_tag else ""

        records.append({
            "순위": rank,
            "상품ID": product_id,
            "제목": title,
            "분류": category_type,
            "저자": author,
            "출판사": publisher,
            "출판일": pub_date,
            "판매가": sale_price,
            "정가": original_price,
            "할인율": discount_rate,
            "평점": rating,
            "리뷰수": review_count,
            "판매지수": sales_index,
            "특이사항": features_str,
            "마일리지": mileage,
            "URL": url,
        })

    return records


def get_total_pages(html: str) -> int:
    soup = BeautifulSoup(html, "lxml")
    page_links = soup.select("a[href*='PageNumber=']")
    nums = [int(re.search(r"PageNumber=(\d+)", a.get("href", "")).group(1))
            for a in page_links if re.search(r"PageNumber=(\d+)", a.get("href", ""))]
    return max(nums) if nums else 1


def scrape(category_number: str = "001", max_pages: int = None) -> pd.DataFrame:
    print(f"[yes24] 베스트셀러 수집 시작 (카테고리: {category_number})")
    r = requests.get(BASE_URL, headers=HEADERS,
                     params={"CategoryNumber": category_number, "PageNumber": 1}, timeout=15)
    r.raise_for_status()

    total_pages = get_total_pages(r.text)
    if max_pages:
        total_pages = min(total_pages, max_pages)
    print(f"  총 페이지: {total_pages}")

    all_records = parse_page(r.text, 1)
    print(f"  1/{total_pages} 완료 ({len(all_records)}건)")

    for page in range(2, total_pages + 1):
        time.sleep(0.7)
        r = requests.get(BASE_URL, headers=HEADERS,
                         params={"CategoryNumber": category_number, "PageNumber": page}, timeout=15)
        r.raise_for_status()
        records = parse_page(r.text, page)
        all_records.extend(records)
        print(f"  {page}/{total_pages} 완료 ({len(records)}건, 누적: {len(all_records)}건)")

    return pd.DataFrame(all_records)


if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "yes24_bestseller.csv"

    # 1페이지 테스트
    print("=== 1페이지 테스트 ===")
    r = requests.get(BASE_URL, headers=HEADERS,
                     params={"CategoryNumber": "001", "PageNumber": 1}, timeout=15)
    test_records = parse_page(r.text, 1)
    print(f"1페이지 수집 결과: {len(test_records)}건")

    if test_records:
        print("샘플 (첫 3건):")
        for rec in test_records[:3]:
            print(f"  [{rec['순위']}] {rec['제목']} / {rec['저자']} / {rec['출판사']} / "
                  f"{rec['판매가']}원 / 평점:{rec['평점']} / 리뷰:{rec['리뷰수']}")

        print("\n=== 전체 수집 시작 ===")
        df = scrape(category_number="001")
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"\n저장 완료: {output_path}")
        print(f"총 {len(df)}건, 컬럼: {list(df.columns)}")
        print(df.head(5).to_string())
    else:
        print("수집 실패 - HTML 구조 변경 확인 필요")
