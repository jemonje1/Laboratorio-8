# Informe · Laboratorio 8 · Pruebas automatizadas

**Equipo:**
- Equipo de atras

**Integrantes:**
- Sophia Corea
- Luis Lopez
- Javier Monje

## 1. Defectos encontrados

Durante la ejecución de las pruebas de integración API se identificaron dos defectos relacionados con el incumplimiento de los requisitos del negocio y el comportamiento esperado de los endpoints.

| ID | Nivel que lo detectó | Prueba (archivo::función) | Pasos para reproducir | Resultado esperado (según la especificación) | Resultado obtenido |
|---|---|---|---|---|---|
| DEF-01 | API | `tests/api/test_api.py::test_crear_producto_invalido` y `test_actualizar_producto_invalido` | Autenticarse y enviar una solicitud POST a `/api/productos` con nombre válido, precio 0 y stock 5. Repetir con PUT sobre un producto existente. | HTTP 400, debido a que el precio debe ser estrictamente mayor que cero. | POST devuelve HTTP 201 y PUT devuelve HTTP 200, permitiendo un precio inválido. |
| DEF-02 | API | `tests/api/test_api.py::test_consultar_producto_inexistente` | Autenticarse y enviar una solicitud GET a `/api/productos/999`. | HTTP 404, indicando que el producto solicitado no existe. | HTTP 200 con un objeto JSON vacío. |

**Detección adicional de DEF-01 mediante pruebas unitarias:**

El defecto DEF-01 también fue identificado en el nivel unitario mediante la prueba `tests/unitarias/test_unitarias.py::test_limites_precio`.

Para reproducirlo, se ejecuta la función `validar_producto("Teclado", 0, 5)`, utilizando un nombre válido, precio igual a cero y stock válido.

Según la especificación, el precio debe ser estrictamente mayor que cero, por lo que se espera que la función devuelva una lista con al menos un mensaje de error. Sin embargo, la función devuelve una lista vacía `[]`, aceptando incorrectamente el precio cero.

La prueba correspondiente falló, confirmando que el defecto puede detectarse directamente en la función de validación, sin necesidad de ejecutar el servidor ni realizar solicitudes HTTP. Este hallazgo corresponde al mismo DEF-01 identificado mediante API, por lo que no se contabiliza como un defecto nuevo.

Los defectos se conservaron en el código original de la aplicación, manteniendo las pruebas correspondientes en estado fallido, según las instrucciones del laboratorio.

## 2. Tabla comparativa de niveles

| Criterio | Unitarias | API | E2E |
|---|---|---|---|
| Número de pruebas | 22 | 35 | Pendiente |
| Tiempo total de ejecución (s) | 0.23 | 2.54 | Pendiente |
| Tiempo promedio por prueba (s) | 0.0105 | 0.073 | Pendiente |
| Defectos detectados (IDs) | DEF-01 | DEF-01, DEF-02 | Pendiente |
| ¿Qué cambio en la app rompería estas pruebas sin que haya un defecto? | Un cambio legítimo en las reglas de validación, acompañado de una actualización de la especificación, podría provocar fallos si las pruebas no se actualizan para reflejar los nuevos requisitos. | Cambios válidos en las rutas, nombres de campos JSON o estructura de respuestas que también se reflejen en una especificación actualizada. | Pendiente |
| Costo de mantenimiento (Alto / Medio / Bajo) y por qué | Bajo, porque las pruebas evalúan funciones puras, no necesitan servidor ni navegador y dependen únicamente de las reglas de validación. | Medio, porque las pruebas dependen de los endpoints, los códigos HTTP, la autenticación y los formatos JSON. | Pendiente |

**Resultado de las pruebas unitarias:** 21 pruebas exitosas y 1 fallida, correspondiente al defecto DEF-01. El tiempo total de ejecución fue de 0.23 segundos, con un promedio aproximado de 0.0105 segundos por prueba.

**Resultado de las pruebas API:** 32 pruebas exitosas y 3 fallidas, correspondientes a dos defectos distintos.

**Nota:** El tiempo de 2.54 segundos corresponde a la ejecución registrada previamente. Debe sustituirse si la ejecución final con `pytest tests/api -q` reporta otro valor.

## 3. Recomendación

Se recomienda ejecutar las pruebas unitarias en cada commit, debido a su rapidez y capacidad para detectar errores en funciones individuales. En cada pull request deben ejecutarse tanto las pruebas unitarias como las pruebas de integración API, con el propósito de verificar las reglas de negocio y el comportamiento de los endpoints.

Antes de liberar a producción, se recomienda ejecutar los tres niveles de pruebas: unitarias, API y E2E. Esta estrategia sigue la pirámide de pruebas, priorizando una mayor cantidad de pruebas rápidas y reservando las pruebas más costosas para validar los flujos completos del sistema.

En las pruebas API se detectaron dos defectos: la aceptación de productos con precio cero y la respuesta HTTP 200 al consultar un producto inexistente. Una suite exclusivamente E2E podría no detectar el segundo defecto si únicamente verifica el comportamiento visual de la interfaz. Por otro lado, una suite exclusivamente unitaria podría identificar el problema de validación del precio, pero no necesariamente el incumplimiento del contrato HTTP.

Por lo tanto, se recomienda mantener los tres niveles de pruebas, ya que se complementan y permiten detectar defectos que podrían pasar desapercibidos al utilizar un único enfoque.