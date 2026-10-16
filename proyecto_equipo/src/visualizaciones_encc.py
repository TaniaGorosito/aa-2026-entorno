"""Preparación compartida de datos y gráficos del tablero ENCC 2017."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

REGIONES = ["CABA", "PBA", "CENTRO", "CUYO", "NEA", "NOA", "PATAGONIA"]
PALETA = {"SI": "#176B87", "NO": "#D98E04"}


def preparar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Deriva una franja etaria y deja las variables necesarias para el tablero."""
    columnas = ["edad", "sexo", "region", "p63", "pondera_dem"]
    faltantes = sorted(set(columnas) - set(df.columns))
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")
    out = df[columnas].copy()
    out["edad"] = pd.to_numeric(out["edad"], errors="coerce")
    out["pondera_dem"] = pd.to_numeric(out["pondera_dem"], errors="coerce")
    out = out.dropna(subset=["edad", "sexo", "region", "p63", "pondera_dem"])
    out = out[(out["pondera_dem"] > 0) & out["p63"].isin(["SI", "NO"])]
    out["franja_edad"] = pd.cut(
        out["edad"], bins=[12, 24, 39, 59, 120],
        labels=["13–24", "25–39", "40–59", "60+"], include_lowest=True,
    )
    out["franja_edad"] = out["franja_edad"].astype("string")
    return out.reset_index(drop=True)


def filtrar(datos: pd.DataFrame, regiones=None, sexos=None, edades=(13, 99)) -> pd.DataFrame:
    """Aplica filtros globales; listas vacías representan una selección vacía."""
    out = datos.copy()
    if regiones is not None:
        out = out[out["region"].isin(regiones)]
    if sexos is not None:
        out = out[out["sexo"].isin(sexos)]
    out = out[out["edad"].between(edades[0], edades[1])]
    return out


def resumen_ponderado(datos: pd.DataFrame, grupo: str) -> pd.DataFrame:
    """Calcula porcentajes ponderados y n muestral por grupo y respuesta."""
    if datos.empty:
        return pd.DataFrame(columns=[grupo, "p63", "porcentaje", "n"])
    resumen = (datos.groupby([grupo, "p63"], observed=False)
               .agg(peso=("pondera_dem", "sum"), n=("p63", "size"))
               .reset_index())
    denominador = resumen.groupby(grupo, observed=False)["peso"].transform("sum")
    resumen["porcentaje"] = 100 * resumen["peso"] / denominador
    if grupo == "region":
        resumen[grupo] = pd.Categorical(resumen[grupo], categories=REGIONES, ordered=True)
    elif grupo == "franja_edad":
        resumen[grupo] = pd.Categorical(
            resumen[grupo], categories=["13–24", "25–39", "40–59", "60+"], ordered=True
        )
    return resumen.sort_values([grupo, "p63"])


def crear_tablero(datos: pd.DataFrame):
    """Tablero de tres vistas alineadas a la pregunta de análisis del TP."""
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Asistencia por región", "Asistencia por edad", "Asistencia por sexo"),
        horizontal_spacing=0.11,
    )
    especificaciones = [("region", 1, "bar"), ("franja_edad", 2, "line"), ("sexo", 3, "bar")]
    for grupo, col, tipo in especificaciones:
        tabla = resumen_ponderado(datos, grupo)
        for respuesta in ["SI", "NO"]:
            parte = tabla[tabla["p63"] == respuesta]
            hover = "Grupo: %{x}<br>Respuesta: %{fullData.name}<br>Estimación ponderada: %{y:.1f}%<br>Personas encuestadas: %{customdata}<extra></extra>"
            if tipo == "line":
                traza = go.Scatter(x=parte[grupo], y=parte["porcentaje"], mode="lines+markers+text",
                    text=parte["porcentaje"].round(1).astype(str) + "%", textposition="top center",
                    customdata=parte["n"], name=respuesta, legendgroup=respuesta,
                    line=dict(color=PALETA[respuesta], width=3), marker=dict(size=8),
                    hovertemplate=hover)
            else:
                traza = go.Bar(x=parte[grupo], y=parte["porcentaje"], customdata=parte["n"],
                    name=respuesta, legendgroup=respuesta, marker_color=PALETA[respuesta],
                    text=parte["porcentaje"].round(1).astype(str) + "%", textposition="outside",
                    hovertemplate=hover)
            fig.add_trace(traza, row=1, col=col)
    fig.update_layout(
        template="plotly_white", height=470, barmode="stack",
        title=dict(text="Asistencia al cine durante el último año · ENCC 2017", x=0.02, xanchor="left"),
        legend_title_text="Respuesta", margin=dict(l=35, r=25, t=95, b=55),
    )
    for col in [1, 2, 3]:
        fig.update_yaxes(title_text="Porcentaje ponderado", range=[0, 108], ticksuffix="%", row=1, col=col)
        fig.update_xaxes(title_text="", row=1, col=col)
    return fig
