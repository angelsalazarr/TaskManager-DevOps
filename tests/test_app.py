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


# CP04 / RF03
def test_cp04_editar_tarea(client):
    crear(client)
    resp = client.put("/api/tareas/1", json={"nombre": "Nuevo nombre", "descripcion": "Nueva"})
    assert resp.status_code == 200
    assert resp.get_json()["nombre"] == "Nuevo nombre"
    assert resp.get_json()["descripcion"] == "Nueva"


def test_editar_inexistente(client):
    assert client.put("/api/tareas/5", json={"nombre": "X"}).status_code == 404


def test_editar_nombre_vacio(client):
    crear(client)
    assert client.put("/api/tareas/1", json={"nombre": ""}).status_code == 400


def test_editar_sin_datos(client):
    crear(client)
    assert client.put("/api/tareas/1", json={}).status_code == 400


# CP05 / RF04
def test_cp05_eliminar_tarea(client):
    crear(client)
    assert client.delete("/api/tareas/1").status_code == 200
    assert client.get("/api/tareas").get_json() == []


def test_eliminar_inexistente(client):
    assert client.delete("/api/tareas/9").status_code == 404


# CP06 / RF05
@pytest.mark.parametrize("estado", ["Pendiente", "En proceso", "Terminada"])
def test_cp06_cambiar_estado(client, estado):
    crear(client)
    resp = client.put("/api/tareas/1", json={"estado": estado})
    assert resp.status_code == 200
    assert resp.get_json()["estado"] == estado


def test_estado_invalido(client):
    crear(client)
    assert client.put("/api/tareas/1", json={"estado": "Cancelada"}).status_code == 400


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


# CP08
def test_cp08_filtro_estado_invalido(client):
    resp = client.get("/api/tareas?estado=Cancelada")
    assert resp.status_code == 400
    assert "inválido" in resp.get_json()["error"]
