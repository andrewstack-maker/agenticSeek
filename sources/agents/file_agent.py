
from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.tools.fileFinder import FileFinder
from sources.tools.BashInterpreter import BashInterpreter

class FileAgent(Agent):
    def __init__(self, name, prompt_path, provider, verbose=False):
        """
        The file agent is a special agent for file operations.
        """
        super().__init__(name, prompt_path, provider, verbose)
        self.tools = {
            "file_finder": FileFinder(),
            "bash": BashInterpreter()
        }
        self.role = {
            "en": "find and read files",
            "fr": "trouver et lire des fichiers",
            "zh": "查找和读取文件",
            "es": "encontrar y leer archivos"
        }
        self.type = "file_agent"
    
    def process(self, prompt, speech_module) -> str:
        exec_success = False
        self.memory.push('user', prompt)

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