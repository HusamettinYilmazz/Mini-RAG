from ..LLMInterface import LLMInterface
from ..LLMEnums import CoHereEnums, DocumentTypeEnum
import cohere
import logging

class CohereProvider(LLMInterface):
    def __init__(self, api_key: str, api_url: str=None, max_input_char: int=1028,
                    max_gen_output_tokens: int= None, gen_temperature: float=0.1):
        
        self.api_key = api_key
        self.api_url = api_url
        self.max_input_char = max_input_char
        self.max_gen_output_tokens = max_gen_output_tokens
        self.gen_temperature = gen_temperature

        self.emb_model_id = None
        self.emb_size = None
        self.gen_model_id = None

        self.client = cohere(api_key=self.api_key)
        
        self.logger = logging.getLogger(__name__)
    
    def set_embedding_model(self, model_id: str, emb_size: int):
        self.emb_model_id = model_id
        self.emb_size = emb_size

    def set_generation_model(self, model_id: str):
        self.gen_model_id = model_id

    def process_text(self, text: str):
        return text[:self.max_input_char]
    
    def embed_text(self, text: str, document_type: str = None):
        if not self.client:
            self.logger.error("CoHere client was not set")
            return None
        
        if not self.emb_model_id:
            self.logger.error("Embedding model for CoHere was not set")
            return None
        
        input_type = CoHereEnums.DOCUMENT
        if document_type == DocumentTypeEnum.QUERY:
            input_type = CoHereEnums.QUERY

        response = self.client.embed(
            model = self.emb_model_id,
            texts = [self.process_text(text)],
            input_type = input_type,
            embedding_types=['float'],
        )

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error while embedding text with CoHere")
            return None
        
        return response.embeddings.float[0]
    
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):

        if not self.client:
            self.logger.error("CoHere client was not set")
            return None

        if not self.gen_model_id :
            self.logger.error("Generation model for CoHere was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.max_gen_output_tokens
        temperature = temperature if temperature else self.gen_temperature

        response = self.client.chat(
            model = self.gen_model_id ,
            chat_history = chat_history,
            message = self.process_text(prompt),
            temperature = temperature,
            max_tokens = max_output_tokens
        )

        if not response or not response.text:
            self.logger.error("Error while generating text with CoHere")
            return None
        
        return response.text
    
    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "text": self.process_text(prompt)
        }