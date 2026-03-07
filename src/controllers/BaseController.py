import os

from utils.config import Settings, get_settings

class BaseController:
    def __init__(self):
        self.app_settings: Settings = get_settings()
        self.base_path = os.path.dirname(__file__)
        self.root_path = os.path.dirname(self.base_path)

