from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums
from openai import OpenAI
import logging

class OpenAIProvider(LLMInterface):
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

        self.client = OpenAI(api_key=self.api_key,
                              base_url=self.api_url if self.api_url and len(self.api_url) else None)
        
        self.logger = logging.getLogger(__name__)
    
    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.emb_model_id = model_id
        self.emb_size = embedding_size

    def set_generation_model(self, model_id: str):
        self.gen_model_id = model_id

    def process_text(self, text: str):
        return text[:self.max_input_char]
    
    def embed_text(self, text, document_type = None):
        if not self.client:
            self.logger.error("OpenAI client isn't setted")
            return None
        
        if not self.emb_model_id:
            self.logger.error("OpenAI embedding model isn't setted")
            return None
        
        response = self.client.embeddings.create(
            input=text,
            model=self.emb_model_id
        )

        if not response or not response.data or len(response.data)==0 or not response.data[0].embedding:
            self.logger.error("No result from embeding model")
            return None
        
        return response.data[0].embedding
    
    def generate_text(self, prompt: str, chat_histroy: list=[], 
                      max_output_tokens: int=None, temperature: float=None):
        if not self.client:
            self.logger.error("OpenAI client isn't setted")
            return None
        
        if not self.gen_model_id:
            self.logger.error("OpenAI generation model isn't setted")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.max_gen_output_tokens
        temperature = temperature if temperature else self.gen_temperature

        messages = chat_histroy.append(self.constract_prompt(
                prompt=prompt, role=OpenAIEnums.USER.value))
        
        response = self.client.chat.completions.create(
            model= self.gen_model_id,
            messages= messages,
            max_tokens= max_output_tokens,
            temperature= temperature
        )

        if not response or not response.choices or len(response.choices)==0 or not response.choices[0].message:
            self.logger.error("No result from generation model")
            return None

        return response.choices[0].message["content"]
    
    def constract_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }