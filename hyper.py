import streamlit as st
import pandas as pd
import joblib
import pickle

backgroundColor = "#F0F0F0"
st.set_page_config(layout="wide")

st.title("🤖 RUL 예측 머신러닝")
st.text(' ')

@st.cache_data(show_spinner=False)
def load_data(csv_path="excel/rerct.csv"):
    df = pd.read_csv(csv_path)
    return df

df = load_data()

features = ['Temperature', 'Cutoff', 'Discharge_Current', 'Re', 'Rct', 'SOH', 'SOH_Diff']
X = df[features]
y = df['RUL']

with open('hyper_pkl/metrics.pkl', 'rb') as f:
    metrics = pickle.load(f)
rf_model = joblib.load('hyper_pkl/rf_model.pkl')  
xgb_model = joblib.load('hyper_pkl/xgb_model.pkl')
selector = joblib.load('hyper_pkl/feature_selector.pkl')
scaler_X = joblib.load('hyper_pkl/scaler_X.pkl')  
scaler_y = joblib.load('hyper_pkl/scaler_y.pkl')
feature_selector = joblib.load('hyper_pkl/feature_selector.pkl')  
pca = joblib.load('hyper_pkl/pca.pkl')
with open("hyper_pkl/rf_graph.pkl", "rb") as f:
    graphs = pickle.load(f)
with open("hyper_pkl/xgb_graph.pkl", "rb") as f:
    graphs2 = pickle.load(f)

def get_top_pca_features_expander(pca, features, top_n=3):
    components = pd.DataFrame(pca.components_, columns=features, index=[f"PC{i+1}" for i in range(pca.n_components_)])

    with st.expander("**PCA 주성분별 주요 특성 보기**"): 
        
        for pc, row in components.iterrows():
            top_features = row.abs().nlargest(top_n)
            top_feature_names = top_features.index.tolist()
            top_feature_values = (top_features / top_features.sum() * 100).tolist()

            st.markdown(f"{pc}",)
            for name, value in zip(top_feature_names, top_feature_values):
                st.write(f"- {name}: {value:.2f}%")
            st.divider()

battery_list = sorted(df['Battery'].unique())

default_battery = 5

if "battery_id" not in st.session_state or st.session_state["battery_id"] not in battery_list:
    st.session_state["battery_id"] = default_battery

battery_id = st.sidebar.selectbox(
    "🔍 배터리 선택", 
    battery_list, 
    index=battery_list.index(st.session_state["battery_id"])
)

st.session_state["battery_id"] = battery_id

st.subheader("📊 모델 성능 평가")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌲 RandomForest")
    col1_1, col1_2, col1_3 = st.columns(3, border=True)
    col1_1.metric("RMSE", f"{metrics['RandomForest']['RMSE']:.4f}")
    col1_2.metric("R-squared", f"{metrics['RandomForest']['R-squared']:.4f}")
    col1_3.metric("MAE", f"{metrics['RandomForest']['MAE']:.4f}")
    

with col2:
    st.markdown("### 🚀 XGBoost")
    col2_1, col2_2, col2_3 = st.columns(3, border=True)
    col2_1.metric("RMSE", f"{metrics['XGBoost']['RMSE']:.4f}")
    col2_2.metric("R-squared", f"{metrics['XGBoost']['R-squared']:.4f}")
    col2_3.metric("MAE", f"{metrics['XGBoost']['MAE']:.4f}")

st.subheader("예측 결과")
col3, col4 = st.columns(2, border=True)

with col3:
    fig = graphs[battery_id]
    st.pyplot(fig)

with col4:
    fig = graphs2[battery_id]
    st.pyplot(fig)

st.subheader('특성 중요도')

col1_4, col2_4 = st.columns(2, border=True)

with col1_4 :
    st.image('img/hy_rf.png')

with col2_4 :
    st.image('img/hy_xg.png')

_, col1_5 = st.columns(2)

with col1_5 :
    get_top_pca_features_expander(pca, features)