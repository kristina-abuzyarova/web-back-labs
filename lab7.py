from flask import Blueprint, render_template, request, jsonify, abort

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films_data = [
    {
        "id": 0,
        "title": "Ferrari vs Lamborghini",
        "title_ru": "Феррари против Ламборгини",
        "year": "2023",
        "description": "История соперничества двух легендарных автомобильных брендов - Феррари и Ламборгини. Фильм рассказывает о страсти, инновациях и бескомпромиссной конкуренции в мире суперкаров."
    },
    {
        "id": 1,
        "title": "Ford v Ferrari",
        "title_ru": "Ford против Ferrari",
        "year": "2019",
        "description": "Американский автомобильный конструктор Кэрролл Шелби и британский гонщик Кен Майлз объединяются, чтобы построить революционный автомобиль для Ford и победить доминирующую команду Ferrari на 24 часах Ле-Мана в 1966 году."
    },
    {
        "id": 2,
        "title": "Rush",
        "title_ru": "Гонка",
        "year": "2013",
        "description": "История эпического соперничества двух гонщиков Формулы-1 - британца Джеймса Ханта и австрийца Ники Лауды - во время сезона 1976 года."
    },
    {
        "id": 3,
        "title": "The Iron Giant",
        "title_ru": "Железный гигант",
        "year": "1999",
        "description": "В разгар холодной войны молодой мальчик по имени Хогарт Хьюз находит гигантского металлического робота, упавшего с неба. Между ними завязывается необычная дружба."
    },
    {
        "id": 4,
        "title": "Real Steel",
        "title_ru": "Железный кулак",
        "year": "2011",
        "description": "В недалёком будущем, где боксёрские поединки проводятся между огромными роботами, бывший боксёр Чарли Кентон и его сын Макс находят старого робота-боксёра, который может стать чемпионом."
    },
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_films_by_id(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404

    return jsonify(films[id])


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404

    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404

    film = request.get_json()
    film[id] = film
    return films[id]

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film_data = request.get_json()
    
    if not film_data:
        return jsonify({"error": "Не предоставлены данные фильма"}), 400
    
    films.append(film_data)
    
    new_id = len(films) - 1
    return jsonify({"id": new_id}), 201