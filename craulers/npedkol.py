# -*- encoding: utf-8 -*-
# 

from bs4 import BeautifulSoup

def get_links(post_html):
    all_links = []
    # Парсим ссылки
    soup = BeautifulSoup(post_html, "lxml")
    bs_step_1 = soup.find_all('div', {'class': "art-postmetadataheader"})
    
    for item_1 in bs_step_1:
        link_href = item_1.find('a')
        all_links.append(link_href)

    return all_links


def get_content(post_html):
    # Парсим контент
    soup = BeautifulSoup(post_html, "lxml")
    # <div class="art-article">
    content = soup.find('div', {'class': "art-article"})
    content_text = ""
    try:
        content_text = content.get_text()
    except:
        pass

    return content_text
