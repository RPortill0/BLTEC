import sqlite3
import os
from werkzeug.security import generate_password_hash

# Obtener la ruta correcta
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'database.db')

def inicializar():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tabla de usuarios
    cursor.execute('DROP TABLE IF EXISTS usuarios')
    cursor.execute('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Crear tabla de técnicos (si no existe)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tecnicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cuadrilla TEXT NOT NULL,
            tipo_lista TEXT NOT NULL,
            telefono TEXT,
            comentario TEXT
        )
    ''')

    # INSERTAR USUARIO ADMIN CON HASH
    # La contraseña será: admin123
    password_encriptada = generate_password_hash('admin123')
    cursor.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', 
                   ('admin', password_encriptada))

    conn.commit()
    conn.close()
    print(f"✅ Base de datos inicializada en: {db_path}")

if __name__ == '__main__':
    inicializar()