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
async def index_project_into_vectordb(request: Request, project_id: str, push_request: PushRequest,
                                      app_settings: Settings= Depends(get_settings)):
    
    project_model = ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_or_insert_project(project_id=project_id)

    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)
    
    nlp_controller = NLPController(embedding_client= request.app.emb_client,
                                   generation_client= request.app.gen_client,
                                   vectordb_client= request.app.vectordb_client,
                                   template_parser=request.app.template_parser)
    
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

@nlp_router.get("/index/info/{project_id}")
async def index_info(request: Request, project_id: str):
    
    project_model = ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_or_insert_project(project_id=project_id)
    
    nlp_controller = NLPController(embedding_client= request.app.emb_client,
                                   generation_client= request.app.gen_client,
                                   vectordb_client= request.app.vectordb_client,
                                   template_parser=request.app.template_parser)
    
    collection_info = nlp_controller.get_vectordb_collection_info(project=project)

    if not collection_info:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.VECTORDB_COLLECTION_RETRIEVE_FAILED.value
                }
            )
                

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "signal": ResponseSignal.VECTORDB_COLLECTION_RETRIEVED.value,
            "collection info": collection_info
        }
    )

@nlp_router.post("/index/search/{project_id}")
async def search_index(request: Request, project_id: str, search_request: SearchRequest):
    
    project_model = ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_or_insert_project(project_id=project_id)
    
    nlp_controller = NLPController(embedding_client= request.app.emb_client,
                                   generation_client= request.app.gen_client,
                                   vectordb_client= request.app.vectordb_client,
                                   template_parser=request.app.template_parser)
    
    results = nlp_controller.search_vectordb_collection(
        project= project, text= search_request.text, limit=search_request.limit
    )

    if not results:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.VECTORDB_SEARCH_FAILED.value
                }
            )
                

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "signal": ResponseSignal.VECTORDB_SEARCH_SUCCES.value,
            "results": [{"score": point.score,
                         "text": point.payload.get("text")}
                        
                        for point in results.points
                       ]
        }
    )

@nlp_router.post("/index/answer/{project_id}")
async def answer_rag(request: Request, project_id: str, search_request: SearchRequest):
    
    project_model = ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_or_insert_project(project_id=project_id)
    
    nlp_controller = NLPController(embedding_client= request.app.emb_client,
                                   generation_client= request.app.gen_client,
                                   vectordb_client= request.app.vectordb_client,
                                   template_parser=request.app.template_parser)
    
    answer = nlp_controller.answer_rag_question(project= project,
                                                 query=search_request.text,
                                                 limit=search_request.limit)

    if not answer:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.RAG_ANSWER_ERROR.value
                }
            )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "signal": ResponseSignal.RAG_ANSWER_SUCCES.value,
            "answer": answer
        }
    )
