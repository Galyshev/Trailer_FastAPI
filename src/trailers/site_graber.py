from datetime import date
import requests
from fastapi import Depends
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy import get_async_session
from src.trailers.model_bd import trailers

async def BS(link):
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = link
    r = requests.get(page, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

async def link_graber(session: AsyncSession = Depends(get_async_session)):
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
    for part in bs_link:
        part_link = str(part["href"])
        all_list.append(part_link)

    for i in range(1, len(all_list) - 1, 2):  # шаг по нечетным, что бы не вносились ссылки дважды
        id_film: str = all_list[i].split('/')[2]
        id_video: str = all_list[i - 1].split('/')[2]

        query = select(trailers).where(trailers.c.id_film == id_film, trailers.c.id_video == id_video)
        result = await session.execute(query)
        chk = result.all()

        if len(chk) == 0:
            # добавление в базу
            link_trailer: str = 'https://www.imdb.com' + all_list[i]
            status: str = 'no_view'
            date_update: str = str(date.today())
            add_trailer = {"id_film": id_film, "id_video": id_video, "link_trailer": link_trailer,
                           "status": status, "date_update": date_update}
            stmt = insert(trailers).values(add_trailer)
            await session.execute(stmt)
            await session.commit()

async def no_view_trailer(session: AsyncSession = Depends(get_async_session)):
    query = select(trailers.c.link_trailer).where(trailers.c.status == 'no_view')
    result = await session.execute(query)
    link_list = result.all()
    for link in link_list:
        link = link[0]
        query = select(trailers.c.id_video).where(trailers.c.link_trailer == link)
        result = await session.execute(query)
        id_video_list = result.all()
        link_video = "https://www.imdb.com/video/" + str(id_video_list[0][0])

# ----------------------------------------------------------------- #TODO TEST (все что ниже сместить под цикл выше)
    #     Прямая ссыылка на обложку
        cover_soup = await BS(link)
        # cover_soup = await BS('https://www.imdb.com/title/tt13629530/?ref_=vi_tr_tr_tt_39')
        cover_tmp = "https://www.imdb.com" + cover_soup.find("div", {"class": "ZYxwn"}).find('a')["href"]
        cover_soup_image = await BS(cover_tmp)
        cover_image_tmp = cover_soup_image.findAll("div", {"class": "kEDMKk"})
        for i in cover_image_tmp:
            peek_find = str(i).find("peek")
            if peek_find == -1:
                cover_image = i.find("img")["src"]

        site = link_video
        # site = "https://www.imdb.com/video/vi3922511641"
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.get(site)
        pageSource = driver.page_source
        actual_trailer_soup = BeautifulSoup(pageSource, 'html.parser')
        actual_trailer_tmp = actual_trailer_soup.find("div", {"class": "jw-media"}).find("video")
        actual_trailer_link = actual_trailer_tmp["src"]








    return None

