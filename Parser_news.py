# -*- encoding: utf-8 -*-
# 
import os


import traceback
from bs4 import BeautifulSoup
import random, time, datetime
import requests
from requests.exceptions import ProxyError

from urllib.parse import urlparse, urljoin
import tldextract

# download stopwords corpus, you need to run it once
import nltk
nltk.download("stopwords")
#--------#

from nltk.corpus import stopwords
import pymorphy2
from string import punctuation

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import sys
# директория файла
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# иначе не видит этот файл
# https://stackoverflow.com/questions/67631/how-do-i-import-a-module-given-the-full-path
sys.path.append(BASE_DIR)
import config, edufunc
import importlib


#декларативное определение
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from db import News, Lemmas, Log

#Инициализация SQLLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'main.db?check_same_thread=False')
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
db_session = Session()
from db import News, Log, Search, KeyWords


import flask
from flask import Blueprint
parser_news = Blueprint('parser_news', __name__)


#---------------------------------- Variables ----------
MAX_EXEC_PAGES = 10

user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:23.0) Gecko/20100101 Firefox/23.0",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.1; rv:23.0) Gecko/20100101 Firefox/23.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Opera/9.80 (Windows NT 5.1) Presto/2.12.388 Version/12.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 YaBrowser/1.7.1364.21027 Safari/537.22",
    "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.16",
    "Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25",
    "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.15",
    "Mozilla / 5.0 (Macintosh; Intel Mac OS X 10.14; rv: 75.0) Gecko / 20100101 Firefox / 75.0",
    "Mozilla / 5.0 (Windows NT 6.1; Win64; x64; rv: 74.0) Gecko / 20100101 Firefox / 74.0",
    "Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit / 537.36 (KHTML, как Gecko) Chrome / 80.0.3987.163 Safari / 537.36",
    "Dalvik/2.1.0 (Linux; U; Android 10; Mi 9T MIUI/V12.0.5.0.QFJMIXM)"
]
#---------------------------------- Variables End ----------



@parser_news.route('/parser_news', methods=['post', 'get'])
def parser_news_func():
    menu_tpl = "<a href='/log'>Log</a> ~ <a href='/crauler_news'>Crauler</a> ~ <b>Parser</b> ~ <a href='/users'>Users</a> ~ <a href='/news'>Digest</a> ~ <a href='/trends'>Trends</a> ~ <a href='/inside'>InSide</a> ~ "
    header_tpl = "<center><h2>NPPK32. Development Platform 4 VTB Hack. Case: #Data.</h2></center>"
    content_tpl = ""

    #время начала парсинга
    start_ts = int(time.time())

    try:
        # https://www.kaggle.com/code/alxmamaev/how-to-easy-preprocess-russian-text/script - не то
        #Create lemmatizer and stopwords list
        morph = pymorphy2.MorphAnalyzer()
        russian_stopwords = stopwords.words("russian")

        #Preprocess function
        def preprocess_text(text):
            words = text.lower().split()
            
            # очистка от прилегающего к слову мусора (слово, "или так")
            clear_words = []
            for word in words:
                clear_word = ""
                for s in word:
                    if not s in punctuation:
                        clear_word = clear_word + s
                clear_words.append(clear_word)
            # если сервер не справляется
            """
            clear_words = words
            """        
            tokens = [morph.parse(token)[0].normal_form for token in clear_words if token not in russian_stopwords\
                    and token != " " \
                    and token.strip() not in punctuation]

            text = " ".join(tokens)
            
            return tokens, text

        link_n = db_session.query(News).filter(News.status == 0).order_by(News.parse_date.desc()).count()
        # парсим по MAX_EXEC_PAGES случайных ссылок за раз
        links_4pars = 0
        if (link_n >= MAX_EXEC_PAGES):
            links_4pars = MAX_EXEC_PAGES
        else:
            links_4pars = link_n
            
        if (links_4pars > 0):
            for i in range(0, links_4pars):
                # ссылки с ключевиками
                needle_keys_n = 0
                # случайная ссылка
                # link = db_session.query(News).filter(News.status == 0).order_by(func.random()).first()
                link = db_session.query(News).filter(News.status == 0).order_by(News.parse_date.desc()).first()

                content_tpl += "<p>Парсим News: " + str(link.href) + "<br>"
                
                #формируем запрос
                user_agent = random.choice(user_agents)
                donor_parsed = urlparse(link.href)
                
                headers = {
                        "Host": str(donor_parsed.hostname),
                        'User-Agent': str(user_agent),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Referer': str(link.href),
                        'Upgrade-Insecure-Requests': '1',
                        'Connection': 'keep-alive'}
                
                response = ""
                try:
                    response = requests.get(link.href, headers=headers)
                    content_tpl += "status_code: " + str(response.status_code) + "<br>"
                    response_text = response.text

                except:
                    status = str(traceback.format_exc())
                    content_tpl += "Ошибка: <pre>"+ str(status) + "</pre><br>"
                    
                    options = Options()
                    options.add_argument('--headless')
                    options.add_argument('--disable-gpu')  # Last I checked this was necessary.

                    browser = webdriver.Chrome(executable_path=os.path.join(BASE_DIR, "chromedriver_win"), chrome_options=options)
                    browser.get(link.href)

                    response_text = browser.page_source



                # link.html = response.text
                # парсинг html в текст
                response_text = response_text.replace("\n", " ")
                soup = BeautifulSoup(response_text, "lxml")
                title = ""
                try:
                    title = soup.find('title').string.strip()
                    content_tpl += "<b>Title: </b>" + str(title) + "<br>"
                    link.title = title.replace("\n", "")
                except:
                    status = str(traceback.format_exc())
                    content_tpl += "Ошибка: <pre>"+ str(status) + "</pre><br>"

                # text = soup.get_text()
                text = ""
                # ищем модуль для парсинга контента
                if "banki.ru" in link.href:
                    site_crauler = importlib.import_module(f"craulers.banki")
                    text = site_crauler.get_content(response_text)
                else:
                    if "lenta.ru" in link.href:
                        site_crauler = importlib.import_module(f"craulers.lenta")
                        text = site_crauler.get_content(response_text)
                    else:
                        for donor_item in config.donors_data:
                            donor_url = donor_item["url"]
                            #content_tpl += f"<li>{donor_url} - {link.donor}"
                            if donor_item["url"] == link.donor:
                                module_name = donor_item["module_name"]
                                site_crauler = importlib.import_module(f"craulers.{module_name}")
                                #content_tpl += f"craulers: {module_name}"
                                text = site_crauler.get_content(response_text)

                text = str(text).replace("\n", ".")
                link.text = text
                
                # выводим четыре первых предложения
                desc = text.split(".")
                desc = ". ".join(desc[:4])
                content_tpl += f"<p><b>Desc</b>: {desc}"

                summary_text = title + " " + text
                tokens, tokens_str = preprocess_text(summary_text)
                link.lemmas = tokens_str
                content_tpl += "<p><b>Lemmas: </b>" + str(tokens_str) + "<br><br>"
                
                # ищем ключевые слова в словоформах из текста
                link.status = 1
                for key in config.keywords:
                    if key in tokens:
                        link.status = 2
                        needle_keys_n += 1
                        content_tpl += "<b>Ключевое слово в леммах присутствует</b><br><br>"


                db_session.commit()

                

                #добавляем леммы по одной
                id_news = link.id
                # уникальные леммы
                myset = set(tokens)
                for lemma in myset:
                    new_lemma = Lemmas(
                        id_news = id_news, 
                        lemma = lemma,
                    )
                    db_session.add(new_lemma)

            content_tpl += "<br>"
            """
            except:
                status = str(traceback.format_exc())
                content_tpl += "Ошибка: <pre>"+ str(status) + "</pre><br>"

                link.status = 4

                log_status = str(link.href) + "<br>"
                log_status += "Ошибка парсинга: " + status
                new_log = Log(
                    action = "parser_news", 
                    status = log_status, 
                    time = int(time.time()),
                    donor = str(urlparse(link.href).hostname), 
                )
                db_session.add(new_log)
                db_session.commit()
            """
            # время окончания парсинга
            end_ts = int(time.time())
            exec_time = end_ts - start_ts
            log_status = str(link.href) + "; " + "<br>"
            log_status += "Время парсинга: " + str(exec_time) + " с.; " + "<br>"
            #log_status += "Нужных ключевиков: " + str(needle_keys_n) + "; " + "<br>"
            log_donor = str(urlparse(link.href).hostname) 

        else:
            content_tpl += "Нет ссылок для парсинга<br>"    
            log_status = "Нет ссылок для парсинга"  
            log_donor = ""
            exec_time = 0


        new_log = Log(
            action = "parser", 
            status = log_status, 
            time = int(time.time()),
            donor = log_donor, 
        )
        db_session.add(new_log)
        db_session.commit()


        db_session.close()
        content_tpl += "Время парсинга: " + str(exec_time) + " с.; " + "<br>"

        return flask.render_template('local_crauler_1.html', menu=menu_tpl, header=header_tpl, content=content_tpl )

    except:
        status = str(traceback.format_exc())
        content_tpl = "Ошибка: <pre>"+ str(status) + "</pre><br>"
        return flask.render_template('local_crauler_1.html', menu=menu_tpl, header=header_tpl, content=content_tpl )
