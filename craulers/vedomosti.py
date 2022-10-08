# -*- encoding: utf-8 -*-
# 

from bs4 import BeautifulSoup

def get_links(post_html):
    all_links = []
    # Парсим ссылки
    soup = BeautifulSoup(post_html, "lxml")
    # <a href="/politics/articles/2022/10/03/943663-gosduma-podderzhala-sozdanie-novih-subektov" data-vr-contentbox="politics 140737489175535" data-vr-contentbox-url="/politics/articles/2022/10/03/943663-gosduma-podderzhala-sozdanie-novih-subektov" data-vr-headline="Госдума поддержала создание в России четырех новых субъектов" data-vr-title="Госдума поддержала создание в России четырех новых субъектов" class="articles-cards-list__card card-article cols-2 rows-2 --article">
    bs_step_1 = soup.select("a.articles-cards-list__card")



    
    return bs_step_1


def get_content(post_html):
    # Парсим контент
    soup = BeautifulSoup(post_html, "lxml")
    # <div class="article__text article__text_free" itemprop="articleBody">
    content = soup.select_one('div.article-boxes-list.article__boxes')
    content_text = ""
    try:
        content_text = content.get_text()
    except:
        pass

    return content_text
