"""NIVEL UNITARIO (componente) — pytest puro.

Objeto de prueba: app/validaciones.py (funciones puras, sin servidor ni navegador).
Técnicas sugeridas: partición de equivalencia y análisis de valores límite.

Ejecuta solo este nivel:   pytest tests/unitarias -v
"""
import pytest

from app.validaciones import validar_credenciales, validar_producto


# ---------------------------------------------------------------- EJEMPLO
def test_credenciales_con_formato_valido_no_tienen_errores():
    assert validar_credenciales("admin", "Admin123") == []

# PRUEBA 1: Usuario vacío o con espacios
@pytest.mark.parametrize("usuario", [
    "",
    "   "
])
def test_usuario_invalido(usuario):
    errores = validar_credenciales(usuario, "Admin123")

    assert isinstance(errores, list)
    assert len(errores) > 0

# PRUEBA 2: Longitud mínima de contraseña
@pytest.mark.parametrize("password, valido", [
    ("12345", False),
    ("123456", True)
])
def test_limite_password(password, valido):
    errores = validar_credenciales("admin", password)

    assert (errores == []) == valido

# PRUEBA 3: Producto con datos válidos
def test_producto_valido():
    errores = validar_producto("Teclado", 250.00, 10)

    assert errores == []

# PRUEBA 4: Valores límite del nombre del producto
@pytest.mark.parametrize("nombre, valido", [
    ("AB", False),
    ("ABC", True),
    ("A" * 50, True),
    ("A" * 51, False)
])
def test_limites_nombre_producto(nombre, valido):
    errores = validar_producto(nombre, 100.0, 5)

    assert (errores == []) == valido

 # PRUEBA 5: Espacios al inicio y final del nombre
@pytest.mark.parametrize("nombre, valido", [
    ("  ABC  ", True),
    ("  AB  ", False),
    ("  Teclado  ", True)
])
def test_nombre_con_espacios(nombre, valido):
    errores = validar_producto(nombre, 100.0, 5)

    assert (errores == []) == valido  

# PRUEBA 6: Valores límite del precio
@pytest.mark.parametrize("precio, valido", [
    (-1, False),
    (0, False),
    (0.01, True),
    (100000, True),
    (100000.01, False)
])
def test_limites_precio(precio, valido):
    errores = validar_producto("Teclado", precio, 5)

    assert (errores == []) == valido 

# PRUEBA 7: Valores límite del stock
@pytest.mark.parametrize("stock, valido", [
    (-1, False),
    (0, True),
    (1, True),
    (1.5, False)
])
def test_limites_stock(stock, valido):
    errores = validar_producto("Teclado", 100.0, stock)

    assert (errores == []) == valido
# ------------------------------------------------------------------ TODO
# 1. validar_credenciales: usuario vacío, contraseña en el límite (5 y 6 caracteres).
# 2. validar_producto: un producto válido no tiene errores.
# 3. validar_producto: aplica VALORES LÍMITE a cada regla de la especificación
#    (nombre, precio y stock). Pregúntate: ¿cuál es el último valor inválido
#    y el primer valor válido de cada regla?
#
# Pista: @pytest.mark.parametrize evita repetir la misma prueba con datos distintos.
#
# @pytest.mark.parametrize("stock, valido", [(-1, False), (0, True)])
# def test_limites_de_stock(stock, valido):
#     errores = validar_producto("Teclado", 100.0, stock)
#     assert (errores == []) == valido
