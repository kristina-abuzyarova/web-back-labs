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
from lab7 import lab7 

app = Flask(__name__)

app.secret_key = 'секретно-секретный секрет'
load_dotenv()

app.secret_key = 'your-secret-key-here'  
app.config['DB_TYPE'] = 'postgres' 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///offices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)

try:
    from lab7 import lab7_bp  
    app.register_blueprint(lab7_bp, url_prefix='/lab7')
    print("✓ Blueprint lab7_bp зарегистрирован с префиксом /lab7")
    print("   Маршруты: /lab7/, /lab7/rest-api/films/, /lab7/rest-api/films/<id>")
except ImportError as e:
    print(f"⚠ Ошибка импорта lab7.py: {e}")
    print("⚠ Используются fallback-маршруты для lab7")

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



@app.route('/lab7-fallback/')
def lab7_fallback_index():
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lab7 - Fallback (основной API не загружен)</title>
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
            color: #e74c3c; 
            margin-bottom: 20px;
            text-align: center;
            border-bottom: 2px solid #e74c3c;
            padding-bottom: 10px;
        }
        .warning {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
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
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin: 5px;
        }
        .btn:hover {
            background: #2980b9;
        }
        .btn-primary {
            background: #3498db;
        }
        .btn-secondary {
            background: #95a5a6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Lab7 - Fallback Mode</h1>
        
        <div class="warning">
            <strong>⚠ Внимание:</strong> Основной модуль lab7.py не загружен или содержит ошибки.
            <p>Используются упрощенные fallback-маршруты.</p>
        </div>
        
        <div class="api-info">
            <h2>🎬 Fallback REST API Endpoints:</h2>
            <ul>
                <li><a href="/lab7-fallback/api/films/">GET /lab7-fallback/api/films/</a> - Все фильмы (JSON)</li>
                <li>GET /lab7-fallback/api/films/&lt;id&gt; - Конкретный фильм (id 0-2)</li>
            </ul>
            
            <h3>Примеры запросов:</h3>
            <ul>
                <li><a href="/lab7-fallback/api/films/0">Фильм 0 - Test Film 1</a></li>
                <li><a href="/lab7-fallback/api/films/1">Фильм 1 - Test Film 2</a></li>
                <li><a href="/lab7-fallback/api/films/2">Фильм 2 - Test Film 3</a></li>
            </ul>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="/lab7/" class="btn btn-primary">Попробовать основной API</a>
            <a href="/lab7-fallback/api/films/" class="btn btn-secondary">🧪 Протестировать Fallback API</a>
        </div>
        
        <footer style="margin-top: 40px; text-align: center; color: #7f8c8d;">
            <p><a href="/" style="color: #3498db;">← Вернуться на главную</a></p>
            <p>&copy; Lab7 - Fallback REST API демонстрация</p>
        </footer>
    </div>
</body>
</html>
'''

fallback_films_db = [
    {
        "id": 0,
        "title": "Fallback Film 1",
        "title_ru": "Запасной фильм 1",
        "year": "2023",
        "description": "Это fallback-фильм, пока основной модуль не загружен."
    },
    {
        "id": 1,
        "title": "Fallback Film 2",
        "title_ru": "Запасной фильм 2",
        "year": "2024",
        "description": "Второй fallback-фильм для тестирования API."
    },
    {
        "id": 2,
        "title": "Fallback Film 3",
        "title_ru": "Запасной фильм 3",
        "year": "2025",
        "description": "Третий fallback-фильм с тестовыми данными."
    },
]

@app.route('/lab7-fallback/api/films/')
def lab7_fallback_get_films():
    return jsonify({
        "success": True,
        "mode": "fallback",
        "count": len(fallback_films_db),
        "films": fallback_films_db,
        "note": "Это fallback API. Основной модуль lab7.py не загружен."
    })

@app.route('/lab7-fallback/api/films/<int:film_id>')
def lab7_fallback_get_film(film_id):
    if 0 <= film_id < len(fallback_films_db):
        return jsonify({
            "success": True,
            "mode": "fallback",
            "film": fallback_films_db[film_id],
            "note": "Это fallback API. Основной модуль lab7.py не загружен."
        })
    return jsonify({
        "success": False,
        "mode": "fallback",
        "error": f"Фильм с ID {film_id} не найден",
        "available_ids": list(range(len(fallback_films_db)))
    }), 404

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
            <a href="mailto:kristina19283746@gmail.com" style="color: #333;">kristina19283746@gmail.com</a>
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
