import os

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .BaseController import BaseController
from .ProjectController import ProjectController
from models.enums import ProcessingEnum

class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]
    
    def get_file_loader(self, file_id: str):
        file_ext = self.get_file_extension(file_id)
        print(file_ext)
        if file_ext == ProcessingEnum.TXT_EXT.value:
            return TextLoader(
                    os.path.join(self.project_path, file_id),
                    encoding="utf-8")
            
        elif file_ext == ProcessingEnum.PDF_EXT.value:
            return PyMuPDFLoader(os.path.join(self.project_path, file_id))
        
        return None
    
    def get_file_content(self, file_id: str):
        file_loader = self.get_file_loader(file_id)
        if not file_loader:
            return None
        file_content = file_loader.load()
        return file_content
    
    def process_file_content(self, file_id: str,
                             chunk_size: int, overlap_size: int):
        file_content = self.get_file_content(file_id)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = overlap_size,
            length_function= len
        )
        
        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            texts= file_content_texts,
            metadatas= file_content_metadata
        )

        return chunks
