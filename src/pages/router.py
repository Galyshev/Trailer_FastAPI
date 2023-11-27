from fastapi import APIRouter, Request, Form
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from src.alchemy import get_async_session
from src.trailers.model_bd import trailers

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

templates = Jinja2Templates(directory="templates")


@router.get('/trailers')
async def no_view_trailers_pages(request: Request, session: AsyncSession = Depends(get_async_session)):
    query = select(trailers).where(trailers.c.status == 'no_view')
    result = await session.execute(query)
    rez = result.all()
    return templates.TemplateResponse('new_trailers.html', {"request": request, "rez": rez})


@router.post('/detail')
async def trailers_detail(request: Request, btn_det=Form(), session: AsyncSession = Depends(get_async_session)):
    id_film = btn_det
    query = select(trailers).where(trailers.c.id_film == id_film)
    result = await session.execute(query)
    rez = result.all()
    for link in rez:
        link_video = link.link_trailer

    response = RedirectResponse(url=link_video)
    return response


@router.post('/del')
async def trailers_del(request: Request, btn_del=Form(), session: AsyncSession = Depends(get_async_session)):
    id_film = btn_del
    stmt = update(trailers).where(trailers.c.id_film == id_film).values(status="viewed")
    await session.execute(stmt)
    await session.commit()
    query = select(trailers).where(trailers.c.status == 'no_view')
    result = await session.execute(query)
    rez = result.all()
    return templates.TemplateResponse('new_trailers.html', {"request": request, "rez": rez})
