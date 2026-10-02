# Notas de seguridad — GastoClaro

Cosas que revisé al armar la app y por qué las dejé así:

**Contraseñas.** Van con bcrypt, no en texto plano ni con MD5/SHA1. Si algún
día se filtra la base de datos, no quedan expuestas tal cual.

**Permisos entre usuarios.** Esto era lo que más me preocupaba: que un
usuario pudiera ver o borrar gastos de otro solo cambiando el ID en la
petición (típico IDOR). Por eso cada query a `/gastos` y `/categorias`
siempre filtra por `owner_id`, tanto para leer como para escribir. Ya lo
cubrí con tests en `backend/tests/`, incluyendo el caso donde el usuario B
intenta tocar recursos del usuario A.

**Login.** Límite de 5 intentos por minuto por IP (está en `rate_limit.py`,
es en memoria, no algo industrial pero frena lo obvio). El mensaje de error
es el mismo si el correo no existe o si la contraseña está mal, para no
regalar pistas de qué correos están registrados.

**CORS.** Nada de `allow_origins=["*"]`. Sale de una variable de entorno
(`CORS_ORIGINS`) para poder poner el dominio real de Vercel sin tocar
código.

**El token en el frontend.** Va en `sessionStorage`, no en `localStorage`,
para que no sobreviva entre pestañas ni quede tirado ahí para siempre.

**Errores.** Si algo truena del lado del servidor, el cliente recibe un
mensaje genérico, no el traceback completo — eso da pistas de cómo está
armado el backend.

**Validaciones.** Montos negativos, textos vacíos, presupuestos negativos,
todo eso lo rechaza Pydantic antes de que llegue a la base de datos.

## Pendientes si esto llega a producción de verdad

- El rate limit vive en memoria del proceso; con más de una instancia hay
  que pasarlo a Redis.
- Configurar bien GASTOCLARO_SECRET_KEY como secreto real del hosting
  (Render la genera sola si usas el blueprint).
- Actualizar dependencias de vez en cuando (pip list --outdated, npm audit).
