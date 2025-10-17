from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1', __name__)


@lab1.route('/lab1')
def lab():
    return '''<!doctype html>
<html>
<head><meta charset="utf-8"><title>Лабораторная 1</title></head>
<body>
    <h1>Лабораторная 1</h1>
    <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, 
    а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, 
    сознательно предоставляющих лишь самые базовые возможности.</p>
    <p><a href="/">На корень сайта</a></p>
    <h2>Список роутов</h2>
    <ul>
        <li><a href="/">Главная страница</a></li>
        <li><a href="/index">Index</a></li>
        <li><a href="/lab1/web">/lab1/web</a></li>
        <li><a href="/lab1/author">/lab1/author</a></li>
        <li><a href="/lab1/image">/lab1/image</a></li>
        <li><a href="/lab1/counter">/lab1/counter</a></li>
        <li><a href="/lab1/counter/clear">/lab1/counter/clear</a></li>
        <li><a href="/lab1/info">/lab1/info</a></li>
        <li><a href="/lab1/created">/lab1/created</a></li>
        <li><a href="400">400 Bad Request</a></li>
        <li><a href="401">401 Unauthorized</a></li>
        <li><a href="402">402 Payment Required</a></li>
        <li><a href="403">403 Forbidden</a></li>
        <li><a href="404">Страница не найдена (404)</a></li>
        <li><a href="405">405 Method Not Allowed</a></li>
        <li><a href="418">418 I'm a teapot</a></li>
        <li><a href="/cause_500">Внутренняя ошибка сервера (500)</a></li>
    </ul>
</body>
</html>'''


@lab1.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/lab1/author">author</a>
            </body>
        </html>""", 200, {
            "X-Server": "sample",
            'Content-Type': 'text/plain; charset=utf-8'
            }


@lab1.route("/lab1/author")
def author():
    name = "Абузярова Кристина Руслановна"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""


@lab1.route('/lab1/image')
def image():
    css = url_for('static', filename='lab1.css')
    img = url_for('static', filename='oak.jpg')
    html = f'''<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>кот</title>
    <link rel="stylesheet" href="{css}">
</head>
<body>
    <h1>кот</h1>
    <img class="lab1" src="{img}" alt="кот">
</body>
</html>'''
    headers = {
        'Content-Language': 'ru',
        'X-Project': 'lab1',
        'X-Author': 'Abuzyarova'
    }
    return html, 200, headers

count = 0


@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr
    clear_url = url_for('clear_counter')
    return f'''
<!doctype html>
<html>
<head><title>Счётчик</title></head>
<body>
    Сколько раз вы сюда заходили: {count}
    <hr>
    Дата и время: {time} <br>
    Запрошенный адрес: {url} <br>
    Ваш IP-адрес: {client_ip} <br>
    <p><a href="{clear_url}">Очистить счётчик</a></p>
</body>
</html>
'''


@lab1.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect(url_for('counter'))


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
def created():
    return '''
<!doctype html"
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''',201