# Operación y monitoreo

## Cómo se monitorea

El script `scripts/monitoreo.py` verifica la disponibilidad (`/health`), el tiempo de respuesta y el funcionamiento de las funcionalidades principales (registrar, consultar, editar y eliminar una tarea de prueba).

```bash
python scripts/monitoreo.py https://URL-DE-LA-APLICACION --repeticiones 5
```

## Registro de monitoreo

Pegar aquí la salida del script ejecutado contra la URL publicada (una entrada por revisión).

| Fecha y hora | Entorno | Disponibilidad | Tiempo promedio | Funcionalidades principales | Observaciones |
| --- | --- | --- | --- | --- | --- |
| (completar) | Render (producción) | | | | |

### Verificación local previa al despliegue

```text
Monitoreo de http://127.0.0.1:5055 - 2026-11-26 02:43:33
  [1] GET /health -> 200 en 19 ms OK
  [2] GET /health -> 200 en 1 ms OK
  [3] GET /health -> 200 en 1 ms OK
  [4] GET /health -> 200 en 1 ms OK
  [5] GET /health -> 200 en 1 ms OK
Disponibilidad: 100%
Tiempo de respuesta promedio: 4 ms
Prueba de funcionalidades principales:
  Registrar tarea   -> 201
  Consultar tareas  -> 200
  Editar tarea      -> 200
  Eliminar tarea    -> 200
```

## Aspectos verificados

- Disponibilidad de la aplicación: `/health`.
- Tiempo de respuesta: medido por el script.
- Errores que presente el sistema: revisar los logs del servicio en Render.
- Correcto almacenamiento de la información: se registra, consulta, edita y elimina una tarea de prueba.
- Funcionamiento de las funcionalidades principales: RF01 a RF05.

Nota sobre el plan gratuito de Render: el servicio puede "dormirse" tras un periodo sin tráfico, por lo que la primera petición puede tardar varios segundos. La base SQLite se reinicia en cada nuevo despliegue.

## Registro de incidencias

Cada problema detectado se documenta como un Issue con la etiqueta `incidencia` usando esta plantilla:

- Fecha de detección:
- Funcionalidad afectada:
- Descripción del problema:
- Evidencia del error:
- Responsable de corregirlo:
- Solución aplicada:

| Issue | Fecha | Funcionalidad | Responsable | Estado |
| --- | --- | --- | --- | --- |
| (completar con los Issues reales) | | | | |
