"""NIVEL DE SISTEMA (E2E) — Playwright en un navegador real.

Objeto de prueba: los flujos del usuario en la interfaz web.
La fixture `page` la provee pytest-playwright; las rutas relativas usan base_url.
Los datos se reinician antes de cada prueba.

Ejecuta solo este nivel:          pytest tests/e2e -v
Para VER el navegador:            pytest tests/e2e --headed --slowmo 500
Para grabar interacciones:        playwright codegen http://127.0.0.1:5000
                                  (con la app corriendo: python run.py)
"""
from playwright.sync_api import Page, expect


# 1. Login exitoso: debe mostrarse "Bienvenido, admin".
#    (Ojo: aparece con retraso. NO uses time.sleep: expect() espera solo.)
def test_pagina_login_exitoso(page: Page) -> None:
    page.goto("http://127.0.0.1:5000/login")
    page.get_by_role("textbox", name="Usuario").click()
    page.get_by_role("textbox", name="Usuario").fill("admin")
    page.get_by_role("textbox", name="Usuario").press("Tab")
    page.get_by_role("textbox", name="Contraseña").fill("Admin123")
    page.get_by_role("textbox", name="Contraseña").press("Enter")

# 2. Login fallido: se muestra un mensaje de error.
def test_pagina_login_fallido(page: Page) -> None:
    page.goto("http://127.0.0.1:5000/login")
    page.get_by_role("textbox", name="Usuario").click()
    page.get_by_role("textbox", name="Usuario").fill("admin")
    page.get_by_role("textbox", name="Usuario").press("Tab")
    page.get_by_role("textbox", name="Contraseña").fill("123")
    page.get_by_role("button", name="Ingresar").click()

# 3. Crear un producto desde el formulario y verificar que aparece en la tabla.
def test_pagina_creacion_producto(page: Page) -> None:
    test_pagina_login_exitoso(page)

    page.get_by_role("link", name="Nuevo producto").click()
    page.get_by_role("textbox", name="Nombre").click()
    page.get_by_role("textbox", name="Nombre").fill("Consola de videojuegos")
    page.get_by_role("textbox", name="Nombre").press("Tab")
    page.get_by_role("textbox", name="Precio").fill("500")
    page.get_by_role("textbox", name="Precio").press("Tab")
    page.get_by_role("textbox", name="Stock").fill("10")
    page.get_by_role("button", name="Guardar").click()


# 4. Eliminar un producto desde la tabla.
#    Verifica el resultado esperado Y que no haya efectos colaterales
#    sobre los demás registros.

def test_pagina_eliminacion_producto(page: Page) -> None:
    test_pagina_login_exitoso(page)
    page.get_by_role("row", name="3 Monitor 1450.00 5 Editar").get_by_role("button").click()

# Localizadores recomendados (por rol/etiqueta, como los ve el usuario):
#     page.get_by_label("Usuario").fill("admin")
#     page.get_by_role("button", name="Ingresar").click()
#     fila = page.get_by_role("row").filter(has_text="Teclado")
#     fila.get_by_role("button", name="Eliminar").click()