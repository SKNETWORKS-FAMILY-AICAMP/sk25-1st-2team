# congestion.py
import pandas as pd
from datetime import datetime

def load_and_preprocess(file_path):
    df = pd.read_csv(file_path)
    df["일자"] = pd.to_datetime(df["일자"])

    hour_cols = [c for c in df.columns if c.endswith("시")]

    df_long = df.melt(
        id_vars=["일자", "충전방식"],
        value_vars=hour_cols,
        var_name="hour",
        value_name="load"
    )

    df_long["hour"] = df_long["hour"].str.replace("시", "").astype(int)
    return df_long


def build_congestion_table(df_long):
    hourly_mean = (
        df_long
        .groupby(["충전방식", "hour"])["load"]
        .mean()
        .reset_index()
    )

    def assign_level(df):
        q25 = df["load"].quantile(0.25)
        q75 = df["load"].quantile(0.75)

        def classify(x):
            if x >= q75:
                return "혼잡"
            elif x <= q25:
                return "여유"
            else:
                return "보통"

        df = df.copy()
        df["congestion"] = df["load"].apply(classify)
        return df

    return (
        hourly_mean
        .groupby("충전방식", group_keys=False)
        .apply(assign_level)
    )


def get_current_congestion(congestion_table, charge_type):
    current_hour = datetime.now().hour

    row = congestion_table[
        (congestion_table["충전방식"] == charge_type) &
        (congestion_table["hour"] == current_hour)
    ]

    message_map = {
        "혼잡": "이 시간대는 충전 수요가 비교적 높은 편입니다.",
        "보통": "이 시간대는 보통 수준의 충전 수요를 보입니다.",
        "여유": "이 시간대는 비교적 여유로운 편입니다."
    }

    if row.empty:
        return None

    level = row["congestion"].iloc[0]

    return {
        "hour": current_hour,
        "charge_type": charge_type,
        "congestion": level,
        "message": message_map[level]
    }