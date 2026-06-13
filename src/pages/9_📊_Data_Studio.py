import streamlit as st
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer

st.set_page_config(page_title="Data Studio", page_icon="📊", layout="wide")

st.title("📊 커스텀 데이터 스튜디오 (Data Studio)")
st.markdown("사용자의 데이터셋(CSV/Excel)을 직접 업로드하여, Tableau와 같은 유연한 환경에서 데이터를 자유롭게 시각화하고 분석할 수 있습니다.")

if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.warning("로그인이 필요한 서비스입니다.")
    st.stop()

uploaded_file = st.file_uploader("분석할 CSV 파일을 업로드하세요", type=["csv", "xlsx"])

@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)
        st.success(f"파일 업로드 성공! ({len(df)}행 데이터)")
        
        with st.expander("원본 데이터 미리보기"):
            st.dataframe(df.head(100))
            
        st.subheader("🎨 데이터 시각화 보드")
        st.markdown("원하는 필드를 드래그 앤 드롭하여 차트를 구성해보세요.")
        
        # PyGWalker 렌더러 생성 (캐싱 적용 권장이나 streamlit 환경에서는 Renderer 인스턴스화 필요)
        renderer = StreamlitRenderer(df, spec="./gw_config.json")
        renderer.explorer()

    except Exception as e:
        st.error(f"데이터를 불러오거나 시각화하는 중 오류가 발생했습니다: {e}")
else:
    st.info("여기에 파일을 드롭하여 분석을 시작하세요.")
