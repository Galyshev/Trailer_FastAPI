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
    Column("title", String),
    Column("genre", String),
    Column("director", String),
    Column("writers", String),
    Column("stars", String),
    Column("link_film", String),
    Column("cover", String),
)
