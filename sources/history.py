import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class History():
    """
    History is a class for managing the conversation history
    It provides a method to compress the history (experimental, use with caution).
    """
    def __init__(self, system_prompt: str, memory_compression: bool = True):
        self._history = []
        self._history = [{'role': 'user', 'content': system_prompt},
                 {'role': 'assistant', 'content': f'Hello, How can I help you today ?'}]
        self.model = "pszemraj/led-base-book-summary"
        self.device = self.get_cuda_device()
        self.memory_compression = memory_compression
        if memory_compression:
            self._tokenizer = AutoTokenizer.from_pretrained(self.model)
            self._model = AutoModelForSeq2SeqLM.from_pretrained(self.model)
    
    def get_cuda_device(self) -> str:
        if torch.backends.mps.is_available():
            return "mps"
        elif torch.cuda.is_available():
            return "cuda"
        else:
            return "cpu"

    def summarize(self, text: str, min_length: int = 64) -> str:
        if self._tokenizer is None or self._model is None:
            return text
        max_length = len(text) // 2 if len(text) > min_length*2 else min_length*2
        input_text = "summarize: " + text
        inputs = self._tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = self._model.generate(
            inputs['input_ids'],
            max_length=max_length,  # Maximum length of the summary
            min_length=min_length,  # Minimum length of the summary
            length_penalty=1.0,  # Adjusts length preference
            num_beams=4,  # Beam search for better quality
            early_stopping=True  # Stop when all beams finish
        )
        summary = self._tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

    def timer_decorator(func):
        from time import time
        def wrapper(*args, **kwargs):
            start_time = time()
            result = func(*args, **kwargs)
            end_time = time()
            print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute")
            return result
        return wrapper
    
    @timer_decorator
    def compress(self) -> str:
        if not self.memory_compression:
            return
        for i in range(len(self._history)):
            if i <= 2:
                continue
            if self._history[i]['role'] == 'assistant':
                self._history[i]['content'] = self.summarize(self._history[i]['content'])
    
    def reset(self, history: list) -> None:
        self._history = history
    
    def push(self, role: str, content: str) -> None:
        self._history.append({'role': role, 'content': content})
        # EXPERIMENTAL
        if self.memory_compression and role == 'assistant':
            self.compress()
    
    def clear(self) -> None:
        self._history = []
    
    def get(self) -> list:
        return self._history

if __name__ == "__main__":
    history = History("You are a helpful assistant.")
    
    sample_text = """
The error you're encountering:

Copy
cuda.cu:52:10: fatal error: helper_functions.h: No such file or directory
 #include <helper_functions.h>
          ^~~~~~~~~~~~~~~~~~~~
compilation terminated.
indicates that the compiler cannot find the helper_functions.h file. This is because the #include <helper_functions.h> directive is looking for the file in the system's include paths, but the file is either not in those paths or is located in a different directory.

Solutions
1. Use #include "helper_functions.h" Instead of #include <helper_functions.h>
Angle brackets (< >) are used for system or standard library headers.

Quotes (" ") are used for local or project-specific headers.

If helper_functions.h is in the same directory as cuda.cu, change the include directive to:

3. Verify the File Exists
Double-check that helper_functions.h exists in the specified location. If the file is missing, you'll need to obtain or recreate it.

4. Use the Correct CUDA Samples Path (if applicable)
If helper_functions.h is part of the CUDA Samples, ensure you have the CUDA Samples installed and include the correct path. For example, on Linux, the CUDA Samples are typically located in /usr/local/cuda/samples/common/inc. You can include this path like so:

Use #include "helper_functions.h" for local files.

Use the -I flag to specify the directory containing helper_functions.h.

Ensure the file exists in the specified location.
    """
    
    history.push('user', "why do i get this error?")
    history.push('assistant', sample_text)
    print("\n---\nHistory before:", history.get())
    history.compress()
    print("\n---\nHistory after:", history.get())
    
    