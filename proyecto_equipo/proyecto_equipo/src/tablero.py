
# tablero.py — versión con servidor del tablero del LAB 6.
# Se ejecuta desde una terminal, NO desde el cuaderno:  streamlit run tablero.py
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Adopción de IA en Empresas', layout='wide')

@st.cache_data
def cargar_datos():
    nombres_posibles = ['ai_company_adoption_limpio.parquet', 'ai_company_adoption.csv']
    ruta_encontrada = None
    directorios = [Path.cwd(), *Path.cwd().parents]

    for directorio in directorios:
        for nombre in nombres_posibles:
            coincidencias = list(directorio.glob(f"**/{nombre}"))
            if coincidencias:
                ruta_encontrada = coincidencias[0]
                break
        if ruta_encontrada:
            break

    if ruta_encontrada is None:
        st.error("No se encontró el archivo de datos.")
        st.stop()

    if ruta_encontrada.suffix == '.parquet':
        df = pd.read_parquet(ruta_encontrada)
    else:
        df = pd.read_csv(ruta_encontrada)

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df['survey_year'] = pd.to_numeric(df['survey_year'], errors='coerce').astype(int)
    df['ai_adoption_rate'] = pd.to_numeric(df['ai_adoption_rate'], errors='coerce')
    df['num_employees'] = pd.to_numeric(df['num_employees'], errors='coerce')
    df['annual_revenue_usd_millions'] = pd.to_numeric(df['annual_revenue_usd_millions'], errors='coerce')
    df['industry'] = df['industry'].astype(str)
    df['country'] = df['country'].astype(str)
    return df

df = cargar_datos()

# --- Controles en la barra lateral ---
st.sidebar.header('Filtros')

industrias_default = df.groupby('industry')['company_id'].count().nlargest(5).index.tolist()
industrias = st.sidebar.multiselect(
    'Industria',
    sorted(df['industry'].unique()),
    default=industrias_default
)

anios = sorted(df['survey_year'].unique())
desde, hasta = st.sidebar.select_slider(
    'Período analizado',
    options=anios,
    value=(int(min(anios)), int(max(anios)))
)

# Filtrado reactivo
d = df[df['industry'].isin(industrias) & df['survey_year'].between(desde, hasta)]

if d.empty:
    st.warning('El filtro no arroja resultados. Amplía la selección.')
    st.stop()

# --- Fila 1: Indicadores (KPIs) ---
st.title('Tablero: Adopción de IA en Empresas')

ultimo_anio = d['survey_year'].max()
actual = d[d['survey_year'] == ultimo_anio]
anterior = d[d['survey_year'] == (ultimo_anio - 1)]

c1, c2, c3 = st.columns(3)

val_adop_act = actual['ai_adoption_rate'].mean()
val_adop_ant = anterior['ai_adoption_rate'].mean() if len(anterior) > 0 else val_adop_act
delta_adop = (val_adop_act - val_adop_ant) / val_adop_ant * 100 if val_adop_ant else 0.0
c1.metric('Adopción Promedio (%)', f"{val_adop_act:,.1f}%", f"{delta_adop:+.1f}%")

val_emp_act = actual['company_id'].nunique()
val_emp_ant = anterior['company_id'].nunique() if len(anterior) > 0 else val_emp_act
delta_emp = (val_emp_act - val_emp_ant) / val_emp_ant * 100 if val_emp_ant else 0.0
c2.metric('Empresas Observadas', f"{val_emp_act:,}", f"{delta_emp:+.1f}%")

val_rev_act = actual['annual_revenue_usd_millions'].mean()
val_rev_ant = anterior['annual_revenue_usd_millions'].mean() if len(anterior) > 0 else val_rev_act
delta_rev = (val_rev_act - val_rev_ant) / val_rev_ant * 100 if val_rev_ant else 0.0
c3.metric('Ingresos Medios (M USD)', f"${val_rev_act:,.1f}", f"{delta_rev:+.1f}%")

# --- Vistas ---
# Vista temporal
ev = d.groupby(['survey_year', 'industry'], as_index=False)['ai_adoption_rate'].mean()
fig_line = px.line(
    ev, x='survey_year', y='ai_adoption_rate', color='industry', markers=True,
    labels={'survey_year': 'Año', 'ai_adoption_rate': 'Adopción (%)', 'industry': 'Industria'},
    title='Evolución de adopción de IA por industria'
)
fig_line.update_yaxes(range=[0, 100])
st.plotly_chart(fig_line, use_container_width=True)

izq, der = st.columns(2)

# Ranking por país
paises_top = d.groupby('country')['company_id'].count().nlargest(6).index.tolist()
d_paises = d[d['country'].isin(paises_top)]
prov = d_paises.groupby('country', as_index=False)['ai_adoption_rate'].mean().sort_values('ai_adoption_rate')

fig_bar = px.bar(
    prov, x='ai_adoption_rate', y='country', orientation='h',
    labels={'ai_adoption_rate': 'Adopción (%)', 'country': 'País'},
    title='Rendimiento medio por país'
)
fig_bar.update_xaxes(range=[0, 100])
fig_bar.update_traces(marker_color='#1F3864')
izq.plotly_chart(fig_bar, use_container_width=True)

# Dispersión
fig_scatter = px.scatter(
    d.sample(min(1500, len(d)), random_state=42),
    x='num_employees', y='ai_adoption_rate',
    color='ai_adoption_rate', color_continuous_scale='Blues',
    labels={'num_employees': 'Empleados (escala log)', 'ai_adoption_rate': 'Adopción (%)'},
    title='Empleados vs. Tasa de Adopción',
    log_x=True
)
fig_scatter.update_yaxes(range=[0, 100])
der.plotly_chart(fig_scatter, use_container_width=True)

st.caption(f'{len(d):,} registros analizados.')
