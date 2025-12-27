from models import db
from flask import Flask

def init_db():
    with app.app_context():
        db.create_all()
        
        # Создаем администратора
        from models import User
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Администратор создан: admin / admin123")
        
        # Создаем тестовых пользователей
        for i in range(5):
            username = f'testuser{i+1}'
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(username=username)
                user.set_password('password123')
                db.session.add(user)
        
        db.session.commit()