
from .generator import GeneratorLLM

class OllamaLLM(GeneratorLLM):
    import ollama

    def __init__(self):
        """
        Handle generation using Ollama.
        """
        super().__init__()

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
                print(content, end='', flush=True)

                with self.state.lock:
                    self.state.current_buffer += content

        except ollama.ResponseError as e:
            if e.status_code == 404:
                self.logger.info(f"Downloading {self.model}...")
                ollama.pull(self.model)
            with self.state.lock:
                self.state.is_generating = False
            print(f"Error: {e}")
        except Exception as e:
            if "refused" in str(e).lower():
                raise Exception("Ollama connection failed. is the server running ?") from e
        finally:
            with self.state.lock:
                self.state.is_generating = False