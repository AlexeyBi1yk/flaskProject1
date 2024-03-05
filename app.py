from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_
from sqlalchemy import func

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/gym'
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
                     sub_type=sub_type, sub_expiry=sub_expiry, phone_number=phone_number)
        db.session.add(client)
        db.session.commit()
        return client


class GroupSchedule(db.Model):
    __tablename__ = 'group_schedule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trainer_name = db.Column(db.String(50))
    activity_type = db.Column(db.String(50))
    activity_name = db.Column(db.String(100))
    date_time = db.Column(db.DateTime)
    hall = db.Column(db.String(50))

    @classmethod
    def create(cls, trainer_name, activity_type, activity_name, date_time, hall):
        workout = cls(trainer_name=trainer_name, activity_type=activity_type,
                      activity_name=activity_name, date_time=date_time, hall=hall)
        db.session.add(workout)
        db.session.commit()
        return workout


class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    in_working = db.Column(db.Boolean)
    repair = db.Column(db.Boolean)


class DutyTrainer(db.Model):
    __tablename__ = 'duty_trainer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trainer_id = db.Column(db.Integer)
    duty_date = db.Column(db.Date)


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


class TrainersDutyList(db.Model):
    __tablename__ = 'trainers_duty_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trainer_id = db.Column(db.Integer)
    duty_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)


class ClientSchedule(db.Model):
    __tablename__ = 'client_schedule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_name = db.Column(db.String(50))
    trainer_name = db.Column(db.String(50))
    activity_type = db.Column(db.String(50))
    activity_name = db.Column(db.String(100))
    date_time = db.Column(db.DateTime)
    hall = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))

    @classmethod
    def create(cls, client_name, trainer_name, activity_type, activity_name, date_time, hall, phone_number):
        workout = cls(client_name=client_name, trainer_name=trainer_name, activity_type=activity_type,
                      activity_name=activity_name, date_time=date_time, hall=hall, phone_number=phone_number)
        db.session.add(workout)
        db.session.commit()
        return workout

    @classmethod
    def edit(cls, schedule_id, **kwargs):
        schedule = cls.query.get(schedule_id)
        if schedule:
            for attr, value in kwargs.items():
                setattr(schedule, attr, value)
            db.session.commit()
            return schedule
        return None

    @classmethod
    def delete(cls, schedule_id):
        schedule = cls.query.get(schedule_id)
        if schedule:
            db.session.delete(schedule)
            db.session.commit()
            return True
        return False


# Основной маршрут - главная страница
@app.route('/')
def index():
    # Получаем количество клиентов из базы данных
    clients_count = Clients.query.count()
    abonements_count = Abonements.query.all()
    return render_template('index.html', clients_count=clients_count, abonements_count=abonements_count)

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')


@app.route('/group_schedule')
def group_schedule():
    group_workouts = GroupSchedule.query.all()
    return render_template('group_schedule.html', group_workouts=group_workouts)


@app.route('/add_in_group_schedule', methods=['GET', 'POST'])
def add_in_group_schedule():
    if request.method == 'POST':
        # Получение данных из формы
        trainer_name = request.form['trainer_name']
        activity_type = request.form['activity_type']
        activity_name = request.form['activity_name']
        date_time_iso = request.form['date_time']
        date_time = datetime.strptime(date_time_iso, '%Y-%m-%dT%H:%M')
        hall = request.form['hall']  # Получаем номер телефона из формы
        # Создание нового клиента
        group_schedule = GroupSchedule(trainer_name=trainer_name,
                                        activity_type=activity_type,
                                        activity_name=activity_name,
                                        date_time=date_time,
                                        hall=hall)
        db.session.add(group_schedule)
        db.session.commit()

        return redirect(url_for('index'))  # Перенаправление на главную страницу
    # Получение списка всех тренеров
    trainers = Trainers.query.all()
    halls = Halls.query.all()
    return render_template('add_in_group_schedule.html', trainers=trainers, halls=halls)


@app.route('/client_schedule')
def client_schedule():
    # Получаем параметры фильтрации из запроса
    trainer_name = request.args.get('trainer')
    date = request.args.get('date')
    # Инициализируем базовый запрос
    query = ClientSchedule.query

    # Применяем фильтры, если они указаны
    if trainer_name:
        query = query.filter(ClientSchedule.trainer_name == trainer_name)
    if date:
        query = query.filter(func.DATE(ClientSchedule.date_time) == date)

    # Получаем список тренировок в соответствии с фильтрами
    workouts = query.all()
    trainers = Trainers.query.all()
    return render_template('client_schedule.html', workouts=workouts, trainers=trainers)


@app.route('/add_in_client_schedule', methods=['GET', 'POST'])
def add_schedule():
    if request.method == 'POST':
        # Получение данных из формы
        client_name = request.form['client_name']
        trainer_name = request.form['trainer_name']
        activity_type = request.form['activity_type']
        activity_name = request.form['activity_name']
        date_time_iso = request.form['date_time']
        # date_time = datetime.strptime(request.form['date_time'], '%Y-%m-%d')
        # Преобразование строки времени из формата ISO в формат '%Y-%m-%d %H:%M'
        date_time = datetime.strptime(date_time_iso, '%Y-%m-%dT%H:%M')
        hall = request.form['hall']  # Получаем номер телефона из формы
        phone_number = request.form['phone_number']
        # Создание нового клиента
        client_schedule = GroupSchedule(client_name=client_name,
                                         trainer_name=trainer_name,
                                         activity_type=activity_type,
                                         activity_name=activity_name,
                                         date_time=date_time,
                                         hall=hall,
                                         phone_number=phone_number)
        db.session.add(client_schedule)
        db.session.commit()

        return redirect(url_for('index'))  # Перенаправление на главную страницу
    # Получение списка всех тренеров
    trainers = Trainers.query.all()
    halls = Halls.query.all()
    return render_template('add_in_client_schedule.html', trainers=trainers, halls=halls)


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


@app.route('/search')
def search():
    query = request.args.get('query')

    if query:
        # Используем метод filter() для фильтрации записей по нескольким полям с помощью логического оператора ИЛИ (OR)
        search_results = Clients.query.filter(
            or_(
                Clients.first_name.ilike(f'%{query}%'),  # Ищем по имени (игнорируя регистр)
                Clients.last_name.ilike(f'%{query}%'),  # Ищем по фамилии (игнорируя регистр)
                Clients.sub_type.ilike(f'%{query}%'),  # Ищем по типу подписки (игнорируя регистр)
                Clients.phone_number.ilike(f'%{query}%')  # Ищем по номеру телефона (игнорируя регистр)
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
        phone_number = request.form['phone_number']  # Получаем номер телефона из формы
        # Создание нового клиента
        client = Clients(first_name=first_name, last_name=last_name, birth_date=birth_date, gender=gender,
                         sub_type=sub_type, sub_expiry=sub_expiry,
                         phone_number=phone_number)  # Используем полученный номер телефона при создании клиента
        db.session.add(client)
        db.session.commit()

        return redirect(url_for('index'))  # Перенаправление на главную страницу

    return render_template('add_client.html')


# Определяем маршрут для редактирования клиента
@app.route('/edit_client/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    client = Clients.query.get_or_404(id)  # Получаем клиента из базы данных или возвращаем ошибку 404, если не найден

    if request.method == 'POST':
        # Обновляем данные клиента
        client.first_name = request.form['first_name']
        client.last_name = request.form['last_name']
        client.birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d')
        client.gender = request.form['gender']
        client.sub_type = request.form['sub_type']
        client.sub_expiry = datetime.strptime(request.form['sub_expiry'], '%Y-%m-%d')
        client.phone_number = request.form['phone_number']

        db.session.commit()  # Сохраняем изменения в базе данных

        return redirect(url_for('index'))  # Перенаправляем на главную страницу

    return render_template('edit_client.html', client=client)


if __name__ == '__main__':
    app.run(debug=True)
