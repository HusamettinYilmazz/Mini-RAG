import os
import sys

ROOT = '/home/husammm/Desktop/Courses/CS_courses/DL/Clabs/Mini-Rag/src'
sys.path.append(ROOT)

from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse

from utils import get_settings, Settings
from controllers import DataController, ProjectController
from models import ResponseSignal

import aiofiles
from io import BytesIO
import asyncio


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

    valid_write, file_name = await data_controller.write_file(project_id, file)

    if not valid_write:
    
        return JSONResponse( 
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
            "signal": ResponseSignal.FILE_SAVE_ERROR.value
            }
        )

    return JSONResponse( 
            content={
            "signal": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
            "file_name": file_name
            }
        )

class FakeFile(UploadFile):
    def __init__(self, filename="file.txt", content=b"Hello world!!!!!"):
        super().__init__(filename=filename, file=BytesIO(content))

if __name__ == "__main__":

    fake_file = FakeFile()
    app_settings = Settings()
    result = asyncio.run(upload_file("4", fake_file, app_settings))
