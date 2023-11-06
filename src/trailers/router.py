
from fastapi import APIRouter, Depends

from src.alchemy import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.trailers.site_graber import link_graber

router = APIRouter(
    prefix="/trailers",
    tags=["Trailers"]
)
@router.get("/")
async def get_trailers(session: AsyncSession = Depends(get_async_session)):
    # UPDATE (получение ссылок и добаление  базу новых)
    await link_graber(session)

    # Получение данных по НЕПРОСМОТРЕННЫМ трейлерам
    # contnt = await no_view_trailer(session)


