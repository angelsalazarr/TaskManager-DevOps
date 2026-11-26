import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402


@pytest.fixture()
def client(tmp_path):
    app = create_app({"DATABASE": str(tmp_path / "test.db"), "TESTING": True})
    return app.test_client()


def crear(client, **extra):
    datos = {"nombre": "Realizar actividad DevOps", "prioridad": "Alta"}
    datos.update(extra)
    return client.post("/api/tareas", json=datos)


def test_registro_tarea_ejemplo():
    tarea = {"nombre": "Realizar actividad DevOps", "estado": "Pendiente"}
    assert tarea["nombre"] == "Realizar actividad DevOps"
    assert tarea["estado"] == "Pendiente"


def test_pagina_principal(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "TaskManager" in resp.get_data(as_text=True)


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


# CP01 / RF01
def test_cp01_registrar_tarea(client):
    resp = crear(client, descripcion="Detalle")
    assert resp.status_code == 201
    datos = resp.get_json()
    assert datos["id"] == 1
    assert datos["nombre"] == "Realizar actividad DevOps"
    assert datos["estado"] == "Pendiente"
    assert datos["descripcion"] == "Detalle"


# CP02
def test_cp02_registrar_sin_nombre(client):
    resp = client.post("/api/tareas", json={"nombre": "   "})
    assert resp.status_code == 400
    assert "obligatorio" in resp.get_json()["error"]
    assert client.get("/api/tareas").get_json() == []


def test_registrar_sin_json(client):
    assert client.post("/api/tareas", data="hola").status_code == 400


def test_nombre_demasiado_largo(client):
    assert crear(client, nombre="x" * 101).status_code == 400


# CP03 / RF02
def test_cp03_consultar_tareas(client):
    crear(client, nombre="Tarea A")
    crear(client, nombre="Tarea B")
    lista = client.get("/api/tareas").get_json()
    assert [t["nombre"] for t in lista] == ["Tarea B", "Tarea A"]


def test_consultar_una_tarea(client):
    crear(client)
    assert client.get("/api/tareas/1").get_json()["nombre"] == "Realizar actividad DevOps"
    assert client.get("/api/tareas/99").status_code == 404


def test_filtrar_por_estado(client):
    crear(client, nombre="A")
    crear(client, nombre="B", estado="Terminada")
    lista = client.get("/api/tareas?estado=Terminada").get_json()
    assert len(lista) == 1 and lista[0]["nombre"] == "B"


# CP07 / RF06
@pytest.mark.parametrize("prioridad", ["Alta", "Media", "Baja"])
def test_cp07_seleccionar_prioridad(client, prioridad):
    resp = crear(client, prioridad=prioridad)
    assert resp.get_json()["prioridad"] == prioridad


def test_prioridad_invalida(client):
    assert crear(client, prioridad="Urgente").status_code == 400


def test_prioridad_por_defecto(client):
    resp = client.post("/api/tareas", json={"nombre": "Sin prioridad"})
    assert resp.get_json()["prioridad"] == "Media"
