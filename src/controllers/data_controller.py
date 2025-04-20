import os
import sys
import re

from fastapi import UploadFile

import aiofiles

from .base_controller import BaseController
from .project_controller import ProjectController
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
    
    async def write_file(self, project_id, file:UploadFile):

        file_path, file_name = self.generate_unique_file_path(file.filename, project_id)
        try:
            async with aiofiles.open(file_path, "wb") as f:
                while chunck := await file.read(self.app_settings.FILE_DEFAULT_MAX_CHUNK_SIZE):
                    await f.write(chunck)
            
            return True, file_name

        except Exception as e:
            self.logger.error(f"Error while uploading file: {e}")
            return False, file_name

    def generate_unique_file_path(self, orig_file_name: str,  project_id: str):
        random_key = self.generate_random_string()
        project_path, _ = ProjectController().get_project_path(project_id=project_id)

        cleaned_file_name = self.clean_file_name(orig_file_name=orig_file_name)

        new_file_path = os.path.join(project_path, f"{project_id}_{random_key}_{cleaned_file_name}")

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_path, f"{project_id}_{random_key}_{cleaned_file_name}")

        return new_file_path, f"{project_id}_{random_key}_{cleaned_file_name}"

    def clean_file_name(self, orig_file_name: str):
        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
