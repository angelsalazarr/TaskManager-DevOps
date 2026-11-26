"""TaskManager - Sistema web para la gestión de tareas.

API REST + interfaz web (Flask + SQLite).
"""
import os
import sqlite3

from flask import Flask, g, jsonify, render_template, request

ESTADOS = ("Pendiente", "En proceso", "Terminada")
PRIORIDADES = ("Alta", "Media", "Baja")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def create_app(config=None):
    app = Flask(__name__)
    app.config["DATABASE"] = os.environ.get(
        "DATABASE_PATH", os.path.join(BASE_DIR, "tasks.db")
    )
    if config:
        app.config.update(config)

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        db = sqlite3.connect(app.config["DATABASE"])
        db.execute(
            """CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL DEFAULT '',
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                prioridad TEXT NOT NULL DEFAULT 'Media',
                creada TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        db.commit()
        db.close()

    init_db()

    def validar(datos, parcial=False):
        """Valida los datos de una tarea. Devuelve (datos_limpios, error)."""
        if not isinstance(datos, dict):
            return None, "El cuerpo de la petición debe ser un objeto JSON."
        limpio = {}
        if "nombre" in datos or not parcial:
            nombre = str(datos.get("nombre", "")).strip()
            if not nombre:
                return None, "El nombre de la tarea es obligatorio."
            if len(nombre) > 100:
                return None, "El nombre no puede exceder 100 caracteres."
            limpio["nombre"] = nombre
        if "descripcion" in datos:
            limpio["descripcion"] = str(datos["descripcion"] or "").strip()
        if "estado" in datos:
            if datos["estado"] not in ESTADOS:
                return None, "Estado inválido. Use: " + ", ".join(ESTADOS) + "."
            limpio["estado"] = datos["estado"]
        if "prioridad" in datos:
            if datos["prioridad"] not in PRIORIDADES:
                return None, "Prioridad inválida. Use: " + ", ".join(PRIORIDADES) + "."
            limpio["prioridad"] = datos["prioridad"]
        return limpio, None

    def fila_a_dict(fila):
        return {k: fila[k] for k in fila.keys()}

    @app.get("/")
    def index():
        return render_template("index.html", estados=ESTADOS, prioridades=PRIORIDADES)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    # RF02 - Consultar tareas
    @app.get("/api/tareas")
    def listar():
        estado = request.args.get("estado")
        db = get_db()
        if estado:
            filas = db.execute(
                "SELECT * FROM tareas WHERE estado = ? ORDER BY id DESC", (estado,)
            ).fetchall()
        else:
            filas = db.execute("SELECT * FROM tareas ORDER BY id DESC").fetchall()
        return jsonify([fila_a_dict(f) for f in filas])

    @app.get("/api/tareas/<int:tarea_id>")
    def obtener(tarea_id):
        fila = get_db().execute(
            "SELECT * FROM tareas WHERE id = ?", (tarea_id,)
        ).fetchone()
        if fila is None:
            return jsonify({"error": "Tarea no encontrada."}), 404
        return jsonify(fila_a_dict(fila))

    # RF01 + RF06 - Registrar tareas con prioridad
    @app.post("/api/tareas")
    def crear():
        datos, error = validar(request.get_json(silent=True))
        if error:
            return jsonify({"error": error}), 400
        db = get_db()
        cur = db.execute(
            "INSERT INTO tareas (nombre, descripcion, estado, prioridad) VALUES (?, ?, ?, ?)",
            (
                datos["nombre"],
                datos.get("descripcion", ""),
                datos.get("estado", "Pendiente"),
                datos.get("prioridad", "Media"),
            ),
        )
        db.commit()
        fila = db.execute("SELECT * FROM tareas WHERE id = ?", (cur.lastrowid,)).fetchone()
        return jsonify(fila_a_dict(fila)), 201

    # RF03 + RF05 + RF06 - Editar tarea, cambiar estado y prioridad
    @app.put("/api/tareas/<int:tarea_id>")
    def editar(tarea_id):
        db = get_db()
        if db.execute("SELECT 1 FROM tareas WHERE id = ?", (tarea_id,)).fetchone() is None:
            return jsonify({"error": "Tarea no encontrada."}), 404
        datos, error = validar(request.get_json(silent=True), parcial=True)
        if error:
            return jsonify({"error": error}), 400
        if not datos:
            return jsonify({"error": "No hay datos para actualizar."}), 400
        campos = ", ".join(f"{c} = ?" for c in datos)
        db.execute(
            f"UPDATE tareas SET {campos} WHERE id = ?", (*datos.values(), tarea_id)
        )
        db.commit()
        fila = db.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,)).fetchone()
        return jsonify(fila_a_dict(fila))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
