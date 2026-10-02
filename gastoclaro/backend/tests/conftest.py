import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ["DATABASE_URL"] = "sqlite:///./test_gastoclaro.db"
os.environ["GASTOCLARO_SECRET_KEY"] = "clave-de-pruebas-no-usar-en-produccion"
os.environ["CORS_ORIGINS"] = "http://localhost:5173"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import rate_limit

TEST_DB = "sqlite:///./test_gastoclaro.db"
engine = create_engine(TEST_DB, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def limpiar_db():
    Base.metadata.create_all(bind=engine)
    rate_limit._intentos.clear()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def registrar_y_loguear(client, email="ana@correo.com", password="clave1234", nombre="Ana"):
    client.post("/auth/registro", json={"email": email, "password": password, "nombre": nombre})
    resp = client.post("/auth/login", json={"email": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def headers_usuario_a(client):
    return registrar_y_loguear(client, email="ana@correo.com", nombre="Ana")


@pytest.fixture
def headers_usuario_b(client):
    return registrar_y_loguear(client, email="beto@correo.com", nombre="Beto")
