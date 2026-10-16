"""Aplicación Streamlit del tablero ENCC 2017. Ejecutar desde la raíz del repositorio."""
from pathlib import Path
import sys
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from visualizaciones_encc import REGIONES, crear_tablero, filtrar, preparar_datos

ARCHIVO = ROOT / "proyecto_equipo/datos/derivados/encc_2017_limpio.parquet"

st.set_page_config(page_title="ENCC 2017 · Asistencia al cine", page_icon="🎬", layout="wide")
st.title("¿Quiénes fueron al cine?")
st.caption("ENCC 2017 · Personas de 13 años y más · estimaciones ponderadas con pondera_dem")
st.markdown("Este tablero describe diferencias en la asistencia al cine durante el último año (`p63`). Las asociaciones observadas no implican causalidad.")

@st.cache_data
def cargar():
    return preparar_datos(pd.read_parquet(ARCHIVO))

if not ARCHIVO.exists():
    st.error("No se encontró el parquet limpio. Ejecutá primero el cuaderno 02_limpieza_encc.ipynb.")
    st.stop()

datos = cargar()
with st.sidebar:
    st.header("Filtros globales")
    regiones = st.multiselect("Regiones", REGIONES, default=REGIONES)
    sexos_disponibles = sorted(datos["sexo"].dropna().unique().tolist())
    sexos = st.multiselect("Sexo", sexos_disponibles, default=sexos_disponibles)
    edades = st.slider("Edad", int(datos.edad.min()), int(datos.edad.max()),
                       (int(datos.edad.min()), int(datos.edad.max())))

vista = filtrar(datos, regiones, sexos, edades)
if vista.empty:
    st.info("No hay personas para la combinación de filtros seleccionada.")
    st.stop()

peso_si = vista.loc[vista.p63 == "SI", "pondera_dem"].sum()
peso_total = vista.pondera_dem.sum()
porcentaje = 100 * peso_si / peso_total if peso_total else float("nan")
por_region = vista.groupby("region").apply(
    lambda g: 100 * g.loc[g.p63 == "SI", "pondera_dem"].sum() / g.pondera_dem.sum(),
    include_groups=False,
)
col1, col2, col3 = st.columns(3)
col1.metric("Asistencia estimada", f"{porcentaje:.1f}%")
col2.metric("Respuestas válidas", f"{len(vista):,}")
if len(por_region) >= 2:
    orden = por_region.sort_values()
    col3.metric("Brecha entre regiones", f"{orden.iloc[-1]-orden.iloc[0]:.1f} pp",
                help=f"{orden.index[-1]} ({orden.iloc[-1]:.1f}%) − {orden.index[0]} ({orden.iloc[0]:.1f}%)")
else:
    col3.metric("Regiones seleccionadas", str(len(por_region)))

if len(por_region) >= 2:
    orden = por_region.sort_values()
    st.subheader(f"En la selección actual, la estimación va de {orden.iloc[0]:.1f}% en {orden.index[0]} a {orden.iloc[-1]:.1f}% en {orden.index[-1]}.")

st.plotly_chart(crear_tablero(vista), width="stretch")
st.caption("Cada panel muestra la composición ponderada de respuestas SI/NO dentro del grupo; n indica casos observados. Fuente: ENCC 2017, Secretaría de Cultura de la Nación. Las barras no representan intervalos de confianza: no se cuenta aquí con información suficiente del diseño muestral para estimarlos.")
