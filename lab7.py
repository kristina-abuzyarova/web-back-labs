from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import copy

lab7 = Blueprint('lab7', __name__)

current_id = 5

films = [
    {
        "id": 0,
        "title": "Midnight Express",
        "title_ru": "Полуночный экспресс",
        "year": "2023",
        "description": "Молодой гонщик-изгой участвует в запрещённых ночных гонках по улицам Токио, пытаясь доказать своё превосходство и выиграть легендарный приз. Его главным соперником оказывается загадочный гонщик в маске, чья личность скрыта за тайной."
    },
    {
        "id": 1,
        "title": "Velocity Dreams",
        "title_ru": "Мечты о скорости",
        "year": "2024",
        "description": "Гонщица-новичок бросает вызов патриархальному миру профессиональных автогонок. Преодолевая предрассудки и сомнения, она строит собственный гоночный автомобиль и готовится к участию в престижном чемпионате, где её ждёт противостояние с ветеранами трассы."
    },
    {
        "id": 2,
        "title": "Neon Circuits",
        "title_ru": "Неоновые трассы",
        "year": "2025",
        "description": "В киберпанк-будущем гонки на антигравитационных автомобилях стали главным спортивным событием. Молодой пилот, выступающий под псевдонимом 'Феникс', раскрывает коррупционный скандал в лиге, рискуя своей карьерой и жизнью ради честных соревнований."
    },
    {
        "id": 3,
        "title": "Dust & Glory",
        "title_ru": "Пыль и слава",
        "year": "2022",
        "description": "История команды механиков из маленького гаража, которые решают принять участие в легендарном ралли 'Дакар'. Не имея финансирования и опыта, они модифицируют старый внедорожник и отправляются в самое экстремальное путешествие своей жизни через пустыни Африки."
    },
    {
        "id": 4,
        "title": "The Last Lap",
        "title_ru": "Последний круг",
        "year": "2023",
        "description": "Ветеран гонок, находящийся на грани завершения карьеры, получает шанс на финальный заезд в легендарном гонке '24 часа Ле-Мана'. Ему предстоит не только побороться за победу, но и передать опыт молодому напарнику, становясь для него наставником и другом."
    }
]

def validate_film_data(film_data):
    errors = {}
    
    title_ru = film_data.get('title_ru', '').strip()
    if not title_ru:
        errors['title_ru'] = 'Русское название обязательно'
    
    title = film_data.get('title', '').strip()
    if not title and not title_ru:
        errors['title'] = 'Название на оригинальном языке обязательно, если русское название пустое'
    
    year_str = film_data.get('year', '')
    try:
        year = int(year_str)
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть от 1895 до {current_year}'
    except (ValueError, TypeError):
        errors['year'] = 'Год должен быть числом'
    
    description = film_data.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание обязательно'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    
    return errors

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    """Получить все фильмы"""
    return jsonify({"films": films})

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_films_by_id(id):
    """Получить фильм по ID"""
    film = next((f for f in films if f["id"] == id), None)
    
    if film is None:
        return jsonify({
            "success": False,
            "error": "Фильм не найден"
        }), 404
    
    return jsonify({
        "success": True,
        "film": film
    })

def validate_film_data(film_data):
    """Валидация данных фильма"""
    errors = {}
    
    if not film_data.get('title_ru', '').strip():
        errors['title_ru'] = 'Название на русском обязательно'
    
    if not film_data.get('year', '').strip():
        errors['year'] = 'Год выпуска обязателен'
    
    if not film_data.get('description', '').strip():
        errors['description'] = 'Описание обязательно'

    if film_data.get('year') and not film_data['year'].isdigit():
        errors['year'] = 'Год должен быть числом'
    elif film_data.get('year'):
        year = int(film_data['year'])
        if year < 1888 or year > 2100:  
            errors['year'] = 'Некорректный год'
    
    return errors

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    """Удалить фильм по ID"""
    global films

    film_index = next((i for i, f in enumerate(films) if f["id"] == id), -1)
    
    if film_index == -1:
        return jsonify({
            "success": False,
            "error": "Фильм не найден"
        }), 404

    del films[film_index]
    
    return jsonify({
        "success": True,
        "message": "Фильм удален"
    }), 200

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    """Обновить фильм по ID"""
    global films

    film_index = next((i for i, f in enumerate(films) if f["id"] == id), -1)
    
    if film_index == -1:
        return jsonify({
            "success": False,
            "error": "Фильм не найден"
        }), 404
    
    film_data = request.get_json()
    
    if not film_data:
        return jsonify({
            "success": False,
            "errors": {"general": "Не предоставлены данные для обновления"}
        }), 400

    errors = validate_film_data(film_data)
    if errors:
        return jsonify(errors), 400
    
    title = film_data.get('title', '').strip()
    title_ru = film_data.get('title_ru', '').strip()
    if not title.strip() and title_ru.strip():
        film_data['title'] = title_ru

    errors = validate_film_data(film_data)
    if errors:
        return jsonify({
            "success": False,
            "errors": errors
        }), 400

    film_data['id'] = id

    films[film_index] = film_data
    
    return jsonify({
        "success": True,
        "film": film_data
    })

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    """Добавить новый фильм"""
    global films, current_id
    
    film_data = request.get_json()
    
    if not film_data:
        return jsonify({
            "success": False,
            "errors": {"general": "Не предоставлены данные фильма"}
        }), 400

    errors = validate_film_data(film_data)
    if errors:
        return jsonify(errors), 400
    
    title = film_data.get('title', '').strip()
    title_ru = film_data.get('title_ru', '').strip()
    if not title.strip() and title_ru.strip():
        film_data['title'] = title_ru

    errors = validate_film_data(film_data)
    if errors:
        return jsonify({
            "success": False,
            "errors": errors
        }), 400
 
    if not film_data.get('title', '').strip():
        film_data['title'] = film_data['title_ru']

    film_data['id'] = current_id
    current_id += 1

    films.append(film_data)
    
    return jsonify({
        "success": True,
        "film": film_data
    }), 201