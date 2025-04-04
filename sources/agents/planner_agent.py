import json
from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.agents.code_agent import CoderAgent
from sources.agents.file_agent import FileAgent
from sources.agents.browser_agent import BrowserAgent
from sources.tools.tools import Tools

class PlannerAgent(Agent):
    def __init__(self, name, prompt_path, provider, verbose=False, browser=None):
        """
        The planner agent is a special agent that divides and conquers the task.
        """
        super().__init__(name, prompt_path, provider, verbose, None)
        self.tools = {
            "json": Tools()
        }
        self.tools['json'].tag = "json"
        self.browser = browser
        self.agents = {
            "coder": CoderAgent(name, "prompts/base/coder_agent.txt", provider, verbose=False),
            "file": FileAgent(name, "prompts/base/file_agent.txt", provider, verbose=False),
            "web": BrowserAgent(name, "prompts/base/browser_agent.txt", provider, verbose=False, browser=browser)
        }
        self.role = {
            "en": "Complex Task",
            "fr": "Tache complexe",
            "zh": "复杂任务",
        }
        self.type = "planner_agent"

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
        if needed_infos is None:
            needed_infos = "No needed informations."
        prompt = f"""
        You are given the following informations:
        {needed_infos}
        Your task is:
        {task}
        """
        return prompt
    
    def show_plan(self, json_plan):
        agents_tasks = self.parse_agent_tasks(json_plan)
        if agents_tasks == (None, None):
            return
        pretty_print("▂▘ P L A N ▝▂", color="output")
        for task_name, task in agents_tasks:
                    pretty_print(f"{task['agent']} -> {task['task']}", color="info")
        pretty_print("▔▗ E N D ▖▔", color="output")
    
    def process(self, prompt, speech_module) -> str:
        ok = False
        agents_tasks = (None, None)
        while not ok:
            self.wait_message(speech_module)
            animate_thinking("Thinking...", color="status")
            self.memory.push('user', prompt)
            answer, _ = self.llm_request()
            pretty_print(answer.split('\n')[0], color="output")
            self.show_plan(answer)
            ok_str = input("Is the plan ok? (y/n): ")
            if ok_str == 'y':
                ok = True
            else:
                prompt = input("Please reformulate: ")

        agents_tasks = self.parse_agent_tasks(answer)
        if agents_tasks == (None, None):
            return "Failed to parse the tasks", reasoning
        prev_agent_answer = None
        for task_name, task in agents_tasks:
            pretty_print(f"I will {task_name}.", color="info")
            agent_prompt = self.make_prompt(task['task'], prev_agent_answer)
            pretty_print(f"Assigned agent {task['agent']} to {task_name}", color="info")
            if speech_module: speech_module.speak(f"I will {task_name}. I assigned the {task['agent']} agent to the task.")
            try:
                prev_agent_answer, _ = self.agents[task['agent'].lower()].process(agent_prompt, speech_module)
                pretty_print(f"-- Agent answer ---\n\n", color="output")
                self.agents[task['agent'].lower()].show_answer()
                pretty_print(f"\n\n", color="output")
            except Exception as e:
                raise e
        self.last_answer = prev_agent_answer
        return prev_agent_answer, ""

if __name__ == "__main__":
    from llm_provider import Provider
    server_provider = Provider("server", "deepseek-r1:14b", "192.168.1.100:5000")
    agent = PlannerAgent("deepseek-r1:14b", "jarvis", "prompts/planner_agent.txt", server_provider)
    ans = agent.process("Make a cool game to illustrate the current relation between USA and europe")