import pandas as pd
from datetime import datetime

# =========================
# 혼잡도 메타데이터 (UI용)
# =========================
CONGESTION_META = {
    "혼잡": {
        "label": "혼잡",
        "emoji": "🔴",
        "color": "#d62728",
        "message": "이 시간대는 충전 수요가 비교적 높은 편입니다."
    },
    "보통": {
        "label": "보통",
        "emoji": "🟠",
        "color": "#ff7f0e",
        "message": "이 시간대는 보통 수준의 충전 수요를 보입니다."
    },
    "여유": {
        "label": "여유",
        "emoji": "🟢",
        "color": "#2ca02c",
        "message": "이 시간대는 비교적 여유로운 편입니다."
    }
}

# =========================
# 데이터 로드 + 전처리
# =========================
def load_and_preprocess(file_path):
    """
    CSV 로드 → wide → long 변환
    """
    # 인코딩 안전 처리
    try:
        ev_load = pd.read_csv(file_path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            ev_load = pd.read_csv(file_path, encoding="cp949")
        except UnicodeDecodeError:
            ev_load = pd.read_csv(file_path, encoding="euc-kr")

    ev_load["일자"] = pd.to_datetime(ev_load["일자"])

    hour_cols = [c for c in ev_load.columns if c.endswith("시")]

    ev_load_long = ev_load.melt(
        id_vars=["일자", "충전방식"],
        value_vars=hour_cols,
        var_name="hour",
        value_name="kWh"
    )

    ev_load_long["hour"] = ev_load_long["hour"].str.replace("시", "").astype(int)
    return ev_load_long


# =========================
# 혼잡도 기준 테이블 생성
# =========================
def build_congestion_table(ev_load_long):
    """
    2024년 기준 시간대 평균 + 분위 기반 혼잡도
    """
    hourly_mean = (
        ev_load_long
        .groupby(["충전방식", "hour"])["kWh"]
        .mean()
        .reset_index()
    )

    def assign_level(ev_load):
        q25 = ev_load["kWh"].quantile(0.25)
        q75 = ev_load["kWh"].quantile(0.75)

        def classify(x):
            if x >= q75:
                return "혼잡"
            elif x <= q25:
                return "여유"
            else:
                return "보통"

        ev_load = ev_load.copy()
        ev_load["congestion"] = ev_load["kWh"].apply(classify)
        return ev_load

    return (
        hourly_mean
        .groupby("충전방식", group_keys=False)
        .apply(assign_level)
    )


# =========================
# 현재 시간 혼잡도 조회 (표시용 메타 포함)
# =========================
def get_current_congestion(congestion_table, charge_type):
    """
    서버 현재 시간 기준 혼잡도 반환
    """
    current_hour = datetime.now().hour

    row = congestion_table[
        (congestion_table["충전방식"] == charge_type) &
        (congestion_table["hour"] == current_hour)
    ]

    if row.empty:
        return None

    level = row["congestion"].iloc[0]
    meta = CONGESTION_META[level]

    return {
        "hour": current_hour,
        "charge_type": charge_type,
        "level": level,
        "label": meta["label"],
        "emoji": meta["emoji"],
        "color": meta["color"],
        "message": meta["message"]
    }


# =========================
# Streamlit chart용 시계열 데이터
# =========================
def get_hourly_timeseries(congestion_table, charge_type):
    """
    Streamlit line_chart / area_chart 전용 데이터 반환
    index: hour
    column: kWh
    """
    ev_load = (
        congestion_table[congestion_table["충전방식"] == charge_type]
        .sort_values("hour")
        .set_index("hour")[["kWh"]]
    )
    return ev_load