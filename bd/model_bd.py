from sqlalchemy import Column, Integer, Text
from bd.alchemy import Base


class Link_trailer(Base):
    __tablename__ = "link_trailer"

    id = Column(Integer, primary_key=True)
    id_film = Column(Text)
    link_trailer = Column(Text)
    status = Column(Text)  # просмотрено / не просмотрено
    date_update = Column(Text)

    def __init__(self, id_film, link_trailer, status, date_update):
        self.id_film = id_film
        self.link_trailer = link_trailer
        self.status = status
        self.date_update = date_update