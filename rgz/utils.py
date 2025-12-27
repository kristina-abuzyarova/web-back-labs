import sqlite3
import bcrypt
import re
from datetime import datetime
from contextlib import contextmanager
from config import Config

class Database:
    """Класс для работы с базой данных"""
    
    @staticmethod
    @contextmanager
    def get_connection():
        """Контекстный менеджер для подключения к БД"""
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    @staticmethod
    def execute_query(query, params=(), fetch_one=False, fetch_all=False):
        """Выполнение SQL запроса"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = cursor.lastrowid
            
            conn.commit()
            return result

class Validator:
    """Класс для валидации данных"""
    
    @staticmethod
    def validate_username(username):
        """Валидация имени пользователя"""
        if not username:
            return False, "Имя пользователя не может быть пустым"
        
        if len(username) < Config.USERNAME_MIN_LENGTH:
            return False, f"Имя пользователя должно быть не менее {Config.USERNAME_MIN_LENGTH} символов"
        
        if len(username) > Config.USERNAME_MAX_LENGTH:
            return False, f"Имя пользователя должно быть не более {Config.USERNAME_MAX_LENGTH} символов"
        
        # Проверка на латинские буквы, цифры и подчеркивание
        pattern = r'^[a-zA-Z0-9_]+$'
        if not re.match(pattern, username):
            return False, "Имя пользователя может содержать только латинские буквы, цифры и подчеркивание"
        
        return True, ""
    
    @staticmethod
    def validate_password(password):
        """Валидация пароля"""
        if not password:
            return False, "Пароль не может быть пустым"
        
        if len(password) < Config.PASSWORD_MIN_LENGTH:
            return False, f"Пароль должен быть не менее {Config.PASSWORD_MIN_LENGTH} символов"
        
        # Проверка на русские буквы
        if re.search(r'[а-яА-ЯёЁ]', password):
            return False, "Пароль не должен содержать русские буквы"
        
        # Проверка на наличие хотя бы одной буквы и цифры
        if not re.search(r'[a-zA-Z]', password):
            return False, "Пароль должен содержать хотя бы одну букву"
        
        if not re.search(r'\d', password):
            return False, "Пароль должен содержать хотя бы одну цифру"
        
        return True, ""
    
    @staticmethod
    def validate_initiative_title(title):
        """Валидация заголовка инициативы"""
        if not title:
            return False, "Заголовок не может быть пустым"
        
        title = title.strip()
        
        if len(title) < Config.INITIATIVE_TITLE_MIN:
            return False, f"Заголовок должен быть не менее {Config.INITIATIVE_TITLE_MIN} символов"
        
        if len(title) > Config.INITIATIVE_TITLE_MAX:
            return False, f"Заголовок должен быть не более {Config.INITIATIVE_TITLE_MAX} символов"
        
        return True, ""
    
    @staticmethod
    def validate_initiative_content(content):
        """Валидация содержания инициативы"""
        if not content:
            return False, "Содержание не может быть пустым"
        
        content = content.strip()
        
        if len(content) < Config.INITIATIVE_CONTENT_MIN:
            return False, f"Содержание должно быть не менее {Config.INITIATIVE_CONTENT_MIN} символов"
        
        if len(content) > Config.INITIATIVE_CONTENT_MAX:
            return False, f"Содержание должно быть не более {Config.INITIATIVE_CONTENT_MAX} символов"
        
        return True, ""

class PasswordHasher:
    """Класс для хеширования паролей"""
    
    @staticmethod
    def hash_password(password):
        """Хеширование пароля с использованием bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed
    
    @staticmethod
    def check_password(password, hashed):
        """Проверка пароля"""
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed)