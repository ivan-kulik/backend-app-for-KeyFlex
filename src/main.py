import uvicorn
from fastapi import FastAPI

from contextlib import asynccontextmanager

from core.config import settings
from core.models import db_helper

from api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    #startapp
    yield
    #shutdown
    print("dispose engine")
    await db_helper.dispose()


app = FastAPI(
    lifespan=lifespan,
    name='backend app for KeyFlex project',
)

app.include_router(
    api_router,
    prefix=settings.api.prefix
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
