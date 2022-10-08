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

# download stopwords corpus, you need to run it once
import nltk
nltk.download("stopwords")
#--------#

from matplotlib.colors import rgb2hex

from nltk.corpus import stopwords
import pymorphy2
from string import punctuation

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
show_news = Blueprint('show_news', __name__)


LINKS_PER_PAGE = 10

@show_news.route('/news', methods=['post', 'get'])
def show_news_func():
    try:
        try:
            get_cat_id = int(flask.request.args.get('cat_id'))
        except:
            get_cat_id = 0
        cat_tpl = ""
        for cat_item in config.wtb_categories:
            cat_name = cat_item["name"]
            wtb_cat_id = int(cat_item["id"])
            if wtb_cat_id == get_cat_id:
                cat_tpl += f"<b>{cat_name}</b> ~ "
            else:
                cat_tpl += f"<a href='/news?cat_id={wtb_cat_id}'>{cat_name}</a> ~ "

        try:
            get_user_id = int(flask.request.args.get('user_id'))
        except:
            get_user_id = 0

        
        get_mode = str(flask.request.args.get('mode'))
        print(get_mode)
        if get_mode == str(None):
            get_mode = "all"
        print(get_mode)


        mode_tpl = ""
        if (get_mode == "all"):
            mode_tpl = f"<b>All</b> | <a href='/news?user_id={get_user_id}&mode=recc'>Recc</a>"
        else:
            mode_tpl = f"<a href='/news?user_id={get_user_id}&mode=all'>All</a> | <b>Recc</b>"

        menu_tpl = f"<a href='/log'>Log</a> ~ <a href='/crauler_news'>Crauler</a> ~ <a href='/parser_news'>Parser</a> ~ <a href='/users'>Users</a> ~ <b>Digest</b> ~ <a href='/trends'>Trends</a> ~ <a href='/inside'>InSide</a> ~ <br><a href='/teach_news?user_id={get_user_id}'>Teach</a>; {mode_tpl}"
        header_tpl = "<center><h2>NPPK32. Development Platform MORE.Tech 4.0 VTB Hack</h2></center>"

        users_tpl = ""
        for user_item in config.wtb_users:
            user_name = user_item["name"]
            user_desc = user_item["desc"]
            wtb_user_id = int(user_item["id"])
            if wtb_user_id == get_user_id:
                users_tpl += f"<b><font color='magenta'>{user_name}</font></b><br>{user_desc}<br><br>"
            else:
                users_tpl += f"<a href='/news?user_id={wtb_user_id}&mode={get_mode}'>{user_name}</a><br>{user_desc}<br><br>"

        #модель
        try:
            get_model = str(flask.request.args.get('model'))
        except:
            get_model = 1
        
        # пагинация
        try:
            get_page = int(flask.request.args.get('page'))
        except:
            get_page = 1


        
        
        news_tpl = ""
        desc = ""
        links = db_session.query(News).filter(News.status == 1).order_by(News.parse_date.desc())

        from_links = (get_page-1) * LINKS_PER_PAGE
        to_links = get_page * LINKS_PER_PAGE
        r = 1
        g = 1
        b = 1
        if (get_mode == "all"):
            for link in links[from_links:to_links]:
                if (len(link.title) > 3) :
                    title = link.title
                    dt_object = datetime.fromtimestamp(link.parse_date)

                    # разбиваем текст на предложения и берем первые 4
                    desc_list = str(link.text).split(".")[:4]
                    desc = ".".join(desc_list)
                
                    donor_name = str(link.donor).split('/')
                    favicon_filename = BASE_DIR + f"favicon.ico"
                    try:
                        favicon_filename = BASE_DIR + f"/favicon/{donor_name[2]}.ico"
                    except:
                        pass

                    if (Path(favicon_filename).is_file()):
                        favicon_url = "https://search.steelfeet.ru/favicon/" + f"{donor_name[2]}.ico"
                    else:
                        favicon_url = "https://search.steelfeet.ru/favicon/favicon.ico"
                    
                    
                    #фон случайным цветом (/3 - чтобы не нормализовывать)
                    r -= random.randint(0, 255) / 255 / 15
                    g -= random.randint(0, 255) / 255 / 15
                    b -= random.randint(0, 255) / 255 / 15
                    cat_accuracies = [r, g, b]
                    #print(cat_accuracies)
                    hex_color = rgb2hex(cat_accuracies)
                    
                    news_tpl += f"<div style='background-color: {hex_color}; padding: 5px;';><img width='16' src='" + favicon_url + "'> <b><a href='/go?id=" + str(link.id) + f"&model={get_model}&user_id={get_user_id}' target='_new'>" + title + "</a></b><br>" + desc + "<br>Дата: "+ str(dt_object) + "; Модель: </div><br><br>"

                    # записываем просмотренные новости
                    new_user_action = UsersAction(user_id=get_user_id, show_id=int(link.id), click_id=0, model="")
                    db_session.add(new_user_action)

   
        else:
            #загружаем классификаторы
            import joblib
            vectorizer = joblib.load(os.path.join(BASE_DIR, "models", "users", str(get_user_id), "vectorizer.pkl"))
            tfidf_transformer = joblib.load(os.path.join(BASE_DIR, "models", "users", str(get_user_id), "tfidf_transformer.pkl"))
            clf = joblib.load(os.path.join(BASE_DIR, "models", "users", str(get_user_id), "MultinomialNB.pkl"))



            #оставляем, чтобы было наглядно видно, сколько нерелевантных отсеялось
            for link in links[from_links:to_links]:
                if (len(link.title) > 3) :
                    lemmas = link.lemmas # title уже там, добавлено при парсинге
                    X_new = vectorizer.transform([lemmas])
                    X_new_tfidf = tfidf_transformer.transform(X_new)
                    predict_proba = clf.predict_proba(X_new_tfidf)[0]
                    print(predict_proba)
                    
                    title = link.title
                    dt_object = datetime.fromtimestamp(link.parse_date)

                    # разбиваем текст на предложения и берем первые 4
                    desc_list = str(link.text).split(".")[:4]
                    desc = ".".join(desc_list)
                
                    donor_name = str(link.donor).split('/')
                    favicon_filename = BASE_DIR + f"favicon.ico"
                    try:
                        favicon_filename = BASE_DIR + f"/favicon/{donor_name[2]}.ico"
                    except:
                        pass

                    if (Path(favicon_filename).is_file()):
                        favicon_url = "https://search.steelfeet.ru/favicon/" + f"{donor_name[2]}.ico"
                    else:
                        favicon_url = "https://search.steelfeet.ru/favicon/favicon.ico"
                    
                    
                    if (predict_proba[0] < 0.5):
                        r = 1
                        g = 1
                        b = 1
                    else:
                        r = 0.5
                        g = 0.5
                        b = 0.5

                    cat_accuracies = [r, g, b]
                    #print(cat_accuracies)
                    hex_color = rgb2hex(cat_accuracies)
                    
                    news_tpl += f"<div style='background-color: {hex_color}; padding: 5px;';><img width='16' src='" + favicon_url + "'> <b><a href='/go?id=" + str(link.id) + f"&model={get_model}&user_id={get_user_id}' target='_new'>" + title + "</a></b><br>" + desc + "<br>Дата: "+ str(dt_object) + "; Модель: </div><br><br>"

                    # записываем просмотренные новости
                    new_user_action = UsersAction(user_id=get_user_id, show_id=int(link.id), click_id=0, model="")
                    db_session.add(new_user_action)

        db_session.commit()
        db_session.close()
        
        # пагинация
        pages_tpl = ""
        from_pages = get_page-5
        if from_pages < 1:
            from_pages = 1
        to_pages = get_page + 5
        # дополняем общую сумму страниц до 10 (для красоты)
        n_pages = to_pages - from_pages
        to_pages = to_pages + (10 - n_pages)

        for i in range(from_pages, to_pages):
            if i == get_page:
                pages_tpl += f"<b> {i} | </b>"
            else:
                pages_tpl += f"<a href=/news?model={get_model}&user_id={get_user_id}&page={i}&mode={get_mode}> {i} | </a>"

        

        resp = flask.make_response(flask.render_template('news.html', menu=menu_tpl, header=header_tpl, users=users_tpl, news=news_tpl, pages=pages_tpl))
        return resp
        
    
    
    except: # общий
        status = str(traceback.format_exc())
        return "Ошибка: <pre>"+ str(status) + "</pre><br>"



@show_news.route('/go', methods=['post', 'get'])
def go_func():
    user_id = int(flask.request.args.get('user_id'))
    click_id = int(flask.request.args.get('id'))
    model = str(flask.request.args.get('model'))

    # записываем новост, на которую перешли
    new_user_action = UsersAction(user_id=user_id, show_id=0, click_id=click_id, model=model)
    db_session.add(new_user_action)

    # переходим на новость
    current_news = db_session.query(News).filter(News.id == click_id).first()
    url = current_news.href

    db_session.commit()
    db_session.close()
    resp = flask.make_response(flask.redirect(url, code=302))
    return resp
