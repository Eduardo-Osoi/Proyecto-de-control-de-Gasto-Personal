def crear_categoria(client, headers, nombre="Comida"):
    resp = client.post("/categorias/", json={"nombre": nombre, "presupuesto_mensual": 0}, headers=headers)
    return resp.json()


def crear_gasto(client, headers, categoria_id, descripcion="Tacos", monto=150):
    return client.post("/gastos/", json={
        "descripcion": descripcion, "monto": monto, "categoria_id": categoria_id,
    }, headers=headers)


def test_crear_gasto_en_categoria_propia(client, headers_usuario_a):
    categoria = crear_categoria(client, headers_usuario_a)
    resp = crear_gasto(client, headers_usuario_a, categoria["id"])
    assert resp.status_code == 201
    assert resp.json()["descripcion"] == "Tacos"


def test_idor_no_puede_crear_gasto_en_categoria_de_otro(client, headers_usuario_a, headers_usuario_b):
    categoria_de_ana = crear_categoria(client, headers_usuario_a)

    # Beto intenta colgar un gasto en categoría de Ana
    resp = crear_gasto(client, headers_usuario_b, categoria_de_ana["id"])
    assert resp.status_code == 404


def test_usuario_no_ve_gastos_de_otro(client, headers_usuario_a, headers_usuario_b):
    categoria = crear_categoria(client, headers_usuario_a)
    crear_gasto(client, headers_usuario_a, categoria["id"])

    resp = client.get("/gastos/", headers=headers_usuario_b)
    assert resp.status_code == 200
    assert resp.json() == []


def test_idor_no_puede_borrar_gasto_de_otro_usuario(client, headers_usuario_a, headers_usuario_b):
    categoria = crear_categoria(client, headers_usuario_a)
    gasto = crear_gasto(client, headers_usuario_a, categoria["id"]).json()

    resp = client.delete(f"/gastos/{gasto['id']}", headers=headers_usuario_b)
    assert resp.status_code == 404

    resp_lista = client.get("/gastos/", headers=headers_usuario_a)
    assert len(resp_lista.json()) == 1


def test_monto_negativo_es_rechazado(client, headers_usuario_a):
    categoria = crear_categoria(client, headers_usuario_a)
    resp = crear_gasto(client, headers_usuario_a, categoria["id"], monto=-100)
    assert resp.status_code == 422


def test_monto_cero_es_rechazado(client, headers_usuario_a):
    categoria = crear_categoria(client, headers_usuario_a)
    resp = crear_gasto(client, headers_usuario_a, categoria["id"], monto=0)
    assert resp.status_code == 422


def test_descripcion_vacia_es_rechazada(client, headers_usuario_a):
    categoria = crear_categoria(client, headers_usuario_a)
    resp = crear_gasto(client, headers_usuario_a, categoria["id"], descripcion="   ")
    assert resp.status_code == 422


def test_no_se_puede_crear_gasto_sin_autenticacion(client):
    resp = client.post("/gastos/", json={"descripcion": "Tacos", "monto": 100, "categoria_id": 1})
    assert resp.status_code == 401
