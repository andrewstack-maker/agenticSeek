import json
from typing import List, Tuple, Type, Dict
from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.agents.code_agent import CoderAgent
from sources.agents.file_agent import FileAgent
from sources.agents.browser_agent import BrowserAgent
from sources.text_to_speech import Speech
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
    
    def make_prompt(self, task: dict, agent_infos_dict: dict):
        infos = ""
        if agent_infos_dict is None or len(agent_infos_dict) == 0:
            infos = "No needed informations."
        else:
            for agent_id, info in agent_infos_dict.items():
                infos += f"\t- According to agent {agent_id}:\n{info}\n\n"
        prompt = f"""
        You are given informations from your AI friends work:
        {infos}
        Your task is:
        {task}
        """
        return prompt
    
    def show_plan(self, json_plan: dict) -> None:
        agents_tasks = self.parse_agent_tasks(json_plan)
        if agents_tasks == (None, None):
            pretty_print("Failed to make a plan.", color="failure")
            return
        pretty_print("\n▂▘ P L A N ▝▂", color="status")
        for task_name, task in agents_tasks:
            pretty_print(f"{task['agent']} -> {task['task']}", color="info")
        pretty_print("▔▗ E N D ▖▔", color="status")
    
    def make_plan(self, prompt: str) -> str:
        ok = False
        answer = None
        while not ok:
            animate_thinking("Thinking...", color="status")
            self.memory.push('user', prompt)
            answer, _ = self.llm_request()
            for line in answer.split('\n'):
                if "```json" in line:
                    break
            pretty_print(line, color="output")
            self.show_plan(answer)
            ok_str = input("Is the plan ok? (y/n): ")
            if ok_str == 'y':
                ok = True
            else:
                prompt = input("Please reformulate: ")
        return answer
    
    def start_agent_process(self, task: str, required_infos: dict | None) -> str:
        agent_prompt = self.make_prompt(task['task'], required_infos)
        pretty_print(f"Agent {task['agent']} started working...", color="status")
        agent_answer, _ = self.agents[task['agent'].lower()].process(agent_prompt, None)
        self.agents[task['agent'].lower()].show_answer()
        pretty_print(f"Agent {task['agent']} completed task.", color="status")
        return agent_answer
    
    def get_work_result_agent(self, task_needs, agents_work_result):
        return {k: agents_work_result[k] for k in task_needs if k in agents_work_result}

    def process(self, prompt: str, speech_module: Speech) -> str:
        agents_tasks = (None, None)
        agents_work_result = dict()

        answer = self.make_plan(prompt)
        agents_tasks = self.parse_agent_tasks(answer)

        if agents_tasks == (None, None):
            return "Failed to parse the tasks.", reasoning
        for task_name, task in agents_tasks:
            pretty_print(f"I will {task_name}.", color="info")
            pretty_print(f"Assigned agent {task['agent']} to {task_name}", color="info")
            if speech_module: speech_module.speak(f"I will {task_name}. I assigned the {task['agent']} agent to the task.")

            if agents_work_result is not None:
                required_infos = self.get_work_result_agent(task['need'], agents_work_result)
            try:
                self.last_answer = self.start_agent_process(task, required_infos)
            except Exception as e:
                raise e
            agents_work_result[task['id']] = self.last_answer
        return self.last_answer, ""