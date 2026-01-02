// --- FUNCIÓN DE LOGIN ---
async function ejecutarLogin() {
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;
    const errorMsg = document.getElementById('mensaje_error');

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: user, password: pass })
        });

        const data = await response.json();

        if (data.success) {
            window.location.href = '/dashboard';
        } else {
            errorMsg.style.display = 'block';
            errorMsg.innerText = "Usuario o contraseña incorrectos";
        }
    } catch (e) {
        console.error("Error en login:", e);
    }
}

// --- FUNCIÓN PARA GUARDAR O EDITAR ---
async function guardarTecnico() {
    const id = document.getElementById('id_tecnico').value;
    const datos = {
        id: id || null,
        nombre: document.getElementById('nombre').value.toUpperCase().trim(),
        cuadrilla: document.getElementById('cuadrilla').value.trim(),
        tipo_lista: document.getElementById('tipo_lista').value,
        telefono: document.getElementById('telefono').value.trim(),
        comentario: document.getElementById('comentario').value.trim()
    };

    if (!datos.nombre || !datos.cuadrilla) {
        alert("⚠️ El Nombre y la Cuadrilla son obligatorios.");
        return;
    }

    try {
        const response = await fetch('/api/guardar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });

        const res = await response.json();
        if (res.success) {
            alert(id ? "✅ Registro actualizado correctamente" : "✅ Técnico registrado con éxito");
            limpiarFormulario();
            buscarTecnico(); // Refresca la lista y los contadores
        } else {
            alert("❌ Error: " + res.error);
        }
    } catch (e) {
        console.error("Error al guardar:", e);
    }
}

// --- FUNCIÓN DE BÚSQUEDA Y COLORES ---
async function buscarTecnico() {
    const q = document.getElementById('input_buscar').value;
    const contenedor = document.getElementById('resultados');

    try {
        const response = await fetch(`/api/buscar?q=${q}`);
        const tecnicos = await response.json();

        contenedor.innerHTML = '';
        
        // Variables para los contadores
        let countBL = 0, countWL = 0, countINTER = 0;

        tecnicos.forEach(t => {
            // Lógica de colores y conteo
            let colorPrincipal = '#95a5a6';
            if (t.tipo_lista === 'BL') { colorPrincipal = '#e74c3c'; countBL++; }
            if (t.tipo_lista === 'WL') { colorPrincipal = '#27ae60'; countWL++; }
            if (t.tipo_lista === 'INTER') { colorPrincipal = '#f39c12'; countINTER++; }

            contenedor.innerHTML += `
                <div class="card-tecnico" style="border-left: 10px solid ${colorPrincipal}; padding: 15px; background: white; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0; color: #2c3e50;">${t.nombre}</h3>
                        <span class="badge" style="background: ${colorPrincipal}; color: white; padding: 4px 10px; border-radius: 15px; font-size: 0.7rem; font-weight: bold;">
                            ${t.tipo_lista}
                        </span>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; font-size: 0.9rem;">
                        <span><strong>Cuadrilla:</strong> ${t.cuadrilla}</span>
                        <span><strong>Tel:</strong> ${t.telefono || '---'}</span>
                    </div>

                    <div style="margin-top: 8px; font-style: italic; color: #555; font-size: 0.85rem; border-top: 1px solid #eee; padding-top: 8px;">
                        "${t.comentario || 'Sin observaciones'}"
                    </div>

                    <div style="margin-top: 12px; display: flex; gap: 8px;">
                        <button onclick='cargarEdicion(${JSON.stringify(t)})' style="flex: 1; background: #3498db; color: white; border: none; padding: 6px; border-radius: 4px; cursor: pointer;">📝 Editar</button>
                        <button onclick="eliminarTecnico(${t.id})" style="flex: 1; background: #e74c3c; color: white; border: none; padding: 6px; border-radius: 4px; cursor: pointer;">🗑️ Eliminar</button>
                    </div>
                </div>
            `;
        });

        // Opcional: Si quieres imprimir los contadores en consola o en un div
        console.log(`Resumen: BL(${countBL}) WL(${countWL}) INTER(${countINTER})`);

    } catch (e) {
        console.error("Error en búsqueda:", e);
    }
}

// --- CARGAR DATOS EN FORMULARIO PARA EDITAR ---
function cargarEdicion(t) {
    document.getElementById('id_tecnico').value = t.id;
    document.getElementById('nombre').value = t.nombre;
    document.getElementById('cuadrilla').value = t.cuadrilla;
    document.getElementById('tipo_lista').value = t.tipo_lista;
    document.getElementById('telefono').value = t.telefono;
    document.getElementById('comentario').value = t.comentario;
    
    document.getElementById('form_title').innerText = "⚠️ EDITANDO REGISTRO";
    document.getElementById('form_title').style.color = "#d35400";
    document.getElementById('btn_cancelar').style.display = 'block';
    
    // Scroll hacia el formulario para avisar al usuario
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// --- LIMPIAR FORMULARIO ---
function limpiarFormulario() {
    document.getElementById('id_tecnico').value = '';
    document.getElementById('nombre').value = '';
    document.getElementById('cuadrilla').value = '';
    document.getElementById('tipo_lista').value = 'WL';
    document.getElementById('telefono').value = '';
    document.getElementById('comentario').value = '';
    
    document.getElementById('form_title').innerText = "REGISTRO TÉCNICO";
    document.getElementById('form_title').style.color = "#2c3e50";
    document.getElementById('btn_cancelar').style.display = 'none';
}

// --- ELIMINAR REGISTRO ---
async function eliminarTecnico(id) {
    if (!confirm("🚨 ¿Está seguro de eliminar a este técnico de forma permanente?")) return;

    try {
        const response = await fetch(`/api/eliminar/${id}`, { method: 'DELETE' });
        const res = await response.json();
        if (res.success) {
            buscarTecnico();
        }
    } catch (e) {
        console.error("Error al eliminar:", e);
    }
}

// Ejecutar búsqueda inicial al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    if(document.getElementById('resultados')) buscarTecnico();
});