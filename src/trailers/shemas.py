from datetime import datetime

from pydantic import BaseModel

class Add_Content(BaseModel):
    id: int
    id_film: str
    id_video: str
    link_trailer: str
    status: str
    date_update: str