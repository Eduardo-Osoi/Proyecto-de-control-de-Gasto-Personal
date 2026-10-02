def test_registro_exitoso(client):
    resp = client.post("/auth/registro", json={
        "email": "nueva@correo.com", "password": "clave1234", "nombre": "Nueva",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "nueva@correo.com"
    assert "hashed_password" not in data
    assert "password" not in data


def test_no_permite_registrar_email_duplicado(client):
    datos = {"email": "dup@correo.com", "password": "clave1234", "nombre": "Dup"}
    client.post("/auth/registro", json=datos)
    resp = client.post("/auth/registro", json=datos)
    assert resp.status_code == 400


def test_password_corto_es_rechazado(client):
    resp = client.post("/auth/registro", json={
        "email": "corta@correo.com", "password": "123", "nombre": "Corta",
    })
    assert resp.status_code == 422


def test_password_sin_numero_es_rechazado(client):
    resp = client.post("/auth/registro", json={
        "email": "sinnum@correo.com", "password": "abcdefgh", "nombre": "SinNum",
    })
    assert resp.status_code == 422


def test_login_correcto_devuelve_token(client):
    client.post("/auth/registro", json={
        "email": "login@correo.com", "password": "clave1234", "nombre": "Login",
    })
    resp = client.post("/auth/login", json={"email": "login@correo.com", "password": "clave1234"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_password_incorrecta(client):
    client.post("/auth/registro", json={
        "email": "mal@correo.com", "password": "clave1234", "nombre": "Mal",
    })
    resp = client.post("/auth/login", json={"email": "mal@correo.com", "password": "otraclave1"})
    assert resp.status_code == 401


def test_login_usuario_inexistente_mismo_mensaje_que_password_mala(client):
    # mismo mensaje en los dos casos, si no se puede adivinar qué correos existen
    resp_inexistente = client.post("/auth/login", json={"email": "fantasma@correo.com", "password": "loquesea1"})
    client.post("/auth/registro", json={"email": "real@correo.com", "password": "clave1234", "nombre": "Real"})
    resp_password_mala = client.post("/auth/login", json={"email": "real@correo.com", "password": "loquesea1"})

    assert resp_inexistente.status_code == 401
    assert resp_password_mala.status_code == 401
    assert resp_inexistente.json()["detail"] == resp_password_mala.json()["detail"]


def test_rate_limit_bloquea_tras_varios_intentos(client):
    client.post("/auth/registro", json={"email": "limite@correo.com", "password": "clave1234", "nombre": "Limite"})
    for _ in range(5):
        client.post("/auth/login", json={"email": "limite@correo.com", "password": "mala"})
    resp = client.post("/auth/login", json={"email": "limite@correo.com", "password": "mala"})
    assert resp.status_code == 429


def test_endpoint_protegido_sin_token_da_401(client):
    resp = client.get("/auth/me")
    assert resp.status_code == 401


def test_endpoint_protegido_con_token_invalido_da_401(client):
    resp = client.get("/auth/me", headers={"Authorization": "Bearer token-invalido"})
    assert resp.status_code == 401


def test_me_devuelve_datos_del_usuario_logueado(client, headers_usuario_a):
    resp = client.get("/auth/me", headers=headers_usuario_a)
    assert resp.status_code == 200
    assert resp.json()["email"] == "ana@correo.com"
