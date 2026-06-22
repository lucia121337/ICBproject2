# 🚀 범용 데이터 분석 플랫폼 (SaaS형) 확장 구현 계획서

단순 네이버 API 대시보드를 넘어, 다중 데이터 소스 통합, 로그인 기반 구독형/SaaS 기능, 유연한 커스텀 데이터 분석, 그리고 범용 원시 데이터 추출 기능을 모두 아우르는 **종합 범용 데이터 플랫폼**으로 진화하기 위한 그랜드 플랜입니다.

## User Review Required

> [!WARNING]
> **대규모 아키텍처 변경 알림**
> 요청하신 "모든 범용성 요소"를 포함할 경우 프로젝트의 규모가 단순 대시보드에서 **풀스택 데이터 웹 서비스(SaaS)** 수준으로 커지게 됩니다. 
> 
> * **의존성 급증:** 사용자 인증(DB), 구글/유튜브 API, 동적 차트 라이브러리(PyGWalker 등)가 추가됩니다.
> * **사전 준비 필요:** Google Cloud API 키, Supabase(또는 Firebase)와 같은 인증/DB 서버 연동 설정이 필요해집니다.
> 
> 이 모든 기능을 한 번에 도입하는 것에 동의하시나요? 아니면 단계별(Phase 1, 2...)로 나누어 점진적으로 도입하는 것이 좋을까요?

## Open Questions

> [!IMPORTANT]
> 1. **사용자 로그인 및 DB (SaaS화):** Streamlit 환경에서 가장 쉽고 강력한 `Supabase` (또는 Firebase) 연동을 통해 로그인 기능을 구현해도 괜찮으신가요?
> 2. **외부 API 키 관리:** 구글 트렌드, 유튜브 등의 연동을 위해 추가 API 키를 발급받아 환경 변수(`.env`)에 세팅해 주실 수 있나요?

---

## Proposed Changes

### 1. 범용 다중 소스 통합 (확장된 소스 지원)
#### [NEW] [src/pages/8_🌐_Global_Trends.py](file:///c:/Users/user1/Desktop/ICB10/icb10proj2/src/pages/8_%F0%9F%8C%90_Global_Trends.py)
- **Google Trends 연동:** `pytrends` 라이브러리를 활용하여 전 세계/국가별 구글 검색 트렌드 분석 기능 추가.
- **YouTube 트렌드 연동:** YouTube Data API v3를 연동하여 특정 키워드의 관련 인기 영상 및 조회수 트렌드 분석.

### 2. 화이트라벨 / SaaS 형태 (사용자 인증 및 관리)
#### [MODIFY] [src/main.py](file:///c:/Users/user1/Desktop/ICB10/icb10proj2/src/main.py)
- `streamlit-authenticator` 또는 `Supabase` 기반의 **로그인/회원가입 페이지** 도입.
- 로그인한 사용자만 대시보드에 접근할 수 있도록 라우팅 가드(Routing Guard) 추가.
- (옵션) 관리자(Admin)가 부여한 전역 API 키를 사용하여 개별 유저는 API 키를 입력하지 않아도 되게끔 동작 모드 변경.

### 3. 유연한 커스텀 환경 (Data Studio)
#### [NEW] [src/pages/9_📊_Data_Studio.py](file:///c:/Users/user1/Desktop/ICB10/icb10proj2/src/pages/9_%F0%9F%93%8A_Data_Studio.py)
- **CSV/Excel 업로드 기능:** 사용자가 자신의 회사 데이터나 외부 데이터를 직접 업로드 가능.
- **동적 시각화 도구(PyGWalker):** 업로드된 데이터나 기존 검색 결과를 Tableau(태블로)처럼 드래그 앤 드롭으로 자유롭게 시각화하고 커스텀 차트를 만들 수 있는 기능 연동.

### 4. 범용 데이터 추출 도구 (Raw Data API Explorer)
#### [NEW] [src/pages/10_🔌_API_Explorer.py](file:///c:/Users/user1/Desktop/ICB10/icb10proj2/src/pages/10_%F0%9F%94%8C_API_Explorer.py)
- **네이버 만능 호출기:** 파파고(번역), 클로바(음성/비전), 백과사전 등 네이버 OpenAPI의 엔드포인트 URL과 파라미터를 사용자가 직접 입력하고 즉시 JSON 형태의 원시 데이터(Raw data)를 테스트 및 다운로드할 수 있는 샌드박스 페이지.

### 환경 및 패키지 설정
#### [MODIFY] [requirements.txt](file:///c:/Users/user1/Desktop/ICB10/icb10proj2/requirements.txt)
- `pytrends`, `google-api-python-client`, `streamlit-authenticator`, `pygwalker`, `supabase` 등 대규모 패키지 추가.

---

## Verification Plan

### Automated Tests
- 모든 새로운 라이브러리가 로컬 환경에 정상적으로 설치되고 Streamlit이 부팅되는지 확인 (`pip install -r requirements.txt`).

### Manual Verification
- **로그인 테스트:** 회원가입 및 로그인 폼이 동작하고 세션이 유지되는지 확인.
- **Data Studio 테스트:** 임의의 CSV 파일을 업로드하여 PyGWalker 화면이 정상 렌더링되는지 확인.
- **Global Trends 테스트:** 구글 트렌드 연동이 정상적으로 작동하는지 확인.
