# Flask Project Base

## Run server

```
python -m venv .venv
source .venv/bin/activate
./scripts/run
```

Then the API should be available at http://localhost:5000/


## Deploy
`scp -r app.py db.py utility.py alembic.ini alembic/ scripts/ models/ resources/ services/  DESTINATION`

Then copy environment if new installation and edit proper values

## Generate Http client

1. Install openapi-generator `community/openapi-generator`
2. Start server
3. `openapi-generator generate -i http://localhost:5000/apispec_1.json -g typescript-rxjs -o client/generated-api --skip-validate-spec`


## Create a new database revision

1. Install python-alembic
2. ```alembic revision -m "Name of revision"```
