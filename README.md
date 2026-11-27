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

```bash
export LOCATION="eastus2"
export SUFFIX="$(date +%s)$RANDOM"
export RG="rg-demo-labs-${SUFFIX}"
export FOUNDRY_ACCOUNT="demo-foundry-${SUFFIX}"
export FOUNDRY_PROJECT="demo-project-${SUFFIX}"
export FOUNDRY_MODEL="gpt-4.1-mini"
export FOUNDRY_MODEL_VERSION="2025-04-14"

az group create --name "$RG" --location "$LOCATION"

az cognitiveservices account create \
  --name "$FOUNDRY_ACCOUNT" \
  --resource-group "$RG" \
  --location "$LOCATION" \
  --kind "AIServices" \
  --sku "S0" \
  --custom-domain "$FOUNDRY_ACCOUNT" \
  --assign-identity

az cognitiveservices account project create \
  --name "$FOUNDRY_ACCOUNT" \
  --resource-group "$RG" \
  --project-name "$FOUNDRY_PROJECT" \
  --location "$LOCATION"

az cognitiveservices account deployment create \
  --name "$FOUNDRY_ACCOUNT" \
  --resource-group "$RG" \
  --deployment-name "$FOUNDRY_MODEL" \
  --model-name "$FOUNDRY_MODEL" \
  --model-version "$FOUNDRY_MODEL_VERSION" \
  --model-format OpenAI \
  --sku-capacity 50 \
  --sku-name GlobalStandard
```
