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
