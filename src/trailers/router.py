from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.trailers.model_bd import trailers
from src.alchemy import get_async_session
from src.trailers.shemas import Add_Content

router = APIRouter(
    prefix="/trailers",
    tags=["Trailers"]
)
@router.get("/")
async def get_trailers(id_film: str, session: AsyncSession = Depends(get_async_session)):
    query = select(trailers).where(trailers.c.id_film == id_film)
    result = await session.execute(query)
    rr = result.all()
    print(rr)
    print(len(rr))
    return result.all()
@router.post("/add")
async def add_trailers(add_trailer: Add_Content, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(trailers).values(add_trailer.dict())
    await session.execute(stmt)
    await session.commit()