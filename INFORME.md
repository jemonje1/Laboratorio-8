# Informe · Laboratorio 8 · Pruebas automatizadas

**Equipo:**
- Equipo de atras

**Integrantes:**
- Sophia Corea
- Luis Lopez
- Javier Monje

## 1. Defectos encontrados

Durante la ejecución de las pruebas automatizadas se identificaron tres defectos relacionados con el incumplimiento de los requisitos del negocio, el comportamiento esperado de los endpoints y las operaciones realizadas desde la interfaz web.

**DEF-01 — Validación incorrecta del precio igual a cero:** El sistema permite ingresar productos con precio igual a cero, aunque la especificación establece que el precio debe ser estrictamente mayor que cero. Este defecto fue detectado mediante pruebas unitarias y de integración API.

**DEF-02 — Código HTTP incorrecto al consultar un producto inexistente:** Al solicitar mediante la API un producto inexistente, el sistema devuelve HTTP 200 (OK) en lugar de HTTP 404 (Not Found), incumpliendo el contrato establecido en la especificación.

**DEF-03 — Eliminación del producto equivocado:** Al seleccionar la opción de eliminar el producto Monitor desde la interfaz web, el sistema envía la solicitud de eliminación correspondiente al producto Teclado, mientras que Monitor permanece en la tabla.

| ID | Nivel que lo detectó | Prueba (archivo::función) | Pasos para reproducir | Resultado esperado (según la especificación) | Resultado obtenido |
|---|---|---|---|---|---|
| DEF-01 | Unitarias y API | `tests/unitarias/test_unitarias.py::test_limites_precio`, `tests/api/test_api.py::test_crear_producto_invalido` y `test_actualizar_producto_invalido` | Ejecutar `validar_producto("Teclado", 0, 5)`. En API, autenticarse y enviar POST a `/api/productos` con nombre válido, precio 0 y stock 5. Repetir con PUT sobre un producto existente. | La validación debe devolver una lista de errores. Las operaciones API deben responder HTTP 400, porque el precio debe ser estrictamente mayor que cero. | La función devuelve `[]`, aceptando el precio cero. POST responde HTTP 201 y PUT responde HTTP 200, permitiendo un precio inválido. |
| DEF-02 | API | `tests/api/test_api.py::test_consultar_producto_inexistente` | Autenticarse y enviar una solicitud GET a `/api/productos/999`. | HTTP 404, indicando que el producto solicitado no existe. | HTTP 200 con un objeto JSON vacío. |
| DEF-03 | E2E | `tests/e2e/test_e2e.py::test_pagina_eliminacion_producto` | Iniciar sesión con el usuario admin, acceder a la lista de productos y presionar el botón Eliminar en la fila del producto Monitor (ID 3). Verificar posteriormente los productos que permanecen en la tabla. | Debe eliminarse únicamente Monitor (ID 3), mostrar el mensaje "Producto eliminado" y conservar Teclado y Mouse sin modificaciones. | La interfaz envía `POST /productos/1/eliminar`, correspondiente a Teclado (ID 1), aunque se seleccionó Monitor. El producto Monitor permanece en la tabla y la prueba falla al verificar su eliminación. |

**Detección adicional de DEF-01 mediante pruebas unitarias:**

El defecto DEF-01 también fue identificado en el nivel unitario mediante la prueba `tests/unitarias/test_unitarias.py::test_limites_precio`.

Para reproducirlo, se ejecuta la función `validar_producto("Teclado", 0, 5)`, utilizando un nombre válido, precio igual a cero y stock válido.

Según la especificación, el precio debe ser estrictamente mayor que cero, por lo que se espera que la función devuelva una lista con al menos un mensaje de error. Sin embargo, la función devuelve una lista vacía `[]`, aceptando incorrectamente el precio cero.

La prueba correspondiente falló, confirmando que el defecto puede detectarse directamente en la función de validación, sin necesidad de ejecutar el servidor ni realizar solicitudes HTTP. Este hallazgo corresponde al mismo DEF-01 identificado mediante API, por lo que no se contabiliza como un defecto nuevo.

**Detección de DEF-03 mediante pruebas E2E:**

Durante la automatización del flujo de eliminación, Playwright seleccionó el botón correspondiente a la fila del producto Monitor. Sin embargo, los registros del servidor mostraron que se realizó una solicitud POST a `/productos/1/eliminar`.

La prueba verificó el mensaje "Producto eliminado" y posteriormente comprobó que Monitor ya no apareciera en la tabla. Esta última verificación falló porque el producto continuaba visible.

El defecto demuestra que una operación puede mostrar un mensaje de éxito aunque el resultado no corresponda con la acción solicitada por el usuario. También evidencia la importancia de comprobar los efectos de las operaciones y no solamente la aparición de mensajes de confirmación.

Los defectos se conservaron en el código original de la aplicación, manteniendo las pruebas correspondientes en estado fallido, según las instrucciones del laboratorio.

## 2. Tabla comparativa de niveles

| Criterio | Unitarias | API | E2E |
|---|---|---|---|
| Número de pruebas | 22 | 35 | 4 |
| Tiempo total de ejecución (s) | 0.23 | 2.54 | 10.66 |
| Tiempo promedio por prueba (s) | 0.0105 | 0.073 | 2.665 |
| Defectos detectados (IDs) | DEF-01 | DEF-01, DEF-02 | DEF-03 |
| ¿Qué cambio en la app rompería estas pruebas sin que haya un defecto? | Un cambio legítimo en las reglas de validación, acompañado de una actualización de la especificación, podría provocar fallos si las pruebas no se actualizan para reflejar los nuevos requisitos. | Cambios válidos en las rutas, nombres de campos JSON o estructura de respuestas que también se reflejen en una especificación actualizada. | Cambios legítimos en la estructura HTML, etiquetas, nombres accesibles de los controles o localizadores utilizados por Playwright podrían romper las pruebas aunque el comportamiento funcional continúe siendo correcto. |
| Costo de mantenimiento (Alto / Medio / Bajo) y por qué | Bajo, porque las pruebas evalúan funciones puras, no necesitan servidor ni navegador y dependen únicamente de las reglas de validación. | Medio, porque las pruebas dependen de los endpoints, los códigos HTTP, la autenticación y los formatos JSON. | Alto, porque las pruebas dependen del navegador, los elementos de la interfaz, los localizadores y la secuencia completa de interacciones del usuario. |

**Resultado de las pruebas unitarias:** 21 pruebas exitosas y 1 fallida, correspondiente al defecto DEF-01. El tiempo total de ejecución fue de 0.23 segundos, con un promedio aproximado de 0.0105 segundos por prueba.

**Resultado de las pruebas API:** 32 pruebas exitosas y 3 fallidas, correspondientes a dos defectos distintos: DEF-01 y DEF-02. El tiempo total registrado fue de 2.54 segundos, con un promedio aproximado de 0.073 segundos por prueba.

**Resultado de las pruebas E2E:** 3 pruebas exitosas y 1 fallida, correspondiente al defecto DEF-03. El tiempo total registrado fue de 10.66 segundos, con un promedio de 2.665 segundos por prueba.

**Nota:** Los tiempos corresponden a las ejecuciones registradas durante el laboratorio. El tiempo de API de 2.54 segundos debe sustituirse si la ejecución final con `pytest tests/api -q` reporta un valor diferente.

## 3. Recomendación

Se recomienda ejecutar las pruebas unitarias en cada commit, debido a su bajo costo de ejecución (0.23 segundos para 22 casos) y su capacidad para detectar errores en funciones individuales. En cada pull request deben ejecutarse las pruebas unitarias y de integración API, que permiten verificar las reglas de negocio y el contrato HTTP. Antes de liberar a producción deben ejecutarse los tres niveles, incluyendo las pruebas E2E, cuyo tiempo fue de 10.66 segundos para cuatro casos.

Esta estrategia sigue la pirámide de pruebas, priorizando las verificaciones rápidas y de menor mantenimiento, sin excluir las pruebas de sistema que permiten validar los flujos completos del usuario.

Los resultados demostraron que una suite exclusivamente E2E podría no detectar DEF-02 si únicamente verificara la interfaz sin comprobar códigos HTTP. Asimismo, una suite exclusivamente unitaria podría detectar DEF-01, pero no necesariamente DEF-02 ni DEF-03, porque estos requieren comprobar la comunicación HTTP y las interacciones de la interfaz.

El defecto DEF-03 demuestra especialmente la importancia de las pruebas E2E, ya que las validaciones individuales y de API no necesariamente detectan que un botón de la interfaz elimina un producto distinto al seleccionado.

Por lo tanto, se recomienda combinar los tres niveles para obtener una cobertura complementaria, identificar defectos desde diferentes perspectivas y reducir el riesgo de liberar funcionalidades que incumplan los requisitos del negocio.