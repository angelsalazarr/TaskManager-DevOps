# Historias de usuario

## HU01: Registrar tareas (RF01)
Como usuario del sistema, quiero registrar nuevas tareas para organizar mis actividades.

Criterios de aceptación:
- El sistema debe permitir ingresar el nombre de la tarea.
- El sistema debe permitir agregar una descripción.
- El sistema debe permitir seleccionar una prioridad.
- El sistema debe guardar la tarea.
- El sistema debe mostrar un mensaje de confirmación.

## HU02: Consultar tareas (RF02)
Como usuario, quiero ver el listado de todas las tareas registradas para conocer mis actividades pendientes y terminadas.

Criterios de aceptación:
- El sistema debe mostrar todas las tareas registradas.
- Cada tarea debe mostrar su nombre, descripción, prioridad y estado.
- El sistema debe permitir filtrar las tareas por estado.
- Si no hay tareas, debe mostrar un mensaje indicándolo.

## HU03: Editar tareas (RF03)
Como usuario, quiero modificar la información de una tarea para corregir o actualizar sus datos.

Criterios de aceptación:
- Debe permitir cargar los datos actuales de la tarea en el formulario.
- Debe permitir modificar nombre, descripción y prioridad.
- No debe permitir guardar la tarea con el nombre vacío.
- El cambio debe reflejarse en el listado de tareas.

## HU04: Eliminar tareas (RF04)
Como usuario, quiero eliminar tareas que ya no necesito para mantener el listado ordenado.

Criterios de aceptación:
- Debe solicitar confirmación antes de eliminar.
- La tarea eliminada debe desaparecer del listado.
- Si la tarea no existe, el sistema debe informar el error.

## HU05: Cambiar estado de tareas (RF05)
Como usuario, quiero cambiar el estado de una tarea para conocer su progreso.

Criterios de aceptación:
- Debe permitir seleccionar pendiente.
- Debe permitir seleccionar en proceso.
- Debe permitir seleccionar terminada.
- El cambio debe reflejarse en el listado de tareas.

## HU06: Asignar prioridad (RF06)
Como usuario, quiero clasificar mis tareas como alta, media o baja para atender primero las más importantes.

Criterios de aceptación:
- Debe permitir seleccionar prioridad alta, media o baja.
- La prioridad por defecto debe ser media.
- La prioridad elegida debe guardarse y mostrarse en el listado.
- No debe aceptar prioridades distintas a las definidas.

## HU07: Validar los datos capturados
Como responsable del sistema, quiero que se validen los datos de las tareas para evitar información incorrecta.

Criterios de aceptación:
- El nombre es obligatorio y no puede exceder 100 caracteres.
- El estado y la prioridad solo aceptan los valores definidos.
- El sistema debe mostrar un mensaje claro cuando un dato no es válido.

## HU08: Pruebas automáticas antes de publicar
Como equipo de desarrollo, queremos que las pruebas se ejecuten automáticamente en cada cambio para detectar errores antes de integrarlos a `main`.

Criterios de aceptación:
- GitHub Actions debe ejecutar las pruebas en cada push y Pull Request hacia `main`.
- Si una prueba falla, el equipo debe poder ver el detalle del error.

## HU09: Publicar y monitorear el sistema
Como empresa, quiero que el sistema esté publicado en una URL accesible y supervisado para que los empleados lo usen sin interrupciones.

Criterios de aceptación:
- La aplicación debe estar accesible desde una URL pública.
- Debe existir una forma de verificar disponibilidad y tiempo de respuesta.
- Los problemas detectados deben registrarse como Issues.
