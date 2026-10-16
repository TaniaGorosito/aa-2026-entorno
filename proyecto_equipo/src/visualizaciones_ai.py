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

COLUMNAS = ["survey_year", "region", "industry", "company_size", "ai_adoption_rate"]


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
    """Media, mediana y n (filas empresa-trimestre) de la tasa de adopción por grupo.

    Si se indica `por`, se calcula por cada combinación de `grupo` y `por`.
    """
    claves = [grupo] if por is None else [grupo, por]
    if datos.empty:
        return pd.DataFrame(columns=claves + ["media", "mediana", "n"])
    resumen = (datos.groupby(claves, observed=True)["ai_adoption_rate"]
               .agg(media="mean", mediana="median", n="size")
               .reset_index())
    orden = {"region": REGIONES, "industry": INDUSTRIAS, "company_size": TAMANOS,
             "survey_year": ANIOS}
    for col in claves:
        if col in orden:
            resumen[col] = pd.Categorical(resumen[col], categories=orden[col], ordered=True)
    return resumen.sort_values(claves).reset_index(drop=True)


def crear_tablero(datos: pd.DataFrame):
    """Tablero de cuatro vistas alineadas con las preguntas P1 a P3 y la evolución anual."""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Adopción por región", "Adopción por industria",
                        "Adopción por tamaño de empresa", "Adopción por año"),
        horizontal_spacing=0.10, vertical_spacing=0.20,
    )
    hover = ("Grupo: %{x}<br>Adopción promedio: %{y:.1f}%"
             "<br>Filas (empresa-trimestre): %{customdata:,}<extra></extra>")

    tablas = {
        "region": resumen_por_grupo(datos, "region"),
        "industry": resumen_por_grupo(datos, "industry"),
        "company_size": resumen_por_grupo(datos, "company_size"),
        "anio": resumen_por_grupo(datos, "survey_year", por="company_size"),
    }

    posiciones = [("region", 1, 1), ("industry", 1, 2), ("company_size", 2, 1)]
    for clave, fila, col in posiciones:
        tabla = tablas[clave]
        colores = [PALETA.get(str(g), COLOR_BASE) for g in tabla[clave]]
        fig.add_trace(
            go.Bar(x=tabla[clave].astype(str), y=tabla["media"], customdata=tabla["n"],
                   marker_color=colores, showlegend=False,
                   text=tabla["media"].round(1).astype(str) + "%", textposition="outside",
                   hovertemplate=hover),
            row=fila, col=col)

    # Evolución anual: una línea por tamaño de empresa
    tabla = tablas["anio"]
    for tamano in TAMANOS:
        parte = tabla[tabla["company_size"] == tamano]
        fig.add_trace(
            go.Scatter(x=parte["survey_year"].astype(str), y=parte["media"], mode="lines+markers",
                       customdata=parte["n"], name=tamano, legendgroup=tamano,
                       line=dict(color=PALETA[tamano], width=3), marker=dict(size=8),
                       hovertemplate=hover),
            row=2, col=2)

    # Misma escala vertical en las cuatro vistas, para poder compararlas
    maximo = max([float(t["media"].max()) for t in tablas.values() if not t.empty] or [100.0])
    for fila, col in [(1, 1), (1, 2), (2, 1), (2, 2)]:
        fig.update_yaxes(title_text="Adopción promedio", range=[0, maximo * 1.25],
                         ticksuffix="%", row=fila, col=col)
        fig.update_xaxes(title_text="", row=fila, col=col)

    fig.update_layout(
        template="plotly_white", height=720,
        title=dict(text="Tasa promedio de adopción de IA en empresas · 2023–2026",
                   x=0.02, xanchor="left"),
        legend_title_text="Tamaño de empresa", margin=dict(l=35, r=25, t=95, b=55),
    )
    return fig
