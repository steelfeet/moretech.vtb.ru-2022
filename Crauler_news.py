# -*- encoding: utf-8 -*-
# 
import os

import traceback, random, time, json
import time
import datetime

import requests
from requests.exceptions import ProxyError
from urllib.parse import urlparse, urljoin

#декларативное определение
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func

from bs4 import BeautifulSoup

import sys
# директория файла
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# иначе не видит этот файл
# https://stackoverflow.com/questions/67631/how-do-i-import-a-module-given-the-full-path
sys.path.append(BASE_DIR)
import config, edufunc

import importlib


#Инициализация SQLLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'main.db')
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
db_session = Session()
from db import News, Log, Search, KeyWords


import flask
from flask import Blueprint
сrauler_news = Blueprint('сrauler_news', __name__)


#---------------------------------- Variables ----------

keywords = [
    "олимпиада",
    "хакатон",
    "конкурс"
]

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



@сrauler_news.route('/crauler_news', methods=['post', 'get'])
def сrauler_news_func():
    menu_tpl = "<a href='/log'>Log</a> ~ <b>Crauler</b> ~ <a href='/parser_news'>Parser</a> ~ <a href='/users'>Users</a> ~ <a href='/news'>Digest</a> ~ <a href='/trends'>Trends</a> ~ <a href='/inside'>InSide</a> ~ <br> <a href='/crauler_test'>Crauler Test</a> ~ <a href='/crauler_forums'>Crauler Forums</a> ~ <a href='/crauler_lenta'>Crauler Lenta.ru</a> ~ <a href='/crauler_banki'>Crauler Banki.ru</a> ~ <a href='/crauler_vedomosti'>Crauler Vedomosti.ru</a>"
    header_tpl = "<center><h2>NPPK32. Development Platform 4 VTB Hack. Case: #Data.</h2></center>"

    log_status = ""
    robots_txt = ""
    content_tpl = ""
    new_links = 0

    try:
        # отбираем 10 случайных донор для избежания перегрузки сервера
        donors = config.donors_data
        random.shuffle(donors)
        donors_10 = donors[:3]
        content_tpl += "Всего отобрано доноров: " + str(len(donors_10)) + " из " + str(len(donors)) + "<br>"
        for donor_item in donors_10:
            donor = donor_item["url"]
            #время начала парсинга
            start_ts = int(time.time())
            new_donor_links = 0
            disallowed = []

            content_tpl += "<h3>Парсим " + donor + "</h3>"
            #формируем запрос
            user_agent = random.choice(user_agents)
            donor_parsed = urlparse(donor)
            
            headers = {
                    "Host": str(donor_parsed.hostname),
                    'User-Agent': str(user_agent),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': str(donor),
                    'Upgrade-Insecure-Requests': '1',
                    'Connection': 'keep-alive'}

            
            # запрашиваем robots.txt
            try:
                response = requests.get(donor + "robots.txt", headers=headers)
                robots_txt = response.text
                robots_txt_for_parsing = robots_txt.split('\n')
                for word in robots_txt_for_parsing:
                    word = word.rstrip('\r')
                    if word in disallowed:
                        pass
                    if 'Disallow: ' in word:
                        if word.lstrip('Disallow: ') == '':
                            pass
                        else:
                            Disallow = word.find('Disallow: ')
                            word = word[Disallow:]
                            disallowed.append(word.lstrip('Disallow: '))
                donor_name = donor.split('/')
                robots_txt_file = open(BASE_DIR + f"/robots.txt/{donor_name[2]}.txt", 'w')
                robots_txt_file.write(response.text)
                robots_txt_file.close()
            except Exception:
                status = str(traceback.format_exc())
                content_tpl += "Ошибка: <pre>"+ str(status) + "</pre><br>"

            
            # запрашиваем favicon.ico и сохраняем
            try:
                response = requests.get(donor + "favicon.ico", headers=headers)
                if response.status_code != 200:
                    content_tpl += "No favicon.ico<br>"
                else:
                    donor_name = donor.split('/')
                    favicon = open(BASE_DIR + f"/favicon/{donor_name[2]}.ico", 'wb')
                    favicon.write(response.content)
                    favicon.close()
            except:
                status = str(traceback.format_exc())
                content_tpl += "Ошибка: <pre>"+ str(status) + "</pre><br>"

            
            # основной контент
            try:
                response = requests.get(donor, headers=headers)
                post_html = response.text

                with open(os.path.join(BASE_DIR + "/html/", donor_parsed.hostname+'.html'), 'w', encoding="utf-8") as f:
                    f.write(post_html)

                # Парсим ссылки
                module_name = donor_item["module_name"]
                site_crauler = importlib.import_module(f"craulers.{module_name}")
                
                all_links = site_crauler.get_links(post_html)
                content_tpl += f"Подходящих ссылок: {len(all_links)}; <br>"
                
                
                for link in all_links:
                    link_href = link.get('href')
                    content_tpl += f"link_href: {link_href}<br>"

                    is_bad, link_1, why_s = edufunc.select_good_link(link_href, donor, disallowed)
                    if (is_bad):
                        content_tpl += f"Плохая ссылка: {why_s}<br><br>"
                        continue
                    content_tpl += f"donor: {donor}<br>"
                    content_tpl += f"good link: {link_1}<br>"


                    #уникальность ссылки в News
                    content_tpl += "Проверяем уникальность в News" + "<br>"
                    link_n = db_session.query(News).filter(News.href == link_1).count()
                    content_tpl += "link_n: " + str(link_n) + "<br>"
                    if (link_n == 0):
                        content_tpl += "<b>Добавляем в базу News</b>" + "<br><br>"
                        new_link = News(
                            title = "", 
                            href = link_1,
                            donor = donor, 
                            parse_date = int(time.time()), 
                            html = "",
                            text = "",
                            lemmas = "",
                            level = 1,
                            status = 0
                        )
                        db_session.add(new_link)
                        db_session.commit()
                        new_links += 1
                        new_donor_links += 1
                    else:
                        content_tpl += "В базе News ссылка есть" + "<br><br>"
                    

                    #уникальность ссылки в Search
                    content_tpl += "Проверяем уникальность в Search" + "<br>"
                    link_n = db_session.query(Search).filter(Search.href == link_1).count()
                    content_tpl += "link_n: " + str(link_n) + "<br>"
                    if (link_n == 0):
                        content_tpl += "<b>Добавляем в базу Search</b>" + "<br><br>"
                        new_link = Search(
                            title = "", 
                            href = link_1,
                            donor = donor, 
                            parse_date = int(time.time()), 
                            html = "",
                            text = "",
                            lemmas = "",
                            level = 1,
                            status = 0
                        )
                        db_session.add(new_link)
                        db_session.commit()
                    else:
                        content_tpl += "В базе Search ссылка есть" + "<br><br>"
                    


                    content_tpl += "<br"
                
            except:
                status = str(traceback.format_exc())
                content_tpl += "Ошибка: " + str(status) + "<br>"
                
        
            
            # время окончания парсинга
            end_ts = int(time.time())
            exec_time = end_ts - start_ts
            log_status = "Время парсинга: " + str(exec_time) + " с.; "
            log_status += "Новых ссылок: " + str(new_donor_links)
            new_log = Log(
                action = "crauler_news", 
                status = log_status, 
                time = int(time.time()),
                donor = donor, 
            )
            db_session.add(new_log)
            db_session.commit()

        content_tpl += "Новых ссылок 1-го уровня: " + str(new_links) + "<br>"

    except:
        status = str(traceback.format_exc())
        content_tpl += "Ошибка: " + str(status) + "<br>"
                

    db_session.close()

    return flask.render_template('local_crauler_10.html', menu=menu_tpl, header=header_tpl, content=content_tpl )








"""
████████   ███████    ██████   ████████   
   ██      ██        ██           ██      
   ██      █████      █████       ██      
   ██      ██             ██      ██      
   ██      ███████   ██████       ██
"""

@сrauler_news.route('/crauler_test', methods=['post', 'get'])
def сrauler_test_func():
    menu_tpl = "<a href='/log'>Log</a> ~ <a href='/crauler_news'>Crauler</a> ~ <a href='/parser_news'>Parser</a> ~ <a href='/users'>Users</a> ~ <a href='/news'>Digest</a> ~ <a href='/trend'>Trands</a> ~ <a href='/insight'>InSide</a> ~ <br> <b>Crauler Test</b>"
    header_tpl = "<center><h2>NPPK32. Development Platform 4 VTB Hack. Case: #Data.</h2></center>"

    test_module = "lenta"
    content_tpl = ""

    donors = config.donors_data
    for donor_item in donors:
        if (donor_item["module_name"] == test_module):
            donor = donor_item["url"]
            new_donor_links = 0

            content_tpl += "<h3>Парсим " + donor + "</h3>"
            #формируем запрос
            user_agent = random.choice(user_agents)
            donor_parsed = urlparse(donor)
        
            headers = {
                    "Host": str(donor_parsed.hostname),
                    'User-Agent': str(user_agent),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': str(donor),
                    'Upgrade-Insecure-Requests': '1',
                    'Connection': 'keep-alive'}

        

            # основной контент
            good_links = []
            try:
                response = requests.get(donor, headers=headers)
                post_html = response.text

                with open(os.path.join(BASE_DIR + "/html/", donor_parsed.hostname+'.html'), 'w', encoding="utf-8") as f:
                    f.write(post_html)

                # Парсим ссылки
                module_name = donor_item["module_name"]
                site_crauler = importlib.import_module(f"craulers.{module_name}")
                
                all_links = site_crauler.get_links(post_html)
                content_tpl += f"Подходящих ссылок: {len(all_links)}; <br>"
                
                
                for link in all_links:
                    link_href = link.get('href')
                    content_tpl += f"link_href: {link_href}<br>"

                    is_bad, link_1, why_s = edufunc.select_good_link(link_href, donor, [])
                    if (is_bad):
                        content_tpl += f"Плохая ссылка: {why_s}<br><br>"
                        continue
                    content_tpl += f"good link: {link_1}<br>"
                    good_links.append(link_1)



                content_tpl += "<h3>Text</h3>"
                try:
                    response = requests.get(good_links[0], headers=headers)
                except:
                    status = str(traceback.format_exc())
                    content_tpl += "Ошибка: <pre>"+ str(status) + "</pre><br>"

                response_text = response.text
                response_text = response_text.replace("\n", " ")
                text = site_crauler.get_content(response_text)
                content_tpl += text
                

            except:
                status = str(traceback.format_exc())
                content_tpl += "Ошибка: " + str(status) + "<br>"
                
       
        

    return flask.render_template('local_crauler_10.html', menu=menu_tpl, header=header_tpl, content=content_tpl )









"""
███████    ██████    ███████    ██    ██   ███    ███    ██████   
██        ██    ██   ██    ██   ██    ██   ██ █  █ ██   ██        
█████     ██    ██   ███████    ██    ██   ██  ██  ██    █████    
██        ██    ██   ██  ██     ██    ██   ██      ██        ██   
██         ██████    ██    ██    ██████    ██      ██   ██████   
"""
@сrauler_news.route('/crauler_forums', methods=['post', 'get'])
def crauler_forums_func():
    menu_tpl = "<a href='/log'>Log</a> ~ <a href='/crauler_news'>Crauler</a> ~ <a href='/parser_news'>Parser</a> ~ <a href='/news'>News</a> ~ <br> <a href='/crauler_test'>Crauler Test</a> ~ <b>Crauler Forums</b> ~ <a href='/crauler_lenta'>Crauler Lenta.ru</a> ~ "
    header_tpl = "<center><h2>NPPK32. Development Platform 4 VTB Hack. Case: #Data.</h2></center>"

    content_tpl = """Парсим форумы в базу Forums. Обязательно с учетом иерархической структуры Вопрос / Ответ и ником пользователя. 
    Youtube, Rutube, TM
    """

    return flask.render_template('index.html', menu=menu_tpl, header=header_tpl, content=content_tpl )













@сrauler_news.route('/crauler_lenta', methods=['post', 'get'])
def crauler_lenta_func():
    menu_tpl = "<a href='/log'>Log</a> ~ <a href='/crauler_news'>Crauler</a> ~ <a href='/parser_news'>Parser</a> ~ <a href='/news'>News</a> ~ <br> <a href='/crauler_test'>Crauler Test</a> ~ <b>Crauler Forums</b> ~ <b>Crauler Lenta.ru</b> ~ "
    header_tpl = "<center><h2>NPPK32. Development Platform 4 VTB Hack. Case: #Data.</h2></center>"


    log_status = ""
    content_tpl = ""
    all_links = []
    new_donor_links = 0
    data = {}

    try:
        f = open(os.path.join(BASE_DIR, 'lenta.json'))
        data = json.load(f)
        day = data["day"]
        month = data["month"]
        year = data["year"]
    except:
        day = 30
        month = 9
        year = 2022

    day = day - 1
    if day == 0:
        day = 30
        month = month - 1
    if month == 0:
        day = 30
        month = 12
        year = year - 1

    day_2digit = f"{day}"
    if day < 10:
        day_2digit = f"0{day}"
    month_2digit = f"{month}"
    if month < 10:
        month_2digit = f"0{month}"
    #формируем запрос
    user_agent = random.choice(user_agents)
    donor = f"https://lenta.ru/news/{year}/{month_2digit}/{day_2digit}/"
    try:
        donor_parsed = urlparse(donor)
        
        headers = {
                "Host": str(donor_parsed.hostname),
                'User-Agent': str(user_agent),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': str(donor),
                'Upgrade-Insecure-Requests': '1',
                'Connection': 'keep-alive'}

        response = requests.get(donor, headers=headers)
        post_html = response.text

        # Парсим ссылки
        soup = BeautifulSoup(post_html, "lxml")
        bs_step_1 = soup.find_all('a')
        
        # отсеиваем мусор
        for item_1 in bs_step_1:
            # /news/2022/09/30/georgia/
            paths = str(item_1).split("/")
            if (paths[1] == "news" and (not "page" in paths)):
                all_links.append(item_1)

        # страницы
        for i in range(2, 9):
            user_agent = random.choice(user_agents)
            donor = f"https://lenta.ru/news/{year}/{month_2digit}/{day_2digit}/page/{i}/"
            time.sleep(1)
            donor_parsed = urlparse(donor)
            headers = {
                    "Host": str(donor_parsed.hostname),
                    'User-Agent': str(user_agent),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': str(donor),
                    'Upgrade-Insecure-Requests': '1',
                    'Connection': 'keep-alive'}

            try:
                response = requests.get(donor, headers=headers)
                post_html = response.text

                # Парсим ссылки
                soup = BeautifulSoup(post_html, "lxml")
                bs_step_1 = soup.find_all('a')
                
                # отсеиваем мусор
                for item_1 in bs_step_1:
                    # /news/2022/09/30/georgia/
                    paths = str(item_1).split("/")
                    if (paths[1] == "news" and (not "page" in paths)):
                        all_links.append(item_1)
            except:
                pass

        content_tpl += f"Подходящих ссылок: {len(all_links)}; <br>"
                
                
        for link in all_links:
            link_href = link.get('href')
            content_tpl += f"link_href: {link_href}<br>"

            is_bad, link_1, why_s = edufunc.select_good_link(link_href, donor, [])
            if (is_bad):
                content_tpl += f"Плохая ссылка: {why_s}<br><br>"
                continue
            content_tpl += f"donor: {donor}<br>"
            content_tpl += f"good link: {link_1}<br>"

            parse_date = int(time.mktime(datetime.datetime.strptime(f"{day}/{month}/{year}", "%d/%m/%Y").timetuple()))
            content_tpl += f"{year}/{month}/{day} => {parse_date}<br>"


            #уникальность ссылки в News
            content_tpl += "Проверяем уникальность в News" + "<br>"
            link_n = db_session.query(News).filter(News.href == link_1).count()
            content_tpl += "link_n: " + str(link_n) + "<br>"
            if (link_n == 0):
                content_tpl += "<b>Добавляем в базу News</b>" + "<br><br>"
                new_link = News(
                    title = "", 
                    href = link_1,
                    donor = "lenta", 
                    parse_date = parse_date, 
                    html = "",
                    text = "",
                    lemmas = "",
                    level = 1,
                    status = 0
                )
                db_session.add(new_link)
                db_session.commit()
                new_donor_links += 1
            else:
                content_tpl += "В базе News ссылка есть" + "<br><br>"
            

            #уникальность ссылки в Search
            content_tpl += "Проверяем уникальность в Search" + "<br>"
            link_n = db_session.query(Search).filter(Search.href == link_1).count()
            content_tpl += "link_n: " + str(link_n) + "<br>"
            if (link_n == 0):
                content_tpl += "<b>Добавляем в базу Search</b>" + "<br><br>"
                new_link = Search(
                    title = "", 
                    href = link_1,
                    donor = "lenta", 
                    parse_date = parse_date, 
                    html = "",
                    text = "",
                    lemmas = "",
                    level = 1,
                    status = 0
                )
                db_session.add(new_link)
                db_session.commit()
            else:
                content_tpl += "В базе Search ссылка есть" + "<br><br>"                


        log_status += f"<br>{year}/{month}/{day}"
        log_status += "Новых ссылок: " + str(new_donor_links)
        new_log = Log(
            action = "crauler_lenta", 
            status = log_status, 
            time = int(time.time()),
            donor = "lenta", 
        )
        db_session.add(new_log)
        db_session.commit()

        data["day"] = day
        data["month"] = month
        data["year"] = year

        f = open(os.path.join(BASE_DIR, 'lenta.json'), 'w')
        json.dump(data, f)
        
    except:
        status = str(traceback.format_exc())
        content_tpl += "Ошибка: " + str(status) + "<br>"



    db_session.close()
    return flask.render_template('local_crauler_1.html', menu=menu_tpl, header=header_tpl, content=content_tpl )




















@сrauler_news.route('/crauler_banki', methods=['post', 'get'])
def crauler_banki_func():
    menu_tpl = "<a href='/log'>Log</a> ~ <a href='/crauler_news'>Crauler</a> ~ <a href='/parser_news'>Parser</a> ~ <a href='/news'>News</a> ~ <br> <a href='/crauler_test'>Crauler Test</a> ~ <b>Crauler Forums</b> ~ <b>Crauler Banki.ru</b> ~ "
    header_tpl = "<center><h2>NPPK32. Development Platform 4 VTB Hack. Case: #Data.</h2></center>"


    log_status = ""
    content_tpl = ""
    all_links = []
    new_donor_links = 0
    data = {}

    try:
        f = open(os.path.join(BASE_DIR, 'banki.json'))
        data = json.load(f)
        id = data["id"]
    except:
        id = 10973497

    id = id - 1

    user_agent = random.choice(user_agents)
    donor = f"https://www.banki.ru/news/lenta/?id={id}"
    try:
        donor_parsed = urlparse(donor)
        
        headers = {
                "Host": str(donor_parsed.hostname),
                'User-Agent': str(user_agent),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': str(donor),
                'Upgrade-Insecure-Requests': '1',
                'Connection': 'keep-alive'}

        response = requests.get(donor, headers=headers)
        post_html = response.text

        # Парсим ссылки
        soup = BeautifulSoup(post_html, "lxml")
        """
        date = soup.find('span', {'class': "l51e0a7a5"})
        date_text = date.get_text() # 07.10.2022 21:37
        date, t = date_text.split()
        """
        date = ""
        title = ""
        try:
            title = soup.find('title').string.strip()
            content_tpl += "<b>Title: </b>" + str(title) + "<br>"
        except:
            status = str(traceback.format_exc())
            content_tpl += "Ошибка: <pre>"+ str(status) + "</pre><br>"


        parse_date = int(time.mktime(datetime.datetime.strptime(f"{date}", "%d.%m.%Y").timetuple()))
        content_tpl += f"{date} => {parse_date}<br>"


        #уникальность ссылки в News
        content_tpl += "<b>Добавляем в базу News</b>" + "<br><br>"
        new_link = News(
            title = "", 
            href = donor,
            donor = "banki", 
            parse_date = parse_date, 
            html = "",
            text = "",
            lemmas = "",
            level = 1,
            status = 0
        )
        db_session.add(new_link)
        db_session.commit()
        new_donor_links += 1
        

        #уникальность ссылки в Search
        content_tpl += "<b>Добавляем в базу Search</b>" + "<br><br>"
        new_link = Search(
            title = "", 
            href = donor,
            donor = "banki", 
            parse_date = parse_date, 
            html = "",
            text = "",
            lemmas = "",
            level = 1,
            status = 0
        )
        db_session.add(new_link)
        db_session.commit()


        new_log = Log(
            action = "crauler_banki", 
            status = log_status, 
            time = int(time.time()),
            donor = "lenta.ru", 
        )
        db_session.add(new_log)
        db_session.commit()

        
        data["id"] = id
        f = open(os.path.join(BASE_DIR, 'banki.json'), 'w')
        json.dump(data, f)
        
    except:
        status = str(traceback.format_exc())
        content_tpl += "Ошибка: " + str(status) + "<br>"



    db_session.close()
    return flask.render_template('local_crauler_1.html', menu=menu_tpl, header=header_tpl, content=content_tpl )

























