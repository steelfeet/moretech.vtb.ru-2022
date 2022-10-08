
import os, traceback

#декларативное определение
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'main.db')
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
#Инициализация SQLLite
Base = declarative_base()


# класс БД собранной информации
class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    donor = Column(String(255))
    title = Column(String(512))
    href = Column(String(512))
    parse_date = Column(Integer)
    html = Column(Text)
    text = Column(Text)
    lemmas = Column(Text) # набор лемм из текста (мешок слов)
    level = Column(Integer) # уровень вложенности ссылки от корня сайта
    status = Column(Integer) # 0 - не загружена,  1 - загружена, ключевика нет; 2 - ключевик есть, уведомление не отправлено; 3 - уведомление не отправлено

    def __init__(self, donor, title, href, parse_date, html, text, lemmas, level, status):
        self.donor = donor
        self.title = title
        self.href = href
        self.parse_date = parse_date
        self.html = html
        self.text = text
        self.lemmas = lemmas
        self.level = level
        self.status = status

    def __repr__(self):
        return "<Link('%s', '%s')>" % (self.title, self.href)


class Lemmas(Base):
    __tablename__ = 'lemmas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_news = Column(Integer)
    lemma = Column(String(255), index=True) # одна лемма из текста
    
    def __init__(self, id_news, lemma):
        self.id_news = id_news
        self.lemma = lemma

    def __repr__(self):
        return "<Lemma('%s')>" % (self.lemma)

class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String(64))
    status = Column(String(64))
    time = Column(Integer)
    donor = Column(String(64))

    def __init__(self, action, status, time, donor):
        self.action = action
        self.status = status
        self.time = time
        self.donor = donor

    def __repr__(self):
        return "<Log('%s','%s', '%s')>" % (self.action, self.status)



class Search(Base):
    __tablename__ = 'search'
    id = Column(Integer, primary_key=True, autoincrement=True)
    donor = Column(String(255))
    title = Column(String(512))
    href = Column(String(512))
    parse_date = Column(Integer)
    html = Column(Text)
    text = Column(Text)
    lemmas = Column(Text) # набор лемм из текста (мешок слов)
    level = Column(Integer) # уровень вложенности ссылки от корня сайта
    status = Column(Integer) # 0 - не загружена,  1 - загружена, ключевика нет; 2 - ключевик есть, уведомление не отправлено; 3 - уведомление не отправлено

    def __init__(self, donor, title, href, parse_date, html, text, lemmas, level, status):
        self.donor = donor
        self.title = title
        self.href = href
        self.parse_date = parse_date
        self.html = html
        self.text = text
        self.lemmas = lemmas
        self.level = level
        self.status = status

    def __repr__(self):
        return "<Link('%s', '%s')>" % (self.title, self.href)


class KeyWords(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(512))
    stat = Column(Integer)

    def __init__(self, stat):
        self.stat = stat

    def __repr__(self):
        return "<Log('%s','%s', '%s')>" % (self.stat)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(512)) 

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Users('%s')>" % ()


class UsersAction(Base):
    __tablename__ = 'users_action'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer) # идентификатор пользователя
    show_id = Column(Integer) # идентификатор новости, которая была показана
    click_id = Column(Integer) # идентификатор новости, по которой кликнул
    model = Column(String(512)) # какая модель использовалась для поиска релевантных новостей

    def __init__(self, user_id, show_id, click_id, model):
        self.user_id = user_id
        self.show_id = show_id
        self.click_id = click_id
        self.model = model

    def __repr__(self):
        return "<UsersAction('%s','%s','%s')>" % (self.user_id, self.show_id, self.click_id)


class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(512)) 

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Roles('%s')>" % (self.name)


# Создание таблиц
Base.metadata.create_all(engine)
