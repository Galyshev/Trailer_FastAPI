import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

# для локалки поменять порт на 5436 !!! ДЛЯ ДОКЕРА 5432
engine = create_engine(f'postgresql+psycopg2://{os.environ.get("DB_USER", "postgres")}:{os.environ.get("DB_PASSWORD", "postgres")}@'
                       f'{os.environ.get("DB_HOST", "127.0.0.1")}:5436/trailer_db')

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from bd import model_bd
    Base.metadata.create_all(bind=engine)