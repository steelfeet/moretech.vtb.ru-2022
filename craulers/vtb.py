# -*- encoding: utf-8 -*-
# 

from bs4 import BeautifulSoup

def get_links(post_html):
    all_links = []
    # Парсим ссылки
    soup = BeautifulSoup(post_html, "lxml")
    bs_step_1 = soup.find_all('a')
    
    for item_1 in bs_step_1:
        # отсеиваем мусор
        # https://www.vtb.ru/about/press/news/?id=179177
        print(str(item_1.get('href')))
        if ("press" in str(item_1.get('href'))) and ("news" in str(item_1.get('href'))):
            all_links.append(item_1)


    return all_links
