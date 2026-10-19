"""Aplicación Streamlit del tablero de adopción de IA en empresas. Ejecutar desde la raíz del repositorio."""
from pathlib import Path
import sys
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from visualizaciones_ai import INDUSTRIAS, REGIONES, TAMANOS, crear_tablero, filtrar, preparar_datos

ARCHIVO = ROOT / "proyecto_equipo/datos/derivados/ai_company_adoption_limpio.parquet"

st.set_page_config(page_title="Adopción de IA en empresas", page_icon="🤖", layout="wide")
st.title("¿Dónde y en qué empresas se adopta más la IA?")
st.caption("Global AI Adoption & Workforce Impact Dataset (Kaggle) · empresa-trimestre, 2023–2026 · medias simples, sin ponderar")
st.markdown("Este tablero describe diferencias en la tasa de adopción de IA (`ai_adoption_rate`) según región, industria, tamaño de empresa y año. Las asociaciones observadas no implican causalidad.")

@st.cache_data
def cargar():
    return preparar_datos(pd.read_parquet(ARCHIVO))

if not ARCHIVO.exists():
    st.error("No se encontró el parquet limpio. Ejecutá primero el cuaderno 02_limpieza_ai.ipynb.")
    st.stop()

datos = cargar()
with st.sidebar:
    st.header("Filtros globales")
    regiones = st.multiselect("Regiones", REGIONES, default=REGIONES)
    industrias = st.multiselect("Industrias", INDUSTRIAS, default=INDUSTRIAS)
    tamanos = st.multiselect("Tamaño de empresa", TAMANOS, default=TAMANOS)
    anio_min, anio_max = int(datos.survey_year.min()), int(datos.survey_year.max())
    anios = st.slider("Año", anio_min, anio_max, (anio_min, anio_max))

vista = filtrar(datos, regiones, industrias, tamanos, anios)
if vista.empty:
    st.info("No hay empresas para la combinación de filtros seleccionada.")
    st.stop()

promedio = vista["ai_adoption_rate"].mean()
por_region = vista.groupby("region", observed=True)["ai_adoption_rate"].mean()
col1, col2, col3 = st.columns(3)
col1.metric("Adopción promedio", f"{promedio:.1f}%")
col2.metric("Filas (empresa-trimestre)", f"{len(vista):,}")
if len(por_region) >= 2:
    orden = por_region.sort_values()
    col3.metric("Brecha entre regiones", f"{orden.iloc[-1]-orden.iloc[0]:.1f} pp",
                help=f"{orden.index[-1]} ({orden.iloc[-1]:.1f}%) − {orden.index[0]} ({orden.iloc[0]:.1f}%)")
else:
    col3.metric("Regiones seleccionadas", str(len(por_region)))

if len(por_region) >= 2:
    orden = por_region.sort_values()
    st.subheader(f"En la selección actual, la adopción promedio va de {orden.iloc[0]:.1f}% en {orden.index[0]} a {orden.iloc[-1]:.1f}% en {orden.index[-1]}.")

st.plotly_chart(crear_tablero(vista), width="stretch")
st.caption("Cada panel muestra la tasa de adopción promedio dentro del grupo; n (al pasar el mouse) cuenta filas empresa-trimestre, no empresas distintas, y las filas de una misma empresa no son independientes. Fuente: Global AI Adoption & Workforce Impact Dataset, Kaggle. El dataset no trae pesos ni se conoce cómo se generaron los datos, así que los resultados no se pueden extrapolar a todas las empresas. Las barras no representan intervalos de confianza.")
