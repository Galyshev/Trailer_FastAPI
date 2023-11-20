
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import get_async_session
from src.trailers.site_graber import link_graber

router = APIRouter(
    prefix="/trailers",
    tags=["Trailers"]
)
@router.get("/")
async def get_trailers(session: AsyncSession = Depends(get_async_session)):
    # UPDATE (получение ссылок и добаление в базу новых)
    await link_graber(session)
