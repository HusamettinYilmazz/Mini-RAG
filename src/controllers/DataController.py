import os

from fastapi import UploadFile
import aiofile
import random
import re

from .BaseController import BaseController
from models import ResponseSignal

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.MBTOBYTE = 1048576

    def verify_file(self, file: UploadFile):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_ERROR.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.MBTOBYTE:
            return False, ResponseSignal.FILE_SIZE_ERROR.value

        return True, ResponseSignal.FILE_UPLOAD_SUCCESS.value

    async def write_file(self, file_path, file: UploadFile):
        async with aiofile.async_open(file_path, "wb") as dest:
            while chunck := await file.read(self.app_settings.FILE_CHUNCK_SIZE):
                await dest.write(chunck)

    def generate_unique_file_path(self, file_name:str, project_id:str):
        random_key = int(random.uniform(1, 9) * 10**7) ## 8 digit random number
        cleaned_file_name = self.get_clean_file_name(file_name)

        project_path = os.path.join(self.root_path, "assets", "files", project_id)
        new_file_path = os.path.join(project_path, 
                                     f"{random_key}_{cleaned_file_name}")

        while os.path.exists(new_file_path):
            random_key = int(random.uniform(1, 9) * 10**7) ## 8 digit random number
            new_file_path = os.path.join(project_path, 
                                         f"{random_key}_{cleaned_file_name}")

        return new_file_path
    
    def get_clean_file_name(self, file_name:str):
        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
