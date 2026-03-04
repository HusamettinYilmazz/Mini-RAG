from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_ERROR= "file_type_not_supported"
    FILE_SIZE_ERROR= "file_size_exceeded"
    FILE_UPLOAD_SUCCESS= "file_upload_success"
    FILE_UPLOAD_FAILED= "file_upload_failed"
