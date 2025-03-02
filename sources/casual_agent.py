
from sources.utility import pretty_print
from sources.agent import Agent

class CasualAgent(Agent):
    def __init__(self, model, name, prompt_path, provider):
        """
        The casual agent is a special for casual talk to the user without specific tasks.
        """
        super().__init__(model, name, prompt_path, provider)
        self.tools = {
        } # TODO implement casual tools like basic web search, basic file search, basic image search, basic knowledge search
        self.role = "talking"

    def show_answer(self):
        lines = self.last_answer.split("\n")
        for line in lines:
            pretty_print(line, color="output")
    
    def process(self, prompt, speech_module) -> str:
        self.memory.push('user', prompt)

        pretty_print("Thinking...", color="status")
        self.wait_message(speech_module)
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