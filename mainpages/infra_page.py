import streamlit as st
import pandas as pd
import altair as alt

def render_infra_page(conn):
    st.title("⚡ 전기차 등록 현황")
    st.markdown("전국 전기차 등록 대수 및 분포 현황 (2025년 4월 기준)")
    st.divider()
    #로드
    try:
        query = "SELECT * FROM ev_registration"
        df = pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return
    
    if df.empty:
        st.warning("데이터가 없습니다. DB에 데이터가 저장되었는지 확인해주세요.")
        return
    
    df['sido'] = df['region'].apply(lambda x: x.split()[0] if isinstance(x, str) else x)

    name_map = {
        '경북': '경상북도',
        '경남': '경상남도',
        '전북': '전북특별자치도',
        '전남': '전라남도',
        '충북': '충청북도',
        '충남': '충청남도'
    }
    df['sido'] = df['sido'].replace(name_map)

    # 3. 핵심 지표 (Metrics) 표시
    total_cars = df['total'].sum()
    total_passenger = df['passenger'].sum()
    total_commercial = df[df['usage_type'] == '사업용']['total'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("총 등록 대수", f"{total_cars:,.0f} 대")
    col2.metric("승용 전기차", f"{total_passenger:,.0f} 대")
    col3.metric("사업용 전기차", f"{total_commercial:,.0f} 대", f"전체의 {total_commercial/total_cars*100:.1f}%")

    st.markdown("---")


    tab1, tab2, tab3 = st.tabs(["🗺️ 지역별 현황", "📊 차종/용도 분석", "📋 상세 데이터"])

    with tab1:
        st.subheader("지역별 전기차 등록 순위")
        
        # 시도별 합계 계산
        sido_grp = df.groupby('sido')['total'].sum().reset_index().sort_values('total', ascending=False)
        
        # Altair 바 차트
        chart_sido = alt.Chart(sido_grp).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
            x=alt.X('sido', sort='-y', title='지역'),
            y=alt.Y('total', title='등록 대수'),
            color=alt.Color('sido', legend=None),
            tooltip=['sido', alt.Tooltip('total', format=',')]
        ).properties(height=400)
        
        st.altair_chart(chart_sido, use_container_width=True)

    with tab2:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("차종별 구성")
            type_sum = df[['passenger', 'bus', 'truck', 'special']].sum().reset_index()
            type_sum.columns = ['차종', '대수']
            
            chart_pie = alt.Chart(type_sum).mark_arc(innerRadius=60).encode(
                theta=alt.Theta(field="대수", type="quantitative"),
                color=alt.Color(field="차종", type="nominal", legend=alt.Legend(title="차종")),
                tooltip=['차종', alt.Tooltip('대수', format=',')]
            ).properties(height=300)
            
            st.altair_chart(chart_pie, use_container_width=True)
            
        with col_chart2:
            st.subheader("용도별 구성 (사업/비사업)")
            usage_grp = df.groupby('usage_type')['total'].sum().reset_index()
            
            chart_usage = alt.Chart(usage_grp).mark_bar().encode(
                x=alt.X('usage_type', title='용도'),
                y=alt.Y('total', title='등록 대수'),
                color='usage_type',
                tooltip=['usage_type', alt.Tooltip('total', format=',')]
            ).properties(height=300)
            
            st.altair_chart(chart_usage, use_container_width=True)

    with tab3:
        st.subheader("원천 데이터 조회")
        with st.expander("데이터프레임 열기"):
            st.dataframe(df, use_container_width=True)