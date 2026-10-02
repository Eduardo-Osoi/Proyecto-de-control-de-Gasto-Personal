from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


# ---- Auth ----
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str

    @field_validator("password")
    @classmethod
    def password_fuerte(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe incluir al menos un número")
        return v

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío")
        return v[:80]


class UserOut(BaseModel):
    id: int
    email: EmailStr
    nombre: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginData(BaseModel):
    email: EmailStr
    password: str


# ---- Categorías ----
class CategoriaCreate(BaseModel):
    nombre: str
    presupuesto_mensual: float = 0.0

    @field_validator("nombre")
    @classmethod
    def nombre_valido(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre de categoría no puede estar vacío")
        return v[:60]

    @field_validator("presupuesto_mensual")
    @classmethod
    def presupuesto_valido(cls, v):
        if v < 0:
            raise ValueError("El presupuesto no puede ser negativo")
        return v


class CategoriaOut(BaseModel):
    id: int
    nombre: str
    presupuesto_mensual: float

    class Config:
        from_attributes = True


# ---- Gastos ----
class GastoCreate(BaseModel):
    descripcion: str
    monto: float
    categoria_id: int

    @field_validator("descripcion")
    @classmethod
    def descripcion_valida(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("La descripción no puede estar vacía")
        return v[:200]

    @field_validator("monto")
    @classmethod
    def monto_valido(cls, v):
        if v <= 0:
            raise ValueError("El monto debe ser mayor que cero")
        if v > 10_000_000:
            raise ValueError("Monto fuera de rango")
        return round(v, 2)


class GastoOut(BaseModel):
    id: int
    descripcion: str
    monto: float
    fecha: datetime
    categoria_id: int

    class Config:
        from_attributes = True
