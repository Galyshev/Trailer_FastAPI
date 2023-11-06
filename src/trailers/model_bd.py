from sqlalchemy import Table, Column, Integer, String, MetaData


metadata = MetaData()

trailers = Table(
    "link_trailer",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_film", String),
    Column("id_video", String),
    Column("link_trailer", String),
    Column("status", String),
    Column("date_update", String),
)

film_info = Table(
    "film_info",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_film", String),
    Column("actual_trailer_link", String),
    Column("cover_image", String),
    Column("title", String),
    Column("genre", String),
    Column("releases", String),
    Column("annotation", String),
)
