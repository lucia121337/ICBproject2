import streamlit as st
from datetime import date, timedelta
import os
from dotenv import load_dotenv

# 로컬 .env 파일 로드
load_dotenv()

def render_sidebar():
    st.sidebar.header("⚙️ 네이버 API 설정")
    
    # 1. 로컬 환경변수(.env 등)에서 가져오기
    default_client_id = os.environ.get("NAVER_CLIENT_ID", "")
    default_client_secret = os.environ.get("NAVER_CLIENT_SECRET", "")
    
    # 2. 환경변수가 없을 경우 Streamlit Secrets에서 가져오기
    try:
        if not default_client_id and "NAVER_CLIENT_ID" in st.secrets:
            default_client_id = st.secrets["NAVER_CLIENT_ID"]
        if not default_client_secret and "NAVER_CLIENT_SECRET" in st.secrets:
            default_client_secret = st.secrets["NAVER_CLIENT_SECRET"]
    except Exception:
        pass

    # Session State 초기화
    if "client_id" not in st.session_state:
        st.session_state.client_id = default_client_id
    if "client_secret" not in st.session_state:
        st.session_state.client_secret = default_client_secret
    if "keywords" not in st.session_state:
        st.session_state.keywords = "파이썬, 자바"
    if "start_date" not in st.session_state:
        st.session_state.start_date = date.today() - timedelta(days=30)
    if "end_date" not in st.session_state:
        st.session_state.end_date = date.today()

    # 입력 폼 (값이 없을 때만 표시)
    if not st.session_state.client_id:
        client_id = st.sidebar.text_input("Client ID", value=st.session_state.client_id, type="password")
    else:
        client_id = st.session_state.client_id

    if not st.session_state.client_secret:
        client_secret = st.sidebar.text_input("Client Secret", value=st.session_state.client_secret, type="password")
    else:
        client_secret = st.session_state.client_secret
    
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 검색 설정")
    keywords = st.sidebar.text_input("검색어 (쉼표로 구분)", value=st.session_state.keywords)
    
    start_date = st.sidebar.date_input("시작일", value=st.session_state.start_date)
    end_date = st.sidebar.date_input("종료일", value=st.session_state.end_date)
    
    # 상태 업데이트
    st.session_state.client_id = client_id
    st.session_state.client_secret = client_secret
    st.session_state.keywords = keywords
    st.session_state.start_date = start_date
    st.session_state.end_date = end_date
    
    # 유효성 검사 경고
    if not client_id or not client_secret:
        st.sidebar.warning("API 키를 입력해주세요.")
        return False
    return True

def get_keyword_list():
    if "keywords" in st.session_state and st.session_state.keywords:
        return [k.strip() for k in st.session_state.keywords.split(",") if k.strip()]
    return []
