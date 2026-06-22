import streamlit as st
import requests
import json
import pandas as pd

st.set_page_config(page_title="API Explorer", page_icon="🔌", layout="wide")

st.title("🔌 네이버 OpenAPI 샌드박스 (API Explorer)")
st.markdown("정해진 대시보드 화면 외에도, 사용자가 원하는 네이버 API 엔드포인트를 직접 호출하고 JSON 원시 데이터(Raw Data)를 확인할 수 있습니다.")

if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.warning("로그인이 필요한 서비스입니다.")
    st.stop()

# 사용자 API 키 가져오기
client_id = st.session_state.get("client_id", "")
client_secret = st.session_state.get("client_secret", "")

st.sidebar.header("🔑 API 인증 정보")
if not client_id or not client_secret:
    st.sidebar.warning("API 키가 설정되지 않았습니다. 메인 화면의 설정 사이드바에서 Client ID와 Secret을 입력해주세요.")
else:
    st.sidebar.success("API 키 로드 완료")

st.subheader("📡 엔드포인트 설정")
col1, col2 = st.columns([1, 4])
method = col1.selectbox("HTTP 메서드", ["GET", "POST"])
endpoint = col2.text_input("요청 URL (Endpoint)", value="https://openapi.naver.com/v1/search/local.json")

st.markdown("---")
st.subheader("⚙️ 파라미터 및 바디 (JSON)")

params_str = st.text_area("파라미터 (GET) 또는 본문 (POST) - JSON 형식으로 입력", 
                          value='{\n    "query": "강남역 맛집",\n    "display": 10\n}', height=150)

if st.button("🚀 API 호출 실행"):
    if not client_id or not client_secret:
        st.error("Client ID와 Secret을 먼저 설정해야 API를 호출할 수 있습니다.")
    else:
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
        
        try:
            payload = json.loads(params_str)
        except json.JSONDecodeError:
            st.error("유효한 JSON 형식이 아닙니다. 파라미터 입력창을 확인해주세요.")
            payload = None
            
        if payload is not None:
            with st.spinner("API 서버와 통신 중입니다..."):
                try:
                    if method == "GET":
                        response = requests.get(endpoint, headers=headers, params=payload)
                    else:
                        headers["Content-Type"] = "application/json"
                        response = requests.post(endpoint, headers=headers, json=payload)
                        
                    response.raise_for_status()
                    data = response.json()
                    
                    st.success(f"상태 코드: {response.status_code}")
                    
                    # 결과를 JSON과 테이블 탭으로 분리하여 표시
                    tab1, tab2 = st.tabs(["JSON 원시 데이터", "테이블 변환 시도"])
                    
                    with tab1:
                        st.json(data)
                        
                        # JSON 다운로드 버튼
                        json_str = json.dumps(data, ensure_ascii=False, indent=2)
                        st.download_button(
                            label="📥 JSON 다운로드",
                            file_name="api_result.json",
                            mime="application/json",
                            data=json_str
                        )
                        
                    with tab2:
                        try:
                            # 일반적으로 리스트 형태의 데이터가 'items' 키 안에 존재함
                            if "items" in data:
                                df = pd.DataFrame(data["items"])
                                st.dataframe(df)
                                
                                # CSV 다운로드 버튼
                                csv = df.to_csv(index=False).encode('utf-8-sig')
                                st.download_button(
                                    label="📥 CSV 다운로드",
                                    data=csv,
                                    file_name='api_result.csv',
                                    mime='text/csv',
                                )
                            else:
                                st.info("테이블로 변환하기 적합한 'items' 리스트 구조가 없습니다.")
                        except Exception as e:
                            st.warning(f"테이블 변환 실패: {e}")
                            
                except requests.exceptions.RequestException as e:
                    st.error(f"API 요청 실패: {e}")
                    if e.response is not None:
                        st.json(e.response.json())
