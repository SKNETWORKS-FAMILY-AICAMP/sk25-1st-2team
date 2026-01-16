import pandas as pd
import streamlit as st
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
# 데이터 로드 + 전처리 (MySQLdb self.conn 사용)
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

    ev_load = pd.read_sql(sql, conn)

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
    hourly_mean = (
        ev_load_long
        .groupby(["충전방식", "hour"])["kWh"]
        .mean()
        .reset_index()
    )

    def assign_level(df):
        q25 = df["kWh"].quantile(0.25)
        q75 = df["kWh"].quantile(0.75)

        def classify(x):
            if x >= q75:
                return "혼잡"
            elif x <= q25:
                return "여유"
            else:
                return "보통"

        df = df.copy()
        df["congestion"] = df["kWh"].apply(classify)
        return df

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
# Streamlit 페이지 엔트리 함수
# =========================
def render_congestion_page(conn):
    st.title("⚡ 시간대별 충전 혼잡도")

    # 데이터 로드
    ev_load_long = load_and_preprocess(conn)

    if ev_load_long.empty:
        st.warning("혼잡도 데이터가 없습니다.")
        return

    congestion_table = build_congestion_table(ev_load_long)

    # 충전방식 선택
    charge_type = st.selectbox(
        "충전 방식 선택",
        sorted(ev_load_long["충전방식"].unique())
    )

    # 현재 혼잡도
    current = get_current_congestion(congestion_table, charge_type)

    if current:
        st.metric(
            label=f"{current['hour']}시 혼잡도",
            value=f"{current['emoji']} {current['label']}",
            help=current["message"]
        )

    # 시간대별 차트
    st.subheader("시간대별 평균 충전량 (kWh)")
    chart_df = (
        congestion_table[congestion_table["충전방식"] == charge_type]
        .sort_values("hour")
        .set_index("hour")[["kWh"]]
    )

    st.line_chart(chart_df)
