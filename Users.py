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
users = Blueprint('users', __name__)




@users.route('/users', methods=['post', 'get'])
def users_func():
    try:
        try:
            get_cat_id = int(flask.request.args.get('cat_id'))
        except:
            get_cat_id = 0
        cat_tpl = "<a href='/users?cat_id=0'>All</a> ~ "
        for cat_item in config.wtb_categories:
            cat_name = cat_item["name"]
            wtb_cat_id = int(cat_item["id"])
            if wtb_cat_id == get_cat_id:
                cat_tpl += f"<b>{cat_name}</b> ~ "
            else:
                cat_tpl += f"<a href='/users?cat_id={wtb_cat_id}'>{cat_name}</a> ~ "


        menu_tpl = f"<a href='/log'>Log</a> ~ <a href='/crauler_news'>Crauler</a> ~ <a href='/parser_news'>Parser</a> ~ <b>Users</b> ~ <a href='/news'>Digest</a> ~ <a href='/trend'>Trands</a> ~ <a href='/insight'>InSide</a> ~ <br> Categories: {cat_tpl} "
        header_tpl = "<center><h2>NPPK32. Development Platform MORE.Tech 4.0 VTB Hack</h2></center>"


        content_tpl = ""
        try:
            get_user_id = int(flask.request.args.get('user_id'))
        except:
            get_user_id = 0
        for user_item in config.wtb_users:
            user_name = user_item["name"]
            user_desc = user_item["desc"]
            user_text = user_item["text"]
            wtb_user_id = int(user_item["id"])
            content_tpl += f"<img width='120' src='https://search.steelfeet.ru/users/{wtb_user_id}.jpg'><br>{user_name} - {user_desc}<br>{user_text}<br><br>"


        resp = flask.make_response(flask.render_template('index.html', menu=menu_tpl, header=header_tpl, content=content_tpl))
        resp.set_cookie('user_id', str(get_user_id))
        return resp
    except:
        status = str(traceback.format_exc())
        return "Ошибка: <pre>"+ str(status) + "</pre><br>"





