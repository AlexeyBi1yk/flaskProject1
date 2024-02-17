from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_

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
    sub_type = db.Column(db.String(50))
    sub_expiry = db.Column(db.Date)
    phone_number = db.Column(db.String(15))

    @classmethod
    def create(cls, first_name, last_name, birth_date, gender, sub_type, sub_expiry):
        client = cls(first_name=first_name, last_name=last_name, birth_date=birth_date, gender=gender,
                     sub_type=sub_type, sub_expiry=sub_expiry)
        db.session.add(client)
        db.session.commit()
        return client


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

# Маршрут для отображения клиентов
@app.route('/clients')
def clients():
    return render_template('clients.html')

@app.route('/clients_list')
def clients_list():
    clients = Clients.query.all()  # Извлекаем всех клиентов из базы данных
    return render_template('clients_list.html', clients=clients)

# Маршрут для отображения оборудования
@app.route('/equipment')
def equipment():
    equipment = Equipment.query.all()  # Извлекаем всё оборудование из базы данных
    return render_template('equipment.html', equipment=equipment)

# Маршрут для отображения абонементов
@app.route('/abonements')
def abonements():
    abonements = Abonements.query.all()  # Извлекаем все абонементы из базы данных
    return render_template('abonements.html', abonements=abonements)

# Маршрут для отображения залов
@app.route('/halls')
def halls():
    halls = Halls.query.all()  # Извлекаем все залы из базы данных
    return render_template('halls.html', halls=halls)

# Маршрут для отображения тренеров
@app.route('/trainers')
def trainers():
    trainers = Trainers.query.all()  # Извлекаем всех тренеров из базы данных
    return render_template('trainers.html', trainers=trainers)

# Маршрут для отображения тренировок
@app.route('/workouts')
def workouts():
    workouts = Workouts.query.all()  # Извлекаем все тренировки из базы данных
    return render_template('workouts.html', workouts=workouts)

@app.route('/search')
def search():
    query = request.args.get('query')

    if query:
        # Используем метод filter() для фильтрации записей по нескольким полям с помощью логического оператора ИЛИ (OR)
        search_results = Clients.query.filter(
            or_(
                Clients.first_name.ilike(f'%{query}%'),  # Ищем по имени (игнорируя регистр)
                Clients.last_name.ilike(f'%{query}%'),   # Ищем по фамилии (игнорируя регистр)
                Clients.sub_type.ilike(f'%{query}%'),    # Ищем по типу подписки (игнорируя регистр)
                Clients.phone_number.ilike(f'%{query}%') # Ищем по номеру телефона (игнорируя регистр)
            )
        ).all()
    else:
        search_results = []

    return render_template('client_search.html', search_results=search_results, query=query)




@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        # Получение данных из формы
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d')
        gender = request.form['gender']
        sub_type = request.form['sub_type']
        sub_expiry = datetime.strptime(request.form['sub_expiry'], '%Y-%m-%d')

        # Создание нового клиента
        client = Clients(first_name=first_name, last_name=last_name, birth_date=birth_date, gender=gender, sub_type=sub_type, sub_expiry=sub_expiry)
        db.session.add(client)
        db.session.commit()

        return redirect(url_for('index'))  # Перенаправление на главную страницу

    return render_template('add_client.html')



if __name__ == '__main__':
    app.run(debug=True)
