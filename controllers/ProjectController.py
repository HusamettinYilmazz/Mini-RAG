import os

from .BaseController import BaseController


class ProjectController(BaseController):
    def __init__(self):
        super().__init__()


    def get_project_path(self, project_id):
        project_path = os.path.join(self.root_path, "assets", "files", f"{project_id}")
        os.makedirs(project_path, exist_ok=True)

        return project_path