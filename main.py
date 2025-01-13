from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import init_models, User, Post
from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from pydantic import BaseModel

# Настройки подключения
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/pysqlalchemy"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
# init_models(engine)
session = SessionLocal()
print("Таблицы успешно созданы!")
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/create/{username}/{email}/{password}")
def create(username: str, email: str, password: str):
    new_user = User(username=username, email=email, password=password)
    session.add(new_user)
    session.commit()
    print("Пользователь добавлен!")
    return {"message": f"Created {username}!"}


@app.get("/read")
def search(username: str):
    user_to_find = session.query(User).filter(User.username == username).first()
    if user_to_find:
        user_to_find.email = "bob_new@example.com"
        session.commit()
        print("Пользователь найден")
        return {"message": f"You searched for: {username} and found {user_to_find}"}
    else:
        print("Пользователь не найден")
        return {"message": f"You searched for: {username} and nobody found"}


@app.get("/updateEmail")
def search(username: str):
    user_to_find = session.query(User).filter(User.username == username).first()
    if user_to_find:
        user_to_find.email = "bob_new@example.com"
        session.commit()
        print(f"Email обновлён: {user_to_find.email}")
        return {"message": f"You tried update: {username} and updated user is {user_to_find}"}
    else:
        print("Пользователь не найден.")
        return {"message": f"You tried to update for: {username} and nobody found"}

@app.get("/delete")
def search(username: str):
    user_to_delete = session.query(User).filter(User.username == username).first()
    if user_to_delete:
        # Удаление связанных постов
        session.query(Post).filter(Post.user_id == user_to_delete.id).delete()
        # Удаление самого пользователя
        session.delete(user_to_delete)
        session.commit()
        print("Пользователь и его посты удалены.")
        return {"message": f"You deleted: {username}"}
    else:
        print("Пользователь не найден.")
        return {"message": f"You tried to deleted: {username} and nobody found"}

# Маршруты для постов

@app.post("/posts/")
def create_post(title: str, content: str, user_id: int):
    post = Post(title=title, content=content, user_id=user_id)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@app.get("/posts/")
def read_posts():
    return session.query(Post).all()

# Обновление content у одного из постов
@app.patch("/posts/")
def update_post_content():
    print("\nОбновление контента поста с ID 1:")
    post = session.query(Post).filter(Post.id == 1).first()
    if post:
        post.content = "This is updated content for the first post."
        session.commit()
        print(f"Контент поста обновлён: {post.content}")
    else:
        print("Пост с ID 1 не найден.")

@app.delete("/posts/")
def delete_post_content(id: int):
    print(f"\nУдаление поста с ID {id}:")
    post_to_delete = session.query(Post).filter(Post.id == id).first()
    if post_to_delete:
        session.delete(post_to_delete)
        session.commit()
        print("Пост удалён.")
    else:
        print(f"Пост с ID {id} не найден.")