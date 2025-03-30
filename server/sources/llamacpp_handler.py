
from .generator import GeneratorLLM
from llama_cpp import Llama
from .decorator import timer_decorator

class LlamacppLLM(GeneratorLLM):

    def __init__(self):
        """
        Handle generation using llama.cpp
        """
        super().__init__()
        self.llm = None
    
    @timer_decorator
    def generate(self, history):
        if self.llm is None:
            self.logger.info(f"Loading {self.model}...")
            self.llm = Llama.from_pretrained(
                repo_id=self.model,
                filename="*Q8_0.gguf",
                n_ctx=4096,
                verbose=True
            )
        self.logger.info(f"Using {self.model} for generation with Llama.cpp")
        try:
            with self.state.lock:
                self.state.is_generating = True
                self.state.last_complete_sentence = ""
                self.state.current_buffer = ""
            output = self.llm.create_chat_completion(
                  messages = history
            )
            with self.state.lock:
                self.state.current_buffer = output['choices'][0]['message']['content']
        except Exception as e:
            self.logger.error(f"Error: {e}")
        finally:
            with self.state.lock:
                self.state.is_generating = False