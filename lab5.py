from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)

def init_db():
    """Инициализация базы данных с созданием таблиц"""
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='kristina_abuzyarova_knowledge_base',  
            user='kristina_abuzyarova_knowledge_base',      
            password='123',
            port=5432
        )
        cur = conn.cursor()

        try:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    login VARCHAR(30) UNIQUE NOT NULL,
                    password VARCHAR(162) NOT NULL
                )
            ''')
            print(" Таблица users создана/проверена")
        except Exception as e:
            print(f" Ошибка при создании users: {e}")

        try:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS user_articles (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    title VARCHAR(200) NOT NULL,
                    article_text TEXT NOT NULL,
                    is_public BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print(" Таблица user_articles создана/проверена")
        except Exception as e:
            print(f" Ошибка при создании user_articles: {e}")

        # Добавляем поле is_public если его нет
        try:
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='user_articles' and column_name='is_public'
            """)
            if not cur.fetchone():
                cur.execute("ALTER TABLE user_articles ADD COLUMN is_public BOOLEAN DEFAULT FALSE")
                print(" Добавлено поле is_public в таблицу user_articles")
        except Exception as e:
            print(f" Ошибка при добавлении поля is_public: {e}")

        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        print(f" Ошибка при инициализации БД: {e}")
        return False

def check_connection():
    """Функция для проверки подключения к БД"""
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='kristina_abuzyarova_knowledge_base',  
            user='kristina_abuzyarova_knowledge_base',      
            password='123',
            port=5432
        )
        cur = conn.cursor()

        cur.execute("SELECT current_database()")
        current_db = cur.fetchone()[0]
        print(f" Подключены к базе данных: {current_db}")

        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print(f" Таблицы в базе: {tables}")

        try:
            cur.execute("SELECT COUNT(*) FROM users")
            count = cur.fetchone()[0]
            print(f" Количество пользователей в БД: {count}")
        except psycopg2.Error as e:
            print(f" Нет доступа к таблице users: {e}")

        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f" Ошибка подключения: {e}")
        return False

print(" Проверяем подключение к БД...")
check_connection()

print(" Инициализируем БД...")
if not init_db():
    print(" Проблема с инициализацией БД, но продолжаем работу")

@lab5.route('/lab5/')
def lab():
    username = session.get('login', 'anonymous')
    return render_template('lab5/lab5.html', username=username)

def db_connect():
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='kristina_abuzyarova_knowledge_base',  
            user='kristina_abuzyarova_knowledge_base',      
            password='123',
            port=5432
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        return conn, cur
    except Exception as e:
        print(f" Ошибка подключения к БД: {e}")
        raise

def db_close(conn, cur):
    try:
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f" Ошибка при закрытии соединения: {e}")

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    if len(login) < 3:
        return render_template('lab5/register.html', error='Логин должен быть не менее 3 символов')

    if len(password) < 3:
        return render_template('lab5/register.html', error='Пароль должен быть не менее 3 символов')

    try:
        conn, cur = db_connect()

        print(f" Проверяем пользователя: {login}")
        cur.execute("SELECT login FROM users WHERE login = %s", (login,))
        existing_user = cur.fetchone()

        if existing_user:
            print(f" Пользователь уже существует: {existing_user}")
            db_close(conn, cur)
            return render_template('lab5/register.html',
                                error="Такой пользователь уже существует")

        print(f" Добавляем пользователя: {login}")
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password_hash))
        conn.commit()

        print(f" Пользователь {login} добавлен в БД")

        db_close(conn, cur)

        return redirect(url_for('lab5.login'))

    except psycopg2.Error as e:
        print(f" Ошибка PostgreSQL: {e}")
        error_msg = "Ошибка доступа к базе данных. Таблица не доступна для записи."
        return render_template('lab5/register.html', error=error_msg)
    except Exception as e:
        print(f" Общая ошибка: {e}")
        return render_template('lab5/register.html', error=f'Ошибка: {str(e)}')

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error="Заполните все поля")

    try:
        conn, cur = db_connect()

        cur.execute("SELECT * FROM users WHERE login = %s", (login,))
        user = cur.fetchone()

        print(f"=== ОТЛАДКА ЛОГИНА ===")
        print(f"Логин из формы: {login}")
        print(f"Найден пользователь: {user}")

        if user:
            print(f"Хэш пароля из БД: {user['password']}")
            print(f"Длина хэша: {len(user['password'])}")

            password_valid = check_password_hash(user['password'], password)
            print(f"Пароль верный: {password_valid}")

        if user and password_valid:
            session['login'] = login
            session['user_id'] = user['id']
            db_close(conn, cur)
            print("УСПЕШНЫЙ ЛОГИН! Редирект на главную")
            return redirect(url_for('lab5.lab'))
        else:
            db_close(conn, cur)
            return render_template('lab5.login.html', error="Неверный логин или пароль")

    except psycopg2.Error as e:
        print(f" Ошибка PostgreSQL при входе: {e}")
        return render_template('lab5/login.html', error="Ошибка доступа к базе данных")
    except Exception as e:
        print(f" Общая ошибка при входе: {e}")
        return render_template('lab5/login.html', error=f'Ошибка: {str(e)}')

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    return redirect(url_for('lab5.lab'))

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'true'

    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните название и текст статьи')

    if len(title.strip()) == 0 or len(article_text.strip()) == 0:
        return render_template('lab5/create_article.html', error='Название и текст статьи не могут быть пустыми')   

    try:
        conn, cur = db_connect()

        cur.execute("SELECT id FROM users WHERE login = %s", (login,))
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return redirect(url_for('lab5.login'))
        
        user_id = user["id"]

        print(f"=== СОЗДАНИЕ СТАТЬИ ===")
        print(f"User ID: {user_id}")
        print(f"Title: {title}")
        print(f"Text length: {len(article_text)}")
        print(f"Is public: {is_public}")

        cur.execute("""
            INSERT INTO user_articles (user_id, title, article_text, is_public) 
            VALUES (%s, %s, %s, %s)
        """, (user_id, title, article_text, is_public))

        conn.commit()
        print(f" Статья '{title}' успешно добавлена в таблицу user_articles")
        
        db_close(conn, cur)
        print("=== РЕДИРЕКТ НА MY_ARTICLES ===")
        return redirect(url_for('lab5.my_articles')) 
    
    except psycopg2.Error as e:
        print(f" Ошибка PostgreSQL при создании статьи: {e}")
        return render_template('lab5/create_article.html', error=f'Ошибка базы данных: {str(e)}')
    except Exception as e:
        print(f" Общая ошибка при создании статьи: {e}")
        return render_template('lab5/create_article.html', error=f'Ошибка: {str(e)}')

@lab5.route('/lab5/my_articles')
def my_articles():
    """Показать статьи пользователя"""
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    try:
        conn, cur = db_connect()

        print(f"=== ЗАГРУЗКА СТАТЕЙ ===")
        print(f"Логин пользователя: {login}")

        cur.execute("""
            SELECT id, title, article_text, is_public, created_at
            FROM user_articles 
            WHERE user_id = (SELECT id FROM users WHERE login = %s)
            ORDER BY created_at DESC
        """, (login,))
        
        articles = cur.fetchall()
        
        db_close(conn, cur)

        print(f" Итого найдено статей: {len(articles)}")
        for article in articles:
            print(f"   - {article['title']} (ID: {article['id']}, Public: {article['is_public']})")

        return render_template('lab5/my_articles.html', articles=articles, username=login)
    
    except Exception as e:
        print(f" Ошибка при получении статей: {e}")
        return f"<h1>Ошибка</h1><p>Ошибка при загрузке статей: {str(e)}</p><a href='/lab5/'>На главную</a>"

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    """Редактирование статьи"""
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    try:
        conn, cur = db_connect()

        cur.execute("""
            SELECT ua.* 
            FROM user_articles ua 
            JOIN users u ON ua.user_id = u.id 
            WHERE ua.id = %s AND u.login = %s
        """, (article_id, login))
        
        article = cur.fetchone()
        
        if not article:
            db_close(conn, cur)
            return "Статья не найдена или у вас нет прав для её редактирования", 403

        if request.method == 'GET':
            db_close(conn, cur)
            return render_template('lab5/edit_article.html', article=article)

        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_public = request.form.get('is_public') == 'true'

        if not title or not article_text:
            return render_template('lab5/edit_article.html', article=article, error='Заполните название и текст статьи')

        cur.execute("""
            UPDATE user_articles 
            SET title = %s, article_text = %s, is_public = %s
            WHERE id = %s
        """, (title, article_text, is_public, article_id))

        conn.commit()
        db_close(conn, cur)

        return redirect(url_for('lab5.my_articles'))

    except Exception as e:
        print(f" Ошибка при редактировании статьи: {e}")
        return f"Ошибка при редактировании статьи: {str(e)}"

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    """Удаление статьи"""
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    try:
        conn, cur = db_connect()

        cur.execute("""
            SELECT ua.* 
            FROM user_articles ua 
            JOIN users u ON ua.user_id = u.id 
            WHERE ua.id = %s AND u.login = %s
        """, (article_id, login))
        
        article = cur.fetchone()
        
        if not article:
            db_close(conn, cur)
            return "Статья не найдена или у вас нет прав для её удаления", 403

        cur.execute("DELETE FROM user_articles WHERE id = %s", (article_id,))
        conn.commit()
        db_close(conn, cur)

        return redirect(url_for('lab5.my_articles'))

    except Exception as e:
        print(f" Ошибка при удалении статьи: {e}")
        return f"Ошибка при удалении статьи: {str(e)}"

@lab5.route('/lab5/list')
def list_redirect():
    """Редирект со старого URL на новый"""
    return redirect(url_for('lab5.my_articles'))