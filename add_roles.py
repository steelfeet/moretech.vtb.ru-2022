
import os, traceback

#декларативное определение
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker


#Инициализация SQLLite
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'main.db')
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
db_session = Session()
from db import Roles

new_role = Roles(
    name = "IT", 
)
db_session.add(new_role)

new_role = Roles(
    name = "Buh", 
)
db_session.add(new_role)


db_session.commit()
db_session.close()

