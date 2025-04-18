import os

from fastapi import FastAPI, APIRouter

base_router = APIRouter()

@base_router.get("/")
async def welcome():
    project_name = os.getenv("PROJECT_NAME")
    project_version = os.getenv("PROJECT_VERSION")
    return {
        "project_name": project_name,
        "project_version": project_version,
        "message": "welcome to my project"
    }
