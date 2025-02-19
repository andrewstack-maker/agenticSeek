from typing import Tuple, Callable
from abc import abstractmethod
import os
import random

class Agent():
    def __init__(self, model: str,
                       name: str,
                       prompt_path:str,
                       provider) -> None:
        self._name = name
        self._current_directory = os.getcwd()
        self._model = model
        self._llm = provider 
        self._history = [] 
        self._tools = {}
        self.set_system_prompt(prompt_path)
    
    def set_system_prompt(self, prompt_path: str) -> None:
        self.set_history(self.load_prompt(prompt_path))
    
    @property
    def history(self):
        return self._history

    @property
    def name(self) -> str:
        return self._name

    @property
    def get_tools(self) -> dict:
        return self._tools

    def set_history(self, system_prompt: str) -> None:
        """
        Set the default history for the agent.
        Deepseek developers recommand not using a system prompt directly.
        We therefore pass the system prompt as a user message.
        """
        self._history = [{'role': 'user', 'content': system_prompt},
                         {'role': 'assistant', 'content': f'Hello, How can I help you today ?'}]
    
    def add_to_history(self, role: str, content: str) -> None:
        self._history.append({'role': role, 'content': content})
    
    def clear_history(self) -> None:
        self._history = []
    
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
    
    def llm_request(self, history, verbose = True) -> Tuple[str, str]:
        thought = self._llm.respond(history, verbose)

        reasoning = self.extract_reasoning_text(thought)
        answer = self.remove_reasoning_text(thought)
        self.add_to_history('assistant', answer)
        return answer, reasoning
    
    def wait_message(self, speech_module):
        messages = ["Please be patient sir, I am working on it.",
                    "At it, sir. In the meantime, how about a joke?",
                    "Computing... I recommand you have a coffee while I work.",
                    "Hold on, I’m crunching numbers.",
                    "Working on it sir, please let me think."]
        speech_module.speak(messages[random.randint(0, len(messages)-1)])

    def execute_modules(self, answer: str) -> Tuple[bool, str]:
        feedback = ""
        blocks = None

        print("Loading tools: ", self._tools.items())
        for name, tool in self._tools.items():
            feedback = ""
            blocks = tool.load_exec_block(answer)

            if blocks != None:
                output = tool.execute(blocks)
                feedback = tool.interpreter_feedback(output)
                answer = tool.remove_block(answer)
                self.add_to_history('user', feedback)

            if "failure" in feedback.lower():
                return False, feedback
            if blocks == None:
                return True, feedback
            return True, feedback
