def crear_categoria(client, headers, nombre="Comida", presupuesto=1000):
    resp = client.post("/categorias/", json={"nombre": nombre, "presupuesto_mensual": presupuesto}, headers=headers)
    return resp.json()


def test_crear_y_listar_categoria_propia(client, headers_usuario_a):
    crear_categoria(client, headers_usuario_a, "Comida")
    resp = client.get("/categorias/", headers=headers_usuario_a)
    assert resp.status_code == 200
    nombres = [c["nombre"] for c in resp.json()]
    assert "Comida" in nombres


def test_usuario_no_ve_categorias_de_otro(client, headers_usuario_a, headers_usuario_b):
    crear_categoria(client, headers_usuario_a, "Comida de Ana")
    resp = client.get("/categorias/", headers=headers_usuario_b)
    assert resp.status_code == 200
    assert resp.json() == []


def test_idor_no_puede_borrar_categoria_de_otro_usuario(client, headers_usuario_a, headers_usuario_b):
    categoria = crear_categoria(client, headers_usuario_a, "Categoria de Ana")

    # Beto intenta borrar la categoría de Ana usando su ID
    resp = client.delete(f"/categorias/{categoria['id']}", headers=headers_usuario_b)
    assert resp.status_code == 404

    # sigue existiendo
    resp_ana = client.get("/categorias/", headers=headers_usuario_a)
    assert len(resp_ana.json()) == 1


def test_categoria_sin_nombre_es_rechazada(client, headers_usuario_a):
    resp = client.post("/categorias/", json={"nombre": "   ", "presupuesto_mensual": 0}, headers=headers_usuario_a)
    assert resp.status_code == 422


def test_categoria_presupuesto_negativo_es_rechazado(client, headers_usuario_a):
    resp = client.post("/categorias/", json={"nombre": "X", "presupuesto_mensual": -50}, headers=headers_usuario_a)
    assert resp.status_code == 422


def test_no_se_puede_crear_categoria_sin_autenticacion(client):
    resp = client.post("/categorias/", json={"nombre": "Comida", "presupuesto_mensual": 0})
    assert resp.status_code == 401
