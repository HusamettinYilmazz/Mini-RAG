from .VectorDBEnums import VectorDBEnums
from .providers.QdrantDBProvider import QdrantDBProvider
from controllers import BaseController

class VectorDBFactory:
    def __init__(self, config):
        self.config = config
        self.base_controller = BaseController()

    def create(self, provider_name: str):
        if provider_name == VectorDBEnums.QDRANT.value:
            dp_path = self.base_controller.get_database_dir(self.config.VECTOR_DB_NAME)

            qdrand_provider = QdrantDBProvider(dp_path=dp_path)
            qdrand_provider.set_distance_method(
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD)
            
            return qdrand_provider
        
        return None