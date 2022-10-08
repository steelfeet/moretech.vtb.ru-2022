# -*- encoding: utf-8 -*-
# 
import os, json, traceback

import sys
# директория файла
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# иначе не видит этот файл
# https://stackoverflow.com/questions/67631/how-do-i-import-a-module-given-the-full-path
sys.path.append(BASE_DIR)

import config

from datetime import datetime


#декларативное определение
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc

from db import News, Log

#Инициализация SQLLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'main.db?check_same_thread=False')
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
db_session = Session()

import flask
from flask import Blueprint
log = Blueprint('log', __name__)


@log.route('/log', methods=['post', 'get'])
def log_func():
    menu_tpl = "<b>Log</b> ~ <a href='/crauler_news'>Crauler</a> ~ <a href='/parser_news'>Parser</a> ~ <a href='/users'>Users</a> ~ <a href='/news'>Digest</a> ~ <a href='/trends'>Trends</a> ~ <a href='/inside'>InSide</a> ~ "
    header_tpl = "<center><h2>NPPK32. Development Platform 4 VTB Hack. Case: #Data.</h2></center>"

    
    status0_n = db_session.query(News).filter(News.status == 0).count()
    status1_n = int(db_session.query(News).filter(News.status == 1).count())
    status2_n = int(db_session.query(News).filter(News.status == 2).count())

    content_tpl = ""
    content_tpl += f"<p>Ссылки со статусом 0 (не парсенные): {status0_n}<br>Ссылки со статусом 1 (парсенные): {status1_n + status2_n}"

    content_tpl += "<table align=left cellspacing=8 cellpading=2 border=0><tr align=center><td>Date</td><td>Action</td><td>Donor</td><td>Status</td></tr>"
    log = db_session.query(Log).order_by(desc(Log.id))[0:50]
    for item in log:
        date_time = datetime.fromtimestamp(item.time)
        s_date = date_time.strftime("%d %m %Y %H:%M:%S")
        content_tpl += f"<tr align=center valign=top><td><nobr>{s_date}</nobr></td><td>{item.action}</td><td>{item.donor}</td><td align=left>{item.status}</td></tr>"


    return flask.render_template('index.html', menu=menu_tpl, header=header_tpl, content=content_tpl )

