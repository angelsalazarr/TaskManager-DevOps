# Matriz de casos de prueba

| ID | Prueba | Resultado esperado | Prueba automática | Resultado |
| --- | --- | --- | --- | --- |
| CP01 | Registrar una tarea | La tarea se guarda correctamente. | test_cp01_registrar_tarea | Aprobada |
| CP02 | Registrar una tarea sin nombre | El sistema muestra una validación. | test_cp02_registrar_sin_nombre | Aprobada |
| CP03 | Consultar tareas | Se muestra el listado. | test_cp03_consultar_tareas | Aprobada |
| CP04 | Editar una tarea | Se actualiza la información. | test_cp04_editar_tarea | Aprobada |
| CP05 | Eliminar una tarea | La tarea desaparece del listado. | test_cp05_eliminar_tarea | Aprobada |
| CP06 | Cambiar estado | Se actualiza el estado. | test_cp06_cambiar_estado (3 estados) | Aprobada |
| CP07 | Seleccionar prioridad | Se guarda la prioridad elegida. | test_cp07_seleccionar_prioridad (3 niveles) | Aprobada |
| CP08 | Filtrar con un estado inválido | El sistema responde con un error de validación. | test_cp08_filtro_estado_invalido | Aprobada |

## Pruebas funcionales manuales (interfaz web)

Ejecutar en la aplicación (local o publicada). Marcar el resultado obtenido.

### CP01: Registrar una tarea
1. Abrir el sistema.
2. Escribir el nombre: Elaborar documentación.
3. Agregar una descripción.
4. Seleccionar prioridad Alta.
5. Presionar Guardar tarea.
6. Verificar que aparezca el mensaje de confirmación y la tarea en el listado.

Resultado esperado: la tarea se registra correctamente.

### CP02: Registrar una tarea sin nombre
1. Dejar el nombre vacío y presionar Guardar tarea.
2. Verificar que se muestre el mensaje "El nombre de la tarea es obligatorio." y que no se cree la tarea.

### CP03 a CP07
- CP03: verificar que el listado muestra todas las tareas registradas.
- CP04: presionar Editar, cambiar el nombre, guardar y verificar el cambio en el listado.
- CP05: presionar Eliminar, confirmar y verificar que la tarea desaparece.
- CP06: cambiar el estado con el selector de la tarea y verificar que se actualiza.
- CP07: registrar tareas con prioridad Alta, Media y Baja y verificar el color y la etiqueta.

## Evidencia de la ejecución automática

Resultado de `pytest -v` ejecutado sobre la versión entregada:

```text
tests/test_app.py::test_registro_tarea_ejemplo PASSED
tests/test_app.py::test_pagina_principal PASSED
tests/test_app.py::test_health PASSED
tests/test_app.py::test_cp01_registrar_tarea PASSED
tests/test_app.py::test_cp02_registrar_sin_nombre PASSED
tests/test_app.py::test_registrar_sin_json PASSED
tests/test_app.py::test_nombre_demasiado_largo PASSED
tests/test_app.py::test_cp03_consultar_tareas PASSED
tests/test_app.py::test_consultar_una_tarea PASSED
tests/test_app.py::test_filtrar_por_estado PASSED
tests/test_app.py::test_cp04_editar_tarea PASSED
tests/test_app.py::test_editar_inexistente PASSED
tests/test_app.py::test_editar_nombre_vacio PASSED
tests/test_app.py::test_editar_sin_datos PASSED
tests/test_app.py::test_cp05_eliminar_tarea PASSED
tests/test_app.py::test_eliminar_inexistente PASSED
tests/test_app.py::test_cp06_cambiar_estado[Pendiente] PASSED
tests/test_app.py::test_cp06_cambiar_estado[En proceso] PASSED
tests/test_app.py::test_cp06_cambiar_estado[Terminada] PASSED
tests/test_app.py::test_estado_invalido PASSED
tests/test_app.py::test_cp07_seleccionar_prioridad[Alta] PASSED
tests/test_app.py::test_cp07_seleccionar_prioridad[Media] PASSED
tests/test_app.py::test_cp07_seleccionar_prioridad[Baja] PASSED
tests/test_app.py::test_prioridad_invalida PASSED
tests/test_app.py::test_prioridad_por_defecto PASSED
tests/test_app.py::test_cp08_filtro_estado_invalido PASSED
============================== 26 passed in 0.25s ==============================
```
