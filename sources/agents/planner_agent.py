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
        self.role = "planification"
        self.type = "planner_agent"
    
    def get_task_names(self, text: str) -> List[str]:
        """
        Extracts task names from the given text.
        This method processes a multi-line string, where each line may represent a task name.
        containing '##' or starting with a digit. The valid task names are collected and returned.
        Args:
            text (str): A string containing potential task titles (eg: Task 1: I will...).
        Returns:
            List[str]: A list of extracted task names that meet the specified criteria.
        """
        tasks_names = []
        lines = text.strip().split('\n')
        for line in lines:
            if line is None:
                continue
            line = line.strip()
            if len(line) == 0:
                continue
            if '##' in line or line[0].isdigit():
                tasks_names.append(line)
                continue
        return tasks_names

    def parse_agent_tasks(self, text: str) -> List[Tuple[str, str]]:
        """
        Parses agent tasks from the given LLM text.
        This method extracts task information from a JSON. It identifies task names and their details.
        Args:
            text (str): The input text containing task information in a JSON-like format.
        Returns:
            List[Tuple[str, str]]: A list of tuples containing task names and their details.
        """
        tasks = []
        tasks_names = self.get_task_names(text)

        blocks, _ = self.tools["json"].load_exec_block(text)
        if blocks == None:
            return []
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
            return list(map(list, zip(names, tasks)))
        return list(map(list, zip(tasks_names, tasks)))
    
    def make_prompt(self, task: str, agent_infos_dict: dict) -> str:
        """
        Generates a prompt for the agent based on the task and previous agents work information.
        Args:
            task (str): The task to be performed.
            agent_infos_dict (dict): A dictionary containing information from other agents.
        Returns:
            str: The formatted prompt for the agent.
        """
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
    
    def show_plan(self, agents_tasks: List[dict], answer: str) -> None:
        """
        Displays the plan made by the agent.
        Args:
            agents_tasks (dict): The tasks assigned to each agent.
            answer (str): The answer from the LLM.
        """
        if agents_tasks == []:
            pretty_print(answer, color="warning")
            pretty_print("Failed to make a plan. This can happen with (too) small LLM. Clarify your request and insist on it making a plan within ```json.", color="failure")
            return
        pretty_print("\n▂▘ P L A N ▝▂", color="status")
        for task_name, task in agents_tasks:
            pretty_print(f"{task['agent']} -> {task['task']}", color="info")
        pretty_print("▔▗ E N D ▖▔", color="status")

    async def make_plan(self, prompt: str) -> str:
        """
        Asks the LLM to make a plan.
        Args:
            prompt (str): The prompt to be sent to the LLM.
        Returns:
            str: The plan made by the LLM.
        """
        ok = False
        answer = None
        while not ok:
            animate_thinking("Thinking...", color="status")
            self.memory.push('user', prompt)
            answer, reasoning = await self.llm_request()
            if "NO_UPDATE" in answer:
                return []
            agents_tasks = self.parse_agent_tasks(answer)
            if agents_tasks == []:
                prompt = f"Failed to parse the tasks. Please make a plan within ```json.\n"
                pretty_print("Failed to make plan. Retrying...", color="warning")
                continue
            self.show_plan(agents_tasks, answer)
            ok = True
        return self.parse_agent_tasks(answer)
    
    async def update_plan(self, goal: str, agents_tasks: List[dict], agents_work_result: dict, id: str, success: bool) -> dict:
        """
        Updates the plan with the results of the agents work.
        Args:
            goal (str): The goal to be achieved.
            agents_tasks (list): The tasks assigned to each agent.
            agents_work_result (dict): The results of the agents work.
        Returns:
            dict: The updated plan.
        """
        self.status_message = "Updating plan..."
        last_agent_work = agents_work_result[id]
        tool_success_str = "success" if success else "failure"
        pretty_print(f"Agent {id} work {tool_success_str}.", color="success" if success else "failure")
        next_task = agents_tasks[int(id)][0]
        #if success:
        #    return agents_tasks # we only update the plan if last task failed, for now
        update_prompt = f"""
        Your goal is : {goal}
        You previously made a plan, agents are currently working on it.
        The last agent working on task: {id}, did the following work:
        {last_agent_work}
        Agent {id} work was a {tool_success_str} according to system interpreter.
        The agent {id} about to work on task: {next_task}
        Is the work done for task {id} leading to sucess or failure ? Did an agent fail with a task?
        If agent work was good: answer "NO_UPDATE"
        If agent work is leading to failure: update the plan.
        plan should be within ```json like before.
        You need to rewrite the whole plan, but only change the tasks after task {id}.
        Keep the plan as short as the original one if possible. Do not change past tasks.
        """
        pretty_print("Updating plan...", color="status")
        plan = await self.make_plan(update_prompt)
        if plan == []:
            pretty_print("No plan update required.", color="info")
            return agents_tasks
        return plan
    
    async def start_agent_process(self, task: dict, required_infos: dict | None) -> str:
        """
        Starts the agent process for a given task.
        Args:
            task (dict): The task to be performed.
            required_infos (dict | None): The required information for the task.
        Returns:
            str: The result of the agent process.
        """
        self.status_message = f"Starting task {task['task']}..."
        agent_prompt = self.make_prompt(task['task'], required_infos)
        pretty_print(f"Agent {task['agent']} started working...", color="status")
        agent_answer, _ = await self.agents[task['agent'].lower()].process(agent_prompt, None)
        success = self.agents[task['agent'].lower()].get_success
        self.agents[task['agent'].lower()].show_answer()
        pretty_print(f"Agent {task['agent']} completed task.", color="status")
        return agent_answer, success
    
    def get_work_result_agent(self, task_needs, agents_work_result):
        return {k: agents_work_result[k] for k in task_needs if k in agents_work_result}

    async def process(self, goal: str, speech_module: Speech) -> Tuple[str, str]:
        """
        Process the goal by dividing it into tasks and assigning them to agents.
        Args:
            goal (str): The goal to be achieved (user prompt).
            speech_module (Speech): The speech module for text-to-speech.
        Returns:
            Tuple[str, str]: The result of the agent process and empty reasoning string.
        """
        agents_tasks = []
        agents_work_result = dict()

        self.status_message = "Making a plan..."
        agents_tasks = await self.make_plan(goal)

        if agents_tasks == []:
            return "Failed to parse the tasks.", ""
        i = 0
        steps = len(agents_tasks)
        while i < steps:
            task_name, task = agents_tasks[i][0], agents_tasks[i][1]
            self.status_message = "Starting agents..."
            pretty_print(f"I will {task_name}.", color="info")
            pretty_print(f"Assigned agent {task['agent']} to {task_name}", color="info")
            if speech_module: speech_module.speak(f"I will {task_name}. I assigned the {task['agent']} agent to the task.")

            if agents_work_result is not None:
                required_infos = self.get_work_result_agent(task['need'], agents_work_result)
            try:
                self.last_answer, success = await self.start_agent_process(task, required_infos)
            except Exception as e:
                raise e
            agents_work_result[task['id']] = self.last_answer
            if i == steps - 1:
                break
            agents_tasks = await self.update_plan(goal, agents_tasks, agents_work_result, task['id'], success)
            steps = len(agents_tasks)
            i += 1

        return self.last_answer, ""