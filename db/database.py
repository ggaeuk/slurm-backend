from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_SETTINGS


database = DATABASE_SETTINGS['database']
server = DATABASE_SETTINGS['server']
port = DATABASE_SETTINGS['port']
schema = DATABASE_SETTINGS['schema']
user = DATABASE_SETTINGS['user']
password = DATABASE_SETTINGS['password']

SQLALCHEMY_DATABASE_URL = database + "://" + user + ":" + password + "@" + server + ":" + port + "/" + schema


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()