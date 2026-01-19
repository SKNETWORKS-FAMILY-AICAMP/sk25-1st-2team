import streamlit as st
import pandas as pd
import re
from utils.db import get_db

# --- 1. 유틸리티 및 데이터 로딩 함수 ---
TRANSLATION_MAP = {
    "충전": "charge", "배터리": "battery", "보증": "warranty",
    "타이어": "tire", "유지보수": "maintenance", "소프트웨어": "software",
    "결제": "payment", "속도": "speed", "예약": "reserve",
    "성능": "performance", "안전": "safety", "서비스": "service"
}

def highlight_keyword(text, keyword, eng_keyword=None):
    if not keyword:
        return text
    clean_keyword = re.escape(keyword)
    text = re.sub(f"({clean_keyword})", r"**\1**", text, flags=re.IGNORECASE)
    if eng_keyword:
        clean_eng = re.escape(eng_keyword)
        text = re.sub(f"({clean_eng})", r"**\1**", text, flags=re.IGNORECASE)
    return text

@st.cache_data(ttl=600)
def get_cached_faq_data(table_name):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            sql = f"SELECT * FROM {table_name}"
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            result = cursor.fetchall()
            return pd.DataFrame(result, columns=columns)
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

# --- 2. 메인 렌더링 함수 ---
def render_faq_page(conn=None):
    st.header("⚡전기차 관련 FAQ 찾아보기")
    st.markdown("궁금한 브랜드와 카테고리를 선택하여 자주 묻는 질문을 확인하세요.")
    #st.markdown("<p style='font-size: 0.9rem; color: gray;'>(KIA / BMW / Tesla / BYD)</p>", unsafe_allow_html=True)
    #st.divider()

# 1. 컬럼을 생성하여 가로 배치 준비 (비율은 1:1로 설정하거나 조정 가능)
    col1, col2 = st.columns([1, 1])

    with col1:
        # 왼쪽 컬럼: 브랜드 선택 박스
        brand_option = st.selectbox(
            "⚡ 🚗 브랜드를 선택하세요 (KIA / BMW / Tesla / BYD)",
            ("선택", "KIA", "BMW", "Tesla", "BYD"),
            key="faq_brand_selectbox"
        )
    st.divider()
    with col2:
        # 오른쪽 컬럼: 사진 배치 (브랜드 선택 전 초기 화면일 때만 표시)
        if brand_option == "선택":
            st.image(
                "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&q=80&w=1000",
                use_container_width=True # 컬럼 너비에 맞춰 크기 자동 조정
            )

    if brand_option == "선택":
        #st.info("드롭다운 메뉴에서 자동차 브랜드를 선택해 주세요!")
        return

    # 브랜드에 따른 테이블 매핑
    table_mapping = {
        "KIA": "kia_faq", 
        "BMW": "bmw_faq", 
        "Tesla": "tesla_faq", 
        "BYD": "byd_faq"
    }
    target_table = table_mapping[brand_option]

    # 데이터 로딩
    df = get_cached_faq_data(target_table)

    if df.empty:
        st.warning("데이터가 없거나 불러올 수 없습니다.")
        return

    # 검색 창
    search_term = st.text_input("🔍 키워드 검색 (예: 충전, 배터리)", "", key="faq_search_input")
    eng_search_term = TRANSLATION_MAP.get(search_term, None)

    # 필터링 로직
    if search_term:
        mask = df['question'].str.contains(search_term, case=False, na=False)
        if eng_search_term:
            mask = mask | df['question'].str.contains(eng_search_term, case=False, na=False)
        display_df = df[mask]
    else:
        display_df = df

    if search_term:
        st.caption(f"'{search_term}' 관련 질문이 {len(display_df)}건 검색되었습니다.")

    # --- 출력 방식 결정 ---
    # KIA와 Tesla만 카테고리 탭 구성을 사용합니다.
    if brand_option in ["KIA", "Tesla"] and not display_df.empty and 'category' in display_df.columns:
        raw_categories = display_df['category'].unique().tolist()
        categories = [c for c in raw_categories if c] 
        
        tab_titles = ["전체"] + categories
        tabs = st.tabs(tab_titles)
        
        for i, tab in enumerate(tabs):
            with tab:
                tab_df = display_df if tab_titles[i] == "전체" else display_df[display_df['category'] == tab_titles[i]]
                if tab_df.empty:
                    st.write("결과가 없습니다.")
                else:
                    for _, row in tab_df.iterrows():
                        q = highlight_keyword(row['question'], search_term, eng_search_term)
                        with st.expander(q):
                            st.write(row['answer'])
    else:
        # BMW와 BYD는 카테고리 없이 바로 전체 리스트 출력
        if display_df.empty:
            st.warning("결과가 없습니다.")
        else:
            for _, row in display_df.iterrows():
                q = highlight_keyword(row['question'], search_term, eng_search_term)
                with st.expander(q):
                    st.write(row['answer'])