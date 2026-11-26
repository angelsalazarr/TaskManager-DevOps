# TaskManager-DevOps

Sistema web para la gestión de tareas.

Proyecto remedial de **Gestión del Proceso de Desarrollo de Software** (Universidad Tecnológica de Puebla, 10° A).
Implementa las fases del ciclo de vida DevOps utilizando GitHub.

**Equipo:** Angel Ramos Salazar · Manuel Antonio García Huerta

## Contexto

TechSolutions administra las tareas de sus empleados en hojas de cálculo, lo que provoca pérdida de información, duplicidad de tareas y falta de seguimiento. TaskManager centraliza la gestión de tareas y se desarrolla con un proceso DevOps automatizado.

## Funcionalidades

| Código | Funcionalidad | Descripción |
| --- | --- | --- |
| RF01 | Registrar tareas | Agregar nuevas tareas con nombre, descripción y prioridad. |
| RF02 | Consultar tareas | Mostrar todas las tareas (con filtro por estado). |
| RF03 | Editar tareas | Modificar la información de una tarea. |
| RF04 | Eliminar tareas | Eliminar tareas existentes. |
| RF05 | Cambiar estado | Pendiente, En proceso o Terminada. |
| RF06 | Asignar prioridad | Alta, Media o Baja. |

## Tecnologías

- Frontend: HTML, CSS y JavaScript
- Backend: Python con Flask
- Base de datos: SQLite
- Control de versiones: Git y GitHub
- Automatización: GitHub Actions
- Pruebas: Pytest
- Despliegue: Render (gunicorn)

## Estructura

```text
TaskManager-DevOps/
├── app.py
├── requirements.txt
├── README.md
├── templates/index.html
├── static/css/style.css
├── static/js/app.js
├── tests/test_app.py
├── scripts/monitoreo.py
├── docs/
└── .github/workflows/ (ci.yml, cd.yml)
```

## Ejecución local

```bash
git clone https://github.com/USUARIO/TaskManager-DevOps.git
cd TaskManager-DevOps
python -m venv venv
venv\Scripts\activate        # En Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

La aplicación queda disponible en http://127.0.0.1:5000

## Pruebas

```bash
pytest -v
```

## API REST

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/api/tareas` | Lista las tareas (`?estado=Pendiente` para filtrar). |
| GET | `/api/tareas/<id>` | Consulta una tarea. |
| POST | `/api/tareas` | Registra una tarea. |
| PUT | `/api/tareas/<id>` | Edita nombre, descripción, estado o prioridad. |
| DELETE | `/api/tareas/<id>` | Elimina una tarea. |
| GET | `/health` | Verificación de disponibilidad. |

## Flujo de trabajo DevOps

1. **Plan:** GitHub Projects (tablero Board), Issues e historias de usuario (`docs/historias-usuario.md`).
2. **Code:** ramas `feature/*`, commits descriptivos y Pull Requests con revisión cruzada.
3. **CI:** GitHub Actions ejecuta `pytest` en cada push y Pull Request hacia `main` (`.github/workflows/ci.yml`).
4. **Test:** matriz de casos de prueba (`docs/matriz-pruebas.md`) y reporte de errores con Issues.
5. **Release:** versión `v1.0.0` y workflow de entrega que genera un artefacto (`.github/workflows/cd.yml`).
6. **Deploy:** publicación en Render desde el repositorio.
7. **Operate & Monitor:** `scripts/monitoreo.py`, registro de incidencias (`docs/monitoreo.md`) y mejoras (`docs/mejoras.md`).
