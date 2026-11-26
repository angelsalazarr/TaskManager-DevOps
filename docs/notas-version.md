# Notas de versión

## v1.0.0: Primera versión estable de TaskManager

Funcionalidades incorporadas:
- RF01 Registrar tareas con nombre, descripción y prioridad.
- RF02 Consultar tareas con filtro por estado.
- RF03 Editar tareas.
- RF04 Eliminar tareas con confirmación.
- RF05 Cambiar estado (Pendiente, En proceso, Terminada).
- RF06 Asignar prioridad (Alta, Media, Baja).
- Validación de datos y mensajes de error claros.
- API REST y endpoint `/health`.
- Pruebas automatizadas con Pytest (integración continua con GitHub Actions).
- Workflow de entrega que genera el artefacto `TaskManager-v1`.
- Despliegue en Render.

Limitaciones conocidas:
- Sin autenticación de usuarios.
- SQLite se reinicia en cada despliegue en Render (plan gratuito).
