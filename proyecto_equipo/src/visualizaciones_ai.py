"""Preparación compartida de datos y gráficos del tablero: adopción de IA en empresas (2023–2026).

Fuente: Kaggle, Global AI Adoption & Workforce Impact Dataset (ai_company_adoption.csv).
Cada fila es una empresa en un trimestre (empresa-trimestre). El dataset no trae pesos,
así que todas las medias son simples (sin ponderar).
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

REGIONES = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"]
INDUSTRIAS = ["Agriculture", "Consulting", "Education", "Finance", "Healthcare",
              "Logistics", "Manufacturing", "Retail", "Technology"]
# Ordenados por la mediana de empleados de cada categoría (54, 543 y 10.796)
TAMANOS = ["Startup", "SME", "Enterprise"]
ANIOS = [2023, 2024, 2025, 2026]
PALETA = {"Startup": "#D98E04", "SME": "#176B87", "Enterprise": "#7A3E9D"}
COLOR_BASE = "#176B87"

COLUMNAS = ["company_id", "survey_year", "region", "industry", "company_size", "ai_adoption_rate"]


def preparar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Deja solo las variables necesarias para el tablero y valida su contenido."""
    faltantes = sorted(set(COLUMNAS) - set(df.columns))
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")
    out = df[COLUMNAS].copy()
    out["survey_year"] = pd.to_numeric(out["survey_year"], errors="coerce")
    out["ai_adoption_rate"] = pd.to_numeric(out["ai_adoption_rate"], errors="coerce")
    out = out.dropna(subset=COLUMNAS)
    out = out[out["ai_adoption_rate"].between(0, 100)]
    for col in ["region", "industry", "company_size"]:
        out[col] = out[col].astype("string")
    out["survey_year"] = out["survey_year"].astype(int)
    return out.reset_index(drop=True)


def filtrar(datos: pd.DataFrame, regiones=None, industrias=None, tamanos=None,
            anios=(2023, 2026)) -> pd.DataFrame:
    """Aplica filtros globales; listas vacías representan una selección vacía."""
    out = datos.copy()
    if regiones is not None:
        out = out[out["region"].isin(regiones)]
    if industrias is not None:
        out = out[out["industry"].isin(industrias)]
    if tamanos is not None:
        out = out[out["company_size"].isin(tamanos)]
    out = out[out["survey_year"].between(anios[0], anios[1])]
    return out


def resumen_por_grupo(datos: pd.DataFrame, grupo: str, por=None) -> pd.DataFrame:
    """Media, mediana, empresas distintas y filas empresa-trimestre por grupo.

    Si se indica `por`, se calcula por cada combinación de `grupo` y `por`.
    """
    claves = [grupo] if por is None else [grupo, por]
    if datos.empty:
        return pd.DataFrame(columns=claves + ["media", "mediana", "n_empresas", "n_filas"])
    resumen = (datos.groupby(claves, observed=True)
               .agg(media=("ai_adoption_rate", "mean"),
                    mediana=("ai_adoption_rate", "median"),
                    n_empresas=("company_id", "nunique"),
                    n_filas=("ai_adoption_rate", "size"))
               .reset_index())
    orden = {"region": REGIONES, "industry": INDUSTRIAS, "company_size": TAMANOS,
             "survey_year": ANIOS}
    for col in claves:
        if col in orden:
            resumen[col] = pd.Categorical(resumen[col], categories=orden[col], ordered=True)
    return resumen.sort_values(claves).reset_index(drop=True)


def crear_tablero(datos: pd.DataFrame):
    """Tablero de tres vistas: evolución, diferencias regionales e industriales."""
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"colspan": 2}, None], [{}, {}]],
        subplot_titles=("Evolución anual", "Por región", "Por industria"),
        horizontal_spacing=0.12, vertical_spacing=0.22,
    )
    hover_linea = ("Año: %{x}<br>Adopción media: %{y:.1f}%"
                   "<br>Empresas distintas: %{customdata[0]:,}"
                   "<br>Filas empresa-trimestre: %{customdata[1]:,}<extra></extra>")
    hover_barras = ("Grupo: %{y}<br>Adopción media: %{x:.1f}%"
                    "<br>Empresas distintas: %{customdata[0]:,}"
                    "<br>Filas empresa-trimestre: %{customdata[1]:,}<extra></extra>")

    tablas = {
        "region": resumen_por_grupo(datos, "region"),
        "industry": resumen_por_grupo(datos, "industry"),
        "anio": resumen_por_grupo(datos, "survey_year"),
    }

    for clave, fila, col in [("region", 2, 1), ("industry", 2, 2)]:
        tabla = tablas[clave]
        tabla = tabla.sort_values("media")
        fig.add_trace(
            go.Bar(x=tabla["media"], y=tabla[clave].astype(str), orientation="h",
                   customdata=tabla[["n_empresas", "n_filas"]].to_numpy(),
                   marker_color=COLOR_BASE, showlegend=False,
                   text=tabla["media"].round(1).astype(str) + "%", textposition="outside",
                   hovertemplate=hover_barras),
            row=fila, col=col)
        fig.add_vline(x=datos["ai_adoption_rate"].mean(), line_dash="dot",
                      line_color="#7F7F7F", row=fila, col=col,
                      annotation_text="Promedio del recorte", annotation_position="top")

    # El período completo se conserva para no ocultar cambios que contradigan el titular.
    tabla = tablas["anio"]
    inicio, fin = tabla.iloc[0], tabla.iloc[-1]
    cambio = fin["media"] - inicio["media"]
    if int(inicio["survey_year"]) == int(fin["survey_year"]):
        titular = f"La adopción media fue {fin['media']:.1f}% en {int(fin['survey_year'])}"
    elif abs(cambio) < 0.05:
        titular = (f"La adopción media se mantuvo en {fin['media']:.1f}% entre "
                   f"{int(inicio['survey_year'])} y {int(fin['survey_year'])}")
    else:
        verbo = "subió" if cambio > 0 else "bajó"
        titular = (f"La adopción media {verbo} {abs(cambio):.1f} puntos porcentuales "
                   f"entre {int(inicio['survey_year'])} y {int(fin['survey_year'])}")
    fig.add_trace(go.Scatter(
        x=tabla["survey_year"].astype(str), y=tabla["media"], mode="lines+markers+text",
        customdata=tabla[["n_empresas", "n_filas"]].to_numpy(),
        text=tabla["media"].round(1).astype(str) + "%", textposition="top center",
        line=dict(color=COLOR_BASE, width=3), marker=dict(size=9), showlegend=False,
        hovertemplate=hover_linea), row=1, col=1)
    fig.update_xaxes(title_text="Año de encuesta", row=1, col=1)

    fig.update_yaxes(title_text="Adopción media (%)", range=[0, 100], row=1, col=1)
    for fila, col in [(2, 1), (2, 2)]:
        fig.update_xaxes(title_text="Adopción media (%)", range=[0, 100], row=fila, col=col)
        fig.update_yaxes(title_text="", row=fila, col=col)

    fig.update_layout(
        template="plotly_white", height=760,
        title=dict(text=titular,
                   x=0.02, xanchor="left"),
        margin=dict(l=35, r=45, t=100, b=55),
    )
    return fig
