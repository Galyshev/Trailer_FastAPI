import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from pages.router import router as router_pages
from trailers.router import router as router_trailers

app = FastAPI(
    title='Trailers'
)

app.mount("/static", StaticFiles(directory="static"), name='static')

app.include_router(router_trailers)
app.include_router(router_pages)

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
