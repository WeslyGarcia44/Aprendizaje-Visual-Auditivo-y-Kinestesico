from flask_sqlalchemy import SQLAlchemy

# Inicializamos SQLAlchemy
db = SQLAlchemy()

# Modelo para la tabla 'students'
class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    learning_style = db.Column(db.String(50), nullable=True)
    score = db.Column(db.Integer, nullable=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

# Modelo para la tabla 'exercises'
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)

    def __init__(self, student_id, question, answer, correct_answer):
        self.student_id = student_id
        self.question = question
        self.answer = answer
        self.correct_answer = correct_answer
