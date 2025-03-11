import streamlit as st

pages = [
    st.Page("CE.py", title="전기화학적 특성 분석", icon="🔍", default=True),
    st.Page("chemical.py", title="물리적 특성 분석", icon="🔬"),
    st.Page('predict_copy.py', title = '수명 예측', icon="⏳"),
    st.Page("hyper.py", title="머신러닝", icon="🤖")
]

selected_page = st.navigation(pages)

selected_page.run()