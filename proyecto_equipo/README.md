# Bitácora del equipo — Aprendizaje Automático y Grandes Datos

> Este archivo se actualiza en cada entrega.

Repositorio: https://github.com/TaniaGorosito/aa-2026-entorno

## Integrantes y rol

| Integrante | Rol |
|---|---|
| (nombre) | (rol) |
| (nombre) | (rol) |
| (nombre) | (rol) |

## Conjunto de datos del equipo
- Nombre y origen: Encuesta Nacional de Consumos Culturales y Entorno Digital 2017 (ENCC 2017), publicada por la Secretaría de Cultura de la Nación en el portal de datos abiertos datos.gob.ar. Relevamiento a cargo de la consultora Ibarómetro, sobre población de 13 años y más.
- Enlace: https://datos.gob.ar/dataset/encuesta-nacional-de-consumos-culturales/resource/e7cd5858-b854-5bf5-a14c-71eb5017cadf (archivo original encc_2017.csv; en el proyecto se usa convertido a Excel, encc_2017.xlsx). Cuestionario aplicado: https://datos.gob.ar/dataset/encuesta-nacional-de-consumos-culturales/resource/6d3b9b6d-1596-558a-a459-42f85393830e
- Licencia: CC BY 4.0 (Creative Commons Atribución 4.0). Cita: Secretaría de Cultura de la Nación, Encuesta Nacional de Consumos Culturales 2017, datos.gob.ar.
- Última actualización en el portal: 30 de octubre de 2023.
- Tamaño: 2.802 encuestas × 450 columnas. Incluye una columna de ponderación (pondera_dem) y variables derivadas, como el nivel socioeconómico (NSEpuntaje, NSEcat1) y los totales de horas por actividad.
- Pregunta de análisis: ¿Qué características de las personas (edad, región, nivel de estudios, acceso a internet) se asocian con sus hábitos de consumo cultural?
- Problemas de calidad detectados: alrededor del 36 % de las celdas está vacío, en 439 de las 450 columnas, en buena parte por los saltos del cuestionario. Casi todas las columnas están guardadas como texto, incluso respuestas numéricas como gastos y cantidades, y hay que convertirlas. Hay 2 filas con sexo "ALQUILADA", un valor que corresponde a otra pregunta, y 2 con región y fecha vacías, que hay que revisar. Los códigos NS/NC (99, 999, 9999) conviven con valores reales.
- Datos personales: el archivo no tiene nombres, teléfonos ni domicilios.
- Estado de la validación (clase 9): aprobado

## Entorno de cada integrante

| Integrante | Modalidad (venv / conda / Docker / Colab) | Versión de Python | Sistema operativo |
|---|---|---|---|
| (nombre) | (completar) | (completar) | (completar) |

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

Salida de `python scripts/verificar_entorno.py` (pegar completa, una por modalidad):


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
| conda | | |
| Docker | | |

## Prueba del entorno limpio

- Quién la hizo y cuándo: (completar)
- Tiempo que tardó: (completar)
- Qué falló y cómo se resolvió: (completar)

## Desafíos

### Romper la reproducibilidad a propósito
(describir la celda, por qué cambia entre ejecuciones y por qué la semilla no alcanza)

### Qué pudo fallar con una hoja de cálculo publicada por una cuenta personal
1. (falla 1 y qué habría que hacer en su lugar)
2. (falla 2 y qué habría que hacer en su lugar)
3. (falla 3 y qué habría que hacer en su lugar)
