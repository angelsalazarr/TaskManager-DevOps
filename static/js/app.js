const API = "/api/tareas";
const $ = (id) => document.getElementById(id);
const form = $("form-tarea");
let tareas = [];

function mostrarMensaje(texto, tipo) {
  const m = $("mensaje");
  m.textContent = texto;
  m.className = tipo;
}

async function peticion(url, opciones) {
  const resp = await fetch(url, opciones);
  const datos = await resp.json();
  if (!resp.ok) throw new Error(datos.error || "Error inesperado.");
  return datos;
}

function escapar(t) {
  const d = document.createElement("div");
  d.textContent = t;
  return d.innerHTML;
}

async function cargar() {
  const filtro = $("filtro-estado").value;
  tareas = await peticion(filtro ? `${API}?estado=${encodeURIComponent(filtro)}` : API);
  render();
}

function render() {
  const ul = $("lista-tareas");
  ul.innerHTML = "";
  $("vacio").hidden = tareas.length > 0;
  const estados = ["Pendiente", "En proceso", "Terminada"];
  for (const t of tareas) {
    const li = document.createElement("li");
    li.className = `tarea ${t.prioridad}`;
    if (t.estado === "Terminada") li.classList.add("Terminada");
    li.innerHTML = `
      <div class="titulo">${escapar(t.nombre)}</div>
      <div class="meta">Prioridad: ${t.prioridad} · Estado: ${t.estado}</div>
      <div>${escapar(t.descripcion || "")}</div>
      <div class="tarea-acciones">
        <select data-id="${t.id}" class="cambiar-estado" aria-label="Cambiar estado">
          ${estados.map((e) => `<option ${e === t.estado ? "selected" : ""}>${e}</option>`).join("")}
        </select>
        <button data-id="${t.id}" class="editar secundario">Editar</button>
      </div>`;
    ul.appendChild(li);
  }
}

function limpiarFormulario() {
  form.reset();
  $("tarea-id").value = "";
  $("form-titulo").textContent = "Nueva tarea";
  $("btn-cancelar").hidden = true;
  $("prioridad").value = "Media";
}

form.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const id = $("tarea-id").value;
  const cuerpo = {
    nombre: $("nombre").value,
    descripcion: $("descripcion").value,
    prioridad: $("prioridad").value,
    estado: $("estado").value,
  };
  try {
    await peticion(id ? `${API}/${id}` : API, {
      method: id ? "PUT" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(cuerpo),
    });
    mostrarMensaje(id ? "Tarea actualizada correctamente." : "Tarea guardada correctamente.", "ok");
    limpiarFormulario();
    await cargar();
  } catch (e) {
    mostrarMensaje(e.message, "error");
  }
});

$("btn-cancelar").addEventListener("click", () => {
  limpiarFormulario();
  mostrarMensaje("", "");
});

$("filtro-estado").addEventListener("change", cargar);

$("lista-tareas").addEventListener("change", async (ev) => {
  if (!ev.target.classList.contains("cambiar-estado")) return;
  try {
    await peticion(`${API}/${ev.target.dataset.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ estado: ev.target.value }),
    });
    mostrarMensaje("Estado actualizado.", "ok");
    await cargar();
  } catch (e) {
    mostrarMensaje(e.message, "error");
  }
});

$("lista-tareas").addEventListener("click", async (ev) => {
  const id = ev.target.dataset.id;
  if (!id) return;
  if (ev.target.classList.contains("editar")) {
    const t = tareas.find((x) => String(x.id) === id);
    $("tarea-id").value = t.id;
    $("nombre").value = t.nombre;
    $("descripcion").value = t.descripcion;
    $("prioridad").value = t.prioridad;
    $("estado").value = t.estado;
    $("form-titulo").textContent = "Editar tarea";
    $("btn-cancelar").hidden = false;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
});

cargar();
