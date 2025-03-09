
from sources.utility import pretty_print
from sources.agents.agent import Agent, CoderAgent, FileAgent

class PlannerAgent(Agent):
    def __init__(self, model, name, prompt_path, provider):
        """
        The planner agent is a special agent that divides and conquers the task.
        """
        super().__init__(model, name, prompt_path, provider)
        self.tools = {
        }
        self.agents = {
            "coder": CoderAgent(model, name, prompt_path, provider),
            "file": FileAgent(model, name, prompt_path, provider)
        }
        self.role = "planning"
    
    def process(self, prompt, speech_module) -> str:
        complete = False
        exec_success = False
        self.memory.push('user', prompt)

        self.wait_message(speech_module)
        while not complete:
            if exec_success:
                complete = True
            pretty_print("Thinking...", color="status")
            answer, reasoning = self.llm_request()
            exec_success, _ = self.execute_modules(answer)
            answer = self.remove_blocks(answer)
            self.last_answer = answer
        return answer, reasoning

if __name__ == "__main__":
    from llm_provider import Provider
    server_provider = Provider("server", "deepseek-r1:14b", "192.168.1.100:5000")
    agent = PlannerAgent("deepseek-r1:14b", "jarvis", "prompts/planner_agent.txt", server_provider)
    ans = agent.process("Make a cool game to illustrate the current relation between USA and europe")