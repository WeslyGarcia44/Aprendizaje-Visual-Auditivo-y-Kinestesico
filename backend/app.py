print("Iniciando el script app.py...")  # Verificación inicial del script

import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

# Asegurar que el directorio raíz del proyecto está en sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

import backend.database as database  # Importar correctamente desde backend

print("Importaciones completadas.")  # Verificación de importaciones

app = Flask(__name__)
print("Aplicación Flask creada.")  # Verificación de instancia de Flask

CORS(app)
print("CORS configurado.")  # Verificación de configuración CORS

# Inicializar la base de datos al inicio del servidor
with app.app_context():
    print("Inicializando la base de datos...")  # Mensaje de verificación
    database.init_db()
    print("Base de datos inicializada correctamente.")  # Confirmación

# Ruta de prueba para verificar que el servidor está funcionando
@app.route('/', methods=['GET'])
def home():
    print("Accediendo a la ruta raíz /")  # Verificación al acceder a /
    return jsonify({"message": "Servidor Flask funcionando correctamente"})

# Endpoint para registrar un nuevo estudiante
@app.route('/api/register', methods=['POST'])
def register():
    print("Intentando registrar un nuevo estudiante...")  # Mensaje de depuración
    data = request.json
    print("Datos recibidos:", data)  # Mostrar datos recibidos

    if not data.get('name') or not data.get('email') or not data.get('password'):
        print("Error: Datos incompletos para el registro.")
        return jsonify({"error": "Faltan datos: nombre, correo o contraseña"}), 400

    try:
        user_id = database.add_user(data['name'], data['email'], data['password'])
        print(f"Estudiante registrado con éxito, ID: {user_id}")
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        print("Error al registrar usuario:", str(e))
        return jsonify({"error": "No se pudo registrar el usuario"}), 500

# Endpoint para iniciar sesión
@app.route('/api/login', methods=['POST'])
def login():
    print("Intentando iniciar sesión...")
    data = request.json
    print("Credenciales recibidas:", data)

    if not data.get('email') or not data.get('password'):
        print("Error: Credenciales incompletas.")
        return jsonify({"error": "Faltan datos: correo o contraseña"}), 400

    user = database.authenticate_user(data['email'], data['password'])
    if user:
        print(f"Usuario autenticado: {user}")
        return jsonify({"message": "Inicio de sesión exitoso", "userId": user['id'], "userName": user['name']}), 200
    else:
        print("Error: Credenciales incorrectas.")
        return jsonify({"error": "Correo o contraseña incorrectos"}), 401

# Endpoint para obtener resultados del usuario
@app.route('/api/user-results', methods=['GET'])
def user_results():
    user_id = request.args.get('userId')

    if not user_id:
        print("Error: userId no proporcionado.")
        return jsonify({"error": "Se requiere userId"}), 400

    results = database.get_results_by_user_id(user_id)
    print(f"Resultados obtenidos para el usuario {user_id}:", results)
    return jsonify(results)

# Endpoint para enviar puntuaciones
@app.route('/api/submit-score', methods=['POST'])
def submit_score():
    data = request.json
    print("Datos recibidos para puntuación:", data)

    if not data.get('studentId'):
        print("Error: studentId no proporcionado.")
        return jsonify({"error": "Se requiere studentId"}), 400

    try:
        database.save_score(data['studentId'], data['visualScore'], data['auditoryScore'], data['readingWritingScore'], data['kinestheticScore'])
        print("Puntuación registrada correctamente.")
        return jsonify({"message": "Puntuación registrada correctamente"}), 200
    except Exception as e:
        print("Error al registrar puntuación:", str(e))
        return jsonify({"error": "Error al registrar puntuación"}), 500

if __name__ == '__main__':
    print("Ejecutando el servidor Flask...")  # Mensaje antes de iniciar el servidor
    app.run(debug=True)

@app.route('/api/save-time', methods=['POST'])
def save_time():
    data = request.json
    user_id = data.get('userId')
    exercise = data.get('exercise')
    time = data.get('time')

    if not user_id or not exercise or not time:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        database.save_time(user_id, exercise, time)
        return jsonify({"message": "Tiempo guardado exitosamente"}), 200
    except Exception as e:
        print("Error al guardar el tiempo:", e)
        return jsonify({"error": "Error al guardar el tiempo"}), 500
