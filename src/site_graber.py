from selenium import webdriver
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from src.alchemy import get_async_conn
from sql.my_sql import check_id

'''Получение всех ссылок на трейлеры на странице, с использованием selenium и BeautifulSoup'''


def get_list_trailer(session: AsyncSession = Depends(get_async_conn)):
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
    # может быть несколько трейлеров и что бы их не терять, будет проверка сразу по ид. фильма и по ид. видео

    all_list = []
    for i in bs_link:
        part_link = str(i["href"])
        all_list.append(part_link)

    for i in range(1, len(all_list)-1, 2):  #шаг по нечетным, что бы не вносились ссылки дважды
        id_film: str = all_list[i].split('/')[2]
        id_video: str = all_list[i-1].split('/')[2]

        # проверка по базе
        chk = check_id(session, id_film, id_video)

        # if len(chk) == 0:
        #     # добавление в базу
        #     link_trailer: str = 'https://www.imdb.com' + all_list[i]
        #     status: str = 'no_view'
        #     date_update: str = str(date.today())
        #     add_to_base(session, id_film, link_trailer, status, date_update, id_video)


get_list_trailer()
