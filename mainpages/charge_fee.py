import re
import pandas as pd
import streamlit as st
import altair as alt


def format_phone(x) -> str:
    if x is None:
        return ""
    digits = re.sub(r"\D", "", str(x))
    if digits == "" or digits == "00000000":
        return ""
    if len(digits) == 8:
        return f"{digits[:4]}-{digits[4:]}"
    if digits.startswith("02") and len(digits) >= 9:
        return f"{digits[:2]}-{digits[2:-4]}-{digits[-4:]}"
    if len(digits) >= 10:
        return f"{digits[:3]}-{digits[3:-4]}-{digits[-4:]}"
    return digits


@st.cache_data(show_spinner=False)
def load(_conn) -> pd.DataFrame:
    sql = """
        SELECT companyName, coPhoneNo, customerType, averageFee
        FROM charge_fee
    """
    df = pd.read_sql(sql, _conn)
    df = df.rename(columns={
        "companyName": "업체명",
        "coPhoneNo": "업체 전화번호",
        "customerType" : "회원가 여부",
        "averageFee": "평균 충전요금(원 / kWh)",
    })
    df["업체 전화번호"] = df["업체 전화번호"].apply(format_phone)
    df['회원가 여부'] = df['회원가 여부'].replace({
        'M': '회원가',
        'G': '비회원가'
    })
    df["평균 충전요금(원 / kWh)"] = pd.to_numeric(df["평균 충전요금(원 / kWh)"], errors="coerce")

    pivot_df = df.pivot_table(
        index=["업체명", "업체 전화번호"],
        columns="회원가 여부",
        values="평균 충전요금(원 / kWh)"
    ).reset_index()

    pivot_df.columns.name = None

    return pivot_df


def render_charge_fee_page(conn):
    st.title("⚡ 충전소 업체별 요금")
    st.caption("차지인포 - 통계정보 - 충전 사업자별 충전요금 (2026년 1월 15일 기준)")

    df = load(conn).copy()
    if df.empty:
        st.warning("데이터가 없습니다.")
        return

    # Define fee columns
    member_fee_col = "회원가"
    non_member_fee_col = "비회원가"

    # =======================
    # 가장 저렴한 곳 TOP 10 차트
    # =======================
    st.subheader("📊 평균 충전요금 가장 저렴한 곳 TOP 10")
    chart_fee_type = st.radio(
        "요금 종류 선택 (저렴한 순)",
        ["비회원가", "회원가"],
        horizontal=True,
    )

    sort_col = non_member_fee_col if chart_fee_type == "비회원가" else member_fee_col

    # Sort by the selected fee type for the chart, showing the cheapest
    # Filter out missing or zero values before sorting
    bottom10 = (
        df.copy()
          .dropna(subset=[sort_col])
          [lambda x: x[sort_col] > 0]
          .sort_values(by=sort_col, ascending=True)
          .head(10)
    )

    chart = (
        alt.Chart(bottom10)
        .mark_bar()
        .encode(
            x=alt.X("업체명:N", sort="y", axis=alt.Axis(labelAngle=-45, title=None)),
            y=alt.Y(f"{sort_col}:Q", title=f"평균가(원 / kWh)"),
            color=alt.Color("업체명:N", legend=None),
            tooltip=["업체명", alt.Tooltip(f"{sort_col}:Q", format=",.2f")],
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)
    st.divider()

    # =======================
    # 표 + 필터
    # =======================
    st.subheader("📋 업체별 평균 충전요금 목록")

    filtered = df.copy()

    # --- 1. Define UI elements and get user input ---
    c1, c2 = st.columns([2, 1])
    with c1:
        keyword = st.text_input("업체명 검색(부분일치)")
    with c2:
        sort_option = st.selectbox(
            "정렬 기준",
            ["비회원가 높은 순", "비회원가 낮은 순", "회원가 높은 순", "회원가 낮은 순", "업체명 가나다 순"]
        )

    # --- 2. Apply filtering based on user input ---
    if keyword.strip():
        filtered = filtered[filtered["업체명"].astype(str).str.contains(keyword.strip(), case=False, na=False)]

    # --- 3. Apply sorting based on user input ---
    if sort_option == "비회원가 높은 순":
        filtered = filtered.sort_values(by=non_member_fee_col, ascending=False, na_position='last')
    elif sort_option == "비회원가 낮은 순":
        filtered = filtered.sort_values(by=non_member_fee_col, ascending=True, na_position='last')
    elif sort_option == "회원가 높은 순":
        filtered = filtered.sort_values(by=member_fee_col, ascending=False, na_position='last')
    elif sort_option == "회원가 낮은 순":
        filtered = filtered.sort_values(by=member_fee_col, ascending=True, na_position='last')
    else:
        filtered = filtered.sort_values(by="업체명")

    st.dataframe(
        filtered,
        hide_index=True,
        column_config={
            member_fee_col: st.column_config.NumberColumn(format="%.2f원"),
            non_member_fee_col: st.column_config.NumberColumn(format="%.2f원"),
        }
    )