import streamlit as st



def render_sidebar():
    """사이드바 메뉴 렌더링"""
    st.sidebar.title("메뉴")

    # 간단한 CSS
    st.markdown("""
      <style>
          /* 사이드바 컨테이너 패딩 조정 */
          section[data-testid="stSidebar"] > div {
              padding-left: 1rem;
              padding-right: 1rem;
          }

          /* 사이드바 버튼 전체 너비 */
          section[data-testid="stSidebar"] .stButton {
              width: 100% !important;
          }

          section[data-testid="stSidebar"] .stButton > button {
              width: 100% !important;
              text-align: left !important;
              justify-content: flex-start !important;
              padding: 0.5rem 1rem !important;
              margin: 0.25rem 0 !important;
              min-height: 2.5rem !important;
              border-radius: 0.5rem !important;
              background-color: #f0f2f6 !important;
              border: 1px solid transparent !important;
              transition: all 0.2s ease !important;
          }

          /* 버튼 호버 효과 */
          section[data-testid="stSidebar"] .stButton > button:hover {
              background-color: #e6f3ff !important;
              border-left: 3px solid #4ECDC4 !important;
              padding-left: calc(1rem - 2px) !important;
              transform: translateX(2px);
          }

          /* 버튼 클릭(활성) 상태 */
          section[data-testid="stSidebar"] .stButton > button:active,
          section[data-testid="stSidebar"] .stButton > button:focus {
              background-color: #4ECDC4 !important;
              color: white !important;
              box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
              outline: none !important;
          }

          /* 버튼 내부 텍스트 */
          section[data-testid="stSidebar"] .stButton > button > div {
              text-align: left !important;
              width: 100% !important;
          }

          section[data-testid="stSidebar"] .stButton > button p {
              text-align: left !important;
              margin: 0 !important;
              font-weight: 500 !important;
          }

          /* 사이드바 제목 스타일 */
          section[data-testid="stSidebar"] h1 {
              font-size: 1.5rem !important;
              margin-bottom: 1.5rem !important;
              padding-bottom: 0.5rem !important;
              border-bottom: 2px solid #4ECDC4 !important;
          }
      </style>
      """, unsafe_allow_html=True)

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "전기차 등록 현황"

    pages = {
        "전기차 등록 현황": "menu_infrastructure",
        "충전소 현황": "menu_heatmap_new",
        "충전소 요금": "menu_keywords",
        "충전소 혼잡도" : "menu_honjab",
        "FAQ" : "menu_FAQ"
    }

    for page, key in pages.items():
        if st.sidebar.button(page, key=key):
            st.session_state.current_page = page