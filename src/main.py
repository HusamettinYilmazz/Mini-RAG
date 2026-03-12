from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

from routes import base_router, data_router
from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import get_settings
from llm.LLMProviderFactory import LLMProviderFactory

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    app.mongo_con = AsyncIOMotorClient(settings.DB_MONGO_URL)
    app.db_client = app.mongo_con[settings.DB_MONGO_NAME]

    llm_provider_factory = LLMProviderFactory(settings)
    app.emb_client = llm_provider_factory.create(settings.EMBEDDING_BACKEND)
    app.emb_client.set_embedding_model(
        model_id=settings.EMBEDDING_MODEL_ID,
        emb_size= settings.EMBEDDING_MODEL_SIZE)
    
    app.gen_client = llm_provider_factory.create(settings.GENERATION_BACKEND)
    app.gen_client.set_generation_model(
        model_id= settings.GENERATION_MODEL_ID
    )

    yield  ## application runs

    app.mongo_con.close()


app = FastAPI(lifespan=lifespan)

app.include_router(base_router)
app.include_router(data_router)
