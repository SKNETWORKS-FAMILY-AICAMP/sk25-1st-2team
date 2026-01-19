

## 1. 프로젝트 소개
SKN AI Camp 25기 1차 단위프로젝트 2팀의 결과물입니다.

본 프로젝트는 전기차 사용자들에게 필요한 다양한 정보를 통합하여 제공하는 Streamlit 기반 웹 애플리케이션입니다. 전국 전기차 충전소의 위치, 요금, 혼잡도 등 실용적인 정보부터 전기차 관련 FAQ까지 한 곳에서 확인할 수 있도록 하여 사용자의 편의성을 높이는 것을 목표로 합니다.

### 주요 기능
- **전국 충전소 현황:** 지도 기반의 전국 전기차 충전소 위치 시각화
- **전기차 인프라 현황:** 국내 전기차 등록 현황 및 관련 인프라 통계 제공
- **충전소별 요금 정보:** 충전소 운영사별 요금 비교 분석
- **충전소 혼잡도:** 충전소 혼잡도 데이터를 제공하여 효율적인 충전소 선택 지원
- **FAQ:** 전기차와 관련된 자주 묻는 질문과 답변 모음

## 2. 팀 소개
| 직책 | 이름 | GitHub | 역할 |
|:---:|:---:|:---:|:---:|
| 팀장 | 김홍익 | [@아이디](https://github.com/아이디) | 전기차 등록 현황 및 추세 Data 전처리, GitHub Repository 관리 |
| 팀원 | 권가영 | [@Gayoung03](https://github.com/Gayoung03) | BYD 전기차 FAQ Data 크롤링, 충전소 현황 Web 구현 |
| 팀원 | 이근혁 | [@아이디](https://github.com/아이디) | KIA, TESLA 전기차 FAQ Data 크롤링 및 FAQ Web 구현 |
| 팀원 | 전운열 | [@아이디](https://github.com/아이디) | 충전소 회사 별 요금 Data 크롤링 및 Web 구현, 발표 |
| 팀원 | 최원준 | [@아이디](https://github.com/아이디) | 전체 Data URL 검색, 전기차 등록 현황 및 충전소 혼잡도 Data Web 구현 |

## 3. 프로젝트 기간
2026.01.16(금) ~ 2026.01.19(월)

## 4. 기술 스택

- **Language**
  - ![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
- **Framework**
  - ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
- **Libraries**
  - ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
  - ![Folium](https://img.shields.io/badge/Folium-77B829?style=for-the-badge&logo=Leaflet&logoColor=white)
  - ![Streamlit-Folium](https://img.shields.io/badge/Streamlit--Folium-black?style=for-the-badge&logo=Streamlit&logoColor=white)

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

## 6. 프로젝트 구조
```
.\sk25-1st-2team\
├───app.py                 # 메인 애플리케이션 클래스 및 페이지 라우팅
├───main.py                # 애플리케이션 실행 진입점
├───README.md              # 프로젝트 설명 문서
├───requirements.txt       # 프로젝트 의존성 목록
├───sidebar.py             # 사이드바 UI 구성
├───data\                  # 데이터 파일 (CSV)
│   ├───한국전력공사_충전소의 위치 및 현황 정보_20250630.csv
│   └───한국환경공단_전기차 충전소 위치 및 운영정보_20221027.csv
├───mainpages\             # 각 페이지를 구성하는 모듈
│   ├───charge_fee.py      # 충전소 요금 페이지
│   ├───congestion_page.py # 충전소 혼잡도 페이지
│   ├───faq_page.py        # FAQ 페이지
│   ├───infra_page.py      # 전기차 등록 현황 페이지
│   └───map_page.py        # 충전소 현황 지도 페이지
└───utils\
    └───db.py              # 데이터베이스 연결 유틸리티
```

### 전기차 등록 현황

<img width="1675" height="837" alt="image" src="https://github.com/user-attachments/assets/1d8342f2-7114-4307-8aee-cad6c022630d" />
<img width="1656" height="806" alt="image" src="https://github.com/user-attachments/assets/82845760-9604-4a3f-9753-22871977c3e7" />



### 충전소 현황
- **전국 전기차 충전소 현황**
<img src="https://github.com/user-attachments/assets/cad72ce5-855c-4539-99ba-5281d6670d92" width="100%"><br>

한국전력공사와 한국환경공단의 데이터를 결합하여 전국 전기차 충전소의 분포 현황을 지도에 시각화했습니다.<br>
두 기관의 데이터가 모두 존재하는 곳(파란색)과 한전 데이터만 존재하는 곳(회색)을 마커 색상으로 구분하여 정보를 제공합니다.

- **🛠️ 기술적 구현 및 최적화**
  - <small>**동적 파일 경로 탐색**: 실행 환경이 바뀌어도 코드 수정 없이 작동하도록, `os` 라이브러리를 활용해 CSV 파일을 자동으로 로딩합니다.</small>
  - <small>**성능 최적화 (Caching)**</small>
    - <small>`@streamlit.cache_data`: 대용량 데이터프레임 로딩 시간을 줄이기 위해 파일 읽기 결과를 캐싱했습니다.</small>
    - <small>`@streamlit.cache_resource`: 지도 객체 생성 비용을 절감하기 위해 리소스를 캐싱하여 렌더링 속도를 높였습니다.</small>
  - <small>**지도 렌더링 오류 해결**: 지도가 반으로 잘리는 문제를 해결하기 위해, `copy.deepcopy()`를 통해 매번 깨끗한 복사본을 생성했습니다.</small>
  - <small>**시각화 개선 (MarkerCluster)**: 마커가 겹쳐 지저분해지는 문제를 해결하기 위해 `MarkerCluster`를 도입하여 가독성을 높였습니다.</small>


### 충전소 요금
- **평균 충전요금 가장 저렴한 곳 TOP 10**
<img width="1543" height="547" alt="image" src="https://github.com/user-attachments/assets/2b14ebea-d5e2-432e-b717-7d761887acdd" /><br>
충전소 Brand 별로 평균 충전요금을 정렬하였을 때, 요금이 가장 저렴한 업체 10곳의 가격 정보를 막대 그래프 형태로 구현하였습니다.<br>
회원가/비회원가로 구분하여 평균 충전요금을 확인할 수 있습니다.

- **업체별 평균 충전요금 목록**
<img width="1570" height="575" alt="image" src="https://github.com/user-attachments/assets/08308b9c-3d88-4b7a-84f6-0bfab12326fc" /><br>
전체 충전소 Brand의 업체명/전화번호/회원가/비회원가를 정리한 표입니다.<br>
특정 keyword를 이용하여 업체 정보를 검색하거나, 비회원가/회원가/업체명 순서를 이용하여 정보를 재정렬할 수 있습니다.

### 충전소 혼잡도

### FAQ
<img width="1139" height="671" alt="스크린샷 2026-01-19 오전 9 12 11" src="https://github.com/user-attachments/assets/f6d2aac8-5078-4389-9e2b-c80768bfd1a0" />
전기차 대표 브랜드인 테슬라와 BYD 사이트의 FAQ와<br>
국산 전기차를 생산하는 기아의 FAQ에서 전기차 관련된 내용을 모아놓은 자료입니다.<br>
특정 키워드로 질문을 검색하실 수 있습니다. BYD의 경우, 한글로 키워드 검색을 해도 알맞는 영어 질문을 보실 수 있습니다.

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
