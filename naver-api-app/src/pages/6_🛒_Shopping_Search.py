import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import render_sidebar, get_keyword_list
from utils.api_client import NaverAPIClient
import re

st.set_page_config(page_title="Shopping Search", page_icon="🛒", layout="wide")

if not render_sidebar():
    st.stop()

st.title("🛒 네이버 쇼핑 상품 검색 분석")
st.markdown("""
입력하신 검색어에 대한 최신 상품(쇼핑) 리스트를 수집하여 가격 및 몰(Mall) 분포를 분석합니다.
*(쇼핑 검색 API는 상품의 등록일/수정일 기준 필터링을 지원하지 않아, 정확도/최신순 검색 결과 상위 100건을 대상으로 분석합니다.)*
""")

keywords = get_keyword_list()

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
                # 100건 가져오기
                res = client.search_shopping(kw, display=100)
                items = res.get("items", [])
                
                for item in items:
                    # lprice (최저가)
                    try:
                        price = int(item.get("lprice", 0))
                    except:
                        price = 0
                        
                    all_data.append({
                        "Keyword": kw,
                        "Title": clean_html(item.get("title", "")),
                        "Price": price,
                        "Mall Name": item.get("mallName", ""),
                        "Brand": item.get("brand", ""),
                        "Category 1": item.get("category1", ""),
                        "Category 2": item.get("category2", ""),
                        "Category 3": item.get("category3", ""),
                        "Link": item.get("link", "")
                    })
            
            df = pd.DataFrame(all_data)
            
            if df.empty:
                st.warning("가져온 데이터가 없습니다.")
            else:
                st.success(f"총 {len(df)}건의 상품 데이터를 가져왔습니다.")
                
                # 1. 가격대 분포 (Box plot)
                st.subheader("검색어별 최저가(Price) 분포")
                fig1 = px.box(df, x="Keyword", y="Price", color="Keyword", title="검색어별 가격 분포도")
                st.plotly_chart(fig1, use_container_width=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # 2. 쇼핑몰 입점 수
                    st.subheader("주요 입점 쇼핑몰 Top 10")
                    top_malls = df['Mall Name'].value_counts().head(10).reset_index()
                    top_malls.columns = ['Mall Name', 'Count']
                    fig2 = px.pie(top_malls, values='Count', names='Mall Name', hole=0.3)
                    st.plotly_chart(fig2, use_container_width=True)
                    
                with col2:
                    # 3. 주요 브랜드
                    st.subheader("주요 브랜드 Top 10")
                    brands = df[df['Brand'] != '']['Brand'].value_counts().head(10).reset_index()
                    brands.columns = ['Brand', 'Count']
                    if not brands.empty:
                        fig3 = px.bar(brands, x='Count', y='Brand', orientation='h', title="브랜드별 상품 수")
                        fig3.update_layout(yaxis={'categoryorder':'total ascending'})
                        st.plotly_chart(fig3, use_container_width=True)
                    else:
                        st.info("브랜드 정보가 제공되지 않았습니다.")
                
                # 4. 데이터 원본
                st.subheader("상품 데이터 상세")
                st.dataframe(df, use_container_width=True)
                    
        except Exception as e:
            st.error(f"API 요청 중 오류가 발생했습니다: {e}")
