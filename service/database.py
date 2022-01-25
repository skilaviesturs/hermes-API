# database.py
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import sqlite3 as sl
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings


# SQLITE3 part
# DBNAME = settings.dbname

# SQLALCHEMY part
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    '''
    Dependency
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def execute_sql(*args):
    '''
    Izpilda sql pieprasījumu datu bāzē\n
    1st argument: sql expression;
    2nd argument: 1st value
    3rd argument: 2nd value
    '''
    sql_expresion = args[0]

    while True:
        try:
            conn = psycopg2.connect(host={settings.database_hostname}, port={settings.database_port},
                                    database={settings.database_name}, user={settings.database_username}, 
                                    password={settings.database_password}, cursor_factory=RealDictCursor)
            cur = conn.cursor()
            print("Database connections was successful.")
            break
        except Exception as error:
            print("Connection to database failed!")
            print("Error: ", error)

    with conn:
        if len(args) == 1:
            cur.execute(sql_expresion)
        elif len(args) == 2:
            cur.execute(sql_expresion, (args[1],))
        else:
            cur.execute(sql_expresion, (args[1], args[2]))
    result = cur.fetchall()
    conn.commit()
    conn.close()

    return result
