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
    bs_link = bs_section.findAll("a", {'href': re.compile('\/title/*')})

    # если не полностью загрузился сайт через селениум (такое бывает), еще раз поиск ссылок. Обычно на второй раз все ок
    if len(bs_link) < 30:
        print(len(bs_link))
        print("!!!!")
        bs_link = bs_section.findAll("a", {'href': re.compile('\/title/*')})

    # парсинг ссылок и проверка на присутствие в базе. Если нет - добавление в базу
    for i in bs_link:
        id_film: str = str(i["href"]).split('/')[2]
        # проверка по базе
        chk: list = check_id(id_film)
        if len(chk) == 0:
            # добавление в базу
            link_trailer: str = 'https://www.imdb.com' + i["href"]
            status: str = 'no_view'
            date_update: str = str(date.today())
            add_to_base(id_film, link_trailer, status, date_update)


get_list_trailer()
