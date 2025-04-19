import os
from .base_controller import BaseController
from models import ResponseSignal

class ProjectController(BaseController):
    def __init__(self, ):
        super().__init__()
    

    def get_project_path(self, project_id: str):
        files_path = os.path.join(self.files_dir, project_id)
        os.makedirs(files_path, exist_ok=True)

        return files_path, ResponseSignal.PATH_CREATION_SUCCESS.value

