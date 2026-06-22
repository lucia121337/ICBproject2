import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import render_sidebar
from utils.api_client import NaverAPIClient

st.set_page_config(page_title="Shopping Trend", page_icon="🛍️", layout="wide")

if not render_sidebar():
    st.stop()

st.title("🛍️ 네이버 데이터랩 쇼핑 분야 트렌드")
st.markdown("쇼핑 인사이트 API를 통해 선택한 카테고리의 기간별 클릭 추이를 분석합니다.")

CATEGORIES = {
    "패션의류":     "50000000",
    "패션잡화":     "50000001",
    "화장품/미용":  "50000002",
    "디지털/가전":  "50000003",
    "가구/인테리어":"50000004",
    "출산/육아":    "50000005",
    "식품":         "50000006",
    "스포츠/레저":  "50000007",
    "생활/건강":    "50000008",
    "여가/생활편의":"50000009",
    "면세점":       "50000010",
    "도서":         "50005542",
}

start_date = st.session_state.start_date.strftime("%Y-%m-%d")
end_date = st.session_state.end_date.strftime("%Y-%m-%d")

selected = st.multiselect(
    "카테고리 선택 (복수 선택 가능)",
    options=list(CATEGORIES.keys()),
    default=["패션의류"],
)

if not selected:
    st.warning("카테고리를 하나 이상 선택해주세요.")
    st.stop()

if st.button("분석 실행", type="primary"):
    with st.spinner("네이버 API에서 데이터를 가져오는 중..."):
        client = NaverAPIClient(st.session_state.client_id, st.session_state.client_secret)

        try:
            url = "https://openapi.naver.com/v1/datalab/shopping/categories"
            body = {
                "startDate": start_date,
                "endDate": end_date,
                "timeUnit": "date",
                "category": [
                    {"name": name, "param": [CATEGORIES[name]]}
                    for name in selected
                ],
            }
            res = client._post_request(url, body)
            results = res.get("results", [])

            if not results:
                st.warning("선택한 기간/카테고리에 대한 데이터가 없습니다.")
            else:
                df_list = []
                for item in results:
                    title = item.get("title")
                    for d in item.get("data", []):
                        df_list.append({
                            "Date": d.get("period"),
                            "Ratio": d.get("ratio"),
                            "Category": title,
                        })

                df = pd.DataFrame(df_list)
                df["Date"] = pd.to_datetime(df["Date"])

                st.subheader("카테고리별 클릭 트렌드")
                fig = px.area(
                    df, x="Date", y="Ratio", color="Category",
                    title="기간별 쇼핑 카테고리 클릭 상대적 비율 (최대 100)",
                )
                fig.update_layout(hovermode="x unified")
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("데이터 상세")
                pivot = df.pivot(index="Date", columns="Category", values="Ratio").reset_index()
                pivot["Date"] = pivot["Date"].dt.strftime("%Y-%m-%d")
                st.dataframe(pivot.sort_values("Date", ascending=False), use_container_width=True)

        except Exception as e:
            st.error(f"API 요청 중 오류가 발생했습니다: {e}")
