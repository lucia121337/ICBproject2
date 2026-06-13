import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import render_sidebar, get_keyword_list
from utils.api_client import NaverAPIClient
import re

st.set_page_config(page_title="News Search", page_icon="📰", layout="wide")

if not render_sidebar():
    st.stop()

st.title("📰 네이버 뉴스 검색 분석")
st.markdown("입력하신 검색어에 대한 최신 뉴스를 수집하여 분석합니다.")

keywords = get_keyword_list()
# 뉴스 pubDate는 timezone 정보가 포함될 수 있으므로 tz-naive 변환이나 localize가 필요합니다.
start_date = pd.to_datetime(st.session_state.start_date).tz_localize('Asia/Seoul')
end_date = (pd.to_datetime(st.session_state.end_date) + pd.Timedelta(days=1)).tz_localize('Asia/Seoul')

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
                res = client.search_news(kw, display=100)
                items = res.get("items", [])
                
                for item in items:
                    pubdate = item.get("pubDate")
                    if pubdate:
                        try:
                            # RFC 2822 포맷
                            dt = pd.to_datetime(pubdate)
                            if dt.tzinfo is None:
                                dt = dt.tz_localize('Asia/Seoul')
                            else:
                                dt = dt.tz_convert('Asia/Seoul')
                                
                            all_data.append({
                                "Keyword": kw,
                                "Title": clean_html(item.get("title", "")),
                                "Description": clean_html(item.get("description", "")),
                                "Date": dt
                            })
                        except:
                            pass
            
            df = pd.DataFrame(all_data)
            
            if df.empty:
                st.warning("가져온 데이터가 없습니다.")
            else:
                # 기간 필터링
                mask = (df['Date'] >= start_date) & (df['Date'] < end_date)
                filtered_df = df.loc[mask]
                
                if filtered_df.empty:
                    st.warning(f"선택한 기간 내에 작성된 기사가 최근 100건 중에는 없습니다.")
                else:
                    st.success(f"총 {len(filtered_df)}건의 데이터를 필터링했습니다.")
                    
                    # 1. 일자별 기사 수 차트 (날짜 단위로 자르기)
                    filtered_df['DateOnly'] = filtered_df['Date'].dt.date
                    daily_counts = filtered_df.groupby(['DateOnly', 'Keyword']).size().reset_index(name='Count')
                    fig = px.line(daily_counts, x="DateOnly", y="Count", color="Keyword", 
                                 title="일자별/검색어별 뉴스 기사 수 추이", markers=True)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 3. 데이터 원본
                    st.subheader("데이터 상세")
                    display_df = filtered_df.drop(columns=['DateOnly']).copy()
                    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
                    st.dataframe(display_df.sort_values(by="Date", ascending=False), use_container_width=True)
                    
        except Exception as e:
            st.error(f"API 요청 중 오류가 발생했습니다: {e}")
