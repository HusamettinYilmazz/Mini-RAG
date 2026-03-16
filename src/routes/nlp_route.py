import os

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse

from models.ChunkModel import ChunkModel
from models.ProjectModel import ProjectModel
from models.enums import ResponseSignal
from utils.config import Settings, get_settings
from .schemes import PushRequest, SearchRequest
from controllers import NLPController

import logging
logger = logging.getLogger("uvicorn.error")

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags= ["api_v1", "nlp"]
)

@nlp_router.post("/index/push/{project_id}")
async def index_project_into_vectordb(request: Request, project_id: str, push_request: PushRequest):
    
    project_model = ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_or_insert_project(project_id=project_id)

    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)
    
    nlp_controller = NLPController(embedding_client= request.app.emb_client,
                                   generation_client= request.app.gen_client,
                                   vectordb_client= request.app.vectordb_client)
    
    has_records = True
    page_num = 1
    inserted_item_cnt = 0
    while has_records:
        page_chunks = await chunk_model.get_chunks_by_project_id(
                            project_id=project.id, page=page_num)
        
        if len(page_chunks):
            page_num += 1
        
        if not page_chunks or len(page_chunks)==0:
            has_records = False
            break
    
        is_indexed = nlp_controller.index_into_vectordb(project= project, chunks= page_chunks, 
                                                        do_reset= push_request.do_reset)
        
        inserted_item_cnt += len(page_chunks)
        if not is_indexed:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.PROJECT_INDEX_FAILED.value
                }
            )
                

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "signal": ResponseSignal.PROJECT_INDEX_SUCCES.value,
            "inserted items count": inserted_item_cnt
        }
    )
