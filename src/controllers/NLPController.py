import json
from typing import List

from .BaseController import BaseController
from models.db_schemes import Project, Chunk
from llm.LLMEnums import DocumentTypeEnum

class NLPController(BaseController):
    def __init__(self, embedding_client, generation_client, vectordb_client):
        super().__init__()
        self.emb_client = embedding_client
        self.gen_client = generation_client

        self.vectordb_client = vectordb_client

    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()
    
    def reset_vectordb_collection(self, project: Project):
        collection_name = self.create_collection_name(
            project_id=project.project_id)
        
        if self.vectordb_client.is_collection_exist(collection_name):
            return self.vectordb_client.delete_collection(collection_name)

    def get_vectordb_collection_info(self, project: Project):
        collection_name = self.create_collection_name(
            project_id=project.project_id)
        
        collection_info = self.vectordb_client.get_collection_info(collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )

    def index_into_vectordb(self, project: Project, chunks:List[Chunk],
                            do_reset: bool=False):
        
        collection_name = self.create_collection_name(
            project_id=project.project_id)
        
        _ = self.vectordb_client.create_collection(
                    collection_name= collection_name, 
                    emb_size= self.emb_client.emb_size , do_reset=do_reset)
        
        
        # if do_reset:
        #     self.reset_vectordb_collection(project=project)
        
        chunks_txt = [
            chunk.chunk_text
            for chunk in chunks]
        
        metadatas= [
            chunk.chunk_metadata
            for chunk in chunks]
        
        records_id = list(range(len(chunks)))
        
        vectors = [
            self.emb_client.embed_text(txt, document_type=DocumentTypeEnum.DOCUMENT.value)
            for txt in chunks_txt]
        
        self.vectordb_client.insert_many_items(self, collection_name=collection_name, 
                                               txt=chunks_txt, vector=vectors, 
                                               metadat=metadatas, record_id=records_id)
        
        return True
        