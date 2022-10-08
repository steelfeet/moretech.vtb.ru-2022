# -*- encoding: utf-8 -*-
# 
import os

import traceback
import random, time
from datetime import datetime
import requests
from requests.exceptions import ProxyError

from pathlib import Path
from urllib.parse import urlparse, unquote
import tldextract

import sys
# директория файла
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# иначе не видит этот файл
# https://stackoverflow.com/questions/67631/how-do-i-import-a-module-given-the-full-path
sys.path.append(BASE_DIR)
import config, edufunc


#декларативное определение
from sqlalchemy import Column, Integer, String, Text, create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from sqlalchemy import and_

#Инициализация SQLLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'main.db?check_same_thread=False')
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
db_session = Session()
from db import News, Log, Users, UsersAction

import flask
from flask import Blueprint
trends = Blueprint('trends', __name__)




@trends.route('/trends', methods=['post', 'get'])
def trends_func():
        menu_tpl = f"<a href='/log'>Log</a> ~ <a href='/crauler_news'>Crauler</a> ~ <a href='/parser_news'>Parser</a> ~ <a href='/users'>Users</a> ~ <a href='/news'>Digest</a> ~ <b>Trends</b> ~ <a href='/inside'>InSide</a> ~  "
        header_tpl = "<center><h2>NPPK32. Development Platform MORE.Tech 4.0 VTB Hack</h2></center>"

        content_tpl = """
        3. Для каждой новости ищем #хештеги. (Леммы, которые встречаются максимально часто в одних, и минимально в других новостях, кластеризуем новости). https://dev-gang.ru/article/analiz-trendov-v-tvittere-s-ispolzovaniem-python-q1m4ymsf4v/<br>

        2. Классифицируем весь мешок слов за день. По суммарной predict_proba ищем тренды (https://habr.com/ru/post/207160/)<br>
        
        1.Простая ежедневная статистика по каждой лемме в течение года. Для каждой роли тренды свои. Выделяем, если аппроксимация методом наименьших квадратов дает за неделю (?) коэффициент наклона прямой больше 45 градусов. И из новостей и из форумов. <i>Возможно добавить общий тренд настроения новостей по лемме.</i>"""

        resp = flask.make_response(flask.render_template('index.html', menu=menu_tpl, header=header_tpl, content=content_tpl))
        return resp





