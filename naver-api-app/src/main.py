import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from utils.ui_components import render_sidebar

st.set_page_config(
    page_title="범용 데이터 분석 플랫폼",
    page_icon="🌐",
    layout="wide"
)

# 사용자 인증 설정
with open('auth_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# 로그인 위젯 랜더링
try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state["authentication_status"]:
    st.sidebar.write(f'환영합니다, *{st.session_state["name"]}* 님!')
    authenticator.logout('로그아웃', 'sidebar')
    
    st.title("🌐 범용 데이터 분석 플랫폼 (SaaS)")
    st.markdown("""
    이 대시보드는 네이버 OpenAPI 뿐만 아니라, 구글 트렌드, 커스텀 데이터 분석 기능 등을 제공하는 통합 데이터 분석 플랫폼입니다.
    왼쪽 사이드바에서 **설정**을 확인한 후, 좌측 메뉴에서 원하는 분석 페이지를 선택해주세요.
    
    ### 📋 제공되는 분석 페이지
    1. **📈 Search Trend**: 데이터랩 검색어 트렌드
    2. **🛍️ Shopping Trend**: 데이터랩 쇼핑분야 트렌드
    3. **📝 Blog Search**: 네이버 블로그 검색 및 분석
    4. **📰 News Search**: 네이버 뉴스 검색 및 분석
    5. **☕ Cafe Search**: 네이버 카페글 검색 및 분석
    6. **🛒 Shopping Search**: 네이버 쇼핑 상품 검색 및 분석
    7. **☁️ Text Analysis**: 형태소 분석 및 워드클라우드 (신규 추가 예정)
    8. **🌐 Global Trends**: 구글 트렌드 연동 글로벌 검색 (신규)
    9. **📊 Data Studio**: 커스텀 데이터(CSV) 업로드 및 자유 시각화 (신규)
    10. **🔌 API Explorer**: 원시 데이터 다용도 호출 및 추출기 (신규)
    
    ---
    **💡 팁**: 데모 모드에서는 별도의 API 키 없이 테스트 데이터를 시각화할 수 있습니다.
    """)
    
    render_sidebar()

elif st.session_state["authentication_status"] is False:
    st.error('아이디/비밀번호가 올바르지 않습니다.')
elif st.session_state["authentication_status"] is None:
    st.warning('플랫폼을 이용하시려면 로그인이 필요합니다. (데모계정: admin / admin123)')
