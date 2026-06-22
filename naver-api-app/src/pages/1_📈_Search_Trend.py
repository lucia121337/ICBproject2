import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import render_sidebar, get_keyword_list
from utils.api_client import NaverAPIClient

st.set_page_config(page_title="Search Trend", page_icon="📈", layout="wide")

if not render_sidebar():
    st.stop()

st.title("📈 네이버 데이터랩 검색어 트렌드")
st.markdown("입력하신 검색어들의 기간별 네이버 검색량 트렌드를 비교 분석합니다.")

keywords = get_keyword_list()
start_date = st.session_state.start_date.strftime("%Y-%m-%d")
end_date = st.session_state.end_date.strftime("%Y-%m-%d")

if not keywords:
    st.warning("👈 왼쪽 사이드바에서 검색어를 하나 이상 입력해주세요.")
    st.stop()

if st.button("분석 실행", type="primary"):
    with st.spinner("네이버 API에서 데이터를 가져오는 중..."):
        client = NaverAPIClient(st.session_state.client_id, st.session_state.client_secret)
        
        try:
            res = client.get_datalab_search_trend(start_date, end_date, keywords)
            results = res.get("results", [])
            
            if not results:
                st.warning("선택한 기간/검색어에 대한 데이터가 없습니다.")
            else:
                # 데이터를 DataFrame으로 변환
                df_list = []
                for item in results:
                    group_name = item.get("title")
                    data = item.get("data", [])
                    for d in data:
                        df_list.append({
                            "Date": d.get("period"),
                            "Ratio": d.get("ratio"),
                            "Keyword": group_name
                        })
                
                df = pd.DataFrame(df_list)
                
                if df.empty:
                    st.warning("가져온 데이터가 비어있습니다.")
                else:
                    df['Date'] = pd.to_datetime(df['Date'])
                    
                    st.subheader("검색어별 트렌드 비교")
                    fig = px.line(df, x="Date", y="Ratio", color="Keyword", 
                                  markers=True, title="기간별 검색량 상대적 비율 (최대 100)")
                    fig.update_layout(hovermode="x unified")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.subheader("데이터 상세")
                    # Pivot table 형태로 변환하여 보기 좋게 표시
                    pivot_df = df.pivot(index='Date', columns='Keyword', values='Ratio').reset_index()
                    pivot_df['Date'] = pivot_df['Date'].dt.strftime('%Y-%m-%d')
                    st.dataframe(pivot_df.sort_values(by="Date", ascending=False), use_container_width=True)
                    
        except Exception as e:
            st.error(f"API 요청 중 오류가 발생했습니다: {e}")
