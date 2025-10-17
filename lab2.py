from flask import Blueprint, url_for, redirect, request, abort, render_template

lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшом'

flower_list = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка', 'price': 330},
    {'name': 'георгин', 'price': 300},
    {'name': 'гладиолус', 'price': 310}
]


@lab2.route('/lab2/flowers/')
def flowers_list():
    return render_template('flowers.html', flowers=flower_list)


@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id): 

    if flower_id >= len(flower_list):
        abort(404)
        flower_list.pop(flower_id)
    return redirect(url_for('lab2.flowers_list'))


@lab2.route('/lab2/add_flower/', methods=['GET', 'POST'])
def add_flower():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            for flower in flower_list:
                if flower['name'] == name:
                    flower['price'] += 10
                    break
            else:
                flower_list.append({'name': name, 'price': 300})
        return redirect(url_for('lab2.flowers_list'))
    return redirect(url_for('lab2.flowers_list'))


@lab2.route('/lab2/flowers/all')
def all_flowers():
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Все цветы</h1>
        <p>Количество цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
        <a href="/lab2/flowers/clear">Очистить список</a>
    </body>
</html>
'''


@lab2.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('lab2.flowers_list'))


@lab2.route
def example():
    name = 'Абузярова Кристина'
    number = 'Лабораторная работа 2'
    group = 'ФБИ-34'
    course = '3 курс'
    
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321},
    ]
    return render_template('example.html', 
                           name=name, number=number, group=group, 
                           course=course, fruits=fruits)


@lab2.route('/lab2/')
def lab2():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    
    return render_template('filter.html', phrase = phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return f'''
<!doctype html>
<html>
<body>
    <h1>Расчёт с параметрами:</h1>
    <div class="result">
        {a} + {b} = {a + b}<br>
        {a} - {b} = {a - b}<br>
        {a} × {b} = {a * b}<br>
        {a} / {b} = {a / b if b != 0 else 'на ноль делить нельзя'}<br>
        {a}<sup>{b}</sup> = {a ** b}
    </div>
    <p><a href="/lab2/calc/">Попробовать с другими числами</a></p>
</body>
</html>
'''


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')


books = [
    {'author': 'Джоан Роулинг', 'title': 'Гарри Поттер и философский камень', 'genre': 'Фэнтези', 'pages': 432},
    {'author': 'Джордж Оруэлл', 'title': '1984', 'genre': 'Антиутопия', 'pages': 328},
    {'author': 'Джон Р. Р. Толкин', 'title': 'Властелин колец', 'genre': 'Фэнтези', 'pages': 1178},
    {'author': 'Агата Кристи', 'title': 'Убийство в Восточном экспрессе', 'genre': 'Детектив', 'pages': 256},
    {'author': 'Стивен Кинг', 'title': 'Оно', 'genre': 'Ужасы', 'pages': 1138},
    {'author': 'Дэн Браун', 'title': 'Код да Винчи', 'genre': 'Триллер', 'pages': 489},
    {'author': 'Харпер Ли', 'title': 'Убить пересмешника', 'genre': 'Роман', 'pages': 376},
    {'author': 'Александр Солженицын', 'title': 'Архипелаг ГУЛАГ', 'genre': 'Историческая проза', 'pages': 1424},
    {'author': 'Владимир Набоков', 'title': 'Лолита', 'genre': 'Роман', 'pages': 336},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
]


@lab2.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)


cats = [
    {
        'name': 'Персидский кот',
        'image': 'persian.jpg',
        'description': 'Пушистый кот с плоской мордочкой и длинной шерстью.'
    },
    {
        'name': 'Сиамский кот',
        'image': 'siamese.jpg',
        'description': 'Элегантный кот с голубыми глазами и контрастным окрасом.'
    },
    {
        'name': 'Мейн-кун',
        'image': 'maine_coon.jpg',
        'description': 'Крупная порода с кисточками на ушах и дружелюбным характером.'
    },
    {
        'name': 'Британский кот',
        'image': 'british.jpg',
        'description': 'Коренастый кот с плюшевой шерстью и спокойным нравом.'
    },
    {
        'name': 'Сфинкс',
        'image': 'sphynx.jpg',
        'description': 'Бесшерстная порода с морщинистой кожей и теплым телом.'
    },
    {
        'name': 'Бенгальский кот',
        'image': 'bengal.jpg',
        'description': 'Дикий вид с леопардовым окрасом и активным характером.'
    },
    {
        'name': 'Русский голубой',
        'image': 'russian_blue.jpg',
        'description': 'Серебристо-голубая шерсть и изумрудные глаза.'
    },
    {
        'name': 'Норвежский лесной',
        'image': 'norwegian.jpg',
        'description': 'Крупный кот с густой водонепроницаемой шерстью.'
    },
    {
        'name': 'Шотландский вислоухий',
        'image': 'scottish_fold.jpg',
        'description': 'Кот с загнутыми вперед ушами и круглыми глазами.'
    },
    {
        'name': 'Абиссинский кот',
        'image': 'abyssinian.jpg',
        'description': 'Стройный кот с тикированной шерстью и активным характером.'
    },
    {
        'name': 'Рэгдолл',
        'image': 'ragdoll.jpg',
        'description': 'Крупный кот, который расслабляется на руках как тряпичная кукла.'
    },
    {
        'name': 'Бирманский кот',
        'image': 'birman.jpg',
        'description': 'Священная порода с белыми "носочками" и голубыми глазами.'
    },
    {
        'name': 'Ориентальный кот',
        'image': 'oriental.jpg',
        'description': 'Стройный кот с большими ушами и грациозной внешностью.'
    },
    {
        'name': 'Турецкий ван',
        'image': 'turkish_van.jpg',
        'description': 'Кот, любящий воду, с характерным красно-белым окрасом.'
    },
    {
        'name': 'Египетский мау',
        'image': 'egyptian_mau.jpg',
        'description': 'Пятнистая порода, одна из древнейших в мире.'
    },
    {
        'name': 'Тонкинский кот',
        'image': 'tonkinese.jpg',
        'description': 'Гибрид сиамской и бирманской пород с аквамариновыми глазами.'
    },
    {
        'name': 'Корниш-рекс',
        'image': 'cornish_rex.jpg',
        'description': 'Кот с волнистой шерстью и стройным телом.'
    },
    {
        'name': 'Девон-рекс',
        'image': 'devon_rex.jpg',
        'description': 'Кот с большими ушами и волнистой шерстью, похож на эльфа.'
    },
    {
        'name': 'Сибирский кот',
        'image': 'siberian.jpg',
        'description': 'Крупный кот с густой шерстью, адаптированной к холоду.'
    },
    {
        'name': 'Манчкин',
        'image': 'munchkin.jpg',
        'description': 'Кот с короткими лапками и игривым характером.'
    }
]


@lab2.route('/lab2/cats/')
def cats_list():
    return render_template('cats.html', cats=cats)