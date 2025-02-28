from typing import Tuple, Callable
from abc import abstractmethod
import os
import random
from sources.memory import Memory
from sources.utility import pretty_print

class Agent():
    def __init__(self, model: str,
                       name: str,
                       prompt_path:str,
                       provider) -> None:
        self._name = name
        self._current_directory = os.getcwd()
        self._model = model
        self._llm = provider 
        self._memory = Memory(self.load_prompt(prompt_path),
                                memory_compression=False)
        self._tools = {}
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def get_tools(self) -> dict:
        return self._tools

    def add_tool(self, name: str, tool: Callable) -> None:
        if tool is not Callable:
            raise TypeError("Tool must be a callable object (a method)")
        self._tools[name] = tool
    
    def load_prompt(self, file_path: str) -> str:
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found at path: {file_path}")
        except PermissionError:
            raise PermissionError(f"Permission denied to read prompt file at path: {file_path}")
        except Exception as e:
            raise e
    
    @abstractmethod
    def answer(self, prompt, speech_module) -> str:
        """
        abstract method, implementation in child class.
        """
        pass

    def remove_reasoning_text(self, text: str) -> None:
        end_tag = "</think>"
        end_idx = text.rfind(end_tag)+8
        return text[end_idx:]
    
    def extract_reasoning_text(self, text: str) -> None:
        start_tag = "<think>"
        end_tag = "</think>"
        start_idx = text.find(start_tag)
        end_idx = text.rfind(end_tag)+8
        return text[start_idx:end_idx]
    
    def llm_request(self, verbose = True) -> Tuple[str, str]:
        memory = self._memory.get()
        thought = self._llm.respond(memory, verbose)

        reasoning = self.extract_reasoning_text(thought)
        answer = self.remove_reasoning_text(thought)
        self._memory.push('assistant', answer)
        return answer, reasoning
    
    def wait_message(self, speech_module):
        messages = ["Please be patient sir, I am working on it.",
                    "At it, sir. In the meantime, how about a joke?",
                    "Computing... I recommand you have a coffee while I work.",
                    "Hold on, I’m crunching numbers.",
                    "Working on it sir, please let me think."]
        speech_module.speak(messages[random.randint(0, len(messages)-1)])
    
    def print_code_blocks(self, blocks: list, name: str):
        for block in blocks:
            pretty_print(f"Executing {name} code...\n", color="output")
            pretty_print("-"*100, color="output")
            pretty_print(block, color="code")
            pretty_print("-"*100, color="output")

    def execute_modules(self, answer: str) -> Tuple[bool, str]:
        feedback = ""
        blocks = None

        for name, tool in self._tools.items():
            feedback = ""
            blocks, save_path = tool.load_exec_block(answer)

            if blocks != None:
                self.print_code_blocks(blocks, name)
                output = tool.execute(blocks)
                feedback = tool.interpreter_feedback(output)
                self._memory.push('user', feedback)

            if "failure" in feedback.lower():
                return False, feedback
            if save_path != None:
                tool.save_block(blocks, save_path)
        return True, feedback
