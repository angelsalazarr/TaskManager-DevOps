# Propuestas de mejora para una futura versión (v1.1.0)

1. **Autenticación de usuarios:** inicio de sesión y asignación de tareas por empleado, para resolver el control de responsables que hoy se hace en hojas de cálculo.
2. **Filtros y búsqueda:** buscar por nombre y filtrar por prioridad además del estado.
3. **Base de datos persistente:** migrar de SQLite a PostgreSQL, porque en Render el disco gratuito se reinicia en cada despliegue.
4. **Notificaciones y fechas límite:** agregar fecha de vencimiento y avisos de tareas próximas a vencer.
5. **Reportes de productividad:** tareas terminadas por periodo y por responsable.

## Planeación de la versión v1.1.0

| Mejora | Fase DevOps | Estimación |
| --- | --- | --- |
| Autenticación de usuarios | Code / Test | 8 h |
| Filtros y búsqueda | Code | 3 h |
| PostgreSQL | Deploy | 5 h |
| Fechas límite y notificaciones | Code | 6 h |
| Reportes de productividad | Code | 6 h |
