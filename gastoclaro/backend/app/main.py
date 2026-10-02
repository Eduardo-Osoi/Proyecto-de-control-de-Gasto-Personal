import os
import logging
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .database import Base, engine
from .routers import auth_router, categorias_router, gastos_router

Base.metadata.create_all(bind=engine)

logger = logging.getLogger("gastoclaro")

SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=os.getenv("ENV", "dev"),
        traces_sample_rate=0.1,
        send_default_pii=False,
    )

app = FastAPI(title="GastoClaro API", version="1.0.0")

# nada de "*" aquí, va por env var según el ambiente
origenes_permitidos = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.exception_handler(Exception)
async def error_handler(request: Request, exc: Exception):
    # el traceback se queda en el log y en Sentry (si está configurado),
    # al cliente no le mando detalles internos
    logger.exception("Error no manejado en %s", request.url.path)
    if SENTRY_DSN:
        sentry_sdk.capture_exception(exc)
    return JSONResponse(status_code=500, content={"detail": "Ocurrió un error interno"})


app.include_router(auth_router.router)
app.include_router(categorias_router.router)
app.include_router(gastos_router.router)


@app.get("/")
def salud():
    return {"status": "ok"}
