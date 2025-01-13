from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import init_models, User, Post

if __name__ == "__main__":
    # Настройки подключения
    DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/pysqlalchemy"
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(bind=engine)
    init_models(engine)
    session = SessionLocal()
    print("Таблицы успешно созданы!")

    # Создание сессии
    session = SessionLocal()

    # Добавление пользователей через модели
    users = [
        User(username="Alice", email="alice@example.com", password="password123"),
        User(username="Bob", email="bob@example.com", password="securepass456"),
        User(username="Charlie", email="charlie@example.com", password="mypassword789"),
    ]

    # Добавляем пользователей в сессию
    session.add_all(users)

    # Сохраняем изменения
    session.commit()
    print("Пользователи добавлены!")

    # Добавление постов через модели
    posts = [
        Post(title="First Post", content="This is Alice's first post", user_id=users[0].id),
        Post(title="Second Post", content="This is Bob's first post", user_id=users[1].id),
        Post(title="Third Post", content="This is Charlie's first post", user_id=users[2].id),
        Post(title="Another Post", content="Alice writes another post", user_id=users[0].id),
    ]

    # Добавляем посты в сессию
    session.add_all(posts)

    # Сохраняем изменения
    session.commit()
    print("Посты добавлены!")

    # Закрываем сессию
    session.close()

