from flask import Blueprint, render_template, session, jsonify, request, redirect, url_for
import random

lab9 = Blueprint('lab9', __name__)

USERS = {
    'admin': 'admin123',
    'user1': 'pas1',
    'user2': 'pas2'
}

greetings = [
    "Пусть загаданное сбудется!",
    "Желаю крепкого здоровья и светлой радости!",
    "Побольше тёплых и весёлых мгновений!",
    "Лёгкости и успеха в любых делах!",
    "Домашнего уюта, мира и согласия!",
    "Каждый пусть новый день будет ярким!",
    "Стабильности и процветания!",
    "Гармонии в сердце и взаимной любви!",
    "Чтобы все желания находили дорогу к вам!",
    "Прекрасного расположения духа каждый день!"
]

gifts = [
    "gift1.jpg", "gift2.jpg", "gift3.jpg", "gift4.jpg", "gift5.jpg",
    "gift6.jpg", "gift7.jpg", "gift8.jpg", "gift9.jpg", "gift10.jpg"
]

boxes = [
    "box1.jpg", "box2.jpg", "box3.jpg", "box4.jpg", "box5.jpg",
    "box6.jpg", "box7.jpg", "box8.jpg", "box9.jpg", "box10.jpg"
]

RESTRICTED_GIFTS = [7, 8, 9]  

def init_session():
    if 'uid' not in session:
        session['uid'] = str(random.randint(10000, 99999))
    
    if 'open' not in session:
        session['open'] = []
    
    if 'states' not in session:
        session['states'] = [False] * 10
    
    if 'pos' not in session:
        generate_positions()

def generate_positions():
    pos = []
    used = []
    
    for i in range(10):
        attempts = 0
        placed = False
        
        while attempts < 100 and not placed:
            top = random.randint(5, 85)
            left = random.randint(5, 90)
            
            conflict = False
            for spot in used:
                if abs(top - spot['top']) < 15 and abs(left - spot['left']) < 15:
                    conflict = True
                    break
            
            if not conflict:
                used.append({'top': top, 'left': left})
                pos.append({
                    'id': i,
                    'top': f"{top}%",
                    'left': f"{left}%"
                })
                placed = True
            attempts += 1
        
        if not placed:
            top = random.randint(5, 85)
            left = random.randint(5, 90)
            pos.append({
                'id': i,
                'top': f"{top}%",
                'left': f"{left}%"
            })
    
    session['pos'] = pos

@lab9.route('/lab9/')
def main():
    init_session()
    
    states = session.get('states', [False] * 10)
    open_count = len(session.get('open', []))
    left_count = 10 - sum(states)
    is_authenticated = session.get('authenticated', False)
    username = session.get('username', '')
    
    return render_template('lab9/index.html',
                         pos=session['pos'],
                         states=states,
                         boxes=boxes,
                         open_count=open_count,
                         left_count=left_count,
                         is_authenticated=is_authenticated,
                         username=username,
                         restricted_gifts=RESTRICTED_GIFTS)

@lab9.route('/lab9/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab9/login.html')
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in USERS and USERS[username] == password:
        session['authenticated'] = True
        session['username'] = username
        return jsonify({'ok': True, 'msg': 'Авторизация успешна'})
    else:
        return jsonify({'ok': False, 'msg': 'Неверное имя пользователя или пароль'})

@lab9.route('/lab9/logout', methods=['POST'])
def logout():
    session.pop('authenticated', None)
    session.pop('username', None)
    return jsonify({'ok': True, 'msg': 'Выход выполнен'})

@lab9.route('/lab9/open', methods=['POST'])
def open_box():
    init_session()
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'ok': False, 'msg': 'Нет данных'}), 400
            
        box_id = data.get('box_id')
        
        if box_id is None:
            return jsonify({'ok': False, 'msg': 'Нет ID подарка'}), 400
            
        box_id = int(box_id)
        
        if box_id < 0 or box_id >= 10:
            return jsonify({'ok': False, 'msg': 'Некорректный номер подарка'}), 400
        
        if box_id in RESTRICTED_GIFTS and not session.get('authenticated', False):
            return jsonify({
                'ok': False, 
                'msg': 'Этот подарок доступен только для авторизованных пользователей. Пожалуйста, войдите в систему.',
                'requires_auth': True
            }), 403

        states = session.get('states', [False] * 10)
        open_list = session.get('open', [])
        
        if len(open_list) >= 3:
            return jsonify({'ok': False, 'msg': 'Можно открыть только 3 подарка!'}), 400
        
        if states[box_id]:
            return jsonify({'ok': False, 'msg': 'Этот подарок уже открыт!'}), 400
        
        open_list.append(box_id)
        session['open'] = open_list
        
        states[box_id] = True
        session['states'] = states
        
        greeting = greetings[box_id]
        gift = gifts[box_id]
        
        left_count = 10 - sum(states)
        
        return jsonify({
            'ok': True,
            'greeting': greeting,
            'gift': gift,
            'open_count': len(open_list),
            'left_count': left_count
        })
        
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Ошибка сервера: {str(e)}'}), 500

@lab9.route('/lab9/status')
def status():
    init_session()
    
    states = session.get('states', [False] * 10)
    open_count = len(session.get('open', []))
    left_count = 10 - sum(states)
    
    return jsonify({
        'open_count': open_count,
        'left_count': left_count
    })

@lab9.route('/lab9/reset', methods=['POST'])
def reset():
    session['open'] = []
    session['states'] = [False] * 10
    generate_positions()
    
    return jsonify({
        'ok': True,
        'msg': 'Игра сброшена!'
    })

@lab9.route('/lab9/santa', methods=['POST'])
def santa():
    if not session.get('authenticated', False):
        return jsonify({'ok': False, 'msg': 'Только авторизованные пользователи могут использовать эту функцию'}), 403
    
    session['open'] = []
    session['states'] = [False] * 10
    
    generate_positions()
    
    return jsonify({
        'ok': True,
        'msg': 'Санта Клаус наполнил все подарки заново!'
    })