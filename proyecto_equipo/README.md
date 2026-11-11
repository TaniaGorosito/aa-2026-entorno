# Bitácora del equipo — Aprendizaje Automático y Grandes Datos

> Este archivo se actualiza en cada entrega.

Repositorio: https://github.com/TaniaGorosito/aa-2026-entorno

## Conjunto de datos del equipo
- Nombre y origen: Global AI Adoption & Workforce Impact Dataset, publicado en Kaggle por mohankrishnathalla. Se usa el archivo ai_company_adoption.csv. La fuente no documenta cómo se generaron ni se recolectaron los datos.
- Enlace: https://www.kaggle.com/datasets/mohankrishnathalla/global-ai-adoption-and-workforce-impact-dataset?select=ai_company_adoption.csv (consultado el 10 de noviembre de 2026). El archivo se usa tal cual, en CSV, y el diccionario de datos en Excel (diccionario_datos_ai_company_adoption.xlsx) se armó a partir de él.
- Licencia del dataset: CC0: Public Domain, confirmada en los metadatos de Kaggle el 10 de noviembre de 2026. Cita: mohankrishnathalla, Global AI Adoption & Workforce Impact Dataset, Kaggle.
- Última actualización en el portal: Hace 7 meses
- Tamaño: 150.000 filas × 43 columnas (40,42 MB). Cada fila es una empresa en un trimestre (2023–2026): hay 10.000 empresas, con entre 10 y 16 filas cada una. Incluye variables de adopción de IA (tasa, etapa, herramienta, proyectos, presupuesto, capacitación), de impacto (productividad, automatización, ahorro de tiempo, empleos creados y desplazados, ingresos, costes) y de gobernanza (cumplimiento, gestión de riesgos, comité de ética, privacidad). No trae columna de ponderación.
- Pregunta de análisis: ¿Cómo se asocia la adopción de IA en las empresas con sus resultados (productividad, empleo, costes e ingresos), y cómo varía según región, sector y tamaño de empresa? Se desglosa en 10 preguntas SMART (ver 01_diccionario_ai.ipynb y 03_descriptiva_ai.ipynb).
- Problemas de calidad detectados: el archivo no tiene celdas vacías, filas duplicadas ni valores imposibles. Aun así: (1) es un panel no balanceado, y response_id llega a 160.000 con solo 150.000 filas (10.000 saltos que la fuente no explica); (2) 2026 trae los cuatro trimestres aunque el Q4 de 2026 no había terminado en octubre de 2026; (3) muchas variables acumulan filas exactamente en su piso o tope (por ejemplo, 15.887 filas con cost_reduction_percent en 0 y 6.106 con revenue_growth_percent en −5), y los datos están tan prolijos que podrían ser sintéticos o compilados, algo que la fuente no aclara; (4) las unidades de varias columnas se infieren del nombre y las escalas de los puntajes no están documentadas; (5) ai_adoption_stage es ai_adoption_rate cortada en tramos, y "none" no equivale a 0 % de adopción; (6) survey_source y data_collection_method se reparten casi en partes iguales entre sus 4 categorías y su procedencia no se puede verificar.
- Datos personales: el archivo no tiene datos personales; los identificadores de empresa (COMP-00001, etc.) son códigos, sin nombres, domicilios ni contactos.
- Estado de la validación (clase 9): Aprobado

## Entorno de ejecución verificado

| Modalidad | Versión de Python | Sistema operativo |
|---|---|---|
| venv local | Python 3.12.14 | macOS 26.6.2 |

## Cómo rehacer el entorno

```bash
# venv
python -m venv .venv
# activar: Linux/macOS -> source .venv/bin/activate   |  Windows -> .venv\Scripts\activate
pip install -r requirements.txt
python scripts/verificar_entorno.py

# conda
conda create -n aa2026 python=3.11
conda activate aa2026
pip install -r requirements.txt

# Docker
docker build -t unraf-aa .
docker run --rm -p 8888:8888 -v "$PWD":/trabajo unraf-aa
```

## Verificación del entorno

Salida registrada de `python scripts/verificar_entorno.py` en un entorno Windows del equipo (no corresponde al venv macOS usado para ejecutar los cuadernos en esta copia):


VERIFICACIÓN DEL ENTORNO — Aprendizaje Automático y Grandes Datos — UNRaf


1. Intérprete de Python
  OK    Python 3.12.0 sobre Windows AMD64

2. Dependencias
  OK    numpy 2.5.3
  OK    pandas 2.3.3
  OK    scipy 1.18.1
  OK    sklearn 1.8.0
  OK    matplotlib 3.11.2
  OK    seaborn 0.13.2
  OK    plotly 6.9.0
  OK    xgboost 3.4.1
  OK    mlxtend 0.25.0
  OK    statsmodels 0.14.6
  OK    ucimlrepo ?
  OK    pyarrow 25.0.1

3. Catálogo de datos de la cátedra
  OK    Catálogo importado: 13 conjuntos registrados
  OK    Directorio de caché: C:\AAG\Practica\datos\cache
  OK    Todos los conjuntos supervisados declaran su variable objetivo
  OK    Todos los conjuntos declaran licencia y citación
  OK    listar() devuelve 13 filas

4. Reproducibilidad de la aleatoriedad
  OK    Generador de NumPy con semilla fija: reproducible
  OK    Partición de scikit-learn con random_state fijo: reproducible

==============================================================================

Huella de `diamantes` en cada modalidad (deben ser idénticas): 

| Modalidad | Huella | Filas × columnas |
|---|---|---|
| venv | 1b8812569e371bba|53940 × 10 |

## Cuadernos del proyecto

1. `notebooks/01_diccionario_ai.ipynb`: perfil y diccionario del dataset.
2. `notebooks/02_limpieza_ai.ipynb`: validaciones y generación del Parquet limpio.
3. `notebooks/03_descriptiva_ai.ipynb`: preguntas y análisis exploratorio.
4. `notebooks/04_flujos_modelado_fuga.ipynb`: flujo de regresión y control de fuga por empresa.
5. `notebooks/05_regresion.ipynb`: línea base, Ridge, árbol y Random Forest; compara MSE, RMSE, MAE y R², y guarda el mejor pipeline para la demo.
6. `notebooks/06_tablero_interactivo.ipynb`: tablero descriptivo.
7. `notebooks/07_clasificacion.ipynb`: clasificadores (regresión logística, su versión ajustada, árbol, Naive Bayes, Random Forest y Dummy de referencia), validación cruzada agrupada, métricas por clase, matrices de confusión y análisis complementario de K-Means.

### Datos y ejecución

El CSV original y el Parquet limpio están versionados en `proyecto_equipo/datos/crudos/` y `proyecto_equipo/datos/derivados/`. Desde la raíz del repositorio, activar el entorno e instalar las dependencias con `pip install -r requirements.txt`. Abrir Jupyter con `python -m jupyter lab` y ejecutar primero `02_limpieza_ai.ipynb`, seguido de `05_regresion.ipynb` y `07_clasificacion.ipynb`. Los gráficos y tablas de `proyecto_equipo/salidas/` se versionan junto con `modelo_regresion_tp2.joblib` y `modelo_clasificacion_tp3.joblib` para la demo.

### Demostración en Streamlit

Los modelos exportados se generaron con scikit-learn 1.8.0. Para reutilizar los archivos joblib versionados, usá esa misma versión; si cambia la versión, regenerá los modelos ejecutando los cuadernos 02, 05 y 07 en la máquina de la demo.

Después de ejecutar los cuadernos 05 y 07, iniciar desde la raíz:

```bash
python -m streamlit run proyecto_equipo/src/app_modelos.py
```

La aplicación permite editar los predictores de una observación reservada del test y ejecutar la predicción o clasificación. Muestra la etiqueta real y el error/acierto únicamente si los campos todavía coinciden con esa fila no vista durante el entrenamiento; para entradas modificadas muestra la salida del modelo sin atribuirles una etiqueta real.

Las particiones separan empresas completas. En clasificación se usa `StratifiedGroupKFold` para aproximar las proporciones de clase sin mezclar filas de la misma empresa entre entrenamiento y prueba.
