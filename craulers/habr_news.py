# -*- encoding: utf-8 -*-
# 

from bs4 import BeautifulSoup

def get_links(post_html):
    all_links = []
    # Парсим ссылки
    soup = BeautifulSoup(post_html, "lxml")
    all_links = soup.find_all('a', {'class': "tm-article-snippet__title-link"})

    return all_links

def get_content(post_html):
    # Парсим контент
    soup = BeautifulSoup(post_html, "lxml")
    # <div id="post-content-body">
    content = soup.find('div', {'id': "post-content-body"})
    content_text = ""
    try:
        content_text = content.get_text()
    except:
        pass

    return content_text
