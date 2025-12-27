import sqlite3
import random
from datetime import datetime, timedelta
import os
import hashlib

def simple_hash(password):
    """Простое хеширование для тестов (В ПРОДУКЦИИ ИСПОЛЬЗУЙТЕ BCRYPT!)"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_database():
    """Создание базы данных и таблиц"""
    
    # Создаем папку database если её нет
    os.makedirs('database', exist_ok=True)
    
    # Подключаемся к базе данных
    conn = sqlite3.connect('database/initiatives.db')
    cursor = conn.cursor()
    
    print(" Создание таблиц...")
    
    # 1. Таблица пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 2. Таблица инициатив
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS initiatives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        votes INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # 3. Таблица голосов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        initiative_id INTEGER NOT NULL,
        vote_value INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, initiative_id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (initiative_id) REFERENCES initiatives (id)
    )
    ''')
    
    print(" Таблицы созданы")
    return conn, cursor

def create_admin_user(cursor):
    """Создание администратора"""
    
    print(" Создание администратора...")
    
    # Используем простое хеширование (для тестов!)
    admin_password = simple_hash('AdminPass123!')
    
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        ('admin', admin_password, 1)
    )
    
    print(" Администратор создан")
    print("   Логин: admin")
    print("   Пароль: AdminPass123! (в БД хранится хеш)")

def create_test_users(cursor, count=10):
    """Создание тестовых пользователей"""
    
    print(f"Создание {count} тестовых пользователей...")
    
    user_ids = []
    for i in range(1, count + 1):
        username = f'user{i}'
        password = simple_hash(f'password{i}')
        
        cursor.execute(
            "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        
        # Получаем ID созданного пользователя
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            user_ids.append(result[0])
    
    print(f"Создано {count} тестовых пользователей")
    print("   Логины: user1, user2, ..., user10")
    print("   Пароли: password1, password2, ..., password10")
    return user_ids

def create_test_initiatives(cursor, user_ids, count=120):
    """Создание тестовых инициатив"""
    
    print(f" Создание {count} тестовых инициатив...")
    
    # Тематики инициатив
    themes = [
        ("Улучшение освещения", "Установить дополнительные фонари в кампусе"),
        ("Ремонт корпусов", "Отремонтировать старые учебные корпуса"),
        ("Новые компьютеры", "Обновить оборудование в компьютерных классах"),
        ("Библиотека 24/7", "Сделать библиотеку круглосуточной"),
        ("Спортивный зал", "Построить новый спортивный зал"),
        ("Wi-Fi покрытие", "Улучшить Wi-Fi во всех зданиях"),
        ("Столовые", "Улучшить качество питания в столовых"),
        ("Парковки", "Создать больше парковок для велосипедов"),
        ("Курсы", "Ввести дополнительные курсы по программированию"),
        ("Мероприятия", "Чаще проводить студенческие мероприятия")
    ]
    
    descriptions = [
        "Это улучшит безопасность в вечернее время.",
        "Студенты смогут учиться в более комфортных условиях.",
        "Современное оборудование необходимо для качественного образования.",
        "Студенты смогут заниматься в любое время суток.",
        "Здоровый образ жизни важен для каждого студента.",
        "Стабильный интернет необходим для учебы и исследований.",
        "Качественное питание важно для здоровья студентов.",
        "Экологичный транспорт должен быть доступен каждому.",
        "Дополнительные навыки помогут в будущей карьере.",
        "Мероприятия помогают студентам общаться и развиваться."
    ]
    
    for i in range(count):
        theme_idx = i % len(themes)
        theme_title, theme_desc = themes[theme_idx]
        
        title = f"{theme_title} #{i+1}"
        content = f"{theme_desc}. {descriptions[theme_idx]}"
        user_id = random.choice(user_ids)
        
        days_ago = random.randint(1, 60)
        created_at = datetime.now() - timedelta(days=days_ago)
        
        votes = random.randint(-5, 50)
        
        cursor.execute('''
        INSERT INTO initiatives (title, content, user_id, created_at, votes)
        VALUES (?, ?, ?, ?, ?)
        ''', (title, content, user_id, created_at, votes))
        
        if (i + 1) % 20 == 0:
            print(f"   Создано {i+1}/{count} инициатив")
    
    print(f" Создано {count} тестовых инициатив")

def main():
    """Основная функция"""
    
    print("=" * 50)
    print(" ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ (упрощенная версия)")
    print("=" * 50)
    
    try:
        conn, cursor = create_database()
        create_admin_user(cursor)
        user_ids = create_test_users(cursor, 10)
        create_test_initiatives(cursor, user_ids, 120)
        
        conn.commit()
        conn.close()
        
        print("=" * 50)
        print(" БАЗА ДАННЫХ СОЗДАНА УСПЕШНО!")
        print("=" * 50)
        
        # Создаем requirements.txt
        with open('requirements.txt', 'w') as f:
            f.write("Flask==2.3.3\n")
        
        print("\nФайл requirements.txt создан")
        print("\nСодержимое папки проекта:")
        for item in os.listdir('.'):
            print(f"   • {item}")
        if os.path.exists('database'):
            print(f"   • database/ (папка с БД)")
        
    except Exception as e:
        print(f" Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()