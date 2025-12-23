from flask import Blueprint, render_template, request, jsonify, abort

lab7_bp = Blueprint('lab7', __name__)

@lab7_bp.route('/')
def main():
    return render_template('lab7/index.html')

films = [
    {
        "id": 0,
        "title": "Midnight Express",
        "title_ru": "Полуночный экспресс",
        "year": "2023",
        "description": "Молодой гонщик-изгой участвует в запрещённых ночных гонках по улицам Токио, \
            пытаясь доказать своё превосходство и выиграть легендарный приз. Его главным соперником \
            оказывается загадочный гонщик в маске, чья личность скрыта за тайной."
    },
    {
        "id": 1,
        "title": "Velocity Dreams",
        "title_ru": "Мечты о скорости",
        "year": "2024",
        "description": "Гонщица-новичок бросает вызов патриархальному миру профессиональных автогонок. \
            Преодолевая предрассудки и сомнения, она строит собственный гоночный автомобиль и готовится \
            к участию в престижном чемпионате, где её ждёт противостояние с ветеранами трассы."
    },
    {
        "id": 2,
        "title": "Neon Circuits",
        "title_ru": "Неоновые трассы",
        "year": "2025",
        "description": "В киберпанк-будущем гонки на антигравитационных автомобилях стали главным \
            спортивным событием. Молодой пилот, выступающий под псевдонимом 'Феникс', раскрывает \
            коррупционный скандал в лиге, рискуя своей карьерой и жизнью ради честных соревнований."
    },
    {
        "id": 3,
        "title": "Dust & Glory",
        "title_ru": "Пыль и слава",
        "year": "2022",
        "description": "История команды механиков из маленького гаража, которые решают принять участие \
            в легендарном ралли 'Дакар'. Не имея финансирования и опыта, они модифицируют старый внедорожник \
            и отправляются в самое экстремальное путешествие своей жизни через пустыни Африки."
    },
    {
        "id": 4,
        "title": "The Last Lap",
        "title_ru": "Последний круг",
        "year": "2023",
        "description": "Ветеран гонок, находящийся на грани завершения карьеры, получает шанс на финальный \
            заезд в легендарной гонке '24 часа Ле-Мана'. Ему предстоит не только побороться за победу, \
            но и передать опыт молодому напарнику, становясь для него наставником и другом."
    }
]

@lab7_bp.route('/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify({
        "success": True,
        "count": len(films),
        "films": films
    })

@lab7_bp.route('/rest-api/films/<int:id>', methods=['GET'])
def get_films_by_id(id):
    for film in films:
        if film["id"] == id:
            return jsonify({
                "success": True,
                "film": film
            })
    
    return jsonify({
        "success": False,
        "error": f"Фильм с ID {id} не найден"
    }), 404

@lab7_bp.route('/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    for i, film in enumerate(films):
        if film["id"] == id:
            del films[i]
            return '', 204
    
    return jsonify({
        "success": False,
        "error": f"Фильм с ID {id} не найден"
    }), 404

@lab7_bp.route('/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    for i, film in enumerate(films):
        if film["id"] == id:
            film_data = request.get_json()
            
            if not film_data:
                return jsonify({
                    "success": False,
                    "error": "Не предоставлены данные для обновления"
                }), 400
            
            film_data["id"] = id  
            films[i] = film_data
            
            return jsonify({
                "success": True,
                "film": film_data
            })
    
    return jsonify({
        "success": False,
        "error": f"Фильм с ID {id} не найден"
    }), 404

@lab7_bp.route('/rest-api/films/', methods=['POST'])
def add_film():
    film_data = request.get_json()
    
    if not film_data:
        return jsonify({
            "success": False,
            "error": "Не предоставлены данные фильма"
        }), 400
    
    new_id = max([film["id"] for film in films], default=-1) + 1
    film_data["id"] = new_id
    films.append(film_data)
    
    return jsonify({
        "success": True,
        "id": new_id,
        "message": f"Фильм успешно добавлен с ID {new_id}"
    }), 201