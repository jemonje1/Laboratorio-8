import pytest
"""NIVEL DE INTEGRACIÓN (API) — Playwright APIRequestContext.

Objeto de prueba: el contrato HTTP de /api/... (rutas, códigos de estado, JSON).
Fixtures disponibles (ver tests/conftest.py):
    api               -> cliente sin token
    api_autenticada   -> cliente con token válido
Los datos se reinician antes de cada prueba (3 productos iniciales, ids 1, 2 y 3).

Ejecuta solo este nivel:   pytest tests/api -v
"""


# ---------------------------------------------------------------- EJEMPLO
def test_listar_productos_devuelve_los_tres_iniciales(api_autenticada):
    respuesta = api_autenticada.get("/api/productos")
    assert respuesta.status == 200
    assert len(respuesta.json()) == 3


# ------------------------------------------------------------------ TODO
# Usa la tabla "Contrato de la API" de la guía como ORÁCULO.
# 1. Login: credenciales correctas (200 + token) e incorrectas (401).
# 2. Seguridad mínima: sin token -> 401.
# 3. CRUD: crear (201), consultar, actualizar y eliminar (204).
# 4. Casos negativos: datos inválidos (400) y recursos que NO existen.
#    Verifica el código de estado exacto que exige el contrato.
#
# Ejemplo de POST con JSON:
#     r = api_autenticada.post("/api/productos",
#                              data={"nombre": "Audífonos", "precio": 199.99, "stock": 3})
#     assert r.status == 201

def test_login_correcto(api):
    respuesta = api.post("/api/login", data={
        "usuario": "admin",
        "password": "Admin123"
    })

    assert respuesta.status == 200
    assert "token" in respuesta.json()
    assert isinstance(respuesta.json()["token"], str)
    assert len(respuesta.json()["token"]) > 0


def test_login_incorrecto(api):
    respuesta = api.post("/api/login", data={
        "usuario": "admin",
        "password": "Incorrecta123"
    })

    assert respuesta.status == 401

@pytest.mark.parametrize("usuario,password", [
    ("", "Admin123"),
    ("   ", "Admin123"),
    ("admin", "12345"),
    ("admin", "")
])
def test_login_formato_invalido(api, usuario, password):
    respuesta = api.post("/api/login", data={
        "usuario": usuario,
        "password": password
    })

    assert respuesta.status == 400
    assert "errores" in respuesta.json()
    assert isinstance(respuesta.json()["errores"], list)
    assert len(respuesta.json()["errores"]) > 0

def test_listar_productos_sin_token(api):
    respuesta = api.get("/api/productos")
    assert respuesta.status == 401
    
def test_crear_producto_correcto(api_autenticada):
    producto = {
        "nombre": "Audifonos",
        "precio": 199.99,
        "stock": 5
    }
    respuesta = api_autenticada.post(
        "/api/productos",
        data=producto
    )
    assert respuesta.status == 201
    producto_creado = respuesta.json()
    assert "id" in producto_creado
    assert producto_creado["nombre"] == "Audifonos"
    assert producto_creado["precio"] == 199.99
    assert producto_creado["stock"] == 5

@pytest.mark.parametrize("nombre,precio,stock", [
    ("AB", 100, 5),
    ("", 100, 5),
    ("Producto", 0, 5),
    ("Producto", -10, 5),
    ("Producto", 100001, 5),
    ("Producto", 100, -1),
    ("Producto", 100, 2.5)
])
def test_crear_producto_invalido(api_autenticada, nombre, precio, stock):
    respuesta = api_autenticada.post(
        "/api/productos",
        data={
            "nombre": nombre,
            "precio": precio,
            "stock": stock
        }
    )
    assert respuesta.status == 400
    assert "errores" in respuesta.json()
    assert isinstance(respuesta.json()["errores"], list)
    assert len(respuesta.json()["errores"]) > 0


def test_consultar_producto_existente(api_autenticada):
    respuesta = api_autenticada.get("/api/productos/1")

    assert respuesta.status == 200

    producto = respuesta.json()

    assert producto["id"] == 1
    assert producto["nombre"] == "Teclado"
    assert producto["precio"] == 250.00
    assert producto["stock"] == 10

def test_consultar_producto_inexistente(api_autenticada):
    respuesta = api_autenticada.get("/api/productos/999")

    assert respuesta.status == 404

def test_actualizar_producto_correcto(api_autenticada):
    datos = {
        "nombre": "Teclado Gamer",
        "precio": 350.00,
        "stock": 8
    }

    respuesta = api_autenticada.put(
        "/api/productos/1",
        data=datos
    )

    assert respuesta.status == 200

    producto = respuesta.json()

    assert producto["id"] == 1
    assert producto["nombre"] == "Teclado Gamer"
    assert producto["precio"] == 350.00
    assert producto["stock"] == 8

    consulta = api_autenticada.get("/api/productos/1")

    assert consulta.status == 200
    assert consulta.json()["nombre"] == "Teclado Gamer"
    assert consulta.json()["precio"] == 350.00
    assert consulta.json()["stock"] == 8

@pytest.mark.parametrize("nombre,precio,stock", [
    ("AB", 100, 5),
    ("Producto", 0, 5),
    ("Producto", 100001, 5),
    ("Producto", 100, -1),
    ("Producto", 100, 2.5)
])
def test_actualizar_producto_invalido(api_autenticada, nombre, precio, stock):
    respuesta = api_autenticada.put(
        "/api/productos/1",
        data={
            "nombre": nombre,
            "precio": precio,
            "stock": stock
        }
    )

    assert respuesta.status == 400
    assert "errores" in respuesta.json()
    assert isinstance(respuesta.json()["errores"], list)
    assert len(respuesta.json()["errores"]) > 0

def test_actualizar_producto_inexistente(api_autenticada):
    respuesta = api_autenticada.put(
        "/api/productos/999",
        data={
            "nombre": "Teclado Gamer",
            "precio": 350.00,
            "stock": 8
        }
    )

    assert respuesta.status == 404

def test_eliminar_producto_correcto(api_autenticada):
    respuesta = api_autenticada.delete("/api/productos/2")

    assert respuesta.status == 204

    consulta = api_autenticada.get("/api/productos")

    assert consulta.status == 200

    productos = consulta.json()

    assert len(productos) == 2

    ids = [producto["id"] for producto in productos]

    assert 2 not in ids
    assert 1 in ids
    assert 3 in ids

def test_eliminar_producto_inexistente(api_autenticada):
    respuesta = api_autenticada.delete("/api/productos/999")

    assert respuesta.status == 404

@pytest.mark.parametrize("metodo,ruta", [
    ("post", "/api/productos"),
    ("put", "/api/productos/1"),
    ("delete", "/api/productos/1")
])
def test_operaciones_sin_token(api, metodo, ruta):
    datos = {
        "nombre": "Producto Nuevo",
        "precio": 150,
        "stock": 5
    }

    respuesta = getattr(api, metodo)(
        ruta,
        data=datos
    )

    assert respuesta.status == 401

@pytest.mark.parametrize("nombre,precio,stock", [
    ("ABC", 100, 5),
    ("A" * 50, 100, 5),
    ("Producto", 100000, 5),
    ("Producto", 100, 0)
])
def test_crear_producto_valores_limite(api_autenticada, nombre, precio, stock):
    respuesta = api_autenticada.post(
        "/api/productos",
        data={
            "nombre": nombre,
            "precio": precio,
            "stock": stock
        }
    )

    assert respuesta.status == 201

    producto = respuesta.json()

    assert "id" in producto
    assert producto["nombre"] == nombre
    assert producto["precio"] == precio
    assert producto["stock"] == stock

def test_token_invalido(api):
    respuesta = api.get(
        "/api/productos",
        headers={
            "Authorization": "Bearer token_inventado"
        }
    )

    assert respuesta.status == 401