
import subprocess
import sys
import os
import webbrowser
import tempfile

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"{package} not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError as e:
            sys.exit(f"Failed to install {package}. Please install it manually and rerun.")
    globals()[package] = __import__(package)

# 필요한 라이브러리 설치 및 불러오기
install_and_import("pandas")
install_and_import("folium")

# --- 설정 ---
# 스크립트의 위치를 기준으로 상대 경로 설정
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE1_PATH = os.path.join(SCRIPT_DIR, '한국전력공사_충전소의 위치 및 현황 정보_20250630.csv')
FILE2_PATH = os.path.join(SCRIPT_DIR, '한국환경공단_전기차 충전소 위치 및 운영정보_20221027.csv')

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
def main():
    print("Reading CSV files...")
    try:
        df1 = pandas.read_csv(FILE1_PATH, encoding='cp949', on_bad_lines='skip')

        # --- 사용자가 제공한 주소를 기반으로 정확한 필터링 ---
        address_to_remove = '강원특별자치도 동해시 이로동 183-2'

        # 제거할 행을 식별하기 위한 불리언 마스크 생성
        mask = (df1[F1_ADDR_COL] == address_to_remove)
        
        if mask.any():
            print(f"Found and removed {mask.sum()} incorrect data point(s) for address: '{address_to_remove}'")
            df1 = df1[~mask].copy() # 일치하지 않는 행만 유지
        else:
            print(f"Warning: Could not find the incorrect data point to remove for address: '{address_to_remove}'")

        # 이제 정리된 데이터프레임에서 좌표가 없는 행 삭제
        df1.dropna(subset=[F1_LAT_COL, F1_LON_COL], inplace=True)
        # --- 필터링 종료 ---

        df2 = pandas.read_csv(FILE2_PATH, encoding='cp949', on_bad_lines='skip')
        print("Files read successfully.")
    except Exception as e:
        sys.exit(f"Error reading files: {e}")

    print("Processing model type information...")
    # df2로부터 기종 정보를 가져오기 위한 룩업 맵 생성
    model_info_map = df2.drop_duplicates(subset=[F2_ADDR_COL]).set_index(F2_ADDR_COL)[[F2_MODEL_L_COL, F2_MODEL_S_COL]].to_dict('index')

    print("Creating map...")
    korea_center = [36.5, 127.5]
    m = folium.Map(location=korea_center, zoom_start=7)

    print(f"Adding {len(df1)} markers to the map...")
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
        icon_color = 'gray'  # 중복되지 않는 충전소의 기본 색상
        icon_symbol = 'charging-station'

        # 중복되는 주소인지 확인
        if address in model_info_map:
            icon_color = 'blue'  # 중복되는 충전소의 색상
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

    # 임시 HTML 파일로 저장하고 브라우저에서 열기
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as fp:
            m.save(fp.name)
            print(f"Map saved to temporary file: {fp.name}")
            webbrowser.open(f'file://{os.path.realpath(fp.name)}')
        print("\nMap should now be open in your default web browser.")
        print("Blue markers are overlapping chargers with model info.")
        print("Gray markers are non-overlapping chargers.")

    except Exception as e:
        print(f"Error opening map in browser: {e}")



if __name__ == "__main__":
    main()
