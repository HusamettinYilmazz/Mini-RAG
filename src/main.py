from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

from routes import base_router, data_router
from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import get_settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    app.mongo_con = AsyncIOMotorClient(settings.DB_MONGO_URL)
    app.db_client = app.mongo_con[settings.DB_MONGO_NAME]

    yield  ## application runs

    app.mongo_con.close()


app = FastAPI(lifespan=lifespan)

app.include_router(base_router)
app.include_router(data_router)
