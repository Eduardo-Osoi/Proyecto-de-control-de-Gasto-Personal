# Despliegue — GastoClaro

## Backend en Render (recomendado, incluye `render.yaml`)

1. Sube el proyecto a un repo de GitHub.
2. En [render.com](https://render.com) → **New → Blueprint** → selecciona el
   repo. Render lee `backend/render.yaml` y crea el servicio web + una base
   de datos Postgres gratis automáticamente.
3. Revisa las variables de entorno que quedaron configuradas:
   - `GASTOCLARO_SECRET_KEY` — Render la genera sola (aleatoria), nunca va
     hardcodeada en el código.
   - `DATABASE_URL` — conectada automáticamente a la base de datos creada.
   - `CORS_ORIGINS` — **edítala** después de desplegar el frontend, con la
     URL real que te dé Vercel (ej. `https://gastoclaro.vercel.app`). Sin
     comodines, solo ese dominio.
4. Copia la URL pública que te da Render (ej.
   `https://gastoclaro-api.onrender.com`) — la necesitas para el frontend.

### Alternativa: Railway
Si prefieres Railway en vez de Render, usa `backend/railway.json`:
1. `railway init` dentro de `backend/` (o conecta el repo desde el dashboard).
2. Agrega un plugin de PostgreSQL desde el dashboard de Railway.
3. En **Variables** define a mano `GASTOCLARO_SECRET_KEY` (genera una cadena
   aleatoria larga, por ejemplo con `openssl rand -hex 32`), `ENV=production`
   y `CORS_ORIGINS` con la URL de Vercel.
4. Railway detecta `railway.json` y usa ese `startCommand`.

## Frontend en Vercel

1. En [vercel.com](https://vercel.com) → **Add New → Project** → importa el
   repo y selecciona la carpeta `frontend` como root del proyecto.
2. Vercel detecta Vite automáticamente; `vercel.json` ya incluye el rewrite
   para que las rutas de `vue-router` (modo history) no den 404 al recargar.
3. En **Environment Variables** agrega:
   - `VITE_API_URL` = la URL del backend que copiaste de Render/Railway
     (ej. `https://gastoclaro-api.onrender.com`).
4. Deploy. Copia la URL final de Vercel.
5. Vuelve a Render/Railway y actualiza `CORS_ORIGINS` con esa URL exacta
   (con `https://`, sin `/` al final). Redeploy el backend para que tome el
   cambio.

## Checklist antes de dar por bueno el deploy

- [ ] `GASTOCLARO_SECRET_KEY` como variable de entorno del hosting, no en el repo.
- [ ] `CORS_ORIGINS` apunta solo al dominio real de Vercel, no a `*`.
- [ ] El backend responde por HTTPS (Render/Railway lo dan por default).
- [ ] `.env` no está commiteado (ya está en `.gitignore`).
- [ ] Corriste `pytest` (backend) y `npm run test` (frontend) antes de cada deploy importante.
- [ ] (Opcional) `SENTRY_DSN` configurado en el backend si quieres ver los errores de producción sin entrar a los logs.
