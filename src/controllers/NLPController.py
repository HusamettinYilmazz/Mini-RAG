import json
from typing import List

from .BaseController import BaseController
from models.db_schemes import Project, Chunk
from llm.LLMEnums import DocumentTypeEnum

class NLPController(BaseController):
    def __init__(self, embedding_client, generation_client,
                  vectordb_client, template_parser):
        super().__init__()
        self.emb_client = embedding_client
        self.gen_client = generation_client

        self.vectordb_client = vectordb_client
        self.template_parser = template_parser

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
        
        self.vectordb_client.insert_many_items(collection_name=collection_name, 
                                               txt=chunks_txt, vector=vectors, 
                                               metadata=metadatas, record_id=records_id)
        
        return True

    def search_vectordb_collection(self, project: Project, text: str, limit: int=10):

        collection_name = self.create_collection_name(project_id=project.project_id)

        query_vector = self.emb_client.embed_text(text, document_type=DocumentTypeEnum.QUERY.value)

        result = self.vectordb_client.search_by_vector(
            collection_name=collection_name, 
            vector=query_vector, limit=limit)

        return result

    def answer_rag_question(self, project: Project, query: str, limit: int=10):
        retrieved_documents = self.search_vectordb_collection(project, query)
        
        ## build system prompt
        system_prompt = self.template_parser.get(key= "system_prompt", group="rag")

        ## build message
        document_prompts = "\n".join([
            self.template_parser.get(key= "document_prompt", group="rag",
                                     vars = {"doc_num": idx+1, "chunk_text": doc.payload.get("text")})
                                     
                                     for idx, doc in enumerate(retrieved_documents.points)
                                     ])
        ## build footer
        footer_prompt = self.template_parser.get(key= "footer_prompt", group="rag",
                                                 vars = {"question": query})

        chat_history = [
            self.gen_client.constract_prompt(
                prompt=system_prompt,
                role=self.gen_client.enums.SYSTEM.value,
            )
        ]

        full_prompt = "\n\n".join([document_prompts, footer_prompt])

        answer = self.gen_client.generate_text(prompt= full_prompt, chat_histroy=chat_history, )

        return answer
