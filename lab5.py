from flask import Blueprint, render_template, request, redirect, session, url_for
lab5 = Blueprint('lab5', __name__)
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', username=session.get('login', 'anonymous'))

def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='kristina_abuzyarova_knowledge_base',  
        user='kristina_abuzyarova_knowledge_base',      
        password='123',
        port=5432
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()  

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    try:
        conn, cur = db_connect()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                login VARCHAR(30) UNIQUE NOT NULL,
                password VARCHAR(162) NOT NULL
            )
        """)

        cur.execute("SELECT login FROM users WHERE login = %s", (login,))
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html',
                                error="Такой пользователь уже существует")
        
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password_hash))

        db_close(conn, cur)
        
        return redirect(url_for('lab5.login'))
    
    except psycopg2.OperationalError as e:
        return render_template('lab5/register.html', error=f'Ошибка подключения к БД: {str(e)}')
    except Exception as e:
         return render_template('lab5/register.html', error=f'Ошибка базы данных: {str(e)}')
    

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if 'login' in session:
        print("Пользователь уже авторизован, редирект на главную")
        return redirect(url_for('lab5.lab'))
        
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error="Заполните поля")
    
    try:
        conn, cur = db_connect()
 
        cur.execute("SELECT * FROM users WHERE login = %s", (login,))
        user = cur.fetchone()

        print(f"=== ОТЛАДКА ЛОГИНА ===")
        print(f"Логин из формы: {login}")
        print(f"Найден пользователь: {user}")

        if not user:
            print("Пользователь не найден в БД")
            db_close(conn, cur)
            return render_template('lab5/login.html',
                                error='Логин и/или пароль неверны')
        
        print(f"Хэш пароля из БД: {user['password']}")
        print(f"Длина хэша: {len(user['password'])}")

        password_valid = check_password_hash(user['password'], password)
        print(f"Пароль верный: {password_valid}")
        
        if not password_valid:
            print("Пароль неверный!")
            db_close(conn, cur)
            return render_template('lab5/login.html',
                                error='Логин и/или пароль неверны')
        
        session['login'] = login
        db_close(conn, cur)
        print("УСПЕШНЫЙ ЛОГИН! Делаем редирект на главную")
        return redirect(url_for('lab5.lab'))
        
    except psycopg2.OperationalError as e:
        return render_template('lab5/login.html', error=f'Ошибка подключения к БД: {str(e)}')
    except Exception as e:
        return render_template('lab5/login.html', error=f'Ошибка базы данных: {str(e)}')


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not (title and article_text):
        return render_template('lab5/create_article.html', error='Заполните все поля')

    try:
        conn, cur = db_connect()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title VARCHAR(200) NOT NULL,
                article_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        cur.execute("SELECT id FROM users WHERE login = %s", (login,))
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return redirect(url_for('lab5.login'))
        
        user_id = user["id"]

        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s)", 
                   (user_id, title, article_text))

        db_close(conn, cur)
        return redirect(url_for('lab5.articles'))
    
    except Exception as e:
        return render_template('lab5/create_article.html', error=f'Ошибка базы данных: {str(e)}')


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('lab5.lab'))


@lab5.route('/lab5/articles')
def articles():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))
    
    try:
        conn, cur = db_connect()

        cur.execute("""
            SELECT a.title, a.article_text, a.created_at 
            FROM articles a 
            JOIN users u ON a.user_id = u.id 
            WHERE u.login = %s 
            ORDER BY a.created_at DESC
        """, (login,))
        
        articles = cur.fetchall()
        db_close(conn, cur)
        
        return render_template('lab5/articles.html', articles=articles, username=login)
    
    except Exception as e:
        return render_template('lab5/articles.html', error=f'Ошибка базы данных: {str(e)}')


@lab5.route('/lab5/list')
def list_redirect():
    return redirect(url_for('lab5.articles'))
    

@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    cur.execute(f"SELECT id FROM users WHERE login='{login}';")
    user_id = cur.fetchone()["id"]

    cur.execute(f"SELECT * FROM articles WHERE user_id='{user_id}';")
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('/lab5/articles.html', articles=articles)