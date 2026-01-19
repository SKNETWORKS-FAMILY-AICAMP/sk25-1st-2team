

## 1. 프로젝트 소개
SKN AI Camp 25기 1차 단위프로젝트 2팀의 결과물입니다.

본 프로젝트는 전기차 사용자들에게 필요한 다양한 정보를 통합하여 제공하는 Streamlit 기반 웹 애플리케이션입니다. 전국 전기차 충전소의 위치, 요금, 혼잡도 등 실용적인 정보부터 전기차 관련 FAQ까지 한 곳에서 확인할 수 있도록 하여 사용자의 편의성을 높이는 것을 목표로 합니다.

### 주요 기능
- **전국 충전소 현황:** 지도 기반의 전국 전기차 충전소 위치 시각화
- **전기차 인프라 현황:** 국내 전기차 등록 현황 및 관련 인프라 통계 제공
- **충전소별 요금 정보:** 충전소 운영사별 요금 비교 분석
- **충전소 혼잡도:** 충전소 혼잡도 데이터를 제공하여 효율적인 충전소 선택 지원
- **전기차 보조금 정보:** 각 지자체의 전기차 보조금 정보 제공
- **FAQ:** 전기차와 관련된 자주 묻는 질문과 답변 모음

<br>

## 2. 팀 소개
| 직책 | 이름 | GitHub | 역할 |
|:---:|:---:|:---:|:---:|
| 팀장 | 김홍익 | [@skidroww](https://github.com/skidroww) | 전기차 등록 현황 및 추세 Data 전처리, GitHub Repository 관리 |
| 팀원 | 권가영 | [@Gayoung03](https://github.com/Gayoung03) | BYD 전기차 FAQ Data 크롤링, 충전소 현황 Web 구현 |
| 팀원 | 이근혁 | [@kookie2626](https://github.com/kookie2626) | KIA,BMW,TESLA 전기차 FAQ Data 크롤링 및 FAQ Web 구현 |
| 팀원 | 전운열 | [@cudaboy](https://github.com/cudaboy) | 충전소 회사 별 요금 Data 크롤링 및 Web 구현, 발표 |
| 팀원 | 최원준 | [@cwj0666](https://github.com/cwj0666) | 전체 Data URL 검색, 전기차 등록 현황·충전소 혼잡도·보조금 Data Web 구현 |

<br>

## 3. 프로젝트 기간
2026.01.16(금) ~ 2026.01.19(월)

<br>

## 4. 기술 스택

- **Language**
  - ![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
- **Framework**
  - ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
- **Libraries**
  - ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
  - ![Folium](https://img.shields.io/badge/Folium-77B829?style=for-the-badge&logo=Leaflet&logoColor=white)
  - ![Streamlit-Folium](https://img.shields.io/badge/Streamlit--Folium-black?style=for-the-badge&logo=Streamlit&logoColor=white)

<br>

## 5. 실행 방법
1. **필요한 라이브러리를 설치합니다.**
   ```bash
   pip install -r requirements.txt 
   # requirements.txt 파일이 없는 경우: pip install streamlit pandas folium streamlit-folium
   ```

2. **Streamlit 애플리케이션을 실행합니다.**
   ```bash
   streamlit run main.py
   ```

<br>

## 6. 프로젝트 내용
### ERD
<img width="1289" height="775" alt="image" src="https://github.com/user-attachments/assets/5817ef28-13fc-403e-b500-535b877d02cd" /><br>


### 자료 구조
```
.\sk25-1st-2team\
├───requirements.txt       # 프로젝트 의존성 목록
├───README.md              # 프로젝트 설명 문서
├───main.py                # 애플리케이션 실행 진입점
├───app.py                 # 메인 애플리케이션 클래스 및 페이지 라우팅
├───sidebar.py             # 사이드바 UI 구성
├───data\                  # 데이터 파일 (CSV)
│   ├───한국전력공사_충전소의 위치 및 현황 정보_20250630.csv
│   └───한국환경공단_전기차 충전소 위치 및 운영정보_20221027.csv
├───mainpages\             # 각 페이지를 구성하는 모듈
│   ├───infra_page.py      # 전기차 등록 현황 페이지
│   ├───map_page.py        # 충전소 현황 지도 페이지
│   ├───charge_fee.py      # 충전소 요금 페이지
│   ├───congestion_page.py # 충전소 혼잡도 페이지
│   ├───subsidy_page.py    # 전기차 보조금 정보 페이지
│   └───faq_page.py        # FAQ 페이지
└───utils\
    └───db.py              # 데이터베이스 연결 유틸리티
```

<br>

### 메인 접속 화면
<img width="1913" height="959" alt="image" src="https://github.com/user-attachments/assets/460aa341-3157-4c37-af35-4ef0c11cea28" />

<br>

### 6-1. 전기차 등록 현황

<img width="1675" height="837" alt="image" src="https://github.com/user-attachments/assets/1d8342f2-7114-4307-8aee-cad6c022630d" />

전국 전기차 등록 현황 데이터를 시각적으로 확인할 수 있는 페이지입니다.
지역별 분포, 차종별 구성, 용도별 현황을 한눈에 파악할 수 있도록 구성하였습니다.

<img width="1656" height="806" alt="image" src="https://github.com/user-attachments/assets/82845760-9604-4a3f-9753-22871977c3e7" />

승용·승합·화물·특수 차량으로 구분하여 차종별 구성 비율을 원형 차트로 표현하였습니다.
사업용 / 비사업용 전기차 등록 현황을 막대 그래프로 제공하여 활용 목적에 따른 분포를 분석할 수 있습니다.

<br>

### 6-2. 충전소 현황
#### 전국 전기차 충전소 현황
한국전력공사와 한국환경공단의 데이터를 결합하여 전국 전기차 충전소의 분포 현황을 지도에 시각화했습니다.<br>
두 기관의 데이터가 모두 존재하는 곳(파란색)과 한전 데이터만 존재하는 곳(회색)을 마커 색상으로 구분하여 정보를 제공합니다.<br>
<img src="https://github.com/user-attachments/assets/cad72ce5-855c-4539-99ba-5281d6670d92" width="100%">
<br>


<img width="649" height="594" alt="image" src="https://github.com/user-attachments/assets/2dfa8068-88fb-463c-9c1d-ae719b8da36e" /><br>

- **🛠️ 기술적 구현 및 최적화**
  - <small>**동적 파일 경로 탐색**: 실행 환경이 바뀌어도 코드 수정 없이 작동하도록, `os` 라이브러리를 활용해 CSV 파일을 자동으로 로딩합니다.</small>
  - <small>**성능 최적화 (Caching)**</small>
    - <small>`@streamlit.cache_data`: 대용량 데이터프레임 로딩 시간을 줄이기 위해 파일 읽기 결과를 캐싱했습니다.</small>
    - <small>`@streamlit.cache_resource`: 지도 객체 생성 비용을 절감하기 위해 리소스를 캐싱하여 렌더링 속도를 높였습니다.</small>
  - <small>**지도 렌더링 오류 해결**: 지도가 반으로 잘리는 문제를 해결하기 위해, `copy.deepcopy()`를 통해 매번 깨끗한 복사본을 생성했습니다.</small>
  - <small>**시각화 개선 (MarkerCluster)**: 마커가 겹쳐 지저분해지는 문제를 해결하기 위해 `MarkerCluster`를 도입하여 가독성을 높였습니다.</small>

<br>

### 6-3. 충전소 요금
#### 평균 충전요금 가장 저렴한 곳 TOP 10
<img width="1543" height="547" alt="image" src="https://github.com/user-attachments/assets/2b14ebea-d5e2-432e-b717-7d761887acdd" /><br>
충전소 Brand 별로 평균 충전요금을 정렬하였을 때, 요금이 가장 저렴한 업체 10곳의 가격 정보를 막대 그래프 형태로 구현하였습니다.<br>
회원가/비회원가로 구분하여 평균 충전요금을 확인할 수 있습니다.

#### 업체별 평균 충전요금 목록
<img width="1570" height="575" alt="image" src="https://github.com/user-attachments/assets/08308b9c-3d88-4b7a-84f6-0bfab12326fc" /><br>
전체 충전소 Brand의 업체명/전화번호/회원가/비회원가를 정리한 표입니다.<br>
특정 keyword를 이용하여 업체 정보를 검색하거나, 비회원가/회원가/업체명 순서를 이용하여 정보를 재정렬할 수 있습니다.

<br>

### 6-4. 충전소 혼잡도
<img width="1603" height="776" alt="스크린샷 2026-01-19 105809" src="https://github.com/user-attachments/assets/5174fd67-dc5e-433f-b9f9-f910c45505f4" />
전기차 충전소의 시간대별 이용 부하(혼잡도)를 시각화한 페이지입니다.  
충전 방식(급속 / 완속)에 따라 하루 24시간 기준 평균 충전량 변화를 확인할 수 있으며,  
사용자는 이를 통해 혼잡 시간대를 파악하고 효율적인 충전 시간을 선택할 수 있습니다.

#### 주요 기능
- 충전 방식 선택  
  급속 및 완속 충전 방식을 선택하여 방식별 이용 패턴을 비교할 수 있습니다.
- 시간대별 혼잡도 표시  
  선택한 시간 기준으로 충전소 혼잡도를 단계별로 제공합니다.
- 시간대별 평균 충전량 시각화  
  0시부터 23시까지의 평균 충전량(kWh)을 선 그래프로 제공하여 충전 수요 변화를 확인할 수 있습니다.

#### 기대 효과
- 혼잡 시간대 회피를 통한 충전 대기 시간 감소
- 사용자 충전 패턴에 맞춘 합리적인 충전 시간 선택 지원

<br>

### 6-5. 전기차 보조금 정보
전국 지자체별 전기차 구매 보조금 현황을 조회할 수 있는 페이지입니다.  
시도 및 시군구 단위로 구분된 데이터를 제공하여 지역별 보조금 차이를 직관적으로 비교할 수 있도록 구성하였습니다.

#### 주요 기능
- 지역 검색  
  시·군·구명을 기준으로 원하는 지역의 보조금 정보를 조회할 수 있습니다.<br>
  승용차 및 초소형 전기차에 대해 지역별 보조금 금액을 표 형태로 제공합니다.<br>
  동일 시도 내 여러 지자체의 보조금 정보를 한 화면에서 비교할 수 있도록 구성했습니다.
<img width="1569" height="700" alt="스크린샷 2026-01-19 105819" src="https://github.com/user-attachments/assets/86d6f7d2-9def-4d76-ad01-18c809660292" />
<br>

<br>

- 차종별 보조금 정보 제공  
  차종 및 차량 브랜드 별로 구분된 지역별 보조금 정보를 표 형태로 정리하였습니다.
<img width="1582" height="410" alt="image" src="https://github.com/user-attachments/assets/21a11ade-7658-45cf-9c06-5b4be1dbb2be" />
<br>

<br>

- 담당 부서 연락처  
  지자체별 담당 부서 및 연락처 정보를 지역별로 구분하여 표 형태로 제공합니다.
<img width="1550" height="567" alt="image" src="https://github.com/user-attachments/assets/fe157fe7-21cc-4ff2-b4c7-4781a2d5abfb" />
<br>

<br>

- 자주 묻는 질문  
  보조금 및 전기차에 대해 자주 묻는 질문을 한 눈에 확인할 수 있도록 구성했습니다.
<img width="1545" height="578" alt="image" src="https://github.com/user-attachments/assets/7fe2b003-7936-46e5-b724-8e08bd82c18a" />
<br>

<br>

#### 기대 효과
- 전기차 구매 전 지역별 보조금 차이에 대한 사전 확인
- 거주 지역 또는 구매 예정 지역에 따른 합리적인 구매 판단 지원

<br>

### 6-6. FAQ
<img width="842" height="854" alt="image" src="https://github.com/user-attachments/assets/1849ed81-f304-4b66-ba8c-86859757d6d9" /><br>
전기차 관련된 FAQ를 볼 수 있는 페이지입니다.<br>
전기차를 생산하는 국내 브랜드(기아)와 해외 브랜드(BMW)의 전기차 관련 FAQ 그리고 전기차 대표 브랜드인 테슬라와 BYD 사이트의 FAQ를 볼 수 있습니다.<br>
<br>
<img width="1550" height="667" alt="image" src="https://github.com/user-attachments/assets/35e4fcaa-fa2a-4178-a86a-5f7356df698b" /><br>
<img width="1561" height="508" alt="image" src="https://github.com/user-attachments/assets/fc9d8bc9-eb47-4141-b6a0-dcaeb4658688" /><br>
특정 키워드로 질문을 검색하실 수 있습니다. BYD의 경우, 한글로 키워드 검색을 해도 알맞는 영어 질문을 보실 수 있습니다.

<br>
<br>

## 7. 데이터 출처

### Public Data
- **전기차 등록 현황 및 추세** (담당: 김홍익)
  - URL: [https://www.data.go.kr/data/15142951/fileData.do](https://www.data.go.kr/data/15142951/fileData.do)
- **충전소 위치 정보** (담당: 권가영)
  - 위치: [https://www.data.go.kr/data/15039545/fileData.do](https://www.data.go.kr/data/15039545/fileData.do)
  - 급속/완속 구분: [https://www.data.go.kr/data/15119741/fileData.do](https://www.data.go.kr/data/15119741/fileData.do)
- **충전소 이용 부하 시간대 안내** (담당: 최원준)
  - URL: [https://www.data.go.kr/data/15039553/fileData.do#tab-layer-file](https://www.data.go.kr/data/15039553/fileData.do#tab-layer-file)

### Web Crawling
- **전기차 충전 요금 정보** (담당: 전운열)
  - 출처: [무공해차 통합누리집](https://chargeinfo.ksga.org/front/statistics/fee)
- **기업별 FAQ** (담당: 이근혁, 권가영)
  - Tesla: https://www.tesla.com/ko_KR/support
  - BYD: https://www.reverautomotive.com/en/faq
  - KIA: https://www.kia.com/kr/customer-service/center/faq
  - BMW: https://www.bmw.co.kr/kr/s/article-search?language=ko&searchKey=전기&hashtags
- **보조금 정보** (담당: 최원준)
  - 출처: [무공해차 통합누리집](https://ev.or.kr/nportal/buySupprt/initSubsidyPaymentCheckAction.do)
 
<br>

## 8. 소감 및 회고
### 김홍익
SK네트웍스 AI 과정 첫 프로젝트여서 의미있는 시간이였습니다. 배웠던 내용들을 활용할 수 있어서 좋았습니다. 좋은 팀원분들을 만나서 좋은 결과물이 나온 것 같습니다.

### 권가영
2주 동안 배운 내용을 프로젝트를 통해 적용해 보니 개념이 확실히 잡혔습니다. Streamlit 이나 크롤링 등은 이전에도 해 본 적이 있었지만 FOLIUM 라이브러리는 처음 배운 개념이었고 그 부분을 담당해 진행할 수 있어서 좋았습니다.
어떻게 하면 지도를 조금 더 효율적으로 띄울 수 있을까 고민을 많이 하였고 해결하는 과정에서 많은 걸 배울 수 있었습니다.
깃을 처음 써본 프로젝트라 걱정이 많이 되었지만 좋은 팀원분들을 만나 순조롭게 잘 진행할 수 있었습니다. 함께 고생하신 팀원분들께 감사 드립니다!

### 이근혁
 첫 프로젝트, 첫 깃 허브 작업이었습니다. 2주 동안 빠르게 지나갔던 과정들을 적용해 볼 수 있는 유의미한 프로젝트였습니다. 모든 게 처음이었지만 팀원들 덕분에 큰 오류 없이 무사히 작업을 완성할 수 있었습니다. 아직 혼자서는 어렵지만 프로젝트 과정을 이해하게 되었고, 어떤 걸 더 공부 해야하는 지 알게 되어 뿌듯한 시간이었습니다.

### 전운열
프로젝트 기간도 짧았고, GitHub 다루는 법, 웹으로 페이지를 구현하는 법, DB 서버에 크롤링한 데이터를 저장하는 방법 등 처음 해보는 작업들이 많았던 것 같습니다. 수업시간에 배웠던 방법을 직접 구현하는 방식이 낯설고 어렵기도 했지만 하나하나 배워나가고 만들어가는 재미가 있었습니다. 또한 적극적으로 소통하면서 열심히 하는 팀원들을 만나서 너무 좋았습니다 :)

### 최원준
이론으로만 배운 내용을 직접 적용해보는 값진 시간이었습니다. 데이터 크롤링 부분에서 조금 헤매는 부분이 있었지만 문제를 해결하는 과정에서 한층 더 성장하는 계기가 되었습니다. 팀원분들과의 의사소통도 원활하여 의미있는 프로젝트가 될 수 있었습니다.
