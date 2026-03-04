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

