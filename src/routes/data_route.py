import os

from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse

from utils.config import Settings, get_settings
from controllers import DataController, ProjectController, ProcessController
from models.enums import ResponseSignal
from .schemes import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import Chunk

import logging
logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags= ["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_file(request: Request, project_id: str, file: UploadFile,
                app_settings: Settings= Depends(get_settings)):
    
    project_model = ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_or_insert_project(project_id=project_id)

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

@data_router.post("/process/{project_id}")
async def process_files(request: Request, project_id: str, process_request: ProcessRequest):
    file_id = process_request.file_id

    project_model = ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_or_insert_project(project_id=project_id)

    chunk_model = ChunkModel(db_client=request.app.db_client)

    chunks = ProcessController(project_id).process_file_content(
        file_id=file_id,
        chunk_size= process_request.chunk_size,
        overlap_size= process_request.overlap_size)
    
    if not chunks or len(chunks)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_PROCESSING_FAILED.value
            }
            
        )

    file_chunks = [
        Chunk(
            chunk_text= chunk.page_content,
            chunk_metadata= chunk.metadata,
            chunk_order= i,
            chunk_project_id= project.id
        )
        for i, chunk in enumerate(chunks, start=1)
    ]
    
    if process_request.do_reset: 
        ## Delete all records then store new records
        num_del_chunks = await chunk_model.delete_chunks_by_project_id(
            project_id= project.id)
    else:
        num_del_chunks = 0
    num_chunks = await chunk_model.insert_many_chunks(chunks=file_chunks)

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "signal": ResponseSignal.FILE_PROCESSING_SUCCES.value,
                "num_of_inserted_chunks": num_chunks,
                "num_of_deleted_chunks": num_del_chunks
            }
            
        )
