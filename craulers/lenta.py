# -*- encoding: utf-8 -*-
# 

from bs4 import BeautifulSoup
from bs4.element import Comment

def get_links(post_html):
    all_links = []
    # Парсим ссылки
    soup = BeautifulSoup(post_html, "lxml")
    bs_step_1 = soup.find_all('a')
    
    for item_1 in bs_step_1:
        # отсеиваем мусор
        # /articles/2022/09/27/parkchanwookinterview/
        # /news/2022/09/30/georgia/
        paths = str(item_1).split("/")
        if (paths[1] == "articles") or (paths[1] == "news"):
            all_links.append(item_1)


    return all_links

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def get_content(post_html):
    # print("!!! lenta !!!")
    # Парсим контент
    soup = BeautifulSoup(post_html, "lxml")
    # <div class="_news topic-body okjx">
    content = soup.select_one('div._news.topic-body')
    content_text = ""
    try:
        content_text = content.get_text()
    except:
        pass

    if len(content_text) == 0:
        content = soup.select_one('div._news.topic-page__content')
        content_text = ""
        try:
            content_text = content.get_text()
        except:
            pass

    if len(content_text) == 0:
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)  

        return u" ".join(t.strip() for t in visible_texts)

    return content_text

