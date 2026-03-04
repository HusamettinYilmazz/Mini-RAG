import os

from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse

from utils import Settings, get_settings
from controllers import DataController, ProjectController
from models import ResponseSignal

import logging
logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags= ["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile,
                app_settings: Settings= Depends(get_settings)):
    
    
    data_controller = DataController()
    is_valid, response_signal = data_controller.verify_file(file)

    ## if not valid return an error
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": response_signal
            }
            
        )
    ## if is_valid save file
    project_path = ProjectController().get_project_path(project_id)
    ## change the file name to an unique one
    