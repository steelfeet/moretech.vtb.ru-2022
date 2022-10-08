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
teach_news = Blueprint('teach_news', __name__)




@teach_news.route('/teach_news', methods=['post', 'get'])
def teach_news_func():
    try:
        user_id = flask.request.args.get('user_id')
        
        menu_tpl = f"<a href='/log'>Log</a> ~ <a href='/crauler_news'>Crauler</a> ~ <a href='/parser_news'>Parser</a> ~ <a href='/news'>Digest</a> <br> User ID: {user_id} ~ <b>Teach</b>; "
        header_tpl = "<center><h2>NPPK32. Development Platform MORE.Tech 4.0 VTB Hack</h2></center>"


        content_tpl = ""

        # преобразуем в формат для обучения
        X_train = []
        X_train_1 = [] # клики
        y_train = []
        all_click_ids = []
        all_show_ids = []

        user_actions = db_session.query(UsersAction).filter(UsersAction.user_id == user_id).order_by(UsersAction.id.desc())
        for user_action in user_actions:
            news_id = 0
            if (user_action.click_id > 0):
                news_id = user_action.click_id
                if (news_id not in (all_click_ids)):
                    y_train.append(1)
                    all_click_ids.append(news_id)
                    new = db_session.query(News).filter(News.id == news_id).first()
                    X_train.append(new.lemmas)
                    X_train_1.append(new.lemmas)

        for user_action in user_actions:
            news_id = 0
            if (user_action.show_id > 0):
                news_id = user_action.show_id
                if (news_id not in (all_click_ids)) and (news_id not in (all_show_ids)):
                    y_train.append(0)
                    all_show_ids.append(news_id)
                    new = db_session.query(News).filter(News.id == news_id).first()
                    X_train.append(new.lemmas)


        content_tpl += f"Размер обучающей выборки: {len(X_train)}; Положительных: {len(X_train_1)}<br>"

        content_tpl += f"Векторизация<br>"
        # векторизация
        from sklearn.feature_extraction.text import CountVectorizer        
        vectorizer = CountVectorizer()
        X_train_counts = vectorizer.fit_transform(X_train)

        content_tpl += f"TfidfTransformer<br>"
        # TfidfTransformer - подсчет статистики слов в массиве текстов
        from sklearn.feature_extraction.text import TfidfTransformer
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

        # Классификатор - MultinomialNB
        content_tpl += f"MultinomialNB<br>"
        from sklearn.naive_bayes import MultinomialNB
        clf = MultinomialNB().fit(X_train_tfidf, y_train)

        try:
            os.mkdir(os.path.join(BASE_DIR, "models", "users", str(user_id)))
        except:
            pass
        import joblib
        joblib.dump(vectorizer, os.path.join(BASE_DIR, "models", "users", str(user_id), "vectorizer.pkl"), compress=9)
        joblib.dump(tfidf_transformer, os.path.join(BASE_DIR, "models", "users", str(user_id), "tfidf_transformer.pkl"), compress=9)
        joblib.dump(clf, os.path.join(BASE_DIR, "models", "users", str(user_id), "MultinomialNB.pkl"), compress=9)


        """
        from sklearn.neighbors import KNeighborsClassifier
        clf = KNeighborsClassifier(n_neighbors=1).fit(X_train_tfidf, y_train)

        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import make_pipeline
        from sklearn.svm import SVC
        clf = make_pipeline(StandardScaler(with_mean=False), SVC(gamma='auto')).fit(X_train_tfidf, y_train)

        from sklearn.linear_model import LogisticRegression
        clf = LogisticRegression(random_state=0).fit(X_train_tfidf, y_train)
        """






        resp = flask.make_response(flask.render_template('index.html', menu=menu_tpl, header=header_tpl, content=content_tpl))
        return resp
    except:
        status = str(traceback.format_exc())
        return "Ошибка: <pre>"+ str(status) + "</pre><br>"


