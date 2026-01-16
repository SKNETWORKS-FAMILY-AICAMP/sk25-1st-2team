import subprocess
import sys
import os

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"{package} not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
        except subprocess.CalledProcessError as e:
            # Streamlit 앱에서는 sys.exit() 대신 st.error()를 사용하는 것이 좋습니다.
            # 하지만 이 함수는 render_map_page 외부에 있으므로 일단 print로 유지합니다.
            print(f"Failed to install {package}. Please install it manually and rerun.")
            sys.exit(1)
    globals()[package] = __import__(package)

# 필요한 라이브러리 설치 및 불러오기
install_and_import("pandas")
install_and_import("folium")
install_and_import("streamlit")
install_and_import("streamlit_folium")

# --- 설정 ---
# 스크립트의 위치를 기준으로 상대 경로 설정
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')
FILE1_PATH = os.path.join(DATA_DIR, '한국전력공사_충전소의 위치 및 현황 정보_20250630.csv')
FILE2_PATH = os.path.join(DATA_DIR, '한국환경공단_전기차 충전소 위치 및 운영정보_20221027.csv')

# 열 이름 매핑
F1_LAT_COL = '위도'
F1_LON_COL = '경도'
F1_NAME_COL = '충전소명'
F1_ADDR_COL = '충전소주소'
F1_ADDR_DETAIL_COL = '상세주소'
F1_HOURS_COL = '이용가능시간'

F2_ADDR_COL = '주소'
F2_MODEL_L_COL = '기종(대)'
F2_MODEL_S_COL = '기종(소)'

# --- 메인 스크립트 ---
def render_map_page(conn):
    streamlit.header("전국 전기차 충전소 현황")

    @streamlit.cache_data
    def load_data():
        print("Reading CSV files...")
        try:
            df1 = pandas.read_csv(FILE1_PATH, encoding='cp949', on_bad_lines='skip')

            # --- 사용자가 제공한 주소를 기반으로 정확한 필터링 ---
            address_to_remove = '강원특별자치도 동해시 이로동 183-2'
            mask = (df1[F1_ADDR_COL] == address_to_remove)
            
            if mask.any():
                print(f"Found and removed {mask.sum()} incorrect data point(s) for address: '{address_to_remove}'")
                df1 = df1[~mask].copy()
            else:
                print(f"Warning: Could not find the incorrect data point to remove for address: '{address_to_remove}'")

            df1.dropna(subset=[F1_LAT_COL, F1_LON_COL], inplace=True)
            # --- 필터링 종료 ---

            df2 = pandas.read_csv(FILE2_PATH, encoding='cp949', on_bad_lines='skip')
            print("Files read successfully.")
            return df1, df2
        except FileNotFoundError as e:
            streamlit.error(f"데이터 파일을 찾을 수 없습니다: {e.filename}")
            return None, None
        except Exception as e:
            streamlit.error(f"데이터 파일을 읽는 중 오류가 발생했습니다: {e}")
            return None, None

    df1, df2 = load_data()

    if df1 is None or df2 is None:
        streamlit.warning("데이터를 불러오지 못해 지도를 표시할 수 없습니다.")
        return

    # df2로부터 기종 정보를 가져오기 위한 룩업 맵 생성
    model_info_map = df2.drop_duplicates(subset=[F2_ADDR_COL]).set_index(F2_ADDR_COL)[[F2_MODEL_L_COL, F2_MODEL_S_COL]].to_dict('index')

    # 지도 생성
    korea_center = [36.5, 127.5]
    m = folium.Map(location=korea_center, zoom_start=7)

    # 지도에 마커 추가
    for _, row in df1.iterrows():
        lat = row[F1_LAT_COL]
        lon = row[F1_LON_COL]
        address = row.get(F1_ADDR_COL, 'N/A')
        detail_address = row.get(F1_ADDR_DETAIL_COL, 'N/A')
        
        popup_html = f"""
        <b>{row.get(F1_NAME_COL, 'N/A')}</b><br>
        <b>주소:</b> {address}<br>
        <b>상세주소:</b> {detail_address}
        """
        icon_color = 'gray'
        icon_symbol = 'charging-station'

        if address in model_info_map:
            icon_color = 'blue'
            model_info = model_info_map[address]
            model_l = model_info.get(F2_MODEL_L_COL, 'N/A')
            model_s = model_info.get(F2_MODEL_S_COL, 'N/A')
            popup_html += f"<br><b>기종(대):</b> {model_l}<br><b>기종(소):</b> {model_s}"
        
        popup_html += f"<br><b>이용시간:</b> {row.get(F1_HOURS_COL, 'N/A')}"

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=icon_color, icon=icon_symbol, prefix='fa')
        ).add_to(m)

    # Streamlit에 지도 표시
    streamlit.write("지도에 충전소 위치가 표시됩니다. 마커를 클릭하여 상세 정보를 확인하세요.")
    
    streamlit_folium.st_folium(m, width='100%', height=600, returned_objects=[])

    with streamlit.expander("범례 보기"):
        streamlit.markdown("""
        - <span style='color:blue; font-weight:bold;'>■ 파란색 마커</span>: 한전 및 환경공단 데이터에 모두 존재 (기종 정보 포함)
        - <span style='color:gray; font-weight:bold;'>■ 회색 마커</span>: 한전 데이터에만 존재
        """, unsafe_allow_html=True)