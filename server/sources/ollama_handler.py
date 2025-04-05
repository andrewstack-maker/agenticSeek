
import time
from .generator import GeneratorLLM
from .cache import Cache
import ollama

class OllamaLLM(GeneratorLLM):

    def __init__(self):
        """
        Handle generation using Ollama.
        """
        super().__init__()
        self.cache = Cache()

    def generate(self, history):
        self.logger.info(f"Using {self.model} for generation with Ollama")
        try:
            with self.state.lock:
                self.state.is_generating = True
                self.state.last_complete_sentence = ""
                self.state.current_buffer = ""

            stream = ollama.chat(
                model=self.model,
                messages=history,
                stream=True,
            )
            for chunk in stream:
                content = chunk['message']['content']

                with self.state.lock:
                    if '.' in content:
                        self.logger.info(self.state.current_buffer)
                    self.state.current_buffer += content

        except Exception as e:
            if "404" in str(e):
                self.logger.info(f"Downloading {self.model}...")
                ollama.pull(self.model)
            if "refused" in str(e).lower():
                raise Exception("Ollama connection failed. is the server running ?") from e
            raise e
        finally:
            self.logger.info("Generation complete")
            with self.state.lock:
                self.state.is_generating = False

if __name__ == "__main__":
    generator = OllamaLLM()
    history = [
        {
            "role": "user",
            "content": "Hello, how are you ?"
        }
    ]
    generator.set_model("deepseek-r1:1.5b")
    generator.start(history)
    while True:
        print(generator.get_status())
        time.sleep(1)