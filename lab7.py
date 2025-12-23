from flask import Blueprint, render_template, jsonify, abort, request

lab7_bp = Blueprint('lab7_bp', __name__, template_folder='templates')

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

@lab7_bp.route('/')
def lab7_index():
    return render_template('lab7/index.html', films=films_data)

@lab7_bp.route('/rest-api/films/')
def get_all_films():
    return jsonify({
        "success": True,
        "count": len(films_data),
        "films": films_data
    })

@lab7_bp.route('/rest-api/films/<int:film_id>')
def get_film_by_id(film_id):
    if 0 <= film_id < len(films_data):
        return jsonify({
            "success": True,
            "film": films_data[film_id]
        })
    abort(404, description=f"Фильм с ID {film_id} не найден. Доступные ID: 0-{len(films_data)-1}")

@lab7_bp.route('/rest-api/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    if film_id < 0 or film_id >= len(films_data):
        return jsonify({"error": "Фильм не найден"}), 404

    deleted_film = films_data.pop(film_id)

    for i, film in enumerate(films_data):
        film["id"] = i
    
    return jsonify({
        "success": True,
        "message": f"Фильм '{deleted_film['title_ru']}' удален",
        "remaining": len(films_data)
    }), 200

@lab7_bp.route('/rest-api/films/<int:film_id>', methods=['PUT'])
def update_film(film_id):
    if film_id < 0 or film_id >= len(films_data):
        return jsonify({"error": "Фильм не найден"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Нет данных для обновления"}), 400

    films_data[film_id].update({
        "title": data.get("title", films_data[film_id]["title"]),
        "title_ru": data.get("title_ru", films_data[film_id]["title_ru"]),
        "year": data.get("year", films_data[film_id]["year"]),
        "description": data.get("description", films_data[film_id]["description"])
    })
    
    return jsonify({
        "success": True,
        "message": f"Фильм обновлен",
        "film": films_data[film_id]
    })