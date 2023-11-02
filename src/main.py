from fastapi import FastAPI
import uvicorn
from trailers.router import router as router_trailers

app = FastAPI(
    title='Trailers'
)

app.include_router(router_trailers)

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)