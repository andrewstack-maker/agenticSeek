
from typing import Tuple, Callable
from abc import abstractmethod
import os
import random
import time

from sources.memory import Memory
from sources.utility import pretty_print

random.seed(time.time())

class executorResult:
    """
    A class to store the result of a tool execution.
    """
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
    """
    An abstract class for all agents.
    """
    def __init__(self, model: str,
                       name: str,
                       prompt_path:str,
                       provider,
                       recover_last_session=True) -> None:
        self.agent_name = name
        self.role = None
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
    def get_tools(self) -> dict:
        return self.tools

    def add_tool(self, name: str, tool: Callable) -> None:
        if tool is not Callable:
            raise TypeError("Tool must be a callable object (a method)")
        self.tools[name] = tool
    
    def load_prompt(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found at path: {file_path}")
        except PermissionError:
            raise PermissionError(f"Permission denied to read prompt file at path: {file_path}")
        except Exception as e:
            raise e
    
    @abstractmethod
    def process(self, prompt, speech_module) -> str:
        """
        abstract method, implementation in child class.
        Process the prompt and return the answer of the agent.
        """
        pass

    def remove_reasoning_text(self, text: str) -> None:
        """
        Remove the reasoning block of reasoning model like deepseek.
        """
        end_tag = "</think>"
        end_idx = text.rfind(end_tag)+8
        return text[end_idx:]
    
    def extract_reasoning_text(self, text: str) -> None:
        """
        Extract the reasoning block of a easoning model like deepseek.
        """
        start_tag = "<think>"
        end_tag = "</think>"
        start_idx = text.find(start_tag)
        end_idx = text.rfind(end_tag)+8
        return text[start_idx:end_idx]
    
    def llm_request(self, verbose = False) -> Tuple[str, str]:
        """
        Ask the LLM to process the prompt and return the answer and the reasoning.
        """
        memory = self.memory.get()
        thought = self.llm.respond(memory, verbose)

        reasoning = self.extract_reasoning_text(thought)
        answer = self.remove_reasoning_text(thought)
        self.memory.push('assistant', answer)
        return answer, reasoning
    
    def wait_message(self, speech_module):
        if speech_module is None:
            return
        messages = ["Please be patient, I am working on it.",
                    "Computing... I recommand you have a coffee while I work.",
                    "Hold on, I’m crunching numbers.",
                    "Working on it, please let me think."]
        speech_module.speak(messages[random.randint(0, len(messages)-1)])
    
    def get_blocks_result(self) -> list:
        return self.blocks_result

    def show_answer(self):
        """
        Show the answer in a pretty way.
        Show code blocks and their respective feedback by inserting them in the ressponse.
        """
        lines = self.last_answer.split("\n")
        for line in lines:
            if "block:" in line:
                block_idx = int(line.split(":")[1])
                if block_idx < len(self.blocks_result):
                    self.blocks_result[block_idx].show()
            else:
                pretty_print(line, color="output")
        self.blocks_result = []

    def remove_blocks(self, text: str) -> str:
        """
        Remove all code/query blocks within a tag from the answer text.
        """
        tag = f'```'
        lines = text.split('\n')
        post_lines = []
        in_block = False
        block_idx = 0
        for line in lines:
            if tag in line and not in_block:
                in_block = True
                continue
            if not in_block:
                post_lines.append(line)
            if tag in line:
                in_block = False
                post_lines.append(f"block:{block_idx}")
                block_idx += 1
        return "\n".join(post_lines)

    def execute_modules(self, answer: str) -> Tuple[bool, str]:
        """
        Execute all the tools the agent has and return the result.
        """
        feedback = ""
        success = False
        blocks = None

        for name, tool in self.tools.items():
            feedback = ""
            blocks, save_path = tool.load_exec_block(answer)

            if blocks != None:
                pretty_print(f"Executing tool: {name}", color="status")
                output = tool.execute(blocks)
                feedback = tool.interpreter_feedback(output) # tool interpreter feedback
                success = not tool.execution_failure_check(output)
                pretty_print(feedback, color="success" if success else "failure")
                self.memory.push('user', feedback)
                self.blocks_result.append(executorResult(blocks, feedback, success))
                if not success:
                    return False, feedback
                if save_path != None:
                    tool.save_block(blocks, save_path)
        return True, feedback
