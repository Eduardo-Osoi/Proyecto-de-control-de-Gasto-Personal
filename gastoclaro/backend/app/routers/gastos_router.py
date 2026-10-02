from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/gastos", tags=["gastos"])


@router.get("/", response_model=List[schemas.GastoOut])
def listar(db: Session = Depends(get_db), usuario: models.User = Depends(auth.get_current_user)):
    return db.query(models.Gasto).filter(models.Gasto.owner_id == usuario.id).order_by(models.Gasto.fecha.desc()).all()


@router.post("/", response_model=schemas.GastoOut, status_code=201)
def crear(datos: schemas.GastoCreate, db: Session = Depends(get_db),
          usuario: models.User = Depends(auth.get_current_user)):
    # checo que la categoría sea del usuario, si no cualquiera cuelga gastos ajenos
    categoria = db.query(models.Categoria).filter(
        models.Categoria.id == datos.categoria_id,
        models.Categoria.owner_id == usuario.id,
    ).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    nuevo = models.Gasto(**datos.model_dump(), owner_id=usuario.id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.delete("/{gasto_id}", status_code=204)
def eliminar(gasto_id: int, db: Session = Depends(get_db),
             usuario: models.User = Depends(auth.get_current_user)):
    gasto = db.query(models.Gasto).filter(
        models.Gasto.id == gasto_id,
        models.Gasto.owner_id == usuario.id,
    ).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    db.delete(gasto)
    db.commit()
