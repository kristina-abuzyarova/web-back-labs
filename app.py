from flask import Flask, url_for, request, render_template, jsonify
import os
import datetime
from dotenv import load_dotenv
from models import db, Office
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6

app = Flask(__name__)

app.secret_key = 'секретно-секретный секрет'
load_dotenv()

app.secret_key = 'your-secret-key-here'  
app.config['DB_TYPE'] = 'postgres' 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///offices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Регистрируем существующие blueprints
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)

# Пробуем зарегистрировать lab7, если есть
try:
    from lab7 import lab7 as lab7_bp
    app.register_blueprint(lab7_bp, url_prefix='/lab7')
    print("✓ Blueprint lab7 зарегистрирован")
except ImportError as e:
    print(f"⚠ lab7 не найден: {e}")

access_log = []

with app.app_context():
    db.create_all()

    if Office.query.count() == 0:
        offices_data = []
        for i in range(1, 11):
            offices_data.append(Office(
                number=i,
                tenant='',
                price=900 + i % 3 * 100
            ))
        
        db.session.add_all(offices_data)
        db.session.commit()
        print("База данных инициализирована с офисами")


# ========== ПРЯМЫЕ МАРШРУТЫ ДЛЯ LAB7 ==========
# (работают даже если lab7.py не существует)

@app.route('/lab7/')
def lab7_index():
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lab7 - REST API для фильмов</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: Arial, sans-serif; 
            line-height: 1.6; 
            background: #f4f4f4;
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 { 
            color: #2c3e50; 
            margin-bottom: 20px;
            text-align: center;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .api-info {
            margin-top: 30px;
            padding: 20px;
            background: #ecf0f1;
            border-radius: 5px;
        }
        h2 { color: #34495e; margin: 20px 0 15px 0; }
        ul { margin-left: 20px; margin-bottom: 15px; }
        li { margin-bottom: 8px; }
        a { 
            color: #2980b9; 
            text-decoration: none;
            font-weight: bold;
        }
        a:hover { color: #1a5276; text-decoration: underline; }
        .film-card {
            background: #fff;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #e74c3c;
        }
        .test-btn {
            text-align: center;
            margin: 20px 0;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }
        .btn:hover {
            background: #2980b9;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Lab7 - REST API для фильмов</h1>
        
        <div class="api-info">
            <h2>🎬 REST API Endpoints:</h2>
            <ul>
                <li><a href="/lab7/api/films/">GET /lab7/api/films/</a> - Все фильмы (JSON)</li>
                <li>GET /lab7/api/films/&lt;id&gt; - Конкретный фильм (id 0-4)</li>
            </ul>
            
            <h3>Примеры запросов:</h3>
            <ul>
                <li><a href="/lab7/api/films/0">Фильм 0 - Ferrari vs Lamborghini</a></li>
                <li><a href="/lab7/api/films/1">Фильм 1 - Ford v Ferrari</a></li>
                <li><a href="/lab7/api/films/2">Фильм 2 - Rush</a></li>
                <li><a href="/lab7/api/films/3">Фильм 3 - The Iron Giant</a></li>
                <li><a href="/lab7/api/films/4">Фильм 4 - Real Steel</a></li>
            </ul>
        </div>
        
        <div class="test-btn">
            <a href="/lab7/api/films/" class="btn">🧪 Протестировать API</a>
        </div>
        
        <footer style="margin-top: 40px; text-align: center; color: #7f8c8d;">
            <p><a href="/" style="color: #3498db;">← Вернуться на главную</a></p>
            <p>&copy; Lab7 - REST API демонстрация</p>
        </footer>
    </div>
</body>
</html>
'''

# API endpoints для lab7
films_db = [
    {
        "id": 0,
        "title": "Ferrari vs Lamborghini",
        "title_ru": "Феррари против Ламборгини",
        "year": "2023",
        "description": "История соперничества двух легендарных автомобильных брендов - Феррари и Ламборгини."
    },
    {
        "id": 1,
        "title": "Ford v Ferrari",
        "title_ru": "Ford против Ferrari",
        "year": "2019",
        "description": "Американский автомобильный конструктор Кэрролл Шелби и британский гонщик Кен Майлз объединяются."
    },
    {
        "id": 2,
        "title": "Rush",
        "title_ru": "Гонка",
        "year": "2013",
        "description": "История эпического соперничества двух гонщиков Формулы-1."
    },
    {
        "id": 3,
        "title": "The Iron Giant",
        "title_ru": "Железный гигант",
        "year": "1999",
        "description": "В разгар холодной войны молодой мальчик находит гигантского металлического робота."
    },
    {
        "id": 4,
        "title": "Real Steel",
        "title_ru": "Железный кулак",
        "year": "2011",
        "description": "В недалёком будущем боксёрские поединки проводятся между огромными роботами."
    },
]

@app.route('/lab7/api/films/')
def lab7_get_films():
    return jsonify({
        "success": True,
        "count": len(films_db),
        "films": films_db
    })

@app.route('/lab7/api/films/<int:film_id>')
def lab7_get_film(film_id):
    if 0 <= film_id < len(films_db):
        return jsonify({
            "success": True,
            "film": films_db[film_id]
        })
    return jsonify({
        "success": False,
        "error": f"Фильм с ID {film_id} не найден",
        "available_ids": list(range(len(films_db)))
    }), 404


# ========== ОСТАЛЬНОЙ КОД (без изменений) ==========

@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    access_time = datetime.datetime.now()
    requested_url = request.url

    log_entry = {
        'time': access_time,
        'ip': client_ip,
        'url': requested_url
    }
    access_log.append(log_entry)

    journal_html = ''
    for entry in reversed(access_log):  
        journal_html += f'''
        <div class="log-entry">
            [{entry["time"].strftime("%Y-%m-%d %H:%M:%S.%f")}, пользователь {entry["ip"]}] зашёл на адрес: {entry["url"]}
        </div>'''

    return f'''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <link rel="stylesheet" href="{url_for('static', filename='lab1/lab1.css')}">
        <style>
            body {{
                text-align: center;
                padding: 50px;
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                background-color: #f8f9fa;
            }}
            .error-container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }}
            h1 {{
                font-size: 80px;
                color: #ff6b6b;
                margin: 0;
                text-align: center;
            }}
            h2 {{
                color: #333;
                margin: 20px 0;
                text-align: center;
            }}
            .info-box {{
                background: #e9ecef;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .info-box p {{
                margin: 5px 0;
                color: #495057;
            }}
            .journal {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .journal h3 {{
                color: #333;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
                margin-top: 0;
            }}
            .log-entry {{
                padding: 10px;
                border-bottom: 1px solid #dee2e6;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }}
            .log-entry:last-child {{
                border-bottom: none;
            }}
            .log-time {{
                color: #6c757d;
            }}
            .log-user {{
                color: #007bff;
                font-weight: bold;
            }}
            .log-action {{
                color: #28a745;
            }}
            .home-link {{
                display: inline-block;
                padding: 12px 24px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin: 20px 0;
            }}
            .home-link:hover {{
                background: #5a67d8;
                text-decoration: none;
            }}
            img {{
                max-width: 300px;
                margin: 20px auto;
                display: block;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1>404</h1>
            <h2>Страница не найдена</h2>
            
            <img src="{url_for('static', filename='lab1/404.jpg')}" alt="Страница не найдена">
            
            <div class="info-box">
                <p><strong>Ваш IP-адрес:</strong> {client_ip}</p>
                <p><strong>Дата и время доступа:</strong> {access_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Запрошенный адрес:</strong> {requested_url}</p>
            </div>
            
            <p style="text-align: center; color: #666;">
                Запрашиваемая страница не существует или была перемещена.<br>
                Проверьте правильность адреса или вернитесь на главную страницу.
            </p>
            
            <div style="text-align: center;">
                <a href="/" class="home-link">← Вернуться на главную</a>
            </div>
        </div>
        
        <div class="journal">
            <h3>Журнал:</h3>
            {journal_html if journal_html else '<p>Пока нет записей в журнале</p>'}
        </div>
    </body>
</html>''', 404


@app.before_request
def log_all_requests():
    if not request.path.startswith('/static/'):
        log_entry = {
            'time': datetime.datetime.now(),
            'ip': request.remote_addr,
            'url': request.url
        }
        access_log.append(log_entry)


@app.route("/bad_request")
def bad_request():
    return f'''
<!doctype html>
<html>
    <head>
        <title>400 Bad Request</title>
        <link rel="stylesheet" href="{url_for('static', filename='lab1/lab1.css')}">
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не может обработать запрос из-за некорректного синтаксиса.</p>
        <a href="/">На главную</a>
    </body>
</html>''', 400


@app.route("/unauthorized")
def unauthorized():
    return f'''
<!doctype html>
<html>
    <head>
        <title>401 Unauthorized</title>
        <link rel="stylesheet" href="{url_for('static', filename='lab1/lab1.css')}">
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Требуется аутентификация для доступа к ресурсу.</p>
        <a href="/">На главную</a>
    </body>
</html>''', 401


@app.route("/payment_required")
def payment_required():
    return f'''
<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
        <link rel="stylesheet" href="{url_for('static', filename='lab1/lab1.css')}">
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Зарезервировано для будущего использования. Первоначально предназначалось для цифровых платежных систем.</p>
        <a href="/">На главную</a>
    </body>
</html>''', 402


@app.route("/forbidden")
def forbidden():
    return f'''
<!doctype html>
<html>
    <head>
        <title>403 Forbidden</title>
        <link rel="stylesheet" href="{url_for('static', filename='lab1/lab1.css')}">
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>Доступ к запрошенному ресурсу запрещен.</p>
        <a href="/">На главную</a>
    </body>
</html>''', 403


@app.route("/method_not_allowed")
def method_not_allowed():
    return f'''
<!doctype html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
        <link rel="stylesheet" href="{url_for('static', filename='lab1/lab1.css')}">
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод запроса не поддерживается для данного ресурса.</p>
        <a href="/">На главную</a>
    </body>
</html>''', 405


@app.route("/teapot")
def teapot():
    return f'''
<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
        <link rel="stylesheet" href="{url_for('static', filename='lab1/lab1.css')}">
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Я - чайник. Не могу заварить кофе.</p>
        <a href="/">На главную</a>
    </body>
</html>''', 418


@app.errorhandler(500)
def internal_server_error(err):
    return f'''
<!doctype html>
<html>
    <head>
        <title>500 - Ошибка сервера</title>
        <link rel="stylesheet" href="{url_for('static', filename='lab1/lab1.css')}">
        <style>
            body {{
                text-align: center;
                padding: 50px;
                font-family: Arial, sans-serif;
                background-color: #fff5f5;
            }}
            h1 {{
                font-size: 80px;
                color: #e53e3e;
                margin: 0;
            }}
            h2 {{
                color: #333;
                margin: 20px 0;
            }}
            .error-box {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                max-width: 600px;
                margin: 20px auto;
                border-left: 4px solid #e53e3e;
            }}
            a {{
                display: inline-block;
                padding: 10px 20px;
                background: grey;
                color: black;
                text-decoration: none;
                border-radius: 5px;
                margin: 10px;
            }}
            a:hover {{
                background: black;
            }}
        </style>
    </head>
    <body>
        <h1>500</h1>
        <h2>Внутренняя ошибка сервера</h2>
        
        <div class="error-box">
            <p>На сервере произошла непредвиденная ошибка.</p>
            <p>Мы уже знаем о проблеме и работаем над её решением.</p>
            <p>Попробуйте обновить страницу через несколько минут.</p>
        </div>
        
        <div>
            <a href="/">На главную</a>
            <a href="javascript:location.reload()">Обновить страницу</a>
        </div>
        
        <p style="margin-top: 30px; color: #999; font-size: 14px;">
            Если ошибка повторяется, свяжитесь с администратором: 
            <a href="mailto:aalinkaaaaaaaaaaaa@vk.com" style="color: #333;">aalinkaaaaaaaaaaaa@vk.com</a>
        </p>
    </body>
</html>''', 500


@app.route('/server_error')
def cause_server_error():
    try:
        result = 1 / 0
        return f"Result: {result}"
    except ZeroDivisionError:
        return "Error: Division by zero", 500

@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="/static/lab1/main.css">
        <link rel="icon" type="image/x-icon" href="/static/lab2/favicon.ico">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/lab2/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/lab2/favicon-16x16.png">
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        
        <main>
            <nav>
                <ul>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab2">Вторая лабораторная</a></li>
                    <li><a href="/lab3">Третья лабораторная</a></li>
                    <li><a href="/lab4">Четвертая лабораторная</a></li>
                    <li><a href="/lab5">Пятая лабораторная</a></li>
                    <li><a href="/lab6">Шестая лабораторная</a></li>
                    <li><a href="/lab7">Седьмая лабораторная</a></li>
                </ul>
            </nav>
        </main>
        
        <footer>
            <hr>
            &copy; Абузярова Кристина Руслановна, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
</html>'''   

@app.route("/http_codes")
def http_codes():
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{url_for('static', filename='lab1/lab1.css')}">
        <title>Коды ответов HTTP</title>
    </head>
    <body>
        <h1>Коды ответов HTTP</h1>
        <ul>
            <li><a href="/bad_request">400 - Bad Request</a></li>
            <li><a href="/unauthorized">401 - Unauthorized</a></li>
            <li><a href="/payment_required">402 - Payment Required</a></li>
            <li><a href="/forbidden">403 - Forbidden</a></li>
            <li><a href="/method_not_allowed">405 - Method Not Allowed</a></li>
            <li><a href="/teapot">418 - I'm a teapot</a></li>
            <li><a href="/server_error">500 - Internal Server Error</a></li>
        </ul>
        <a href="/">На главную</a>
    </body>
</html>'''

if __name__ == '__main__':
    app.run(debug=True)
