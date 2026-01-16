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
# 데이터 로드 + 전처리 (MySQLdb 버전)
# =========================
def load_and_preprocess(conn):
    """
    app.py에서 전달받은 self.conn (MySQLdb connection) 사용
    """
    sql = """
        SELECT
            date,
            charge_type,
            hour,
            kwh
        FROM ev_charge_load
    """

    # MySQLdb connection 그대로 사용
    ev_load = pd.read_sql(sql, conn)

    # 기존 congestion 로직과 컬럼명 맞추기
    ev_load = ev_load.rename(columns={
        "date": "일자",
        "charge_type": "충전방식",
        "kwh": "kWh"
    })

    ev_load["일자"] = pd.to_datetime(ev_load["일자"])
    return ev_load


# =========================
# 혼잡도 기준 테이블 생성
# =========================
def build_congestion_table(ev_load_long):
    """
    시간대 평균 + 분위 기반 혼잡도
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
# 현재 시간 혼잡도 조회
# =========================
def get_current_congestion(congestion_table, charge_type):
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
    ev_load = (
        congestion_table[congestion_table["충전방식"] == charge_type]
        .sort_values("hour")
        .set_index("hour")[["kWh"]]
    )
    return ev_load