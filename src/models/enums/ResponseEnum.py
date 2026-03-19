from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_ERROR= "file_type_not_supported"
    FILE_SIZE_ERROR= "file_size_exceeded"
    FILE_UPLOAD_SUCCESS= "file_upload_success"
    FILE_UPLOAD_FAILED= "file_upload_failed"
    FILE_PROCESSING_SUCCES= "file_processing_succes"
    FILE_PROCESSING_FAILED= "file_processing_failed"
    PROJECT_INDEX_SUCCES= "project_indexing_into_vectordb_success"
    PROJECT_INDEX_FAILED="project_indexing_into_vectordb_failed"
    VECTORDB_COLLECTION_RETRIEVED = "collection_retrieved_sucess"
    VECTORDB_COLLECTION_RETRIEVE_FAILED= "collection_retrieve_failed"
    VECTORDB_SEARCH_SUCCES = "vectordb_search_succes"
    VECTORDB_SEARCH_FAILED = "vectordb_search_failed"
    RAG_ANSWER_ERROR = "rag_answer_error"
    RAG_ANSWER_SUCCES = "rag_answer_success"