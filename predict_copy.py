import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib

st.set_page_config(layout="wide")

st.title("🔮 배터리 잔존 수명 예측")
st.text(' ')
st.subheader('특성을 입력해주세요')

df = pd.read_csv('excel/rerct.csv')

features = ['Temperature', 'Cutoff', 'Discharge_Current', 'Re', 'Rct', 'SOH']
X = df[features]
y = df['RUL']

rf_model = joblib.load('pred_pkl/rf_model.pkl')  
xgb_model = joblib.load('pred_pkl/xgb_model.pkl')
scaler_X = joblib.load('pred_pkl/scaler_X.pkl')  
scaler_y = joblib.load('pred_pkl/scaler_y.pkl')

col1, col2, col3, col4, col5, col6 = st.columns(6, border=True)
with col1:
    if "slider_temp" not in st.session_state:
        st.session_state["slider_temp"] = df['Temperature'].min()
    if "num_input_temp" not in st.session_state:
        st.session_state["num_input_temp"] = df['Temperature'].min()

    def update_temp_input():
        st.session_state["num_input_temp"] = st.session_state["slider_temp"]
    def update_temp_slider():
        st.session_state["slider_temp"] = st.session_state["num_input_temp"]
    col1_1, col1_2 = st.columns([2, 1])
    with col1_1:
        st.slider(
            "Temperature(°C)", 
            df['Temperature'].min(), 
            df['Temperature'].max(), 
            key="slider_temp",
            on_change=update_temp_input
        )

    with col1_2:
        st.number_input(
            " ",
            df['Temperature'].min(), 
            df['Temperature'].max(), 
            step=1,
            key="num_input_temp",
            on_change=update_temp_slider
        )
temp = st.session_state["slider_temp"]

with col2:
    if "slider_cutoff" not in st.session_state:
        st.session_state["slider_cutoff"] = df['Cutoff'].min()
    if "num_input_cutoff" not in st.session_state:
        st.session_state["num_input_cutoff"] = df['Cutoff'].min()

    def update_cutoff_input():
        st.session_state["num_input_cutoff"] = st.session_state["slider_cutoff"]
    def update_cutoff_slider():
        st.session_state["slider_cutoff"] = st.session_state["num_input_cutoff"]

    col2_1, col2_2 = st.columns([2, 1])
    with col2_1:
        st.slider(
            "Cutoff Voltage(V)", 
            df['Cutoff'].min(), 
            df['Cutoff'].max(), 
            key="slider_cutoff",
            on_change=update_cutoff_input
        )

    with col2_2:
        st.number_input(
            " ",
            df['Cutoff'].min(), 
            df['Cutoff'].max(), 
            step=0.01,
            key="num_input_cutoff",
            on_change=update_cutoff_slider
        )
    cut = st.session_state["slider_cutoff"]

with col3:
    if "slider_dc" not in st.session_state:
        st.session_state["slider_dc"] = df['Discharge_Current'].min()
    if "num_input_dc" not in st.session_state:
        st.session_state["num_input_dc"] = df['Discharge_Current'].min()

    def update_dc_input():
        st.session_state["num_input_dc"] = st.session_state["slider_dc"]
    def update_dc_slider():
        st.session_state["slider_dc"] = st.session_state["num_input_dc"]

    col3_1, col3_2 = st.columns([2, 1])
    with col3_1:
        st.slider(
            "DischargeCurrent(A)", 
            df['Discharge_Current'].min(), 
            df['Discharge_Current'].max(), 
            key="slider_dc",
            on_change=update_dc_input
        )

    with col3_2:
        st.number_input(
            " ",
            df['Discharge_Current'].min(), 
            df['Discharge_Current'].max(), 
            step=0.01,
            key="num_input_dc",
            on_change=update_dc_slider
        )
    dc = st.session_state["slider_dc"]

with col4:
    if "slider_re" not in st.session_state:
        st.session_state["slider_re"] = df['Re'].min()
    if "num_input_re" not in st.session_state:
        st.session_state["num_input_re"] = df['Re'].min()

    def update_re_input():
        st.session_state["num_input_re"] = st.session_state["slider_re"]
    def update_re_slider():
        st.session_state["slider_re"] = st.session_state["num_input_re"]

    col4_1, col4_2 = st.columns([2, 1])
    with col4_1:
        st.slider(
            "Re(Ω)", 
            df['Re'].min(), 
            df['Re'].max(), 
            key="slider_re",
            on_change=update_re_input
        )

    with col4_2:
        st.number_input(
            " ",
            df['Re'].min(), 
            df['Re'].max(), 
            step=0.01,
            key="num_input_re",
            on_change=update_re_slider
        )
    re = st.session_state["slider_re"]

with col5:
    if "slider_rct" not in st.session_state:
        st.session_state["slider_rct"] = df['Rct'].min()
    if "num_input_rct" not in st.session_state:
        st.session_state["num_input_rct"] = df['Rct'].min()

    def update_rct_input():
        st.session_state["num_input_rct"] = st.session_state["slider_rct"]
    def update_rct_slider():
        st.session_state["slider_rct"] = st.session_state["num_input_rct"]

    col5_1, col5_2 = st.columns([2, 1])
    with col5_1:
        st.slider(
            "Rct(Ω)", 
            df['Rct'].min(), 
            df['Rct'].max(), 
            key="slider_rct",
            on_change=update_rct_input
        )

    with col5_2:
        st.number_input(
            " ",
            df['Rct'].min(), 
            df['Rct'].max(), 
            step=0.01,
            key="num_input_rct",
            on_change=update_rct_slider
        )
    rct = st.session_state["slider_rct"]

with col6:
    if "slider_soh" not in st.session_state:
        st.session_state["slider_soh"] = 100
    if "num_input_soh" not in st.session_state:
        st.session_state["num_input_soh"] = 100

    def update_soh_input():
        st.session_state["num_input_soh"] = st.session_state["slider_soh"]
    def update_soh_slider():
        st.session_state["slider_soh"] = st.session_state["num_input_soh"]

    col6_1, col6_2 = st.columns([2, 1])
    with col6_1:
        st.slider(
            "SOH(%)", 
            80, 
            100,
            key="slider_soh",
            on_change=update_soh_input
        )

    with col6_2:
        st.number_input(
            " ",
            80, 
            100,
            step=1,
            key="num_input_soh",
            on_change=update_soh_slider
        )
    soh = st.session_state["slider_soh"]


def predict_rul(model):
    X_ = np.array([[temp, cut, dc, re, rct, soh]])
    X_scaled_ = scaler_X.transform(X_)
    prediction_scaled = model.predict(X_scaled_)
    prediction = scaler_y.inverse_transform([[prediction_scaled[0]]]) 
    return max(0, prediction[0][0])

rf_prediction = predict_rul(rf_model)
xgb_prediction = predict_rul(xgb_model)
predicted_charge_cycles = int((rf_prediction + xgb_prediction) / 2)

bar_color = "red" if predicted_charge_cycles <= 20 else "limegreen"

def create_gauge_chart(value, max_value):
    
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            gauge={
                "axis": {"range": [0, max_value], "tickfont": {"size": 18}},
                "bar": {"color": bar_color, "thickness": 1.0},
                "steps": [
                    {"range": [0, max_value], "color": "white"},
                ],
            },
        )
    )
    return fig

fig = create_gauge_chart(predicted_charge_cycles, 120)
st.plotly_chart(fig)

st.markdown(f"<h3 style='text-align: center;'>이 배터리는 <span style='color: {bar_color};'>{predicted_charge_cycles}번</span> 더 충전 가능해요. 그 후엔 교체가 필요해요.</h3>", unsafe_allow_html=True)
