# -*- encoding: utf-8 -*-
# 
import os

from urllib.parse import urlparse, urljoin
import tldextract
import config, typing

bad_file_extensions = [".pdf", ".doc", ".docx"]

#функция обработки ссылок и приведения их к каноничному виду, удаления мусора 
def select_good_link(link_href, donor, disallowed):
    out_s = ""
    is_bad = False
    donor_parsed = urlparse(donor)
    link_parsed = urlparse(link_href)

    # приводим ссылку к каноничному виду
    if (link_parsed.hostname == None):
        link_2 = donor_parsed.scheme + "://" + donor_parsed.hostname
        link_2 = urljoin(link_2, link_href)
    else:
        link_2 = link_href

    # нас интересуют только внутренние ссылки (и с поддоменов тоже)
    donor_domain = tldextract.extract(donor).domain
    link_domain = tldextract.extract(link_2).domain
    if (link_domain != donor_domain):
        out_s = "внешняя ссылка"
        is_bad = True


    # GET переменные не нужны
    try:
        link_2, get = str(link_2).split("?")
        link_2, get = str(link_2).split("#")
    except:
        pass

    # убираем .pdf, mailto и пр.
    pos = str(link_2).find("mailto")
    if (pos != -1):
        out_s = "mailtoв"
        is_bad = True

    filename, file_extension = os.path.splitext(link_2)
    if (file_extension in bad_file_extensions):
        out_s = str(file_extension) + "<br>"
        is_bad = True

    # сам домен тоже не нужен
    if (link_2 == donor):
        out_s = "главная страница<br>"
        is_bad = True

    # исключить ссылки из robots.txt Disallow
    for disallow in disallowed:
        if disallow in link_2:
            out_s = "страница запрещена в robots.txt<br>"
            is_bad = True
            break

    return is_bad, link_2, out_s

from matplotlib.colors import rgb2hex

# функция преобразования предсказания категории в суммарный цвет
# cat_accuracies = [0.5, 0,01, 0.07]
def acc2str(cat_accuracies: typing.List[float]) -> str: 
    sum_list = [0, 0, 0]
    for i, cat_acc in enumerate(cat_accuracies):
        current_main_color = []
        print(sum_list)
        for cat_item in config.wtb_categories:
            current_main_color = cat_item["main_colors"]
            # поэлементное умножение
            for j in range(0, len(current_main_color)):
                val = cat_acc * current_main_color[j]
                sum_list[i] = sum_list[i] + val
                
    # в строку
    print(sum_list)
    out_str = rgb2hex(sum_list)
    print()


    return out_str
        
        
