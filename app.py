from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "proyectos.db")

def conexionDB():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def inicializar_db():
    conn = conexionDB()
    cursor = conn.cursor()
    
    # Entidad 1: Proyectos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT
        )
    """)
    
    # Entidad 2: Tareas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Pendiente',
            proyecto_id INTEGER,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
        )
    """)
    conn.commit()
    conn.close()

# ==========================================
# ENDPOINTS PARA PROYECTOS (Entidad 1)
# ==========================================

@app.route("/proyectos", methods=["GET"])
def obtener_proyectos():
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proyectos")
        datos = cursor.fetchall()
        
        proyectos = []
        for fila in datos:
            proyectos.append({
                "id": fila[0],
                "titulo": fila[1],
                "descripcion": fila[2]
            })
        conn.close()
        return jsonify(proyectos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/proyectos/<int:id>", methods=["GET"])
def obtener_proyecto(id):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proyectos WHERE id = ?", (id,))
        fila = cursor.fetchone()
        conn.close()
        
        if fila:
            proyecto = {
                "id": fila[0],
                "titulo": fila[1],
                "descripcion": fila[2]
            }
            return jsonify(proyecto), 200
        else:
            return jsonify({"error": "Proyecto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/proyectos", methods=["POST"])
def crear_proyecto():
    try:
        data = request.json
        if "titulo" not in data:
            return jsonify({"error": "Falta titulo del proyecto"}), 400
            
        conn = conexionDB()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO proyectos (titulo, descripcion)
            VALUES (?, ?)
        """, (data["titulo"], data.get("descripcion", "")))
        
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Proyecto creado", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/proyectos/<int:id>", methods=["PUT"])
def actualizar_proyecto(id):
    try:
        data = request.json
        conn = conexionDB()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM proyectos WHERE id = ?", (id,))
        fila = cursor.fetchone()
        
        if not fila:
            conn.close()
            return jsonify({"error": "Proyecto no encontrado"}), 404
            
        titulo = data.get("titulo", fila[1])
        descripcion = data.get("descripcion", fila[2])

        cursor.execute("""
            UPDATE proyectos 
            SET titulo = ?, descripcion = ?
            WHERE id = ?
        """, (titulo, descripcion, id))
        
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Proyecto actualizado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/proyectos/<int:id>", methods=["DELETE"])
def eliminar_proyecto(id):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM proyectos WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Proyecto eliminado"}), 200
    except sqlite3.IntegrityError:
         return jsonify({"error": "No se puede eliminar el proyecto porque tiene tareas asociadas"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# ENDPOINTS PARA TAREAS (Entidad 2)
# ==========================================

@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.nombre, t.estado, t.proyecto_id, p.titulo 
            FROM tareas t
            LEFT JOIN proyectos p ON t.proyecto_id = p.id
        """)
        datos = cursor.fetchall()
        
        tareas = []
        for fila in datos:
            tareas.append({
                "id": fila[0],
                "nombre": fila[1],
                "estado": fila[2],
                "proyecto_id": fila[3],
                "proyecto_titulo": fila[4]
            })
        conn.close()
        return jsonify(tareas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tareas/<int:id>", methods=["GET"])
def obtener_tarea(id):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.nombre, t.estado, t.proyecto_id, p.titulo 
            FROM tareas t
            LEFT JOIN proyectos p ON t.proyecto_id = p.id
            WHERE t.id = ?
        """, (id,))
        fila = cursor.fetchone()
        conn.close()
        
        if fila:
            tarea = {
                "id": fila[0],
                "nombre": fila[1],
                "estado": fila[2],
                "proyecto_id": fila[3],
                "proyecto_titulo": fila[4]
            }
            return jsonify(tarea), 200
        else:
            return jsonify({"error": "Tarea no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tareas", methods=["POST"])
def crear_tarea():
    try:
        data = request.json
        if "nombre" not in data: return jsonify({"error": "Falta nombre"}), 400
        if "proyecto_id" not in data: return jsonify({"error": "Falta proyecto_id"}), 400
            
        conn = conexionDB()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM proyectos WHERE id = ?", (data["proyecto_id"],))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "El proyecto no existe"}), 400
        
        cursor.execute("""
            INSERT INTO tareas (nombre, estado, proyecto_id)
            VALUES (?, ?, ?)
        """, (data["nombre"], data.get("estado", "Pendiente"), data["proyecto_id"]))
        
        new_id = cursor.lastrowid
        conn.commit() 
        conn.close()
        return jsonify({"mensaje": "Tarea insertada", "id": new_id}), 201
    except Exception as e: 
        return jsonify({"error": str(e)}), 500

@app.route("/tareas/<int:id>", methods=["PUT"])
def actualizar_tarea(id):
    try:
        data = request.json
        conn = conexionDB()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tareas WHERE id = ?", (id,))
        fila = cursor.fetchone()
        
        if not fila:
            conn.close()
            return jsonify({"error": "Tarea no encontrada"}), 404
            
        nombre = data.get("nombre", fila[1])
        estado = data.get("estado", fila[2])
        proyecto_id = data.get("proyecto_id", fila[3])

        if "proyecto_id" in data:
            cursor.execute("SELECT id FROM proyectos WHERE id = ?", (proyecto_id,))
            if not cursor.fetchone():
                conn.close()
                return jsonify({"error": "El proyecto no existe"}), 400

        cursor.execute("""
            UPDATE tareas 
            SET nombre = ?, estado = ?, proyecto_id = ?
            WHERE id = ?
        """, (nombre, estado, proyecto_id, id))
        
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Tarea actualizada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tareas/<int:id>", methods=["DELETE"])
def eliminar_tarea(id):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Tarea eliminada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# FRONTEND
# ==========================================
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    inicializar_db() 
    app.run(debug=True, port=5000)
