import streamlit as st
from utils.ui_components import render_sidebar

st.set_page_config(
    page_title="네이버 API 대시보드",
    page_icon="🟢",
    layout="wide"
)

st.title("🟢 네이버 API 통합 분석 대시보드")
st.markdown("""
이 대시보드는 네이버 OpenAPI를 활용하여 다양한 데이터를 분석하고 시각화합니다.
왼쪽 사이드바에서 **API Key**와 **검색 조건**을 설정한 후, 좌측 메뉴에서 원하는 분석 페이지를 선택해주세요.

### 📋 제공되는 분석 페이지
1. **📈 Search Trend**: 데이터랩 검색어 트렌드
2. **🛍️ Shopping Trend**: 데이터랩 쇼핑분야 트렌드
3. **📝 Blog Search**: 네이버 블로그 검색 및 분석
4. **📰 News Search**: 네이버 뉴스 검색 및 분석
5. **☕ Cafe Search**: 네이버 카페글 검색 및 분석
6. **🛒 Shopping Search**: 네이버 쇼핑 상품 검색 및 분석

---
**💡 팁**: 
- `Client ID`와 `Client Secret`은 [네이버 개발자 센터](https://developers.naver.com/)에서 애플리케이션을 등록하여 발급받을 수 있습니다.
- 검색어는 쉼표(`,`)로 구분하여 여러 개를 동시에 비교할 수 있습니다.
""")

render_sidebar()
