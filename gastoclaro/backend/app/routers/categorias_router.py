from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("/", response_model=List[schemas.CategoriaOut])
def listar(db: Session = Depends(get_db), usuario: models.User = Depends(auth.get_current_user)):
    return db.query(models.Categoria).filter(models.Categoria.owner_id == usuario.id).all()


@router.post("/", response_model=schemas.CategoriaOut, status_code=201)
def crear(datos: schemas.CategoriaCreate, db: Session = Depends(get_db),
          usuario: models.User = Depends(auth.get_current_user)):
    nueva = models.Categoria(**datos.model_dump(), owner_id=usuario.id)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def _obtener_categoria_del_usuario(categoria_id: int, db: Session, usuario: models.User) -> models.Categoria:
    # el filtro por owner_id es lo que evita que alguien borre categorías ajenas
    categoria = db.query(models.Categoria).filter(
        models.Categoria.id == categoria_id,
        models.Categoria.owner_id == usuario.id,
    ).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@router.delete("/{categoria_id}", status_code=204)
def eliminar(categoria_id: int, db: Session = Depends(get_db),
             usuario: models.User = Depends(auth.get_current_user)):
    categoria = _obtener_categoria_del_usuario(categoria_id, db, usuario)
    db.delete(categoria)
    db.commit()
