from enum import Enum

class ResponseSignal(Enum):
    
    FILE_TYPE_ERROR = "File type is not supported"
    FILE_SIZE_ERROR = "File size exceeded"
    FILE_UPLOADED_SUCCESS = "Files uploaded successfully"
    FILE_SAVE_ERROR = "Unexpected ERROR, Files are not saved"
    FILE_CHUNK_FAILED = "File processing faild"
    FILE_CHUNK_SUCCESS = "File is processed successfully"
    PATH_CREATION_SUCCESS = "Path is created successfully"