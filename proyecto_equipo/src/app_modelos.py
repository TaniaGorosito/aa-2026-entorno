"""Demostración interactiva de regresión (TP2) y clasificación (TP3)."""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

PROYECTO = Path(__file__).resolve().parents[1]
SALIDAS = PROYECTO / "salidas"
ETIQUETAS_CAMPOS = {
    "num_employees": "Cantidad de empleados",
    "annual_revenue_usd_millions": "Ingresos anuales (millones de USD)",
    "company_age": "Antigüedad de la empresa (años)",
    "survey_year": "Año de la encuesta",
    "country": "País",
    "industry": "Sector",
    "num_ai_tools_used": "Herramientas de IA utilizadas",
    "ai_training_hours": "Horas de capacitación en IA",
}
ETIQUETAS_SECTOR = {
    "Agriculture": "Agricultura", "Consulting": "Consultoría", "Education": "Educación",
    "Finance": "Finanzas", "Healthcare": "Salud", "Logistics": "Logística",
    "Manufacturing": "Manufactura", "Retail": "Comercio minorista", "Technology": "Tecnología",
}
ETIQUETAS_ETAPA = {"none": "Ninguna", "pilot": "Piloto", "partial": "Parcial", "full": "Completa"}

st.set_page_config(page_title="Demo de modelos de adopción de IA", page_icon="🤖", layout="wide")
st.title("Predicción y clasificación de adopción de IA")
st.caption("Cada ejemplo procede del conjunto de prueba: son observaciones de empresas que los modelos no usaron al entrenar.")


def cargar(nombre_modelo: str, nombre_muestras: str):
    ruta_modelo = SALIDAS / nombre_modelo
    ruta_muestras = SALIDAS / nombre_muestras
    faltan = [str(p.relative_to(PROYECTO)) for p in (ruta_modelo, ruta_muestras) if not p.exists()]
    if faltan:
        st.error("Primero ejecutá los cuadernos 02, 05 y 07 para generar los modelos y las muestras reservadas.")
        st.code("python -m jupyter lab  # abrir los cuadernos y ejecutarlos en orden")
        st.write("Faltan:", ", ".join(faltan))
        st.stop()
    return joblib.load(ruta_modelo), pd.read_csv(ruta_muestras)


def coincide_con_muestra(entrada: pd.DataFrame, muestra: pd.Series, features: list[str]) -> bool:
    for col in features:
        recibido = entrada.iloc[0][col]
        esperado = muestra[col]
        if isinstance(esperado, str):
            if str(recibido) != esperado:
                return False
        elif not np.isclose(float(recibido), float(esperado), rtol=0, atol=1e-8):
            return False
    return True


def selector_muestra(muestras: pd.DataFrame, modo: str) -> pd.Series:
    demo_id = st.selectbox("Elegí una observación reservada del test", muestras["demo_id"].tolist(), key=f"demo_{modo}")
    return muestras.loc[muestras["demo_id"] == demo_id].iloc[0]


def campos_entrada(bundle: dict, muestra: pd.Series, modo: str) -> pd.DataFrame:
    features = bundle["features"]
    categorias = bundle["category_options"]
    st.markdown("Ajustá los campos si querés probar otro caso. La clase real solo se compara si se mantienen los valores de la muestra reservada.")
    with st.form(f"form_{modo}"):
        cols = st.columns(2)
        entrada = {}
        for i, feature in enumerate(features):
            cont = cols[i % 2]
            key = f"{modo}_{muestra.demo_id}_{feature}"
            if feature in categorias:
                opciones = categorias[feature]
                valor = str(muestra[feature])
                indice = opciones.index(valor) if valor in opciones else 0
                entrada[feature] = cont.selectbox(ETIQUETAS_CAMPOS.get(feature, feature), opciones, format_func=lambda opcion: ETIQUETAS_SECTOR.get(opcion, opcion), index=indice, key=key)
            elif feature == "num_employees":
                entrada[feature] = cont.number_input(ETIQUETAS_CAMPOS.get(feature, feature), min_value=1, value=int(muestra[feature]), step=1, key=key)
            elif feature == "annual_revenue_usd_millions":
                entrada[feature] = cont.number_input(ETIQUETAS_CAMPOS.get(feature, feature), min_value=0.0, value=float(muestra[feature]), step=1.0, key=key)
            elif feature == "ai_training_hours":
                entrada[feature] = cont.number_input(ETIQUETAS_CAMPOS.get(feature, feature), min_value=0.0, max_value=80.0, value=float(muestra[feature]), step=1.0, key=key)
            elif feature in {"company_age", "survey_year", "num_ai_tools_used"}:
                minimo = 2023 if feature == "survey_year" else 0
                maximo = 2026 if feature == "survey_year" else (80 if feature == "ai_training_hours" else (6 if feature == "num_ai_tools_used" else 100))
                entrada[feature] = cont.number_input(ETIQUETAS_CAMPOS.get(feature, feature), min_value=minimo, max_value=maximo, value=int(muestra[feature]), step=1, key=key)
            else:
                entrada[feature] = cont.number_input(ETIQUETAS_CAMPOS.get(feature, feature), value=float(muestra[feature]), key=key)
        enviar = st.form_submit_button("Predecir")
    return pd.DataFrame([entrada], columns=features), enviar


def mostrar_regresion():
    bundle, muestras = cargar("modelo_regresion_tp2.joblib", "muestras_prueba_regresion.csv")
    st.subheader("TP2 · Regresión")
    st.write(f"Modelo elegido por RMSE de validación cruzada agrupada: **{bundle['model_name']}**")
    muestra = selector_muestra(muestras, "reg")
    entrada, enviar = campos_entrada(bundle, muestra, "reg")
    if enviar:
        pred = float(bundle["model"].predict(entrada)[0])
        st.metric("Tasa de adopción predicha", f"{pred:.2f} %")
        if coincide_con_muestra(entrada, muestra, bundle["features"]):
            real = float(muestra[bundle["target"]])
            error = pred - real
            col1, col2, col3 = st.columns(3)
            col1.metric("Valor real reservado", f"{real:.2f} %")
            col2.metric("Error firmado", f"{error:+.2f} pp")
            col3.metric("Error absoluto", f"{abs(error):.2f} pp")
        else:
            st.info("La predicción corresponde a los valores ingresados. No se muestra una etiqueta real porque ya no coincide con la fila reservada.")


def mostrar_clasificacion():
    bundle, muestras = cargar("modelo_clasificacion_tp3.joblib", "muestras_prueba_clasificacion.csv")
    st.subheader("TP3 · Clasificación")
    st.write(f"Modelo elegido por F1 macro de validación cruzada agrupada: **{bundle['model_name']}**")
    muestra = selector_muestra(muestras, "clas")
    entrada, enviar = campos_entrada(bundle, muestra, "clas")
    if enviar:
        pred = str(bundle["model"].predict(entrada)[0])
        st.metric("Etapa predicha", ETIQUETAS_ETAPA.get(pred, pred))
        if coincide_con_muestra(entrada, muestra, bundle["features"]):
            real = str(muestra[bundle["target"]])
            col1, col2 = st.columns(2)
            col1.metric("Etapa real reservada", ETIQUETAS_ETAPA.get(real, real))
            col2.metric("Resultado", "Correcta" if pred == real else "No coincide")
        else:
            st.info("La predicción corresponde a los valores ingresados. No se muestra una clase real porque ya no coincide con la fila reservada.")

reg_tab, clas_tab = st.tabs(["Predicción continua", "Clasificación"])
with reg_tab:
    mostrar_regresion()
with clas_tab:
    mostrar_clasificacion()
