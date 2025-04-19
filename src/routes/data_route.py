import os

from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse

from utils import get_settings, Settings
from controllers import DataController, ProjectController
from models import ResponseSignal

import aiofiles


data_router = APIRouter(
    prefix = "/data", 
    tags = ["api", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile,
                     app_settings:Settings = Depends(get_settings)):
    
    data_controller = DataController()
    is_valid_file, data_responsed_signal = data_controller.validate_file(file)
    
    if not is_valid_file:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST, 
            content={
            "signal": data_responsed_signal
            }
        )

    project_controller = ProjectController()

    files_dir, project_responsed_signal = project_controller.get_project_path(project_id)
    file_path = os.path.join(files_dir, file.filename)

    valid_write = await data_controller.write_file(file_path, file)

    if not valid_write:
    
        return JSONResponse( 
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
            "signal": ResponseSignal.FILE_SAVE_ERROR.value
            }
        )

    return JSONResponse( 
            content={
            "signal": ResponseSignal.FILE_UPLOADED_SUCCESS.value
            }
        )