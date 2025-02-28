from typing import Tuple, Callable
from abc import abstractmethod
import os
import random
from sources.memory import Memory
from sources.utility import pretty_print

class executorResult:
    def __init__(self, blocks, feedback, success):
        self.blocks = blocks
        self.feedback = feedback
        self.success = success
    
    def show(self):
        for block in self.blocks:
            pretty_print("-"*100, color="output")
            pretty_print(block, color="code" if self.success else "failure")
            pretty_print("-"*100, color="output")
            pretty_print(self.feedback, color="success" if self.success else "failure")

class Agent():
    def __init__(self, model: str,
                       name: str,
                       prompt_path:str,
                       provider,
                       recover_last_session=False) -> None:
        self.agent_name = name
        self.current_directory = os.getcwd()
        self.model = model
        self.llm = provider 
        self.memory = Memory(self.load_prompt(prompt_path),
                                recover_last_session=recover_last_session,
                                memory_compression=False)
        self.tools = {}
        self.blocks_result = []
        self.last_answer = ""
    
    @property
    def name(self) -> str:
        return self.name

    @property
    def get_tools(self) -> dict:
        return self.tools

    def add_tool(self, name: str, tool: Callable) -> None:
        if tool is not Callable:
            raise TypeError("Tool must be a callable object (a method)")
        self.tools[name] = tool
    
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
        memory = self.memory.get()
        thought = self.llm.respond(memory, verbose)

        reasoning = self.extract_reasoning_text(thought)
        answer = self.remove_reasoning_text(thought)
        self.memory.push('assistant', answer)
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
    
    def get_blocks_result(self) -> list:
        return self.blocks_result

    def execute_modules(self, answer: str) -> Tuple[bool, str]:
        feedback = ""
        success = False
        blocks = None

        for name, tool in self.tools.items():
            feedback = ""
            blocks, save_path = tool.load_exec_block(answer)

            if blocks != None:
                output = tool.execute(blocks)
                feedback = tool.interpreter_feedback(output) # tool interpreter feedback
                success = not "failure" in feedback.lower()
                self.memory.push('user', feedback)
                self.blocks_result.append(executorResult(blocks, feedback, success))
                if not success:
                    return False, feedback
                if save_path != None:
                    tool.save_block(blocks, save_path)
        return True, feedback
