# limitador de intentos de login, en memoria (si algún día crece a varias
# instancias esto hay que pasarlo a redis, pero por ahora resuelve)
import time
from collections import defaultdict
from fastapi import HTTPException, Request, status

INTENTOS_MAX = 5
VENTANA_SEGUNDOS = 60

_intentos = defaultdict(list)


def limitar_login(request: Request):
    ip = request.client.host if request.client else "desconocida"
    ahora = time.time()
    _intentos[ip] = [t for t in _intentos[ip] if ahora - t < VENTANA_SEGUNDOS]

    if len(_intentos[ip]) >= INTENTOS_MAX:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiados intentos. Espera un minuto e intenta de nuevo.",
        )
    _intentos[ip].append(ahora)
