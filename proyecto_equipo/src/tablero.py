"""Aplicación Streamlit del tablero de adopción de IA en empresas. Ejecutar desde la raíz del repositorio."""
from pathlib import Path
import sys
import inspect
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from visualizaciones_ai import INDUSTRIAS, REGIONES, TAMANOS, crear_tablero, filtrar, preparar_datos

ARCHIVO = ROOT / "proyecto_equipo/datos/derivados/ai_company_adoption_limpio.parquet"

st.set_page_config(page_title="Adopción de IA en empresas", page_icon="🤖", layout="wide")
st.title("¿Cómo evoluciona y dónde se adopta más la IA?")
st.caption("Global AI Adoption & Workforce Impact Dataset (Kaggle) · fuente consultada en octubre de 2026 · empresa-trimestre, 2023–2026 · medias simples, sin ponderar")
st.markdown("**Audiencia y decisión:** el equipo que sigue la adopción de IA puede identificar qué regiones e industrias conviene revisar con más detalle. El tablero describe asociaciones; no estima efectos causales ni representa a todas las empresas.")

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
por_anio = vista.groupby("survey_year", observed=True)["ai_adoption_rate"].mean().sort_index()
por_region = vista.groupby("region", observed=True)["ai_adoption_rate"].mean()
col1, col2, col3 = st.columns(3)
col1.metric("Adopción media en la selección", f"{promedio:.1f}%", help="Referencia: escala completa de 0 a 100 %.")
if len(por_anio) >= 2:
    cambio = por_anio.iloc[-1] - por_anio.iloc[0]
    col2.metric(f"Cambio {int(por_anio.index[0])}–{int(por_anio.index[-1])}", f"{cambio:+.1f} pp",
                help="Diferencia entre el primer y el último año seleccionado; puntos porcentuales.")
else:
    col2.metric("Cambio entre años", "—", help="Seleccioná al menos dos años para comparar.")
col3.metric("Empresas distintas", f"{vista.company_id.nunique():,}", help=f"{len(vista):,} filas empresa-trimestre.")

if len(por_region) >= 2:
    orden = por_region.sort_values()
    st.subheader(f"En la selección actual, la adopción media va de {orden.iloc[0]:.1f}% en {orden.index[0]} a {orden.iloc[-1]:.1f}% en {orden.index[-1]}.")

figura = crear_tablero(vista)
if "width" in inspect.signature(st.plotly_chart).parameters:
    st.plotly_chart(figura, width="stretch")
else:  # Compatibilidad con Streamlit 1.30–1.48
    st.plotly_chart(figura, use_container_width=True)
st.caption("Las tres vistas usan los mismos filtros y el período completo seleccionado. Las barras empiezan en cero y comparten escala de 0 a 100 %. Al pasar el cursor se muestran empresas distintas y filas empresa-trimestre; las observaciones de una misma empresa se repiten en el tiempo, por lo que estos conteos no son independientes. La fuente no publica ponderaciones ni un diseño muestral verificable; no se muestran intervalos de confianza ni se extrapolan los resultados a todas las empresas. Fuente: Kaggle, Global AI Adoption & Workforce Impact Dataset; datos 2023–2026.")
