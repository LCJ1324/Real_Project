import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(layout="wide")

backgroundColor = "#F0F0F0"

st.title("물리적 특성 분석")
st.text(' ')

@st.cache_data(show_spinner=False)
def load_data(csv_path="excel/rerct.csv"):
    df = pd.read_csv(csv_path)
    return df

@st.cache_data(show_spinner=False)
def load_data2(csv_path):
    df = pd.read_excel(csv_path)
    return df

df = load_data()
xrd_df = load_data2('excel/XRD.xlsx')

battery_list = sorted(df['Battery'].unique()) + ['전체']

default_battery = 5

if "battery_id" not in st.session_state or st.session_state["battery_id"] not in battery_list:
    st.session_state["battery_id"] = default_battery

battery_id = st.sidebar.selectbox(
    "🔍 배터리 선택", 
    battery_list, 
    index=battery_list.index(st.session_state["battery_id"])
)

st.session_state["battery_id"] = battery_id

idx = battery_list.index(battery_id)


st.subheader("**Secondary Electron Microscopy(SEM) & X-ray Diffraction(XRD)**")


col1, col2 = st.columns(2, border= True)

with col1 :
    col1_1, col1_2 = st.columns(2)
    with col1_1 :
        st.markdown('## SEM')

    with col1_2 :
        mag = st.radio(
        "# **배율 선택**",  
        ['10x', '50x', '100x'],
        horizontal=True
        )

    if mag == '10x' :
        num = 1
    elif mag == '50x' :
        num = 2
    else :
        num = 3

    image = Image.open(f'SEM/{idx+1}/{num}.jpg')
    st.image(image)

with col2 :
    st.markdown('## XRD')
    st.title(' ')
    fig, ax2 = plt.subplots(figsize = (8, 5))
    ax2.plot(xrd_df.iloc[:, idx*2], xrd_df.iloc[:, idx*2+1], color = 'black')
    ax2.set_ylabel('Intensity', fontsize = 12)
    ax2.set_xlabel('2 theta', fontsize = 12)
    ax2.set_yticks([])
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False) 
    st.pyplot(fig)
