
from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.tools.fileFinder import FileFinder
from sources.tools.BashInterpreter import BashInterpreter

class FileAgent(Agent):
    def __init__(self, model, name, prompt_path, provider):
        """
        The file agent is a special agent for file operations.
        """
        super().__init__(model, name, prompt_path, provider)
        self.tools = {
            "file_finder": FileFinder(),
            "bash": BashInterpreter()
        }
        self.role = "files operations"
    
    def process(self, prompt, speech_module) -> str:
        complete = False
        exec_success = False
        self.memory.push('user', prompt)

        self.wait_message(speech_module)
        while not complete:
            if exec_success:
                complete = True
            animate_thinking("Thinking...", color="status")
            answer, reasoning = self.llm_request()
            exec_success, _ = self.execute_modules(answer)
            answer = self.remove_blocks(answer)
            self.last_answer = answer
            complete = True
            for name, tool in self.tools.items():
                if tool.found_executable_blocks():
                    complete = False # AI read results and continue the conversation
        return answer, reasoning

if __name__ == "__main__":
    from llm_provider import Provider

    #local_provider = Provider("ollama", "deepseek-r1:14b", None)
    server_provider = Provider("server", "deepseek-r1:14b", "192.168.1.100:5000")
    agent = FileAgent("deepseek-r1:14b", "jarvis", "prompts/file_agent.txt", server_provider)
    ans = agent.process("What is the content of the file toto.py ?")
    print(ans)