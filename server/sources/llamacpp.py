
from .generator import GeneratorLLM

class LlamacppLLM(GeneratorLLM):
    from llama_cpp import Llama

    def __init__(self):
        """
        Handle generation using llama.cpp
        """
        super().__init__()
        self.llm = Llama.from_pretrained(
            repo_id=self.model,
            filename="*q8_0.gguf",
            verbose=True
        )
    
    def generate(self, history):
        self.logger.info(f"Using {self.model} for generation with Llama.cpp")
        self.llm.create_chat_completion(
              messages = history
        )