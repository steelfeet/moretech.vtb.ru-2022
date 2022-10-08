# -*- encoding: utf-8 -*-
# 
from flask import Flask, Blueprint
import os, traceback, sys, random


#декларативное определение
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


application = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

#Инициализация SQLLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'main.db')
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
Base = declarative_base()

#Инициализация Blueprint 
from Log import log
application.register_blueprint(log)

from Crauler_news import сrauler_news
application.register_blueprint(сrauler_news)

from Parser_news import parser_news
application.register_blueprint(parser_news)

from Show_news import show_news
application.register_blueprint(show_news)

from Teach import teach_news
application.register_blueprint(teach_news)

from Users import users
application.register_blueprint(users)

from Trends import trends
application.register_blueprint(trends)

from Inside import inside
application.register_blueprint(inside)


# Создаем файловую структуру
try:
   os.mkdir(os.path.join(BASE_DIR, "favicon"))
except:
   pass
try:
   os.mkdir(os.path.join(BASE_DIR, "robots.txt"))
except:
   pass
try:
   os.mkdir(os.path.join(BASE_DIR, "html"))
except:
   pass






@application.route("/")
def hello():
   
   return "<h1 style='color:blue'>Hello There! test 4</h1>"








 

if __name__ == "__main__":
   application.run(host='0.0.0.0', debug=True)
