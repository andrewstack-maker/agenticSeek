
from sources.utility import pretty_print
from sources.agents.agent import Agent
from sources.agents.code_agent import CoderAgent
from sources.agents.file_agent import FileAgent
from sources.agents.casual_agent import CasualAgent

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
            "file": FileAgent(model, name, prompt_path, provider),
            "web": CasualAgent(model, name, prompt_path, provider)
        }
        self.role = "complex programming tasks and web research"

    def parse_agent_tasks(self, text):
        agents_tasks = []

        lines = text.strip().split('\n')
        for line in lines:
            if not '-' in line:
                continue
            if not line.strip() or ':' not in line:
                continue
            agent_part, task = line.split(':', 1)
            task = task.strip()
            agent_info = agent_part.strip().split('(')
            agent_type = agent_info[0].strip()
            params_part = agent_info[1].rstrip(')').split(',')
            params = {}
            for param in params_part:
                key, value = param.split('=')
                params[key.strip()] = value.strip().strip('"')
            agent = {
                'type': agent_type,
                'name': params['name'],
                'task': task
            }
            if 'need' in params:
                agent['need'] = params['need']
            agents_tasks.append(agent)
        return agents_tasks
    
    def process(self, prompt, speech_module) -> str:
        self.memory.push('user', prompt)
        self.wait_message(speech_module)
        pretty_print("Thinking...", color="status")
        print(self.memory.get())
        answer, reasoning = self.llm_request()
        agents_tasks = self.parse_agent_tasks(answer)
        print(agents_tasks)
        self.last_answer = answer
        return answer, reasoning

if __name__ == "__main__":
    from llm_provider import Provider
    server_provider = Provider("server", "deepseek-r1:14b", "192.168.1.100:5000")
    agent = PlannerAgent("deepseek-r1:14b", "jarvis", "prompts/planner_agent.txt", server_provider)
    ans = agent.process("Make a cool game to illustrate the current relation between USA and europe")