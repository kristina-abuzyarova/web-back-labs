from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///initiatives.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['INITIATIVES_PER_PAGE'] = 5

db = SQLAlchemy(app)

# ФИО студента
STUDENT_INFO = {'name': 'Абузярова Кристина Руслановна ФБИ-34', 'ФБИ-34': 'ПИН-123'}

# ============= МОДЕЛИ =============
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Initiative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    author = db.relationship('User', backref='initiatives')

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    initiative_id = db.Column(db.Integer, db.ForeignKey('initiative.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)


def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    
    initiatives_query = Initiative.query.order_by(
        Initiative.created_at.desc()
    ).paginate(
        page=page, 
        per_page=app.config['INITIATIVES_PER_PAGE'],
        error_out=False
    )
    
    current_user = get_current_user()
    user_votes = {}
    
    if current_user:
        votes = Vote.query.filter_by(user_id=current_user.id).all()
        for vote in votes:
            user_votes[vote.initiative_id] = vote.value
    
    initiatives_data = []
    for initiative in initiatives_query.items:
        initiatives_data.append({
            'id': initiative.id,
            'title': initiative.title,
            'content': initiative.content,
            'score': initiative.score,
            'created_at': initiative.created_at,
            'author': initiative.author,
            'author_id': initiative.user_id,
            'user_vote': user_votes.get(initiative.id)
        })
    
    return render_template('index.html', 
                         initiatives=initiatives_data,
                         pagination=initiatives_query,
                         current_user=current_user,
                         student_info=STUDENT_INFO)

@app.route('/login', methods=['GET', 'POST'])
def login():
    current_user = get_current_user()
    if current_user:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Заполните все поля', 'error')
            return render_template('login.html', student_info=STUDENT_INFO)
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash(f'Добро пожаловать, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('login.html', student_info=STUDENT_INFO)

@app.route('/register', methods=['GET', 'POST'])
def register():
    current_user = get_current_user()
    if current_user:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Заполните все поля', 'error')
            return render_template('register.html', student_info=STUDENT_INFO)
        
        if len(password) < 6:
            flash('Пароль должен быть не менее 6 символов', 'error')
            return render_template('register.html', student_info=STUDENT_INFO)
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует', 'error')
            return render_template('register.html', student_info=STUDENT_INFO)
        
        user = User(username=username)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', student_info=STUDENT_INFO)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create():
    current_user = get_current_user()
    if not current_user:
        flash('Для создания инициативы нужно войти в систему', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('Заполните все поля', 'error')
            return render_template('create.html', student_info=STUDENT_INFO)
        
        initiative = Initiative(
            title=title,
            content=content,
            user_id=current_user.id
        )
        
        db.session.add(initiative)
        db.session.commit()
        
        flash('Инициатива создана успешно!', 'success')
        return redirect(url_for('index'))
    
    return render_template('create.html', student_info=STUDENT_INFO)

# ============= НОВЫЙ МАРШРУТ: РЕДАКТИРОВАНИЕ =============
@app.route('/edit/<int:initiative_id>', methods=['GET', 'POST'])
def edit_initiative(initiative_id):
    current_user = get_current_user()
    if not current_user:
        flash('Для редактирования нужно войти в систему', 'error')
        return redirect(url_for('login'))
    
    initiative = Initiative.query.get_or_404(initiative_id)
    
    # Проверка прав: только автор или администратор
    if current_user.id != initiative.user_id and not current_user.is_admin:
        flash('Вы не можете редактировать эту инициативу', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('Заполните все поля', 'error')
            return render_template('edit.html', 
                                 initiative=initiative,
                                 student_info=STUDENT_INFO,
                                 current_user=current_user)
        
        # Сохраняем старые данные для сообщения
        old_title = initiative.title
        
        # Обновляем инициативу
        initiative.title = title
        initiative.content = content
        
        db.session.commit()
        
        flash(f'Инициатива "{old_title}" успешно обновлена!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', 
                         initiative=initiative,
                         student_info=STUDENT_INFO,
                         current_user=current_user)

@app.route('/vote/<int:initiative_id>/<int:value>')
def vote(initiative_id, value):
    current_user = get_current_user()
    if not current_user:
        flash('Для голосования нужно войти в систему', 'error')
        return redirect(url_for('login'))
    
    if value not in [1, -1]:
        flash('Неверное значение голоса', 'error')
        return redirect(url_for('index'))
    
    initiative = Initiative.query.get_or_404(initiative_id)
    
    # Проверяем, не голосовал ли уже пользователь
    existing_vote = Vote.query.filter_by(
        user_id=current_user.id,
        initiative_id=initiative_id
    ).first()
    
    if existing_vote:
        if existing_vote.value != value:
            # Меняем голос
            initiative.score += value - existing_vote.value
            existing_vote.value = value
            message = 'Вы изменили свой голос!'
        else:
            # Отменяем голос (удаляем)
            initiative.score -= value
            db.session.delete(existing_vote)
            message = 'Вы отменили свой голос!'
    else:
        # Новый голос
        vote = Vote(
            user_id=current_user.id,
            initiative_id=initiative_id,
            value=value
        )
        initiative.score += value
        db.session.add(vote)
        message = 'Ваш голос учтен!'
    
    db.session.commit()
    
    # Проверяем, нужно ли удалить инициативу (рейтинг < -10)
    if initiative.score < -10:
        db.session.delete(initiative)
        db.session.commit()
        flash('Инициатива удалена из-за низкого рейтинга', 'info')
    else:
        flash(message, 'success')
    
    # Возвращаем на ту же страницу
    page = request.args.get('page', 1)
    return redirect(url_for('index', page=page))

@app.route('/delete/<int:initiative_id>')
def delete(initiative_id):
    current_user = get_current_user()
    if not current_user:
        flash('Нужно войти в систему', 'error')
        return redirect(url_for('login'))
    
    initiative = Initiative.query.get_or_404(initiative_id)
    
    if current_user.id == initiative.user_id or current_user.is_admin:
        db.session.delete(initiative)
        db.session.commit()
        flash('Инициатива удалена', 'success')
    else:
        flash('Вы не можете удалить эту инициативу', 'error')
    
    page = request.args.get('page', 1)
    return redirect(url_for('index', page=page))

@app.route('/delete_account')
def delete_account():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    if not current_user.is_admin:
        session.pop('user_id', None)
        db.session.delete(current_user)
        db.session.commit()
        flash('Ваш аккаунт удален', 'success')
    else:
        flash('Администратор не может удалить свой аккаунт', 'error')
    
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    current_user = get_current_user()
    if not current_user or not current_user.is_admin:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('index'))
    
    users = User.query.all()
    initiatives = Initiative.query.all()
    
    return render_template('admin.html', 
                         student_info=STUDENT_INFO,
                         users=users,
                         initiatives=initiatives,
                         current_user=current_user)

@app.route('/admin/delete_user/<int:user_id>')
def admin_delete_user(user_id):
    current_user = get_current_user()
    if not current_user or not current_user.is_admin:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get(user_id)
    if user and user.id != current_user.id:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь удален', 'success')
    elif user and user.id == current_user.id:
        flash('Вы не можете удалить себя', 'error')
    
    return redirect(url_for('admin'))

@app.route('/init_db')
def init_db():
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            
            for i in range(1, 4):
                user = User(username=f'user{i}')
                user.set_password('password123')
                db.session.add(user)
            
            db.session.commit()
        
        if Initiative.query.count() < 20:
            users = User.query.all()
            
            titles = [
                "Улучшение Wi-Fi в кампусе",
                "Создание зоны отдыха", 
                "Бесплатные курсы английского",
                "Ремонт спортивного зала",
                "Электронная библиотека",
                "Велосипедные стойки",
                "Модернизация компьютерных классов",
                "Электронные пропуска",
                "Студенческий совет",
                "Улучшение освещения",
                "Коворкинг-зона",
                "Программа наставничества",
                "Ремонт аудиторий",
                "Спортивные мероприятия",
                "Улучшение столовой",
                "Мобильное приложение",
                "Проведение хакатонов",
                "Кулеры с водой",
                "Читальный зал 24/7",
                "Языковой клуб"
            ]
            
            for i, title in enumerate(titles):
                author = random.choice(users)
                initiative = Initiative(
                    title=title,
                    content=f"Подробное описание инициативы: {title}. Эта идея поможет улучшить условия для всех студентов.",
                    user_id=author.id,
                    score=random.randint(-5, 25)
                )
                db.session.add(initiative)
            
            db.session.commit()
    
    return '''
    <h1>✅ База данных создана!</h1>
    <p><a href="/">На главную</a></p>
    <h3>Данные для входа:</h3>
    <p><b>Администратор:</b> admin / admin123</p>
    <p><b>Пользователи:</b> user1, user2, user3 / password123</p>
    '''

@app.route('/api/jsonrpc', methods=['POST'])
def jsonrpc_api():
    try:
        import json
        data = request.get_json()
        method = data.get('method', '')
        
        if method == 'get_initiatives':
            page = data.get('params', {}).get('page', 1)
            initiatives = Initiative.query.order_by(
                Initiative.created_at.desc()
            ).paginate(
                page=page, 
                per_page=app.config['INITIATIVES_PER_PAGE'],
                error_out=False
            )
            
            result = []
            for initiative in initiatives.items:
                result.append({
                    'id': initiative.id,
                    'title': initiative.title,
                    'content': initiative.content[:100] + '...' if len(initiative.content) > 100 else initiative.content,
                    'score': initiative.score,
                    'author': initiative.author.username,
                    'created_at': initiative.created_at.isoformat()
                })
            
            return json.dumps({
                'jsonrpc': '2.0',
                'result': result,
                'id': data.get('id', 1)
            })
        else:
            return json.dumps({
                'jsonrpc': '2.0',
                'error': {'code': -32601, 'message': 'Method not found'},
                'id': data.get('id', 1)
            })
    except Exception as e:
        import json
        return json.dumps({
            'jsonrpc': '2.0',
            'error': {'code': -32603, 'message': str(e)},
            'id': data.get('id', 1)
        })

if __name__ == '__main__':
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, port=5000)

    