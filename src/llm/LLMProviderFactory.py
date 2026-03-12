from .LLMEnums import LLMEnums
from .providers import OpenAIProvider, CohereProvider

class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config
    
    def create(self, provider: str):
        if provider == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key= self.config.OPENAI_API_KEY,
                api_url= self.config.OPENAI_API_URL,
                max_input_char= self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                max_gen_output_tokens= self.config.GENERATION_DAFAULT_MAX_TOKENS,
                gen_temperature= self.config.GENERATION_DAFAULT_TEMPERATURE
            )
        
        elif provider == LLMEnums.COHERE.value:
            return CohereProvider(
                api_key= self.config.COHERE_API_KEY,
                max_input_char= self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                max_gen_output_tokens= self.config.GENERATION_DAFAULT_MAX_TOKENS,
                gen_temperature= self.config.GENERATION_DAFAULT_TEMPERATURE
            )
        
        return None