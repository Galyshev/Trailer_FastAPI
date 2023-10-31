from bd.alchemy import db_session
from bd.model_bd import Link_trailer

'''добавление новых данных в базу'''


def add_to_base(id_film: str, link_trailer: str, status: str, date_update: str):
    cont_add = Link_trailer(id_film=id_film, link_trailer=link_trailer, status=status, date_update=date_update)
    db_session.add(cont_add)
    db_session.commit()


'''проверка на присутствие id_film в базе, что бы исключить повторное включение'''


def check_id(id_film: str) -> list:
    chk = Link_trailer.query.filter(Link_trailer.id_film == id_film).all()
    return chk
