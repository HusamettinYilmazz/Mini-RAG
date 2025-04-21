import os

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .base_controller import BaseController
from .project_controller import ProjectController
from models import ProcessingEnum

class ProcessController(BaseController):
    def __init__(self, project_id):
        super().__init__()

        self.project_id = project_id
        self.project_path, _ = ProjectController().get_project_path(self.project_id)

    def get_file_extension(slef, file_id: str):
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):
        file_path = os.path.join(self.project_path, file_id)

        file_ext = self.get_file_extension(file_id)
        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")

        elif file_ext == ProcessingEnum.PDF.value:
            return pyMuPDFLoader(file_path, encoding="utf-8")

        return None

    def get_file_content(self, file_id: str):
        file_loader = self.get_file_loader(file_id)

        return file_loader.load()

    def chunk_file_content(self, file_content: list, chunk_size: int, overlap_size: int):

        text_splitter = RecursiveCharacterTextSplitter(chunk_size= chunk_size,
                        chunk_overlap= overlap_size,  length_function= len)
        
        file_text = [doc.page_content for doc in file_content]

        file_metadata = [doc.metadata for doc in file_content]

        chunks = text_splitter.create_documents(file_text, metadatas= file_metadata)

        return chunks