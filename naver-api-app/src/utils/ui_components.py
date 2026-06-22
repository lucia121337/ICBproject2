import streamlit as st
from datetime import date, timedelta
from pathlib import Path
from dotenv import load_dotenv
import os

# naver-api-app/.env 명시적 로드
_env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=_env_path, override=True)


def render_sidebar():
    client_id = os.environ.get("NAVER_CLIENT_ID", "").strip()
    client_secret = os.environ.get("NAVER_CLIENT_SECRET", "").strip()

    # Session State 초기화
    if "keywords" not in st.session_state:
        st.session_state.keywords = "파이썬, 자바"
    if "start_date" not in st.session_state:
        st.session_state.start_date = date.today().replace(day=1)
    if "end_date" not in st.session_state:
        st.session_state.end_date = date.today()

    # API 키 상태 표시
    st.sidebar.header("🔑 API 키 상태")
    if client_id and client_secret:
        st.sidebar.success("✅ .env에서 API 키 로드됨")
    else:
        st.sidebar.error("❌ .env에 API 키가 없습니다.\n`naver-api-app/.env` 파일에 값을 입력하세요.")
        st.sidebar.code(
            "NAVER_CLIENT_ID=your_id\nNAVER_CLIENT_SECRET=your_secret",
            language="ini",
        )
        return False

    # 검색 설정
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 검색 설정")
    keywords = st.sidebar.text_input("검색어 (쉼표로 구분)", value=st.session_state.keywords)
    start_date = st.sidebar.date_input("시작일", value=st.session_state.start_date)
    end_date = st.sidebar.date_input("종료일", value=st.session_state.end_date)

    st.session_state.keywords = keywords
    st.session_state.start_date = start_date
    st.session_state.end_date = end_date

    # API 키를 session_state에 저장해 각 페이지에서 사용
    st.session_state.client_id = client_id
    st.session_state.client_secret = client_secret

    return True


def get_keyword_list():
    if "keywords" in st.session_state and st.session_state.keywords:
        return [k.strip() for k in st.session_state.keywords.split(",") if k.strip()]
    return []
