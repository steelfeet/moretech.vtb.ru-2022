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
inside = Blueprint('inside', __name__)




@inside.route('/inside', methods=['post', 'get'])
def insidez_func():
        menu_tpl = f"<a href='/log'>Log</a> ~ <a href='/crauler_news'>Crauler</a> ~ <a href='/parser_news'>Parser</a> ~ <a href='/users'>Users</a> ~ <a href='/news'>Digest</a> ~ <a href='/trends'>Trends</a> ~ <b>InSide</b> ~  "
        header_tpl = "<center><h2>NPPK32. Development Platform MORE.Tech 4.0 VTB Hack</h2></center>"

        content_tpl = """Алгоритмы поиска инсайдов: <br>1. Анализируем временной ряд трендов (и / или простой статистики лемм) в поисках аномалий (например https://habr.com/ru/post/588320/). <br>2. Обучаем классификатор на данных (и из новостей и из форумов и тренды и настроение текстов форумов) которые ПРЕДШЕСТВОВАЛИ аномалии (). + Все открытые данные, до которых дотянемся: Правовые акты!, курсы валют, криптовалют, биржа и пр. Catboost должен суметь.<br>
        
        2. Выделяем предложения, в которых инсайт. Анализируем их.

        
        <h2>Список открытых источников</h2>
        https://github.com/kbondar17/pravo.gov-api
        
@opendatarussiachat
https://github.com/abnegantes/open-russian-data
Список внешних данных
https://docs.google.com/spreadsheets/d/1yv-OWO1E1uJcvZKaRQOAHsFy8wnJ0b2CBxbLS6-08vw/edit?usp=sharing




на сайте www.list-org.com/ ищем по ИНН компанию (ИНН предоставляю), в разделе "Виды деятельности" есть кнопка, 
чтобы найти похожие компании. Найденные результаты нужно будет заносить в таблицу.



Полный слепок всех данных из портала Data.gov.ru выложен на Хаб открытых данных [1]. Это архив в 13ГБ, после распаковки 29 ГБ.
Слепок этих данных создавался в архивационных целях, для Национального цифрового архива, но также может быть полезен всем исследователям открытых данных в России, 
тем кто ищет большие данные для собственных задач и так далее.
Ссылки:
[1] https://hubofdata.ru/dataset/datagovru-20220202
D:\external_data\datagovru-20220202

https://www.kaggle.com/c/birdclef-2022
D:\external_data\birdclef-2022


https://habr.com/ru/news/t/653647/
D:\external_data\cdek



ЕГРЮЛ, ЕГРИП в виде архивов ФНС, csv, xml, json (API) и анализ данных
https://habr.com/ru/company/itsoft/blog/656563/

Парсинг исторических данных с Google Scholar используя Python
https://habr.com/ru/post/647873/

Источники открытых данных в России
https://dorozhnij.com/opendata?fbclid=IwAR1kg2mvFAGvgexxs3Y9kzKw7ulgV6m8WmlI-KA9VWrau0dTzcJCtAdDbe8

ЕГРЮЛ, доходы и расходы, налоги, количество сотрудников в XML и JSON бесплатно
https://habr.com/ru/company/itsoft/blog/650291/


Финансы
https://www.investing.com/
http://finam.ru

https://tickstory.com/ru/
которая скачивает исторические данные биржевых котировок, после чего их можно сохранять в любом удобном формате

ну можно с помощью этого - https://github.com/nerevar/stock_prices
с московской биржи те же котировки взять

http://www.finmarket.ru/

Официальная статистика Росстата, в частности по пром. производству
https://rosstat.gov.ru/enterprise_industrial

Курсы вылют от ЦБ РФ
http://www.cbr.ru/currency_base/

Статистическая база данных ЕЭК ООН по экономике
https://w3.unece.org/PXWeb2015/pxweb/ru/STAT/STAT__20-ME/

"Экономический календарь, новости форекса" с сайта MQL5.community
Заявлено, что это "незаменимый инструмент трейдера для фундаментального анализа финансовых рынков на основе экономических новостей. Более 500 показателей и индикаторов крупнейших экономик мира собираются из публичных источников в режиме реального времени."
https://www.mql5.com/ru/economic-calendar




Информация про коронавирус в регионах по времени
https://cloud.yandex.ru/marketplace/products/yandex/coronavirus-dashboard-and-data
(Хопкинс, стопкоронавирус.рф)



Метеоданные по городам
rp5.ru

Соцдем данные о населении по городам, численность, возраст
https://www.data-in.ru/data-catalog/datasets/160/





Пробив адреса
https://habr.com/ru/post/555612/
https://www.fl.ru/projects/4743192/parser-sayta-domgosuslugiru.html#/


Парсим ГАР БД ФИАС в удобный формат в питоне. Бесплатно, без регистрации и СМС
https://habr.com/ru/post/595107/



1. Карта данных Инфокультуры:
https://www.infoculture.ru/2018/12/10/datamaps/
2. Если быть точным:
https://tochno.st/
3. Росстат:
https://rosstat.gov.ru/
4. ЕМИСС:
https://fedstat.ru/
5. Инфометр:
https://read.infometer.org/
6. DataCrafter:
https://beta.apicrafter.ru/
7. Карта ДТП:
https://dtp-stat.ru/opendata/
8. DaData (больше для бизнеса):
https://dadata.ru/
9. ИНИД:
https://data-in.ru/
10. DataGov:
https://data.gov.ru/
11. Trello (агрегатор дата сервисов):
https://trello.com/b/wpWtb0a9/%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5
12. Каталог данных от Андрея Дорожного:
https://dorozhnij.com/opendata?tfc_sort        
        
        """

        resp = flask.make_response(flask.render_template('index.html', menu=menu_tpl, header=header_tpl, content=content_tpl))
        return resp





