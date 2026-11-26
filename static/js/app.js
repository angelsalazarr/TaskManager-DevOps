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
      <div>${escapar(t.descripcion || "")}</div>`;
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

cargar();
