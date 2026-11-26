# Prueba de Function Calling: listar doctores

## Requisitos
- Python 3.10 o superior
- No requiere instalar paquetes externos: `sqlite3` forma parte de Python.

## Archivos
- `database.py`: crea la tabla e inserta 10 doctores de prueba.
- `tools.py`: implementa `listar_doctores()`.
- `consultorio.db`: base SQLite creada al ejecutar el script.

## Ejecutar

Desde esta carpeta:

```bash
python database.py
python app.py
```

La primera ejecución crea `consultorio.db` e inserta los 10 registros.
Las ejecuciones posteriores no duplican los registros porque se usa
`INSERT OR IGNORE` con IDs fijos.

## Resultado esperado

`listar_doctores()` devuelve un diccionario con:
- `total`: cantidad de doctores.
- `doctores`: lista de doctores con ID, nombre, especialidad y horario.

## Ruta de base de datos

Localmente usa `consultorio.db` junto a `database.py`.

Para Azure App Service puedes definir:

```text
DB_PATH=/home/data/consultorio.db
```