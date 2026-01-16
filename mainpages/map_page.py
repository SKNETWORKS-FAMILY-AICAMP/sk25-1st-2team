import os
import unicodedata
import pandas
import folium
import streamlit
import streamlit_folium
import copy
from folium.plugins import MarkerCluster

# --- 설정 ---
# 현재 스크립트 파일의 위치를 기준으로 'data' 폴더의 경로를 설정합니다.
# 이렇게 하면 어떤 위치에서 스크립트를 실행하더라도 파일 경로가 올바르게 지정됩니다.
# os.path.abspath(__file__)는 현재 파일의 절대 경로를 반환합니다.
# os.path.dirname()은 해당 경로의 디렉토리 부분을 반환합니다.
# 'mainpages' 폴더 안에 있으므로, '..'를 사용하여 상위 디렉토리(프로젝트 루트)로 이동한 후 'data' 폴더를 지정합니다.
CURRENT_SCRIPT_PATH = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_SCRIPT_PATH))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

def find_file_by_keyword(directory, keyword):
    """지정된 디렉토리에서 키워드를 포함하는 첫 번째 파일의 전체 경로를 반환합니다."""
    try:
        # 키워드를 NFC 형식으로 정규화
        normalized_keyword = unicodedata.normalize('NFC', keyword)
        for filename in os.listdir(directory):
            # 파일 이름을 NFC 형식으로 정규화
            normalized_filename = unicodedata.normalize('NFC', filename)
            if normalized_keyword in normalized_filename and normalized_filename.endswith('.csv'):
                return os.path.join(directory, filename)
    except FileNotFoundError:
        return None
    return None

# 키워드로 동적으로 파일 경로 찾기
FILE1_PATH = find_file_by_keyword(DATA_DIR, '한국전력공사')
FILE2_PATH = find_file_by_keyword(DATA_DIR, '한국환경공단')

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

# --- 데이터 로딩 및 지도 생성 함수 ---

@streamlit.cache_data
def load_data(file1, file2):
    """CSV 파일들을 읽어 데이터프레임으로 반환합니다. (데이터 캐싱)"""
    print("Reading CSV files...")
    try:
        df1 = pandas.read_csv(file1, encoding='cp949', on_bad_lines='skip')

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

        df2 = pandas.read_csv(file2, encoding='cp949', on_bad_lines='skip')
        print("Files read successfully.")
        return df1, df2
    except FileNotFoundError as e:
        streamlit.error(f"데이터 파일을 찾을 수 없습니다: {e.filename}")
        return None, None
    except Exception as e:
        streamlit.error(f"데이터 파일을 읽는 중 오류가 발생했습니다: {e}")
        return None, None

@streamlit.cache_resource
def generate_map(_df1, _df2):
    """데이터프레임을 기반으로 Folium 지도 객체를 생성합니다. (리소스 캐싱)"""
    print("Generating map from scratch...")
    # df2에서 중복 주소를 제거하고 필요한 열만 선택
    df2_unique = _df2.drop_duplicates(subset=[F2_ADDR_COL])[[F2_ADDR_COL, F2_MODEL_L_COL, F2_MODEL_S_COL]]

    # df1과 df2_unique를 주소 기준으로 left join
    merged_df = pandas.merge(
        _df1,
        df2_unique,
        left_on=F1_ADDR_COL,
        right_on=F2_ADDR_COL,
        how='left'
    )

    # --- itertuples() 에러 방지를 위해 컬럼명 변경 ---
    sanitized_l_col = '기종_대'
    sanitized_s_col = '기종_소'
    merged_df.rename(columns={
        F2_MODEL_L_COL: sanitized_l_col,
        F2_MODEL_S_COL: sanitized_s_col
    }, inplace=True)
    # -----------------------------------------

    # 지도 생성
    korea_center = [36.5, 127.5]
    m = folium.Map(location=korea_center, zoom_start=7)

    # 성능 향상을 위해 MarkerCluster 사용
    marker_cluster = MarkerCluster().add_to(m)

    # itertuples()를 사용하여 반복 성능 향상
    for row in merged_df.itertuples(index=False):
        lat = getattr(row, F1_LAT_COL)
        lon = getattr(row, F1_LON_COL)
        address = getattr(row, F1_ADDR_COL, 'N/A')
        detail_address = getattr(row, F1_ADDR_DETAIL_COL, 'N/A')
        
        popup_html = f"""
        <b>{getattr(row, F1_NAME_COL, 'N/A')}</b><br>
        <b>주소:</b> {address}<br>
        <b>상세주소:</b> {detail_address}
        """
        
        icon_symbol = 'charging-station'

        # 조인된 데이터(기종 정보)가 있는지 확인 (NaN이 아닌지 체크)
        model_l_val = getattr(row, sanitized_l_col, None)
        model_s_val = getattr(row, sanitized_s_col, None)

        if pandas.notna(model_l_val) or pandas.notna(model_s_val):
            icon_color = 'blue'
            model_l = model_l_val or 'N/A'
            model_s = model_s_val or 'N/A'
            popup_html += f"<br><b>기종(대):</b> {model_l}<br><b>기종(소):</b> {model_s}"
        else:
            icon_color = 'gray'
        
        popup_html += f"<br><b>이용시간:</b> {getattr(row, F1_HOURS_COL, 'N/A')}"

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=icon_color, icon=icon_symbol, prefix='fa')
        ).add_to(marker_cluster)
    
    return m

# --- 메인 스크립트 ---
def render_map_page(conn):
    """메인 페이지를 렌더링하는 함수"""
    # 파일 경로가 제대로 찾아졌는지 먼저 확인
    if not FILE1_PATH or not FILE2_PATH:
        streamlit.error(
            f"데이터 폴더('{DATA_DIR}')에서 '한국전력공사' 또는 '한국환경공단' 키워드가 포함된 CSV 파일을 찾을 수 없습니다. "
            "streamlit을 실행하는 위치에 'data' 폴더가 있는지, 그 안에 파일이 있는지 확인해주세요."
        )
        return

    streamlit.header("전국 전기차 충전소 현황")

    # 캐시된 함수를 통해 데이터 로딩
    df1, df2 = load_data(FILE1_PATH, FILE2_PATH)

    if df1 is None or df2 is None:
        streamlit.warning("데이터를 불러오지 못해 지도를 표시할 수 없습니다.")
        return

    # 캐시된 원본 지도 객체를 가져옴
    cached_map = generate_map(df1, df2)

    # 화면에 렌더링할 때는 원본의 깊은 복사본을 사용
    m = copy.deepcopy(cached_map)

    # Streamlit에 지도 표시
    streamlit.write("지도에 충전소 위치가 표시됩니다. 마커를 클릭하여 상세 정보를 확인하세요.")
    streamlit_folium.st_folium(m, width='100%', height=600, returned_objects=[])

    with streamlit.expander("범례 보기"):
        streamlit.markdown("""
        - <span style='color:blue; font-weight:bold;'>■ 파란색 마커</span>: 한전 및 환경공단 데이터에 모두 존재 (기종 정보 포함)
        - <span style='color:gray; font-weight:bold;'>■ 회색 마커</span>: 한전 데이터에만 존재
        """, unsafe_allow_html=True)
