from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import check_password_hash
import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(base_dir, '../templates'),
            static_folder=os.path.join(base_dir, '../static'))

app.secret_key = 'clave_secreta_muy_segura_bl_tecs'

# Configuración extra de seguridad para las cookies de sesión
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

def get_db_conection():
    ruta_dbd = os.path.normpath(os.path.join(base_dir, '../database/database.db'))
    conn = sqlite3.connect(ruta_dbd)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('dashboard'))
    return render_template('Index.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

@app.route('/api/login', methods=['POST'])
def login_api():
    datos = request.get_json()
    conn = get_db_conection()
    # Buscamos al usuario por su nombre
    usuario = conn.execute('SELECT * FROM usuarios WHERE user = ?', 
                           (datos.get('username'),)).fetchone()
    conn.close()

    # Comparamos el hash de la DB con la contraseña escrita
    if usuario and check_password_hash(usuario['pass'], datos.get('password')):
        session['usuario'] = datos.get('username')
        return jsonify({"success": True})
    
    return jsonify({"success": False})

@app.route('/api/buscar')
def buscar_api():
    if 'usuario' not in session:
        return jsonify({"error": "No autorizado"}), 401
    
    query = request.args.get('q', '')
    conn = get_db_conection()
    cursor = conn.execute('''SELECT * FROM tecnicos 
                          WHERE nombre LIKE ? OR cuadrilla LIKE ? OR tipo_lista LIKE ?''', 
                          (f'%{query}%', f'%{query}%', f'%{query}%'))
    tecnicos = [dict(t) for t in cursor.fetchall()]
    conn.close()
    return jsonify(tecnicos)

@app.route('/api/guardar', methods=['POST'])
def guardar_tecnico():
    if 'usuario' not in session:
        return jsonify({"error": "No autorizado"}), 401
        
    datos = request.get_json()
    id_tec = datos.get('id')
    conn = get_db_conection()
    
    try:
        if id_tec:
            conn.execute('''UPDATE tecnicos SET nombre=?, cuadrilla=?, tipo_lista=?, telefono=?, comentario=? 
                            WHERE id=?''', 
                         (datos['nombre'], datos['cuadrilla'], datos['tipo_lista'], 
                          datos['telefono'], datos['comentario'], id_tec))
        else:
            conn.execute('''INSERT INTO tecnicos (nombre, cuadrilla, tipo_lista, telefono, comentario) 
                            VALUES (?, ?, ?, ?, ?)''', 
                         (datos['nombre'], datos['cuadrilla'], datos['tipo_lista'], 
                          datos['telefono'], datos['comentario']))
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/eliminar/<int:id>', methods=['DELETE'])
def eliminar_tecnico(id):
    if 'usuario' not in session:
        return jsonify({"error": "No autorizado"}), 401
        
    conn = get_db_conection()
    conn.execute('DELETE FROM tecnicos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)