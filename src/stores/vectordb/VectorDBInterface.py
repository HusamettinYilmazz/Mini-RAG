from abc import ABC, abstractmethod
from typing import List

class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def create_collection(self, collection_name: str,
                          emb_size: int, do_reset: bool = False):
        pass

    @abstractmethod
    def is_collection_exist(self, collection_name: str) -> bool:
        pass
    
    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def list_all_collections(self) -> List:
        pass

    @abstractmethod
    def insert_item(self, collection_name: str, txt: str,
                    vector: list, metadat: dict=None, record_id: str=None):
        pass

    @abstractmethod
    def insert_many_items(self, collection_name: str, txt: list,
                    vector: list, metadat: list=None, record_id: list=None):
        pass

    @abstractmethod
    def search_by_vector(self, collection_name: str, vector: list, limit:int):
        pass