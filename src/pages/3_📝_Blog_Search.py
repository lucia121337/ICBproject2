import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import render_sidebar, get_keyword_list
from utils.api_client import NaverAPIClient
import re

st.set_page_config(page_title="Blog Search", page_icon="📝", layout="wide")

if not render_sidebar():
    st.stop()

st.title("📝 네이버 블로그 검색 분석")
st.markdown("""
입력하신 검색어에 대한 최신 블로그 글을 수집하여 분석합니다.
*주의: 일반 검색 API는 날짜 범위 필터링을 직접 지원하지 않으므로, 최신순으로 가져온 데이터 중 선택한 기간에 해당하는 데이터만 필터링하여 보여줍니다.*
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
                # 최신 100건 가져오기
                res = client.search_blog(kw, display=100)
                items = res.get("items", [])
                
                for item in items:
                    postdate = item.get("postdate")
                    if postdate:
                        try:
                            dt = pd.to_datetime(postdate, format="%Y%m%d")
                            all_data.append({
                                "Keyword": kw,
                                "Title": clean_html(item.get("title", "")),
                                "Description": clean_html(item.get("description", "")),
                                "Blogger": item.get("bloggername", ""),
                                "Link": item.get("link", ""),
                                "Date": dt
                            })
                        except:
                            pass
            
            df = pd.DataFrame(all_data)
            
            if df.empty:
                st.warning("가져온 데이터가 없습니다.")
            else:
                # 기간 필터링
                mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
                filtered_df = df.loc[mask]
                
                if filtered_df.empty:
                    st.warning(f"선택한 기간({start_date.date()} ~ {end_date.date()}) 내에 작성된 게시글이 최근 100건 중에는 없습니다.")
                else:
                    st.success(f"총 {len(filtered_df)}건의 데이터를 필터링했습니다.")
                    
                    # 1. 일자별 블로그 포스팅 수 차트
                    daily_counts = filtered_df.groupby(['Date', 'Keyword']).size().reset_index(name='Count')
                    fig = px.bar(daily_counts, x="Date", y="Count", color="Keyword", 
                                 title="일자별/검색어별 블로그 포스팅 수", barmode="group")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 2. 블로거 분포 (어떤 블로거가 많이 썼는지)
                    st.subheader("가장 글을 많이 쓴 블로거 Top 10")
                    top_bloggers = filtered_df['Blogger'].value_counts().head(10).reset_index()
                    top_bloggers.columns = ['Blogger', 'Count']
                    fig2 = px.pie(top_bloggers, values='Count', names='Blogger', hole=0.3)
                    st.plotly_chart(fig2, use_container_width=True)
                    
                    # 3. 데이터 원본
                    st.subheader("데이터 상세")
                    display_df = filtered_df.copy()
                    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
                    st.dataframe(display_df, use_container_width=True)
                    
        except Exception as e:
            st.error(f"API 요청 중 오류가 발생했습니다: {e}")
