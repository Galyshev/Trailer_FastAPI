from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import re
from datetime import date
from sql.my_sql import check_id, add_to_base

'''Получение всех ссылок на трейлеры на странице, с использованием selenium и BeautifulSoup'''


def get_list_trailer():
    site = 'https://www.imdb.com/trailers/'

    # СЕЛЕНИУМ
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.get(site)
    pageSource = driver.page_source

    # контент (ссылки на трейлеры на титулке)
    soup = BeautifulSoup(pageSource, 'html.parser')
    bs_section = soup.find("section")
    bs_link = bs_section.findAll("a")

    #  если не полностью загрузился сайт через селениум (такое бывает), еще раз поиск ссылок. Обычно на второй раз все ок
    if len(bs_link) < 66:
        print(len(bs_link))
        print("!!!!")
        bs_link = bs_section.findAll("a")

    # идентификаторы видео и фильма (первый видео, второй фильм) для дальнейшей проверки, так как у одного фильма
    # может быть несколько трейлеров и что бы их не терять, будет проверка сначала по ид. фильма, а если он есть
    # в базе, то по ид. видео

    all_list = []
    for i in bs_link:
        part_link = str(i["href"])
        all_list.append(part_link)

    for i in range(1, len(all_list)-1, 2):
        id_film: str = all_list[i].split('/')[2]
        id_video: str = all_list[i-1].split('/')[2]

        # проверка по базе
        chk: list = check_id(id_film, id_video)
        if len(chk) == 0:
            # добавление в базу
            link_trailer: str = 'https://www.imdb.com' + all_list[i]
            status: str = 'no_view'
            date_update: str = str(date.today())
            add_to_base(id_film, link_trailer, status, date_update, id_video)
        # else:
        #     # добавление в базу, если ид. фильма есть, но ид. видео не совпадает (новый трейлер)
        #     for txt in chk:
        #         if txt.id_video != id_video:
        #             link_trailer: str = 'https://www.imdb.com' + all_list[i]
        #             status: str = 'no_view'
        #             date_update: str = str(date.today())
        #             add_to_base(id_film, link_trailer, status, date_update, id_video)

get_list_trailer()
