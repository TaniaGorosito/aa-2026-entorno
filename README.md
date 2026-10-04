# aa-2026-entorno

Entorno de trabajo reproducible del equipo para *Aprendizaje Automático y Grandes Datos* (2026).

La bitácora del equipo (integrantes, roles, entorno de cada uno, verificación y desafíos) está en [`proyecto_equipo/README.md`](proyecto_equipo/README.md).

## Rehacer el entorno

```bash
python -m venv .venv
# activar: Linux/macOS -> source .venv/bin/activate   |  Windows -> .venv\Scripts\activate
pip install -r requirements.txt
python scripts/verificar_entorno.py
```

La última línea tiene que decir `RESULTADO: entorno correcto`. Con Docker:

```bash
docker build -t unraf-aa .
docker run --rm -p 8888:8888 -v "$PWD":/trabajo unraf-aa
```

## Estructura

```
datos/                 catálogo de datos de la cátedra y manifiesto de huellas
scripts/               verificador del entorno
proyecto_equipo/       datos/crudos, datos/derivados, notebooks, src, salidas
requirements.txt       dependencias con versiones acotadas
Dockerfile             entorno en contenedor
LAB01_entorno_reproducible.ipynb
```

Los datos crudos y la caché no se versionan: se rehacen con el catálogo.
