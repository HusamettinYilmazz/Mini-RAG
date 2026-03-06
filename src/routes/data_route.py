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
    file_path, new_filename = data_controller.generate_unique_file_path(file.filename, project_id)
    # file_path = os.path.join(project_path, file_name)
    
    try:
        await data_controller.write_file(file_path, file)
    except Exception as e:
        ## log the error
        logger.error(f"Error while writing file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
                }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_name": new_filename
        }
    )