from flask import Blueprint, render_template, request, redirect, session
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

        try:
            cur.execute("GRANT ALL PRIVILEGES ON TABLE users TO kristina_abuzyarova_knowledge_base")
            cur.execute("GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO kristina_abuzyarova_knowledge_base")
        except:
            pass  

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
        
        return render_template('lab5/success.html', login=login)
    
    except psycopg2.OperationalError as e:
        return render_template('lab5/register.html', error=f'Ошибка подключения к БД: {str(e)}')
    except Exception as e:
         return render_template('lab5/register.html', error=f'Ошибка базы данных: {str(e)}')
    

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
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

        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html',
                                error='Логин и/или пароль неверны')
        
        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html',
                                error='Логин и/или пароль неверны')
        
        session['login'] = login
        db_close(conn, cur)
        return render_template('lab5/success_login.html', login=login)
        
    except psycopg2.OperationalError as e:
        return render_template('lab5/login.html', error=f'Ошибка подключения к БД: {str(e)}')
    except Exception as e:
        return render_template('lab5/login.html', error=f'Ошибка базы данных: {str(e)}')