from datetime import datetime

from pydantic import BaseModel

class Add_Content(BaseModel):
    id_film: str
    id_video: str
    link_trailer: str
    status: str
    date_update: str