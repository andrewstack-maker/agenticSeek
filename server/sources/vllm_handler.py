from vllm import LLM, SamplingParams
import logging
from typing import List, Dict

class Vllm(GeneratorLLM):
    def __init__(self):
        """
        Handle generation using vLLM.
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.llm = LLM(model=self.model)
        
    def convert_history_to_prompt(self, history: List[Dict[str, str]]) -> str:
        """
        Convert OpenAI-format history to a single prompt string for vLLM.
        """
        prompt = ""
        for message in history:
            role = message["role"]
            content = message["content"]
            if role == "system":
                prompt += f"System: {content}\n"
            elif role == "user":
                prompt += f"User: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"
        prompt += "Assistant: "
        return prompt

    def generate(self, history: List[Dict[str, str]]):
        """
        Generate response using vLLM from OpenAI-format message history.
        
        Args:
            history: List of dictionaries in OpenAI format [{"role": "user", "content": "..."}, ...]
        """
        self.logger.info(f"Using {self.model} for generation with vLLM")
        
        try:
            with self.state.lock:
                self.state.is_generating = True
                self.state.last_complete_sentence = ""
                self.state.current_buffer = ""

            prompt = self.convert_history_to_prompt(history)
            
            sampling_params = SamplingParams(
                temperature=0.7,
                max_tokens=512,
                stream=True  # Enable streaming
            )
            outputs = self.llm.generate(prompt, sampling_params, use_tqdm=False)
            for output in outputs:
                content = output.outputs[0].text
                with self.state.lock:
                    if '.' in content:
                        self.logger.info(self.state.current_buffer)
                    self.state.current_buffer += content
            with self.state.lock:
                self.logger.info(f"Final output: {self.state.current_buffer}")

        except Exception as e:
            self.logger.error(f"Error during generation: {str(e)}")
            raise e
            
        finally:
            self.logger.info("Generation complete")
            with self.state.lock:
                self.state.is_generating = False