import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config

CONNSTR = f'postgresql://{config.get("DB_USER")}:{config.get("DB_PASSWORD")}@{config.get("DB_HOST")}/{config.get("DB_NAME")}'

engine = create_engine(CONNSTR)
SessionLocal = sessionmaker(bind=engine,autocommit=False, autoflush=False)

Base = declarative_base()

# Dependency for api routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()