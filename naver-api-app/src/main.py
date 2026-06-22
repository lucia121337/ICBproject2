import streamlit as st
from utils.ui_components import render_sidebar

st.set_page_config(
    page_title="네이버 API 대시보드",
    page_icon="🔍",
    layout="wide"
)

render_sidebar()

st.title("🔍 네이버 OpenAPI 대시보드")
st.markdown("""
왼쪽 사이드바에서 **API 키**와 **검색어**, **기간**을 설정한 후, 좌측 메뉴에서 원하는 분석 페이지를 선택하세요.

### 📋 제공되는 분석 페이지

| 페이지 | 설명 |
|--------|------|
| 📈 **Search Trend** | 데이터랩 검색어 트렌드 — 기간별 상대적 검색량 비교 |
| 🛍️ **Shopping Trend** | 데이터랩 쇼핑 카테고리별 클릭 트렌드 |
| 📝 **Blog Search** | 블로그 검색 결과 수집 및 포스팅 추이 분석 |
| 📰 **News Search** | 뉴스 검색 결과 수집 및 기사 수 추이 분석 |
| ☕ **Cafe Search** | 카페글 검색 결과 수집 및 카페별 분포 분석 |
| 🛒 **Shopping Search** | 쇼핑 상품 검색 및 가격·몰·브랜드 분포 분석 |

---

**💡 API 키 발급 방법**
1. [네이버 개발자 센터](https://developers.naver.com)에 로그인
2. **Application → 애플리케이션 등록** 선택
3. 사용 API에서 **검색**, **데이터랩(검색어트렌드)**, **데이터랩(쇼핑인사이트)** 추가
4. 발급된 **Client ID**와 **Client Secret**을 왼쪽 사이드바에 입력
""")
