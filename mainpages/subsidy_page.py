import streamlit as st
import pandas as pd

@st.cache_data(ttl=3600)
def get_all_region_subsidy(query, _conn):
    return pd.read_sql(query, _conn)

@st.cache_data(ttl=3600)
def get_model_options(_conn):
    return pd.read_sql("SELECT * FROM ev_model_local_subsidy", _conn)

@st.cache_data(ttl=3600)
def get_contact_info(_conn):
    query = "SELECT sido AS 시도, region_name AS 지역, department AS 담당부서, phone AS 연락처 FROM ev_local_contact"
    return pd.read_sql(query, _conn)

# FAQ 데이터를 가져오는 새로운 함수
@st.cache_data(ttl=3600)
def get_faq_data(_conn):
    # tag, question, answer 컬럼만 사용하며 순서대로 정렬
    query = "SELECT tag, question, answer FROM ev_faq ORDER BY page, faq_order"
    return pd.read_sql(query, _conn)

def render_subsidy_page(conn):
    st.title("🚗 전기차 보조금 정보")

    # FAQ 탭을 두 번째와 세 번째 사이에 추가
    tab1, tab2, tab3, tab4 = st.tabs(["지역별 현황", "차종별 상세조회", "지자체 연락처", "자주 묻는 질문(FAQ)"])

    with tab1:
        render_region_subsidy(conn)
    with tab2:
        render_model_subsidy(conn)
    with tab3:
        render_contact(conn) # FAQ 렌더링 함수 호출
    with tab4:
        render_faq_section(conn)

def render_region_subsidy(conn):
    keyword = st.text_input("지역 검색", placeholder="예: 서울, 수원, 전주시", key="search_region")
    query = "SELECT sido AS 시도, region_name AS 지역, subsidy_passenger AS 승용차, subsidy_micro AS 초소형 FROM ev_local_car_subsidy ORDER BY sido, region_name"
    df = get_all_region_subsidy(query, conn)
    if keyword:
        df = df[df["시도"].str.contains(keyword, case=False, na=False) | df["지역"].str.contains(keyword, case=False, na=False)]
    st.dataframe(df, width="stretch", hide_index=True)

def render_model_subsidy(conn):
    df_all = get_model_options(conn)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        region = st.selectbox("지역 선택", ["지역을 선택해주세요"] + sorted(df_all["region_name"].unique()))
    
    df_s1 = df_all[df_all["region_name"] == region] if region != "지역을 선택해주세요" else pd.DataFrame()
    
    with col2:
        v_type = st.selectbox("차종 선택", ["차종을 선택해주세요"] + sorted(df_s1["vehicle_type"].unique()) if not df_s1.empty else ["지역을 먼저 선택해주세요"])

    df_s2 = df_s1[df_s1["vehicle_type"] == v_type] if v_type not in ["차종을 선택해주세요", "지역을 먼저 선택해주세요"] else pd.DataFrame()

    with col3:
        m_fact = st.selectbox("제조사 선택", ["제조사를 선택해주세요"] + sorted(df_s2["manufacturer"].unique()) if not df_s2.empty else ["차종을 먼저 선택해주세요"])

    df_s3 = df_s2[df_s2["manufacturer"] == m_fact] if m_fact not in ["제조사를 선택해주세요", "차종을 먼저 선택해주세요"] else pd.DataFrame()

    with col4:
        model = st.selectbox("모델 선택", ["모델을 선택해주세요"] + sorted(df_s3["model_name"].unique()) if not df_s3.empty else ["제조사를 먼저 선택해주세요"])

    if model not in ["모델을 선택해주세요", "제조사를 먼저 선택해주세요"]:
        res = df_s3[df_s3["model_name"] == model].iloc[0]
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("국비", f"{res['gov_subsidy']:,} 만원")
        c2.metric("지방비", f"{res['local_subsidy']:,} 만원")
        c3.metric("총 보조금", f"{res['total_subsidy']:,} 만원")

        detail_df = pd.DataFrame([{
            "제조사": res['manufacturer'], "모델명": res['model_name'],
            "국비": f"{res['gov_subsidy']:,}", "지방비": f"{res['local_subsidy']:,}", "합계": f"{res['total_subsidy']:,}"
        }])
        st.dataframe(detail_df, width="stretch", hide_index=True)
    else:
        st.info("상단 항목을 모두 선택하시면 상세 보조금 정보가 표시됩니다.")



def render_contact(conn):
    df_contact = get_contact_info(conn)
    keyword = st.text_input("지자체 또는 부서 검색", placeholder="예: 강원, 수지구, 기후에너지과", key="search_contact")
    if keyword:
        df_contact = df_contact[
            df_contact["시도"].str.contains(keyword, case=False, na=False) | 
            df_contact["지역"].str.contains(keyword, case=False, na=False) |
            df_contact["담당부서"].str.contains(keyword, case=False, na=False)
        ]
    st.dataframe(df_contact.sort_values(["시도", "지역"]), width="stretch", hide_index=True)

    # --- FAQ 섹션 추가 ---
def render_faq_section(conn):
    st.subheader("💡 자주 묻는 질문")
    df_faq = get_faq_data(conn)
    
    # 상단 태그 필터 (사용자가 관심 있는 카테고리만 골라 볼 수 있게 함)
    tags = ["전체"] + sorted(df_faq["tag"].unique().tolist())
    selected_tag = st.selectbox("카테고리를 선택해주세요", tags)
    
    filtered_faq = df_faq if selected_tag == "전체" else df_faq[df_faq["tag"] == selected_tag]
    
    st.write("") # 간격 조절
    
    for _, row in filtered_faq.iterrows():
        # 질문과 태그를 조합하여 제목 생성
        with st.expander(f"[{row['tag']}] {row['question']}"):
            # 답변 출력 (내부 줄바꿈 보존)
            st.markdown(row['answer'])