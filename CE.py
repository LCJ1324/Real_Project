import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

backgroundColor = "#F0F0F0"
st.set_page_config(layout="wide")

@st.cache_data(show_spinner=False)
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return df

@st.cache_data(show_spinner=False)
def load_data2(xlsx_path):
    df = pd.read_excel(xlsx_path)
    return df

df = load_data('excel/rerct.csv')
cal_df = load_data('excel/calculated.csv')
dis_df = load_data('excel/calculated_dis.csv')
eis = load_data2('excel/EIS.xlsx')
cv = load_data2("excel/CV test.xlsx")
vol1 = load_data('excel/Vol_5.csv')
vol2 = load_data('excel/Vol_6.csv')
vol3 = load_data('excel/Vol_7.csv')
vol4 = load_data('excel/Vol_18.csv')
vol5 = load_data('excel/Vol_46.csv')
vol6 = load_data('excel/Vol_47.csv')
vol7 = load_data('excel/Vol_48.csv')
vol8 = load_data('excel/Vol_55.csv')

vol_df = pd.concat([vol1, vol2, vol3, vol4, vol5, vol6, vol7, vol8], ignore_index=True)

battery_list = sorted(cal_df['battery_id'].unique())

default_battery = 5

if "battery_id" not in st.session_state or st.session_state["battery_id"] not in battery_list:
    st.session_state["battery_id"] = default_battery

battery_id = st.sidebar.selectbox(
    "🔍 배터리 선택", 
    battery_list, 
    index=battery_list.index(st.session_state["battery_id"])
)

st.session_state["battery_id"] = battery_id

max_cycle = vol_df[vol_df['Battery'] == battery_id]['Cycle'].max()

if "slider_cycle" not in st.session_state:
    st.session_state["slider_cycle"] = 1
if "num_input_cycle" not in st.session_state:
    st.session_state["num_input_cycle"] = 1

def update_number_input():
    st.session_state["num_input_cycle"] = st.session_state["slider_cycle"]

def update_slider():
    st.session_state["slider_cycle"] = st.session_state["num_input_cycle"]

with st.sidebar:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.slider(
            "# **Cycle**", 
            min_value=1, 
            max_value=max_cycle, 
            key="slider_cycle",
            on_change=update_number_input
        )

    with col2:
        st.number_input(
            " ",
            min_value=1, 
            max_value=max_cycle, 
            step=1,
            key="num_input_cycle",
            on_change=update_slider
        )

cycle = st.session_state["slider_cycle"]

st.title(f'전기화학적 특성 분석 - Battery {battery_id}')
st.text(' ')
idx = battery_list.index(battery_id)

filtered_df = df[df['Battery'] == battery_id]

col111, col222, col333, col444 = st.columns(4, border=True)

col111.metric('초기 용량 (Ah)', f'{filtered_df['Capacity'].iloc[:10].max() : .2f}')
col222.metric("Temperature (°C)", f"{filtered_df['Temperature'].iloc[0]:.2f}")
col333.metric("Cutoff Voltage (V)", f"{filtered_df['Cutoff'].iloc[0]:.2f}")
col444.metric("Discharge Current (A)", f"{filtered_df['Discharge_Current'].iloc[0]:.2f}")

col1, col2 = st.columns(2, border=True)

with col1 :
    st.markdown('### **Galvanostatic Charge/Discharge (GCD)**')
    df_charge = vol_df[(vol_df['Cycle'] == cycle) & (vol_df['type'] == 'charge') & (vol_df['Battery'] == battery_id)]
    df_discharge = vol_df[(vol_df['Cycle'] == cycle) & (vol_df['type'] == 'discharge') & (vol_df['Battery'] == battery_id)]
    fig, ax = plt.subplots(figsize = (8, 5))
    ax.plot(df_charge['Ah'], df_charge['Voltage_measured'], color='indigo', label = 'Charge', alpha = 0.6)
    ax.plot(df_discharge['Ah'], df_discharge['Voltage_measured'], color='coral', label = 'Discharge')
    ax.set_xlabel("Capacity (Ah)")
    ax.set_ylabel("Voltage (V)")
    ax.legend()
    st.pyplot(fig)
    

with col2 :
    st.markdown('### **Coulombic Efficiency**')
    ddd3 = dis_df[dis_df['battery_id'] == battery_id]
    fig, ax1 = plt.subplots(figsize = (8, 5))
    ax1.plot(ddd3['Cycle'], ddd3['Cal_Capacity'], color = 'lightseagreen', marker = 's', label = 'Capacity', alpha = 0.7)
    ax1.set_ylim([0,4])
    ax1.set_ylabel('Capacity (Ah)', fontdict = {'color' : 'black', 'fontsize' : 12,})
    ax1.set_xlabel('Cycle', fontsize = 12)

    ax2 = ax1.twinx()
    ax2.plot(ddd3['Cycle'], ddd3['CE'], color = 'lightpink', marker = 's', label = 'CE',)
    ax2.set_ylim([0,110])
    ax2.set_ylabel('CE (%)', fontdict = {'color' : 'black', 'fontsize' : 12})
    st.pyplot(fig)

col3, col4 = st.columns(2, border=True)

with col3 :
    st.markdown('### **Cyclic voltammetry(CV)**')
    fig, ax = plt.subplots(figsize = (8, 5))
    ax.plot(cv.iloc[1:, idx*2], cv.iloc[1:, idx*2+1], color = 'brown', alpha = 0.7)
    ax.set_ylabel('I (A)', fontsize = 12)
    ax.set_xlabel("Ecell (V)", fontsize = 12)
    st.pyplot(fig)
    
with col4 :
    st.markdown('### **Electrochemical impedance Spectroscopy(EIS)**')
    fig, ax3 = plt.subplots(figsize = (8, 5))
    ax3.plot(eis.iloc[1:, idx*2], eis.iloc[1:, idx*2+1], color = 'slateblue', marker = 'o', alpha = 0.7)
    ax3.set_ylabel("Z' (Ohm)", fontsize = 12)
    ax3.set_xlabel('Z (Ohm)', fontsize = 12)
    st.pyplot(fig)