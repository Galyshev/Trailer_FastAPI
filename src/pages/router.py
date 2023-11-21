from fastapi import APIRouter, Request, Form
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
async def trailers_detail(request: Request, btn_det=Form()):
    print(btn_det)
    return templates.TemplateResponse('tmp.html', {"request": request})


@router.post('/del')
async def trailers_del(request: Request, btn_del=Form()):
    print(btn_del)
    return templates.TemplateResponse('tmp.html', {"request": request})
