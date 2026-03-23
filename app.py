import streamlit as st
import joblib
import numpy as np

st.set_page_config(page_title="Clasificador de Calidad de Vino Tinto",
                   page_icon="🍷",
                   layout="centered")

st.title("🍷 ¿Es este vino de alta calidad?")
st.markdown("Introduce las características químicas y te digo la predicción")


PREDICTOR_PATH = "modelo_vino_pipeline_v1.pkl"


@st.cache_resource
def load_predictor():
    return joblib.load(PREDICTOR_PATH)


predictor = load_predictor()
st.caption(f"Artefacto cargado: {PREDICTOR_PATH}")
# umbral = 0.42               # ← cámbialo según tu curva precision-recall

with st.form("vino_form"):
    col1, col2 = st.columns(2)

    with col1:
        fixed_acidity       = st.slider("Fixed Acidity",       min_value=4.0,  max_value=16.0,  value=7.4,   step=0.1)
        volatile_acidity    = st.slider("Volatile Acidity",    min_value=0.1,  max_value=1.6,   value=0.70,  step=0.01)
        citric_acid         = st.slider("Citric Acid",         min_value=0.0,  max_value=1.0,   value=0.00,  step=0.01)
        residual_sugar      = st.slider("Residual Sugar",      min_value=0.5,  max_value=20.0,  value=1.9,   step=0.1)
        chlorides           = st.slider("Chlorides",           min_value=0.01, max_value=0.7,   value=0.076, step=0.001)

    with col2:
        free_so2            = st.slider("Free SO₂",            min_value=1.0,   max_value=72.0,  value=11.0,  step=1.0)
        total_so2           = st.slider("Total SO₂",           min_value=6.0,   max_value=300.0, value=34.0,  step=1.0)
        density             = st.slider("Density",             min_value=0.99,  max_value=1.004, value=0.998, step=0.0001)
        pH                  = st.slider("pH",                  min_value=2.7,   max_value=4.0,   value=3.51,  step=0.01)
        sulphates           = st.slider("Sulphates",           min_value=0.3,   max_value=2.0,   value=0.56,  step=0.01)
        alcohol             = st.slider("Alcohol (%)",         min_value=8.0,   max_value=15.0,  value=9.4,   step=0.1)

    submitted = st.form_submit_button("Evaluar vino 🍷")


if submitted:
    # Crear fila con los valores ingresados (mismo orden que el entrenamiento)
    datos = np.array([
        fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
        free_so2, total_so2, density, pH, sulphates, alcohol
    ]).reshape(1, -1)

    # Predecir
    proba = predictor.predict_proba(datos)[0, 1]   # probabilidad clase 1 (alta calidad)
    # clase = 1 if proba >= umbral else 0
    clase = predictor.predict(datos)[0]

    # Resultado visual
    if clase == 1:
        st.success(f"**Alta calidad** (probabilidad: {proba:.1%}) 🎉")
    else:
        st.warning(f"Baja calidad (probabilidad alta calidad: {proba:.1%}) 😕")

    st.progress(proba)
    st.caption(f"Probabilidad de ser vino de **alta calidad**: **{proba:.1%}**")
