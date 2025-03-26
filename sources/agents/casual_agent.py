
from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.tools.searxSearch import searxSearch
from sources.tools.flightSearch import FlightSearch
from sources.tools.fileFinder import FileFinder
from sources.tools.BashInterpreter import BashInterpreter

class CasualAgent(Agent):
    def __init__(self, name, prompt_path, provider, verbose=False):
        """
        The casual agent is a special for casual talk to the user without specific tasks.
        """
        super().__init__(name, prompt_path, provider, verbose)
        self.tools = {
        } # No tools for the casual agent
        self.role = {
            "en": "talk",
            "fr": "discuter",
            "zh": "聊天",
            "es": "discutir"
        }
        self.type = "casual_agent"
    
    def process(self, prompt, speech_module) -> str:
        self.memory.push('user', prompt)
        animate_thinking("Thinking...", color="status")
        answer, reasoning = self.llm_request()
        self.last_answer = answer
        return answer, reasoning

if __name__ == "__main__":
    from llm_provider import Provider

    #local_provider = Provider("ollama", "deepseek-r1:14b", None)
    server_provider = Provider("server", "deepseek-r1:14b", "192.168.1.100:5000")
    agent = CasualAgent("deepseek-r1:14b", "jarvis", "prompts/casual_agent.txt", server_provider)
    ans = agent.process("Hello, how are you?")
    print(ans)