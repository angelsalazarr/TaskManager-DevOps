"""Verifica disponibilidad, tiempo de respuesta y funcionamiento básico.

Uso:
    python scripts/monitoreo.py https://tu-app.onrender.com
    python scripts/monitoreo.py http://127.0.0.1:5000 --repeticiones 5
"""
import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import datetime


def peticion(url, metodo="GET", cuerpo=None):
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    req = urllib.request.Request(url, data=datos, method=metodo)
    if datos:
        req.add_header("Content-Type", "application/json")
    inicio = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            texto = resp.read().decode()
            codigo = resp.status
    except urllib.error.HTTPError as e:
        texto, codigo = e.read().decode(), e.code
    ms = (time.perf_counter() - inicio) * 1000
    return codigo, ms, texto


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--repeticiones", type=int, default=3)
    args = ap.parse_args()
    base = args.url.rstrip("/")

    print(f"Monitoreo de {base} - {datetime.now():%Y-%m-%d %H:%M:%S}")
    tiempos, errores = [], 0
    for i in range(args.repeticiones):
        codigo, ms, _ = peticion(base + "/health")
        ok = codigo == 200
        errores += 0 if ok else 1
        tiempos.append(ms)
        print(f"  [{i + 1}] GET /health -> {codigo} en {ms:.0f} ms {'OK' if ok else 'ERROR'}")
    print(f"Disponibilidad: {(args.repeticiones - errores) / args.repeticiones:.0%}")
    print(f"Tiempo de respuesta promedio: {sum(tiempos) / len(tiempos):.0f} ms")

    print("Prueba de funcionalidades principales:")
    codigo, _, texto = peticion(base + "/api/tareas", "POST",
                                {"nombre": "Prueba de monitoreo", "prioridad": "Baja"})
    print(f"  Registrar tarea   -> {codigo}")
    if codigo != 201:
        return
    tid = json.loads(texto)["id"]
    print(f"  Consultar tareas  -> {peticion(base + '/api/tareas')[0]}")
    print(f"  Editar tarea      -> {peticion(f'{base}/api/tareas/{tid}', 'PUT', {'estado': 'En proceso'})[0]}")
    print(f"  Eliminar tarea    -> {peticion(f'{base}/api/tareas/{tid}', 'DELETE')[0]}")


if __name__ == "__main__":
    main()
