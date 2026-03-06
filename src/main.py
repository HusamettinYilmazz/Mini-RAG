from fastapi import FastAPI, APIRouter
from routes import base_router, data_router
from motor.motor_asyncio import AsyncIOMotorClient
from utils import get_settings

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()

    app.mongo_con = AsyncIOMotorClient(settings.DB_MONGO_URL)
    app.db_client = app.mongo_con[settings.DB_MONGO_NAME]

app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_con.close()


app.include_router(base_router)
app.include_router(data_router)
