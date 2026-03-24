from typing import List

from qdrant_client import QdrantClient, models
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMthodEnums
import logging

class QdrantDBProvider(VectorDBInterface):
    def __init__(self, dp_path):
        self.dp_path = dp_path
        self.client = None
        self.distance_method = None

        self.logger = logging.getLogger(__name__)
        ...
    
    def connect(self):
        self.client = QdrantClient(path=self.dp_path)

    def disconnect(self):
        self.client = None

    
    def set_distance_method(self, distance_method):
        if distance_method == DistanceMthodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMthodEnums.DOT.value:
            self.distance_method =models.Distance.DOT

    def create_collection(self, collection_name: str,
                          emb_size: int, do_reset: bool = False):
        
        if self.is_collection_exist(collection_name=collection_name):
            if not do_reset:
                self.logger.error(f"Collection is already existing")
                return False
            
            self.delete_collection(collection_name=collection_name)

        try:
            self.client.create_collection(collection_name=collection_name,
                                        vectors_config=models.VectorParams(
                                            size=emb_size, distance=self.distance_method),
                                        )
        except Exception as e:
            self.logger.error(f"Error while creating collection: {e}")
    
    def is_collection_exist(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
       
    def get_collection_info(self, collection_name: str) -> dict:
        if self.is_collection_exist(collection_name=collection_name):
            return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str) -> bool:
        if self.is_collection_exist(collection_name=collection_name):
            return self.client.delete_collection(collection_name=collection_name)
    
    def list_all_collections(self) -> List:
        return self.client.get_collections()

    def insert_item(self, collection_name: str, txt: str,
                    vector: list, metadata: dict=None, record_id: str=None):
        
        if not self.is_collection_exist(collection_name):
            return False
        
        try:
            self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(vector=vector, 
                                payload={"text": txt, "metadata": metadata}
                                )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error while inserting item: {e}")
            return False
        
        return True
    
    def insert_many_items(self, collection_name: str, txt: list, vector: list,
                    metadata: list=None, record_id: list=None, batch_size: int=50):
        
        if not self.is_collection_exist(collection_name):
            return False
        
        if metadata is None:
            metadata = [None] * len(txt)

        if record_id is None:
            record_id = [None] * len(txt)

        for i in range(0, len(txt), batch_size):
            batch_end = min(i+batch_size, len(txt))
            
            records = [
                        models.Record(id=j, 
                                      vector=vector[j],
                                      payload={
                                        "text": txt[j],
                                        "metadata": metadata[j]
                                    }
                                )
                        for j in range(i, batch_end)
                    ]

            try:
                self.client.upload_records(
                    collection_name=collection_name,
                    records=records
                )
            except Exception as e:
                self.logger.error(f"Error while inserting batch: {e}")
                return False
        
        return True

    def search_by_vector(self, collection_name: str, vector: list, limit:int):
        if not self.is_collection_exist(collection_name):
            return False

        return self.client.query_points(
                            collection_name=collection_name,
                            query=vector, limit=limit)