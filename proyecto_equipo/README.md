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

- Nombre y origen: (completar)
- Licencia: (completar)
- Pregunta de análisis: (completar)
- Estado de la validación (clase 9): (pendiente / aprobado)

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

```
(pegar acá la salida)
```

Huella de `diamantes` en cada modalidad (deben ser idénticas):

| Modalidad | Huella | Filas × columnas |
|---|---|---|
| venv | | |
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
