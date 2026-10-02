from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db
from ..rate_limit import limitar_login

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registro", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def registrar(datos: schemas.UserCreate, db: Session = Depends(get_db)):
    existe = db.query(models.User).filter(models.User.email == datos.email.lower()).first()
    if existe:
        raise HTTPException(status_code=400, detail="No se pudo crear la cuenta con esos datos")

    nuevo = models.User(
        email=datos.email.lower(),
        hashed_password=auth.hash_password(datos.password),
        nombre=datos.nombre,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.post("/login", response_model=schemas.Token)
def login(request: Request, datos: schemas.LoginData, db: Session = Depends(get_db)):
    limitar_login(request)

    user = db.query(models.User).filter(models.User.email == datos.email.lower()).first()

    # mismo mensaje exista o no el usuario, para no dar pistas
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Correo o contraseña incorrectos",
    )

    if not user or not auth.verify_password(datos.password, user.hashed_password):
        raise credenciales_invalidas

    if not user.is_active:
        raise credenciales_invalidas

    token = auth.crear_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserOut)
def perfil(usuario: models.User = Depends(auth.get_current_user)):
    return usuario
