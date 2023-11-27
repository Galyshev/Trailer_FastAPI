import re
from datetime import date

import requests
from bs4 import BeautifulSoup
from fastapi import Depends
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
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


    driver.close()

    for i in range(1, len(all_list) - 1, 2):  # шаг по нечетным, что бы не вносились ссылки дважды
        id_film: str = all_list[i].split('/')[2]
        id_video: str = all_list[i - 1].split('/')[2]

        query = select(trailers).where(trailers.c.id_film == id_film, trailers.c.id_video == id_video)
        result = await session.execute(query)
        chk = result.all()

        if len(chk) == 0:
            # добавление в базу
            link_film: str = 'https://www.imdb.com/title/' + id_film
            link_trailer: str = 'https://www.imdb.com/video/' + id_video
            status: str = 'no_view'
            date_update: str = str(date.today())
            # поиск ссылки на обложку на сайте imdb (она не прямая)
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(link_film, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            # название фильма
            title = soup.find('h1').text
            # жанр фильма
            genre = soup.find('span', {'class': 'ipc-chip__text'}).text
            # в ролях
            roles = soup.find('div', {'class': 'iRxAxS'}).findAll('a', {
                'class': 'ipc-metadata-list-item__list-content-item'})
            ls_director = []
            ls_writers = []
            ls_stars = []
            for role in roles:
                part_ov = str(role['href']).split('=')[-1]
                if part_ov == 'tt_ov_dr':
                    ls_director.append(role.text)
                elif part_ov == 'tt_ov_wr':
                    ls_writers.append(role.text)
                elif part_ov == 'tt_ov_st':
                    ls_stars.append(role.text)
                else:
                    pass

            # ссылка на обложку
            cover_link = 'https://www.imdb.com' + soup.find("a", {'href': re.compile('..\/mediaviewer/.*')})['href']
            # поиск прямой ссылки с сайта Амазона
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(cover_link, headers=headers)
            soup_cover = BeautifulSoup(r.text, 'html.parser')
            cover_link_part = cover_link.split('/')[-2] + '-curr'
            try:
                cover = soup_cover.find("div", {'class': 'ghbUKT'}).find("img", {'data-image-id': cover_link_part})[
                    'src']
                # сохранение обложки на диск, что бы не парсить постоянно и сэкономить времяю Потом картинки будут удаляться
                destination = "./static/cover/" + id_film + ".jpg"
                r = requests.get(cover, stream=True)
                with open(destination, 'wb') as f:
                    f.write(r.content)
            except:
                destination = './static/cover/no_image.jpg'
            cover = destination[9:]

            if len(ls_director) != 0:
                director = str(ls_director).replace('[', '').replace(']', '').replace('\'', '')
            else:
                director = 'no_data'

            if len(ls_writers) != 0:
                writers = str(ls_writers).replace('[', '').replace(']', '').replace('\'', '')
            else:
                writers = 'no_data'

            if len(ls_stars) != 0:
                stars = str(ls_stars).replace('[', '').replace(']', '').replace('\'', '')
            else:
                stars = 'no_data'

            print(title)
            add_trailer = {"id_film": id_film, "id_video": id_video, "link_trailer": link_trailer,
                           "link_film": link_film, "director": director, "writers": writers, "stars": stars,
                           "status": status, "date_update": date_update, "title": title, "genre": genre, "cover": cover}
            stmt = insert(trailers).values(add_trailer)
            await session.execute(stmt)
            await session.commit()
