import sys
sys.stdout.reconfigure(encoding="utf-8")
import requests

url = "https://store.kyobobook.co.kr/api/gw/best/v2/best-seller/online"
params = {
    "page": 1, "per": 50, "saleCmdtClstCode": 33, "soldOutExcludeYn": "N",
    "saleCmdtDsplDvsnCode": "KOR", "period": "002", "dsplDvsnCode": "001",
    "dsplTrgtDvsnCode": "004"
}
headers = {
    "host": "store.kyobobook.co.kr",
    "referer": "https://store.kyobobook.co.kr/category/domestic/33/best?page=1&per=50",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "x-api-gw-key": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..i35xkkCOngvXqCRx.0CqToQel6sj5d0qOS2ftoDu37jRwb0vtQwMBd1e_G1ynl7KUrTrH_qPJnygVpkc0tExt4BUX_pJ4RepB5QsxWmKLjC8tEuMELKG8SvRLEVn6ambMnSmDaJ85mLbGtHcM-zFiDBzi.3y1-RnxGHFxeLNMK2dWZoQ",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-fetch-dest": "empty",
    "accept": "application/json, text/plain, */*",
}

r = requests.get(url, params=params, headers=headers, timeout=15)
print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    books = data.get("data", {}).get("bestSeller", [])
    print("책 수:", len(books))
    if books:
        b = books[0]
        print("첫번째 항목 키:", list(b.keys()))
        p = b.get("product", {})
        pi = p.get("productInfo", {}) if p else {}
        print("productInfo 키:", list(pi.keys()) if pi else "N/A")
        print("샘플:", pi)
else:
    print("응답:", r.text[:500])
