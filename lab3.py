from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name = name if name else "Аноним"
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    age = age if age else "Неизвестно"
    return render_template('/lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')

    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if user == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    drink_name = ''

    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    additions = []
    if request.args.get('milk') == 'on':
        price += 30
        additions.append('молоко')
    if request.args.get('sugar') == 'on':
        price += 10
        additions.append('сахар')
    
    return render_template('lab3/pay.html', price=price, drink_name=drink_name, additions=additions)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    current_color = request.cookies.get('color', '#000000')
    current_bg_color = request.cookies.get('bg_color', "#68a7cc")
    current_font_size = request.cookies.get('font_size', '16')
    current_font_family = request.cookies.get('font_family', 'Arial, sans-serif')

    new_color = request.args.get('color')
    new_bg_color = request.args.get('bg_color')
    new_font_size = request.args.get('font_size')
    new_font_family = request.args.get('font_family')

    if new_color or new_bg_color or new_font_size or new_font_family:
        color_to_use = new_color if new_color is not None else current_color
        bg_color_to_use = new_bg_color if new_bg_color is not None else current_bg_color
        font_size_to_use = new_font_size if new_font_size is not None else current_font_size
        font_family_to_use = new_font_family if new_font_family is not None else current_font_family
        
        resp = make_response(render_template('lab3/settings.html', 
                                            color=color_to_use,
                                            bg_color=bg_color_to_use,
                                            font_size=font_size_to_use,
                                            font_family=font_family_to_use))

        if new_color:
            resp.set_cookie('color', new_color, max_age=60*60*24*365)
        if new_bg_color:
            resp.set_cookie('bg_color', new_bg_color, max_age=60*60*24*365)
        if new_font_size:
            resp.set_cookie('font_size', new_font_size, max_age=60*60*24*365)
        if new_font_family:
            resp.set_cookie('font_family', new_font_family, max_age=60*60*24*365)
        
        return resp
    
    return render_template('lab3/settings.html', 
                          color=current_color, 
                          bg_color=current_bg_color, 
                          font_size=current_font_size,
                           font_family=current_font_family)


@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    bedding = request.args.get('bedding')
    baggage = request.args.get('baggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    if not fio:
        errors['fio'] = 'Заполните поле'
    if not shelf:
        errors['shelf'] = 'Выберите полку'
    if not age:
        errors['age'] = 'Заполните поле'
    elif not age.isdigit() or not (1 <= int(age) <= 120):
        errors['age'] = 'Возраст должен быть от 1 до 120 лет'
    if not departure:
        errors['departure'] = 'Заполните поле'
    if not destination:
        errors['destination'] = 'Заполните поле'
    if not date:
        errors['date'] = 'Заполните поле'
    
    if errors or not all([fio, shelf, age, departure, destination, date]):
        return render_template('lab3/ticket_form.html', 
                             errors=errors,
                             fio=fio, shelf=shelf, bedding=bedding, 
                             baggage=baggage, age=age, departure=departure,
                             destination=destination, date=date, insurance=insurance)
    
    if int(age) < 18:
        base_price = 700
        ticket_type = 'Детский билет'
    else:
        base_price = 1000
        ticket_type = 'Взрослый билет'
    
    total_price = base_price
    
    if shelf in ['lower', 'lower-side']:
        total_price += 100
    if bedding == 'on':
        total_price += 75
    if baggage == 'on':
        total_price += 250
    if insurance == 'on':
        total_price += 150
    
    return render_template('lab3/ticket_result.html',
                         fio=fio, shelf=shelf, bedding=bedding,
                         baggage=baggage, age=age, departure=departure,
                         destination=destination, date=date, insurance=insurance,
                         ticket_type=ticket_type, total_price=total_price)


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.set_cookie('color', '', expires=0)
    resp.set_cookie('bg_color', '', expires=0)
    resp.set_cookie('font_size', '', expires=0)
    resp.set_cookie('font_family', '', expires=0)
    
    return resp

products = [
    {'name': 'MacBook Air 13"', 'price': 119990, 'brand': 'Apple', 'color': 'Серый космос', 'storage': '256GB'},
    {'name': 'ASUS ROG Strix G15', 'price': 89990, 'brand': 'ASUS', 'color': 'Черный', 'storage': '512GB'},
    {'name': 'Dell XPS 13', 'price': 109990, 'brand': 'Dell', 'color': 'Платиновый', 'storage': '1TB'},
    {'name': 'HP Pavilion 15', 'price': 64990, 'brand': 'HP', 'color': 'Серебристый', 'storage': '256GB'},
    {'name': 'Lenovo ThinkPad X1', 'price': 129990, 'brand': 'Lenovo', 'color': 'Черный', 'storage': '512GB'},
    {'name': 'MacBook Pro 16"', 'price': 199990, 'brand': 'Apple', 'color': 'Серебристый', 'storage': '1TB'},
    {'name': 'Acer Aspire 5', 'price': 45990, 'brand': 'Acer', 'color': 'Синий', 'storage': '128GB'},
    {'name': 'MSI Katana 17', 'price': 79990, 'brand': 'MSI', 'color': 'Красный', 'storage': '512GB'},
    {'name': 'Samsung Galaxy Book3', 'price': 74990, 'brand': 'Samsung', 'color': 'Графитовый', 'storage': '256GB'},
    {'name': 'Huawei MateBook D16', 'price': 69990, 'brand': 'Huawei', 'color': 'Серый', 'storage': '512GB'},
    {'name': 'MacBook Air 15"', 'price': 149990, 'brand': 'Apple', 'color': 'Золотой', 'storage': '512GB'},
    {'name': 'ASUS TUF Gaming F15', 'price': 75990, 'brand': 'ASUS', 'color': 'Темно-серый', 'storage': '1TB'},
    {'name': 'Dell Inspiron 14', 'price': 54990, 'brand': 'Dell', 'color': 'Платиновый', 'storage': '256GB'},
    {'name': 'HP Spectre x360', 'price': 139990, 'brand': 'HP', 'color': 'Синий', 'storage': '512GB'},
    {'name': 'Lenovo Yoga 9i', 'price': 119990, 'brand': 'Lenovo', 'color': 'Титановый', 'storage': '1TB'},
    {'name': 'MacBook Pro 14"', 'price': 169990, 'brand': 'Apple', 'color': 'Темная ночь', 'storage': '512GB'},
    {'name': 'Acer Swift 3', 'price': 52990, 'brand': 'Acer', 'color': 'Розовое золото', 'storage': '256GB'},
    {'name': 'MSI Prestige 14', 'price': 89990, 'brand': 'MSI', 'color': 'Синий', 'storage': '512GB'},
    {'name': 'Samsung Odyssey', 'price': 99990, 'brand': 'Samsung', 'color': 'Белый', 'storage': '1TB'},
    {'name': 'Huawei MateBook X Pro', 'price': 129990, 'brand': 'Huawei', 'color': 'Зеленый', 'storage': '512GB'}
]

@lab3.route('/lab3/products')
def products_search():
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')
    
    all_prices = [product['price'] for product in products]
    real_min_price = min(all_prices)
    real_max_price = max(all_prices)
    
    min_price_input = request.args.get('min_price', '')
    max_price_input = request.args.get('max_price', '')
    
    if 'reset' in request.args:
        resp = make_response(render_template('lab3/products.html',
                                           products=products,
                                           min_price='',
                                           max_price='',
                                           real_min_price=real_min_price,
                                           real_max_price=real_max_price,
                                           filtered_count=len(products),
                                           total_count=len(products)))
        resp.set_cookie('min_price', '', expires=0)
        resp.set_cookie('max_price', '', expires=0)
        return resp
    
    if min_price_input or max_price_input:
        min_price = int(min_price_input) if min_price_input else real_min_price
        max_price = int(max_price_input) if max_price_input else real_max_price
        
        if min_price > max_price:
            min_price, max_price = max_price, min_price
        
        filtered_products = [
            product for product in products 
            if min_price <= product['price'] <= max_price
        ]
        
        resp = make_response(render_template('lab3/products.html',
                                           products=filtered_products,
                                           min_price=min_price,
                                           max_price=max_price,
                                           real_min_price=real_min_price,
                                           real_max_price=real_max_price,
                                           filtered_count=len(filtered_products),
                                           total_count=len(products)))
        resp.set_cookie('min_price', str(min_price), max_age=60*60*24*30)
        resp.set_cookie('max_price', str(max_price), max_age=60*60*24*30)
        return resp
    
    if min_price_cookie and max_price_cookie:
        min_price = int(min_price_cookie)
        max_price = int(max_price_cookie)
        
        filtered_products = [
            product for product in products 
            if min_price <= product['price'] <= max_price
        ]
        
        return render_template('lab3/products.html',
                             products=filtered_products,
                             min_price=min_price,
                             max_price=max_price,
                             real_min_price=real_min_price,
                             real_max_price=real_max_price,
                             filtered_count=len(filtered_products),
                             total_count=len(products))
    
    return render_template('lab3/products.html',
                         products=products,
                         min_price='',
                         max_price='',
                         real_min_price=real_min_price,
                         real_max_price=real_max_price,
                         filtered_count=len(products),
                         total_count=len(products))
@app.route('/lab3/')
def lab3():
    name = request.cookies.get('name', 'Гость')
    name_color = request.cookies.get('name_color', 'black')
    return render_template('lab3.html', 
                         name=name, 
                         name_color=name_color)

@lab3.route('/lab3/form1')
def form1():
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex)