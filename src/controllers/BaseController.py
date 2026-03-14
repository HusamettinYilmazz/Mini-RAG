import os

from utils.config import Settings, get_settings

class BaseController:
    def __init__(self):
        self.app_settings: Settings = get_settings()
        self.base_path = os.path.dirname(__file__)
        self.root_path = os.path.dirname(self.base_path)

        self.database_dir = os.path.join(self.root_path, "assets/database")
    
    def get_database_dir(self, db_name: str):
        database_path = os.path.join(self.database_dir, db_name)
        os.makedirs(database_path, exist_ok=True)

        return database_path
