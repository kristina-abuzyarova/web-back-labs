from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import sqlite3
from contextlib import closing
import os

lab7 = Blueprint('lab7', __name__)

def init_db():
    print("=" * 50)
    print("ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ FILMS.DB")
    print(f"Текущая директория: {os.getcwd()}")
    print(f"Файл films.db существует: {os.path.exists('films.db')}")
    
    with closing(sqlite3.connect('films.db')) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS films (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,          -- Оригинальное название
                title_ru TEXT NOT NULL,       -- Русское название  
                year INTEGER NOT NULL,        -- Год выпуска
                description TEXT NOT NULL     -- Описание фильма
            )
        ''')

        cursor.execute("SELECT COUNT(*) FROM films")
        count = cursor.fetchone()[0]
        print(f"Количество фильмов в базе: {count}")
        
        if count == 0:
            print("Добавляем начальные фильмы...")
            initial_films = [
                ("Midnight Express", "Полуночный экспресс", 2023, "Молодой гонщик-изгой участвует в запрещённых ночных гонках по улицам Токио, пытаясь доказать своё превосходство и выиграть легендарный приз. Его главным соперником оказывается загадочный гонщик в маске, чья личность скрыта за тайной."),
                ("Velocity Dreams", "Мечты о скорости", 2024, "Гонщица-новичок бросает вызов патриархальному миру профессиональных автогонок. Преодолевая предрассудки и сомнения, она строит собственный гоночный автомобиль и готовится к участию в престижном чемпионате, где её ждёт противостояние с ветеранами трассы."),
                ("Neon Circuits", "Неоновые трассы", 2025, "В киберпанк-будущем гонки на антигравитационных автомобилях стали главным спортивным событием. Молодой пилот, выступающий под псевдонимом 'Феникс', раскрывает коррупционный скандал в лиге, рискуя своей карьерой и жизнью ради честных соревнований."),
                ("Dust & Glory", "Пыль и слава", 2022, "История команды механиков из маленького гаража, которые решают принять участие в легендарном ралли 'Дакар'. Не имея финансирования и опыта, они модифицируют старый внедорожник и отправляются в самое экстремальное путешествие своей жизни через пустыни Африки."),
                ("The Last Lap", "Последний круг", 2023, "Ветеран гонок, находящийся на грани завершения карьеры, получает шанс на финальный заезд в легендарной гонке '24 часа Ле-Мана'. Ему предстоит не только побороться за победу, но и передать опыт молодому напарнику, становясь для него наставником и другом.")
            ]
            cursor.executemany(
                "INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)",
                initial_films
            )
            print(f"Добавлено {len(initial_films)} фильмов")
        else:
            print("Фильмы уже существуют в базе данных")

        cursor.execute("SELECT id, title, title_ru, year FROM films")
        films = cursor.fetchall()
        print("Фильмы в базе данных:")
        for film in films:
            print(f"  ID: {film[0]}, Англ: '{film[1]}', Рус: '{film[2]}', Год: {film[3]}")
        
        conn.commit()
    print("=" * 50)

init_db()

def get_db_connection():
    conn = sqlite3.connect('films.db')
    conn.row_factory = sqlite3.Row 
    return conn

def validate_film_data(film_data):
    errors = {}

    title_ru = film_data.get('title_ru', '').strip()
    if not title_ru:
        errors['title_ru'] = 'Русское название обязательно'

    year_str = film_data.get('year', '')
    try:
        year = int(year_str)
        current_year = datetime.now().year
        if year < 1888 or year > current_year + 1:  
            errors['year'] = f'Год должен быть от 1888 до {current_year + 1}'
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
    print("=" * 50)
    print("ЗАПРОС НА ПОЛУЧЕНИЕ ВСЕХ ФИЛЬМОВ")
    
    conn = get_db_connection()
    films = conn.execute('SELECT * FROM films ORDER BY year DESC').fetchall()
    conn.close()
    
    print(f"Найдено фильмов в базе: {len(films)}")

    films_list = []
    for film in films:
        films_list.append({
            'id': film['id'],
            'title': film['title'],
            'title_ru': film['title_ru'],
            'year': film['year'],
            'description': film['description']
        })
        print(f"  Фильм: ID={film['id']}, '{film['title']}' / '{film['title_ru']}', год={film['year']}")

    response = jsonify({"films": films_list})  
    print(f"Отправляемый JSON: {response.get_json()}")
    print("=" * 50)
    return response

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_films_by_id(id):
    conn = get_db_connection()
    film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if film is None:
        return jsonify({
            "success": False,
            "error": "Фильм не найден"
        }), 404

    return jsonify({
        "success": True,
        "film": {
            'id': film['id'],
            'title': film['title'],
            'title_ru': film['title_ru'],
            'year': film['year'],
            'description': film['description']
        }
    })

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn = get_db_connection()

    film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    if film is None:
        conn.close()
        return jsonify({
            "success": False,
            "error": "Фильм не найден"
        }), 404

    conn.execute('DELETE FROM films WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({
        "success": True,
        "message": "Фильм успешно удален"
    }), 200

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn = get_db_connection()

    film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    if film is None:
        conn.close()
        return jsonify({
            "success": False,
            "error": "Фильм не найден"
        }), 404
    
    film_data = request.get_json()
    
    if not film_data:
        conn.close()
        return jsonify({
            "success": False,
            "error": "Не предоставлены данные для обновления"
        }), 400

    errors = validate_film_data(film_data)
    if errors:
        conn.close()
        return jsonify({
            "success": False,
            "errors": errors
        }), 400

    title = film_data.get('title', '').strip()
    title_ru = film_data.get('title_ru', '').strip()
    if not title and title_ru:
        film_data['title'] = title_ru

    conn.execute(
        'UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?',
        (film_data['title'], film_data['title_ru'], film_data['year'], film_data['description'], id)
    )
    conn.commit()

    updated_film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    return jsonify({
        "success": True,
        "film": {
            'id': updated_film['id'],
            'title': updated_film['title'],
            'title_ru': updated_film['title_ru'],
            'year': updated_film['year'],
            'description': updated_film['description']
        }
    })

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film_data = request.get_json()
    
    if not film_data:
        return jsonify({
            "success": False,
            "error": "Не предоставлены данные фильма"
        }), 400

    errors = validate_film_data(film_data)
    if errors:
        return jsonify({
            "success": False,
            "errors": errors
        }), 400

    title = film_data.get('title', '').strip()
    title_ru = film_data.get('title_ru', '').strip()
    if not title and title_ru:
        film_data['title'] = title_ru
        
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)',
        (film_data['title'], film_data['title_ru'], film_data['year'], film_data['description'])
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "id": new_id,
        "message": "Фильм успешно добавлен"
    }), 201