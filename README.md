# 🟢 네이버 API 통합 분석 대시보드

네이버 OpenAPI를 활용하여 다양한 데이터를 분석하고 시각화하는 웹 대시보드 프로젝트입니다.

## 🔗 대시보드 접속 주소
**Streamlit Cloud 배포 완료**: [https://icbproject2-wkq3kappwwu6uja79bsgnr3.streamlit.app](https://icbproject2-wkq3kappwwu6uja79bsgnr3.streamlit.app)

## 📋 제공 기능
1. **📈 Search Trend**: 데이터랩 검색어 트렌드 분석
2. **🛍️ Shopping Trend**: 데이터랩 쇼핑분야 트렌드 분석
3. **📝 Blog Search**: 네이버 블로그 검색 및 분석
4. **📰 News Search**: 네이버 뉴스 검색 및 분석
5. **☕ Cafe Search**: 네이버 카페글 검색 및 분석
6. **🛒 Shopping Search**: 네이버 쇼핑 상품 검색 및 분석

## 🛠️ 기술 스택
- **언어**: Python 3.10+
- **웹 프레임워크**: Streamlit
- **데이터 처리 & 시각화**: Pandas, Plotly
- **인프라 & 배포**: Docker, Streamlit Community Cloud

## 🚀 최근 작업 내역 (업데이트 로그)
- **UI 및 편의성 개선**: 
  - 사이드바 네이버 API 키(Client ID, Secret) 입력창 구현 및 자동 숨김 처리 (값이 설정되면 입력창 숨김).
- **프로젝트 구조 최적화**: 
  - 소스코드 및 문서들을 프로젝트 최상위 폴더로 이동하여 구조 평탄화.
- **환경 변수 지원**: 
  - `python-dotenv` 패키지 추가 및 `.env.example` 템플릿 생성 적용.
- **배포 환경 구축**: 
  - 컨테이너 환경에서 배포 가능하도록 `Dockerfile`, `.dockerignore`, `docker-compose.yml` 추가.
  - Streamlit Community Cloud 연동 배포.

## ⚙️ 로컬 실행 방법

**1. 환경 변수 설정**
프로젝트 최상위 디렉토리에 `.env` 파일을 생성하고 네이버 개발자 센터에서 발급받은 키를 입력합니다.
```env
NAVER_CLIENT_ID=여러분의_클라이언트_ID
NAVER_CLIENT_SECRET=여러분의_클라이언트_시크릿
```

**2. 패키지 설치 및 실행**
```bash
pip install -r requirements.txt
streamlit run src/main.py
```

**3. (선택) Docker 환경에서 실행**
```bash
docker-compose up -d --build
```
