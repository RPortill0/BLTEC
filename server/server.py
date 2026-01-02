from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import check_password_hash
import sqlite3
import os

# CONFIGURACIÓN DE RUTAS
# base_dir: .../BL_TECS/server
base_dir = os.path.dirname(os.path.abspath(__file__))
# root_dir: .../BL_TECS
root_dir = os.path.dirname(base_dir)

app = Flask(__name__, 
            template_folder=os.path.join(root_dir, 'templates'),
            static_folder=os.path.join(root_dir, 'static'))

app.secret_key = 'rat_system_secure_2026'

def get_db_conection():
    # RUTA EXACTA: Sube de server/ y entra en database/
    db_path = os.path.normpath(os.path.join(root_dir, 'database', 'database.db'))
    
    # Esto es para que en tu consola veas si realmente la encuentra
    if not os.path.exists(db_path):
        print(f"❌ ERROR: No se encontró la base de datos en: {db_path}")
    
    conn = sqlite3.connect(db_path)
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

@app.route('/api/login', methods=['POST'])
def login_api():
    try:
        datos = request.get_json()
        conn = get_db_conection()
        # Verificamos la tabla usuarios
        usuario = conn.execute('SELECT * FROM usuarios WHERE username = ?', 
                               (datos.get('username'),)).fetchone()
        conn.close()

        if usuario and check_password_hash(usuario['password'], datos.get('password')):
            session['usuario'] = datos.get('username')
            return jsonify({"success": True})
        
        return jsonify({"success": False}), 401
    except Exception as e:
        # Imprime el error real en la terminal para que sepas qué falló
        print(f"🔥 Error Interno: {e}") 
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Asegúrate de que obtener_tecnicos y guardar_tecnico usen también get_db_conection()
# ... (el resto de tus rutas de la API)

if __name__ == '__main__':
    app.run(debug=True)