import platform, os

from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent, executorResult
from sources.tools.C_Interpreter import CInterpreter
from sources.tools.GoInterpreter import GoInterpreter
from sources.tools.PyInterpreter import PyInterpreter
from sources.tools.BashInterpreter import BashInterpreter
from sources.tools.fileFinder import FileFinder

class CoderAgent(Agent):
    """
    The code agent is an agent that can write and execute code.
    """
    def __init__(self, name, prompt_path, provider, verbose=False):
        super().__init__(name, prompt_path, provider, verbose, None)
        self.tools = {
            "bash": BashInterpreter(),
            "python": PyInterpreter(),
            "c": CInterpreter(),
            "go": GoInterpreter(),
            "file_finder": FileFinder()
        }
        self.work_dir = self.tools["file_finder"].get_work_dir()
        self.role = {
            "en": "code",
            "fr": "codage",
            "zh": "编码",
        }
        self.type = "code_agent"

    
    def add_sys_info_prompt(self, prompt):
        """Add system information to the prompt."""
        info = f"System Info:\n" \
               f"OS: {platform.system()} {platform.release()}\n" \
               f"Python Version: {platform.python_version()}\n" \
               f"\nYou must work in directory: {self.work_dir}"
        return f"{prompt}\n\n{info}"

    def process(self, prompt, speech_module) -> str:
        answer = ""
        attempt = 0
        max_attempts = 4
        prompt = self.add_sys_info_prompt(prompt)
        self.memory.push('user', prompt)
        clarify_trigger = "REQUEST_CLARIFICATION"

        while attempt < max_attempts:
            animate_thinking("Thinking...", color="status")
            self.wait_message(speech_module)
            answer, reasoning = self.llm_request()
            if clarify_trigger in answer:
                return answer.replace(clarify_trigger, ""), reasoning
            if not "```" in answer:
                self.last_answer = answer
                break
            animate_thinking("Executing code...", color="status")
            exec_success, _ = self.execute_modules(answer)
            answer = self.remove_blocks(answer)
            self.last_answer = answer
            if exec_success:
                break
            self.show_answer()
            attempt += 1
        if attempt == max_attempts:
            return "I'm sorry, I couldn't find a solution to your problem. How would you like me to proceed ?", reasoning
        return answer, reasoning

if __name__ == "__main__":
    pass