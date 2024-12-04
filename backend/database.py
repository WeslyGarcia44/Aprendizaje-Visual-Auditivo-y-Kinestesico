import sqlite3

DATABASE = 'backend/learning_styles.db'

def connect_db():
    """Conecta a la base de datos SQLite."""
    return sqlite3.connect(DATABASE)

def init_db():
    """Inicializa las tablas de la base de datos."""
    with connect_db() as conn:
        cursor = conn.cursor()
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # Tabla de resultados del test
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                visual_score INTEGER DEFAULT 0,
                auditory_score INTEGER DEFAULT 0,
                reading_writing_score INTEGER DEFAULT 0,
                kinesthetic_score INTEGER DEFAULT 0,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        # Tabla de ejercicios (para kinestésico y tiempo)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                exercise TEXT NOT NULL,
                time_taken TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()

def add_user(name, email, password):
    """Agrega un nuevo usuario a la base de datos."""
    with connect_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise Exception("El correo ya está registrado.")

def authenticate_user(email, password):
    """Autentica a un usuario y devuelve sus datos si las credenciales son correctas."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        if user:
            return {'id': user[0], 'name': user[1]}
        return None

def save_score(user_id, visual_score, auditory_score, reading_writing_score, kinesthetic_score):
    """Guarda los puntajes del test de un usuario."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO results (user_id, visual_score, auditory_score, reading_writing_score, kinesthetic_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, visual_score, auditory_score, reading_writing_score, kinesthetic_score))
        conn.commit()

def get_results_by_user_id(user_id):
    """Obtiene los resultados de un usuario dado su ID."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT visual_score, auditory_score, reading_writing_score, kinesthetic_score, date
            FROM results
            WHERE user_id = ?
        ''', (user_id,))
        return [{'visualScore': row[0], 'auditoryScore': row[1], 'readingWritingScore': row[2], 'kinestheticScore': row[3], 'date': row[4]} for row in cursor.fetchall()]

def get_users():
    """Devuelve todos los usuarios registrados."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email FROM users')
        return cursor.fetchall()

def save_time(user_id, exercise, time_taken):
    """Guarda el tiempo tomado por el usuario en un ejercicio."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO exercises (user_id, exercise, time_taken)
            VALUES (?, ?, ?)
        ''', (user_id, exercise, time_taken))
        conn.commit()
