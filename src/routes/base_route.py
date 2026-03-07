import os

from fastapi import FastAPI, APIRouter, Depends
from utils.config import Settings, get_settings

base_router = APIRouter(
    prefix="/api/v1", 
    tags=["api_v1"]
)

@base_router.get("/")
async def welcome(app_setings:Settings = Depends(get_settings)):
    app_setings = get_settings()
    app_name = app_setings.APP_NAME
    app_version = app_setings.APP_VERSION

    return {
        "app_name": app_name,
        "app_version": app_version
    }