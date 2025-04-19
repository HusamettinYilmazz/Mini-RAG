from fastapi import UploadFile

import aiofiles

from .base_controller import BaseController
from models import ResponseSignal
# from utils import get_logger

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.file_size_scale = 1048575 ## convert to bytes
        

    def validate_file(self, file: UploadFile):
        
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_ERROR.value
        elif file.size > self.app_settings.FILE_MAX_SIZE * self.file_size_scale:
            return False, ResponseSignal.FILE_SIZE_ERROR.value
        
        return True, ResponseSignal.FILE_UPLOADED_SUCCESS.value
    
    async def write_file(self, file_path, file:UploadFile):
        try:
            async with aiofiles.open(file_path, "wb") as f:
                while chunck := await file.read(self.app_settings.FILE_DEFAULT_MAX_CHUNK_SIZE):
                    await f.write(chunck)
            
            return True

        except Exception as e:
            self.logger.error(f"Error while uploading file: {e}")
            return False