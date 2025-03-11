import streamlit as st

if "battery_id" not in st.session_state:
    st.session_state["battery_id"] = 5 

if "slider_cycle" not in st.session_state:
    st.session_state["slider_cycle"] = 1
if "num_input_cycle" not in st.session_state:
    st.session_state["num_input_cycle"] = 1

# 1. 여러 페이지 정보를 등록합니다.
pages = [
    st.Page("CE.py", title="전기 화학적 특성 분석", icon="🔍", default=True),
    st.Page("chemical.py", title="물리적 특성 분석", icon="🔬"),
    st.Page('predict_copy.py', title = '수명 예측', icon="⏳"),
    st.Page("hyper.py", title="머신러닝", icon="🤖")
]

# 2. 사용자가 선택한 페이지를 받아옵니다.
selected_page = st.navigation(pages)

# 3. 선택된 페이지를 실행(run)합니다.
selected_page.run()