# GastoClaro

App para llevar mis gastos personales por categoría, con presupuesto mensual
por categoría y login. Backend en FastAPI, frontend en Vue 3 + TS.

## Correrlo local

Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # y le pones tu propia GASTOCLARO_SECRET_KEY
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Tests

Backend:
```bash
cd backend
pytest -v
```
25 tests. Los que más me importan son los de `test_categorias.py` y
`test_gastos.py` que checan que un usuario no pueda leer/borrar/crear cosas
de otro usuario aunque le adivine el ID (IDOR).

Frontend:
```bash
cd frontend
npm run test
```
10 tests con Vitest + Vue Test Utils: el store de auth, el login (éxito,
error, botón deshabilitado mientras carga) y el dashboard (skeleton loader,
total calculado, manejo de error de red).

## Monitoreo

Si defines `SENTRY_DSN` en el `.env` del backend, los errores 500 que antes
solo quedaban en el log del servidor también llegan a Sentry (plan free
alcanza de sobra para esto). Sin el DSN, la app funciona igual, solo que sin
reportar a Sentry.

## Seguridad

`INFORME_SEGURIDAD.md` tiene el detalle de qué revisé y por qué.

## Deploy

`DEPLOY.md` — Render/Railway para el backend, Vercel para el frontend.
