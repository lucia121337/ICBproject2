import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import render_sidebar, get_keyword_list
from utils.api_client import NaverAPIClient
import re

st.set_page_config(page_title="Cafe Search", page_icon="☕", layout="wide")

if not render_sidebar():
    st.stop()

st.title("☕ 네이버 카페글 검색 분석")
st.markdown("""
입력하신 검색어에 대한 최신 카페글을 수집하여 분석합니다.
""")

keywords = get_keyword_list()
start_date = pd.to_datetime(st.session_state.start_date)
end_date = pd.to_datetime(st.session_state.end_date)

if not keywords:
    st.warning("👈 왼쪽 사이드바에서 검색어를 하나 이상 입력해주세요.")
    st.stop()

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

if st.button("분석 실행", type="primary"):
    with st.spinner("네이버 API에서 데이터를 가져오는 중..."):
        client = NaverAPIClient(st.session_state.client_id, st.session_state.client_secret)
        
        all_data = []
        try:
            for kw in keywords:
                res = client.search_cafearticle(kw, display=100)
                items = res.get("items", [])
                
                for item in items:
                    postdate = item.get("cafeurl") # 카페 URL 파싱 보조
                    date_str = item.get("date") # 카페 API는 date 혹은 postdate 사용 가능, 일반적으로 date는 없음, postdate 확인 불가시 제외할 수도 있음. 카페 API는 'cafename', 'cafeurl' 포함
                    # 공식 문서를 보면, 카페 검색은 date 포맷이 일정하지 않을 수 있음. 
                    # 블로그와 마찬가지로 date 필드가 제공되지 않을 경우 패스하거나 다른 필드 사용.
                    # 여기서는 안전하게 Pandas가 파싱할 수 있는지 확인
                    # 네이버 카페글 검색은 보통 'cafename', 'cafeurl', 'title', 'description' 제공
                    # 날짜 데이터가 없다면 임의로 오늘 날짜를 쓰거나 스킵하지 않고 날짜 필드(없을경우 오늘로)를 채울 수 있음. (단순화)
                    
                    # 검색 결과에서 날짜 필드가 명시되어 있지 않은 경우가 많습니다.
                    # 본 대시보드에서는 검색 기능에 초점을 맞춥니다.
                    all_data.append({
                        "Keyword": kw,
                        "Title": clean_html(item.get("title", "")),
                        "Description": clean_html(item.get("description", "")),
                        "Cafe Name": item.get("cafename", ""),
                        "URL": item.get("cafeurl", "")
                    })
            
            df = pd.DataFrame(all_data)
            
            if df.empty:
                st.warning("가져온 데이터가 없습니다.")
            else:
                st.success(f"총 {len(df)}건의 최신 카페글 데이터를 가져왔습니다. (카페글 검색은 날짜 제공이 제한적일 수 있어 최근 100건 위주로 보여줍니다.)")
                
                # 1. 어떤 카페에서 가장 많이 언급되었는지
                st.subheader("가장 글이 많이 올라온 카페 Top 10")
                top_cafes = df['Cafe Name'].value_counts().head(10).reset_index()
                top_cafes.columns = ['Cafe Name', 'Count']
                fig = px.bar(top_cafes, x='Cafe Name', y='Count', color='Cafe Name', title="주요 카페 분포")
                st.plotly_chart(fig, use_container_width=True)
                
                # 2. 데이터 원본
                st.subheader("데이터 상세")
                st.dataframe(df, use_container_width=True)
                    
        except Exception as e:
            st.error(f"API 요청 중 오류가 발생했습니다: {e}")
