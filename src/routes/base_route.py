import os

from utils import get_settings, Settings
from fastapi import FastAPI, APIRouter, Depends

base_router = APIRouter(
    prefix = "/greating",
    tags = ["api", "greating"]
)

@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    
    project_name = app_settings.PROJECT_NAME
    project_version = app_settings.PROJECT_VERSION
    return {
        "project_name": project_name,
        "project_version": project_version,
        "message": "welcome to my project"
    }
