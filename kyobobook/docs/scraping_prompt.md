## 1) HTTP 요청정보

- **Method**: GET
- **URL**: `https://store.kyobobook.co.kr/category/domestic/33/best?page={N}&per=50`
- **page**: 페이지 번호 (1부터 시작)
- **per**: 페이지당 결과 수 (50 고정)

## 2) HTTP 헤더정보

```
GET /category/domestic/33/best?page=1&per=50 HTTP/1.1
Host: store.kyobobook.co.kr
Referer: https://store.kyobobook.co.kr/category/domestic/33/best?page=1&per=50
sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
sec-ch-ua-platform-version: "26.5.1"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36
x-api-gw-key: eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..i35xkkCOngvXqCRx.0CqToQel6sj5d0qOS2ftoDu37jRwb0vtQwMBd1e_G1ynl7KUrTrH_qPJnygVpkc0tExt4BUX_pJ4RepB5QsxWmKLjC8tEuMELKG8SvRLEVn6ambMnSmDaJ85mLbGtHcM-zFiDBzi.3y1-RnxGHFxeLNMK2dWZoQ
```

## 3) Payload 정보

GET 요청이므로 Request Body 없음. 파라미터는 Query String으로 전달.

| 파라미터 | 설명 | 예시 |
|----------|------|------|
| page | 페이지 번호 | `1`, `2`, `3` |
| per | 페이지당 결과 수 | `50` |

**참고**: `x-api-gw-key`는 세션 기반 JWT 토큰으로 만료될 수 있음. 갱신 필요 시 브라우저 DevTools에서 재발급.

## 4) Response (일부)

JSON 형식 응답 예상. 실제 응답 확인 후 업데이트 필요.

## 5) 한페이지가 성공적으로 수집되는지 확인하기

`kyobobook/src/scraper.py` 실행 후 `kyobobook/data/kyobobook_bestseller.csv` 생성 확인.
