import os
import sys
import torch
from transformers import pipeline

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sources.agents.agent import Agent
from sources.agents.code_agent import CoderAgent
from sources.agents.casual_agent import CasualAgent
from sources.agents.planner_agent import PlannerAgent
from sources.utility import pretty_print

class AgentRouter:
    """
    AgentRouter is a class that selects the appropriate agent based on the user query.
    """
    def __init__(self, agents: list, model_name: str = "facebook/bart-large-mnli"):
        self.model = model_name 
        self.pipeline = pipeline("zero-shot-classification",
                      model=self.model)
        self.agents = agents
        self.labels = [agent.role for agent in agents]

    def get_device(self) -> str:
        if torch.backends.mps.is_available():
            return "mps"
        elif torch.cuda.is_available():
            return "cuda:0"
        else:
            return "cpu"

    def classify_text(self, text: str, threshold: float = 0.5) -> list:
        """
        Classify the text into labels (agent roles).
        Args:
            text (str): The text to classify
            threshold (float, optional): The threshold for the classification.
        Returns:
            list: The list of agents and their scores
        """
        first_sentence = None
        for line in text.split("\n"):
                first_sentence = line.strip()
                break
        if first_sentence is None:
            first_sentence = text
        result = self.pipeline(first_sentence, self.labels, threshold=threshold)
        return result
    
    def select_agent(self, text: str) -> Agent:
        """
        Select the appropriate agent based on the text.
        Args:
            text (str): The text to select the agent from
        Returns:
            Agent: The selected agent
        """
        if len(self.agents) == 0 or len(self.labels) == 0:
            return self.agents[0]
        result = self.classify_text(text)
        for agent in self.agents:
            if result["labels"][0] == agent.role:
                pretty_print(f"Selected agent: {agent.agent_name}", color="warning")
                return agent
        return None

if __name__ == "__main__":
    agents = [
        CoderAgent("deepseek-r1:14b", "agent1", "../prompts/coder_agent.txt", "server"),
        CasualAgent("deepseek-r1:14b", "agent2", "../prompts/casual_agent.txt", "server"),
        PlannerAgent("deepseek-r1:14b", "agent3", "../prompts/planner_agent.txt", "server")
    ]
    router = AgentRouter(agents)
    
    texts = ["""
    Write a python script to check if the device on my network is connected to the internet
    """,
    """
    Hey could you search the web for the latest news on the stock market ?
    """,
    """
    hey can you give give a list of the files in the current directory ?
    """,
    """
    Make a cool game to illustrate the current relation between USA and europe
    """
    ]

    for text in texts:
        print(text)
        results = router.classify_text(text)
        for result in results:
            print(result["label"], "=>", result["score"])
        agent = router.select_agent(text)
        print("Selected agent role:", agent.role)
