import json
from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.agents.code_agent import CoderAgent
from sources.agents.file_agent import FileAgent
from sources.agents.casual_agent import CasualAgent
from sources.tools.tools import Tools

class PlannerAgent(Agent):
    def __init__(self, model, name, prompt_path, provider):
        """
        The planner agent is a special agent that divides and conquers the task.
        """
        super().__init__(model, name, prompt_path, provider)
        self.tools = {
            "json": Tools()
        }
        self.tools['json'].tag = "json"
        self.agents = {
            "coder": CoderAgent(model, name, prompt_path, provider),
            "file": FileAgent(model, name, prompt_path, provider),
            "web": CasualAgent(model, name, prompt_path, provider)
        }
        self.role = "complex programming tasks and web research"
        self.tag = "json"

    def parse_agent_tasks(self, text):
        tasks = []
        tasks_names = []

        lines = text.strip().split('\n')
        for line in lines:
            if line is None or len(line) == 0:
                continue
            line = line.strip()
            if '##' in line or line[0].isdigit():
                tasks_names.append(line)
                continue
        blocks, _ = self.tools["json"].load_exec_block(text)
        if blocks == None:
            return (None, None)
        for block in blocks:
            line_json = json.loads(block)
            if 'plan' in line_json:
                for task in line_json['plan']:
                    agent = {
                        'agent': task['agent'],
                        'id': task['id'],
                        'task': task['task']
                    }
                    if 'need' in task:
                        agent['need'] = task['need']
                    tasks.append(agent)
        if len(tasks_names) != len(tasks):
            names = [task['task'] for task in tasks]
            return zip(names, tasks)
        return zip(tasks_names, tasks)
    
    def make_prompt(self, task, needed_infos):
        prompt = f"""
        You are given the following informations:
        {needed_infos}
        Your task is:
        {task}
        """
        return prompt
    
    def process(self, prompt, speech_module) -> str:
        self.memory.push('user', prompt)
        self.wait_message(speech_module)
        animate_thinking("Thinking...", color="status")
        agents_tasks = (None, None)
        answer, reasoning = self.llm_request()
        agents_tasks = self.parse_agent_tasks(answer)
        if agents_tasks == (None, None):
            return "Failed to parse the tasks", reasoning
        for task_name, task in agents_tasks:
            pretty_print(f"I will {task_name}.", color="info")
            agent_prompt = self.make_prompt(task['task'], task['need'])
            pretty_print(f"Assigned agent {task['agent']} to {task_name}", color="info")
            speech_module.speak(f"I will {task_name}. I assigned the {task['agent']} agent to the task.")
            try:
                self.agents[task['agent'].lower()].process(agent_prompt, None)
                pretty_print(f"-- Agent answer ---\n\n", color="output")
                self.agents[task['agent'].lower()].show_answer()
                pretty_print(f"\n\n", color="output")
            except Exception as e:
                pretty_print(f"Error: {e}", color="failure")
                speech_module.speak(f"I encountered an error: {e}")
                break
        self.last_answer = answer
        return answer, reasoning

if __name__ == "__main__":
    from llm_provider import Provider
    server_provider = Provider("server", "deepseek-r1:14b", "192.168.1.100:5000")
    agent = PlannerAgent("deepseek-r1:14b", "jarvis", "prompts/planner_agent.txt", server_provider)
    ans = agent.process("Make a cool game to illustrate the current relation between USA and europe")