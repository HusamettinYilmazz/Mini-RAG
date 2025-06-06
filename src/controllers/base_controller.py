import os
import random
import string

from utils import get_settings, Settings, get_logger


class BaseController:
    def __init__(self):
        self.app_settings: Settings = get_settings()
        self.parent_path = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.parent_path, "assets", "files")

        self.logger = get_logger(save_dir=self.app_settings.LOGGING_PATH)


    def generate_random_string(self, length: int=6):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
