from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import init_models, User, Post

if __name__ == "__main__":
    # Настройки подключения
    DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/pysqlalchemy"
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(bind=engine)
    init_models(engine)
    #session = SessionLocal()
    print("Таблицы успешно созданы!")
