import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import render_sidebar
from utils.api_client import NaverAPIClient

st.set_page_config(page_title="Shopping Trend", page_icon="🛍️", layout="wide")

if not render_sidebar():
    st.stop()

st.title("🛍️ 네이버 데이터랩 쇼핑 분야 트렌드")
st.markdown("""
쇼핑 인사이트 API는 특정 **카테고리(분야)**의 클릭 추이를 제공합니다. 
원하시는 쇼핑 카테고리 코드를 입력하여 해당 분야의 기간별 트렌드를 확인해보세요.
* 주요 카테고리 코드 예시: 
  - 패션의류: `50000000`
  - 패션잡화: `50000001`
  - 화장품/미용: `50000002`
  - 디지털/가전: `50000003`
  - 가구/인테리어: `50000004`
""")

start_date = st.session_state.start_date.strftime("%Y-%m-%d")
end_date = st.session_state.end_date.strftime("%Y-%m-%d")

col1, col2 = st.columns(2)
with col1:
    category_name = st.text_input("카테고리명 (표시용)", value="패션의류")
with col2:
    category_param = st.text_input("카테고리 코드", value="50000000")

if st.button("분석 실행", type="primary"):
    with st.spinner("네이버 API에서 데이터를 가져오는 중..."):
        client = NaverAPIClient(st.session_state.client_id, st.session_state.client_secret)
        
        try:
            res = client.get_datalab_shopping_trend(start_date, end_date, category_name, category_param)
            results = res.get("results", [])
            
            if not results:
                st.warning("선택한 기간/카테고리에 대한 데이터가 없습니다.")
            else:
                df_list = []
                for item in results:
                    title = item.get("title")
                    data = item.get("data", [])
                    for d in data:
                        df_list.append({
                            "Date": d.get("period"),
                            "Ratio": d.get("ratio"),
                            "Category": title
                        })
                
                df = pd.DataFrame(df_list)
                
                if df.empty:
                    st.warning("가져온 데이터가 비어있습니다.")
                else:
                    df['Date'] = pd.to_datetime(df['Date'])
                    
                    st.subheader(f"'{category_name}' 분야 클릭량 트렌드")
                    fig = px.area(df, x="Date", y="Ratio", color="Category", 
                                  title="기간별 쇼핑 카테고리 클릭 상대적 비율 (최대 100)")
                    fig.update_layout(hovermode="x unified")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.subheader("데이터 상세")
                    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
                    
        except Exception as e:
            st.error(f"API 요청 중 오류가 발생했습니다: {e}")
