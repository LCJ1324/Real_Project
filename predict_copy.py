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
    temp = st.slider('Temperature (°C)', df['Temperature'].min(), df['Temperature'].max())

with col2:
    cut = st.slider('Cutoff Voltage (V)', df['Cutoff'].min(), df['Cutoff'].max())
with col3:
    dc = st.slider('Discharge Current (A)', df['Discharge_Current'].min(), df['Discharge_Current'].max())
with col4:
    re = st.slider('Re (Ω)', df['Re'].min(), df['Re'].max())
with col5:
    rct = st.slider('Rct (Ω)', df['Rct'].min(), df['Rct'].max())
with col6:
    soh = st.slider('SOH (%)', 80, 100, 100)

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
