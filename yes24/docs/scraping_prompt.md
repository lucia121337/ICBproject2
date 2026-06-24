## 1) HTTP 요청정보

- **Method**: GET
- **URL**: `https://www.yes24.com/Product/Category/BestSeller?CategoryNumber=001&PageNumber={N}`
- **CategoryNumber**: `001` = 국내도서 종합 베스트셀러
- **PageNumber**: 1, 2, 3 ... (페이지 번호)

## 2) HTTP 헤더정보

```
GET /Product/Category/BestSeller?CategoryNumber=001&PageNumber=1 HTTP/1.1
Host: www.yes24.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ko-KR,ko;q=0.9
```

## 3) Payload 정보

GET 요청이므로 Request Body 없음. 파라미터는 Query String으로 전달.

| 파라미터 | 설명 | 예시 |
|----------|------|------|
| CategoryNumber | 카테고리 코드 (001=국내도서 종합) | `001` |
| PageNumber | 페이지 번호 (1부터 시작) | `1`, `2`, `3` |

## 4) Response (일부)

```html
<li class="goodsList_item">
  <div class="item_info">
    <div class="info_row info_name">
      <a class="gd_name" href="/product/goods/192145622">패밀리 레스토랑 가자. 下</a>
    </div>
    <div class="info_row info_pubGrp">
      <span class="authPub info_auth">와야마 야마 글그림 / 현승희 역</span>
      <span class="authPub info_pub">문학동네</span>
      <span class="authPub info_date">2026년 06월</span>
    </div>
    <div class="info_row info_price">
      <span class="txt_sale"><em class="num">10</em>%</span>
      <strong class="txt_num"><em class="yes_b">15,120</em>원</strong>
    </div>
    <div class="info_row info_rating">
      <span class="gd_rating"><em class="yes_b">9.3</em></span>
      <span class="gd_ratingCount">(리뷰 142개)</span>
    </div>
  </div>
</li>
```

## 5) 한페이지가 성공적으로 수집되는지 확인하기

`yes24/src/scraper.py` 실행 후 `yes24/data/yes24_bestseller.csv` 생성 확인.
