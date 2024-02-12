from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/gym'  # Замените username, password и db_name на ваши данные
db = SQLAlchemy(app)

# Определяем модели данных
class Clients(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.Enum('Мужской', 'Женский'))

class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

class Abonements(db.Model):
    __tablename__ = 'abonements'
    id = db.Column(db.Integer, primary_key=True)
    abonement_type = db.Column(db.String(50))
    price = db.Column(db.Float)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

class Halls(db.Model):
    __tablename__ = 'halls'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    capacity = db.Column(db.Integer)

class Trainers(db.Model):
    __tablename__ = 'trainers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    specialization = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))

class Workouts(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    workout_type = db.Column(db.Enum('Групповая', 'Индивидуальная'))
    date_time = db.Column(db.DateTime)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'))  # Здесь была исправлена опечатка
    trainer = db.relationship('Trainers', backref='workouts')  # Исправлено на 'Trainers'


# Основной маршрут - главная страница
@app.route('/')
def index():
    clients = Clients.query.all()  # Извлекаем всех клиентов из базы данных
    print(clients)
    return render_template('index.html', clients=clients)  # Передаем список клиентов в шаблон

if __name__ == '__main__':
    app.run(debug=True)
