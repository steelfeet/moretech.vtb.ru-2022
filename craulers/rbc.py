# -*- encoding: utf-8 -*-
# 

from bs4 import BeautifulSoup

def get_links(post_html):
    all_links = []
    # Парсим ссылки
    soup = BeautifulSoup(post_html, "lxml")
    bs_step_1 = soup.find_all('a', {'class': "main__feed__link js-yandex-counter js-visited"})
    
    """
    for item_1 in bs_step_1:
        # отсеиваем мусор
        # /articles/2022/09/27/parkchanwookinterview/
        # /news/2022/09/30/georgia/
        paths = str(item_1).split("/")
        if (paths[1] == "articles") or (paths[1] == "news"):
            all_links.append(item_1)
    """

    return bs_step_1


def get_content(post_html):
    # Парсим контент
    soup = BeautifulSoup(post_html, "lxml")
    # <div class="article__text article__text_free" itemprop="articleBody">
    content = soup.select_one('div.article__text.article__text_free')
    content_text = ""
    try:
        content_text = content.get_text()
    except:
        pass

    return content_text
