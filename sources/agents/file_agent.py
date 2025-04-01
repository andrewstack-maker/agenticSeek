
from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.tools.fileFinder import FileFinder
from sources.tools.BashInterpreter import BashInterpreter

class FileAgent(Agent):
    def __init__(self, name, prompt_path, provider, verbose=False):
        """
        The file agent is a special agent for file operations.
        """
        super().__init__(name, prompt_path, provider, verbose, None)
        self.tools = {
            "file_finder": FileFinder(),
            "bash": BashInterpreter()
        }
        self.work_dir = self.tools["file_finder"].get_work_dir()
        self.role = {
            "en": "files",
            "fr": "fichiers",
            "zh": "文件",
        }
        self.type = "file_agent"
    
    def process(self, prompt, speech_module) -> str:
        exec_success = False
        prompt += f"\nYou must work in directory: {self.work_dir}"
        self.memory.push('user', prompt)
        while exec_success is False:
            self.wait_message(speech_module)
            animate_thinking("Thinking...", color="status")
            answer, reasoning = self.llm_request()
            exec_success, _ = self.execute_modules(answer)
            answer = self.remove_blocks(answer)
            self.last_answer = answer
        return answer, reasoning

if __name__ == "__main__":
    from llm_provider import Provider

    #local_provider = Provider("ollama", "deepseek-r1:14b", None)
    server_provider = Provider("server", "deepseek-r1:14b", "192.168.1.100:5000")
    agent = FileAgent("deepseek-r1:14b", "jarvis", "prompts/file_agent.txt", server_provider)
    ans = agent.process("What is the content of the file toto.py ?")
    print(ans)