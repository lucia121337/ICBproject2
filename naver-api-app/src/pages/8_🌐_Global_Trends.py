import streamlit as st
import pandas as pd
import plotly.express as px
from pytrends.request import TrendReq

st.set_page_config(page_title="Global Trends", page_icon="🌐", layout="wide")

st.title("🌐 구글 검색 트렌드 (Global Trends)")
st.markdown("구글 트렌드(Google Trends) 데이터를 조회하여 특정 키워드의 전 세계/국가별 관심도를 시각화합니다.")

if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.warning("로그인이 필요한 서비스입니다.")
    st.stop()

st.sidebar.header("🔍 검색 설정")
keywords_str = st.sidebar.text_input("검색어 (쉼표로 구분, 최대 5개)", value="Python, Java")
geo = st.sidebar.selectbox("국가 (Geo)", ["", "US", "KR", "JP", "GB"], format_func=lambda x: "전 세계 (Global)" if x == "" else x)
timeframe = st.sidebar.selectbox("기간", ["today 5-y", "today 12-m", "today 3-m", "today 1-m", "now 7-d"])

if st.button("트렌드 조회"):
    keywords = [k.strip() for k in keywords_str.split(",") if k.strip()][:5]
    if not keywords:
        st.error("검색어를 입력해주세요.")
    else:
        with st.spinner("구글 트렌드에서 데이터를 가져오는 중입니다..."):
            try:
                pytrends = TrendReq(hl='ko-KR', tz=540)
                pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo=geo, gprop='')
                df = pytrends.interest_over_time()
                
                if not df.empty:
                    df = df.drop(columns=['isPartial'], errors='ignore')
                    
                    st.success("데이터 조회를 완료했습니다!")
                    st.dataframe(df.tail(10))
                    
                    # 시각화
                    fig = px.line(df, x=df.index, y=keywords, title=f"구글 검색 관심도 변화: {', '.join(keywords)}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("조회된 트렌드 데이터가 없습니다.")
            except Exception as e:
                st.error(f"구글 트렌드 API 호출 중 오류가 발생했습니다: {e}")
