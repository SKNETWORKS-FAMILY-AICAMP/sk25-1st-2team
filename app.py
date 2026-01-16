import streamlit as st
from sidebar import render_sidebar
from mainpages.map_page import render_map_page
from mainpages.keyword_page import render_keyword_page
from mainpages.infra_page import render_infra_page
from mainpages.faq_page import render_faq_page
from mainpages.congestion_page import load_and_preprocess
from mainpages.congestion_page import render_congestion_page
from utils.db import get_db


class App:
    def __init__(self):
        # DB 연결
        self.conn = get_db()

        # 초기 세션 상태 설정
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "전기차 등록 현황"

        # 페이지 설정
        st.set_page_config(page_title="SK25 2팀!", layout="wide")

    def run(self):
        # 사이드바 렌더링
        render_sidebar()
        
        # 현재 페이지 렌더링
        page = st.session_state.current_page
        if page == "충전소 현황":
            render_map_page(self.conn)
        elif page == "충전소 요금":
            render_keyword_page(self.conn)
        elif page == "전기차 등록 현황":
            render_infra_page(self.conn)
        elif page == "FAQ":
            render_faq_page(self.conn)
        elif page == "충전소 혼잡도":
            load_and_preprocess(self.conn)
            render_congestion_page(self.conn)
