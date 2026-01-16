import streamlit as st
import pandas as pd
import pymysql
import re

# --- 1. 유틸리티 함수 및 설정 (함수 밖으로 빼두는 것이 깔끔합니다) ---
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
    # DB 연결 (기존에 사용하시던 접속 정보를 입력하세요)
    conn = pymysql.connect(
        host='175.196.76.209',
        user='sk25_team2',
        password='Encore7277!', # 실제 비밀번호 입력
        db='team2',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            sql = f"SELECT * FROM {table_name}"
            cursor.execute(sql)
            return pd.DataFrame(cursor.fetchall())
    finally:
        conn.close()

# --- 2. 메인 렌더링 함수 (기존 함수를 수정합니다) ---
def render_faq_page(conn): # 기존에 conn 인자를 받으므로 유지
    st.header("⚡전기차 관련 FAQ (KIA/Tesla/BYD)")
    st.markdown("궁금한 브랜드와 카테고리를 선택하여 자주 묻는 질문을 확인하세요.")
    st.divider()

    # 상단 브랜드 선택
    col1, _ = st.columns([1, 2])
    with col1:
        brand_option = st.selectbox(
            "🚗 브랜드를 선택하세요",
            ("선택", "KIA", "Tesla", "BYD"),
            key="faq_brand_selectbox" # 고유 키 설정
        )

    if brand_option == "선택":
        st.info("드롭다운 메뉴에서 자동차 브랜드를 선택해 주세요!")
        st.image("https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&q=80&w=1000", 
                 caption="Welcome to EV FAQ Service", width=700)
        return

    # 데이터 로딩 및 필터링 로직
    table_mapping = {"KIA": "kia_faq", "Tesla": "tesla_faq", "BYD": "byd_faq"}
    target_table = table_mapping[brand_option]

    try:
        df = get_cached_faq_data(target_table)
        search_term = st.text_input("🔍키워드 검색", "", key="faq_search_input")
        eng_search_term = TRANSLATION_MAP.get(search_term, None)

        if search_term and not df.empty:
            mask = df['question'].str.contains(search_term, case=False, na=False)
            if eng_search_term:
                mask = mask | df['question'].str.contains(eng_search_term, case=False, na=False)
            display_df = df[mask]
        else:
            display_df = df

        if search_term:
            st.caption(f"'{search_term}' 관련 질문이 {len(display_df)}건 검색되었습니다.")

        # 브랜드별 출력 방식 (테슬라는 탭 방식)
        if brand_option == "Tesla" and not display_df.empty and 'category' in display_df.columns:
            categories = sorted(display_df['category'].unique().tolist())
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
            if display_df.empty:
                st.warning("결과가 없습니다.")
            else:
                for _, row in display_df.iterrows():
                    q = highlight_keyword(row['question'], search_term, eng_search_term)
                    with st.expander(q):
                        st.write(row['answer'])

    except Exception as e:
        st.error("데이터를 불러오는 중 오류가 발생했습니다.")
        st.caption(f"Error: {e}")