// Cargar todo al inicio
document.addEventListener('DOMContentLoaded', () => {
    cargarProyectos();
    cargarTareas();
});

// ==========================================
// PROYECTOS
// ==========================================
async function cargarProyectos() {
    const res = await fetch('/proyectos');
    const proyectos = await res.json();
    
    // Llenar la tabla de proyectos
    const tbody = document.getElementById('lista-proyectos');
    tbody.innerHTML = '';
    
    // Llenar el select de tareas
    const select = document.getElementById('t-proyecto');
    select.innerHTML = '<option value="">Seleccione...</option>';

    proyectos.forEach(p => {
        // Fila en tabla
        tbody.innerHTML += `
            <tr>
                <td>${p.id}</td>
                <td>${p.titulo}</td>
                <td>${p.descripcion}</td>
                <td>
                    <button class="btn btn-secondary" onclick="editarProyecto(${p.id})">Editar</button>
                    <button class="btn btn-primary" onclick="borrarProyecto(${p.id})">Borrar</button>
                </td>
            </tr>
        `;
        // Opción en select
        select.innerHTML += `<option value="${p.id}">${p.titulo}</option>`;
    });
}

document.getElementById('form-proyecto').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        titulo: document.getElementById('p-titulo').value,
        descripcion: document.getElementById('p-desc').value
    };
    
    const res = await fetch('/proyectos', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    
    if(res.ok) {
        document.getElementById('form-proyecto').reset();
        cargarProyectos();
    } else {
        alert("Error al crear proyecto");
    }
});

async function borrarProyecto(id) {
    if(!confirm("¿Seguro que deseas borrar este proyecto?")) return;
    
    const res = await fetch(`/proyectos/${id}`, { method: 'DELETE' });
    if(res.ok) {
        cargarProyectos();
        cargarTareas(); // Refrescar tareas también
    } else {
        const error = await res.json();
        alert(error.error || "Error al borrar");
    }
}

async function editarProyecto(id) {
    const nuevoTitulo = prompt("Nuevo título del proyecto:");
    if(!nuevoTitulo) return; // Canceló
    
    const nuevaDesc = prompt("Nueva descripción:");
    
    const res = await fetch(`/proyectos/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ titulo: nuevoTitulo, descripcion: nuevaDesc })
    });
    
    if(res.ok) cargarProyectos();
    else alert("Error al actualizar");
}

// ==========================================
// TAREAS
// ==========================================
async function cargarTareas() {
    const res = await fetch('/tareas');
    const tareas = await res.json();
    
    const tbody = document.getElementById('lista-tareas');
    tbody.innerHTML = '';

    tareas.forEach(t => {
        tbody.innerHTML += `
            <tr>
                <td>${t.id}</td>
                <td>${t.nombre}</td>
                <td>${t.proyecto_titulo || 'Sin proyecto'}</td>
                <td><b>${t.estado}</b></td>
                <td>
                    <button class="btn btn-secondary" onclick="cambiarEstado(${t.id}, '${t.nombre}', ${t.proyecto_id})">Estado</button>
                    <button class="btn btn-primary" onclick="borrarTarea(${t.id})">Borrar</button>
                </td>
            </tr>
        `;
    });
}

document.getElementById('form-tarea').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        nombre: document.getElementById('t-nombre').value,
        proyecto_id: document.getElementById('t-proyecto').value
    };
    
    const res = await fetch('/tareas', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    
    if(res.ok) {
        document.getElementById('form-tarea').reset();
        cargarTareas();
    } else {
        alert("Error al crear tarea");
    }
});

async function borrarTarea(id) {
    if(!confirm("¿Borrar tarea?")) return;
    const res = await fetch(`/tareas/${id}`, { method: 'DELETE' });
    if(res.ok) cargarTareas();
}

async function cambiarEstado(id, nombre, proyecto_id) {
    const estados = ["Pendiente", "En progreso", "Completada"];
    const input = prompt("Escribe el nuevo estado (Pendiente, En progreso, Completada):", "Completada");
    
    if(estados.includes(input)) {
        const res = await fetch(`/tareas/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ nombre: nombre, estado: input, proyecto_id: proyecto_id })
        });
        if(res.ok) cargarTareas();
        else alert("Error al actualizar estado");
    } else if(input) {
        alert("Estado inválido. Debe ser exactamente: Pendiente, En progreso o Completada");
    }
}
