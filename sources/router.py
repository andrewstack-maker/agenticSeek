import torch
from transformers import pipeline
from sources.agent import Agent
from sources.code_agent import CoderAgent
from sources.casual_agent import CasualAgent
from sources.utility import pretty_print

class AgentRouter:
    def __init__(self, agents: list, model_name="facebook/bart-large-mnli"):
        self.model = model_name 
        self.pipeline = pipeline("zero-shot-classification",
                      model=self.model)
        self.agents = agents
        self.labels = [agent.role for agent in agents]

    def get_device(self):
        if torch.backends.mps.is_available():
            return "mps"
        elif torch.cuda.is_available():
            return "cuda:0"
        else:
            return "cpu"

    def classify_text(self, text, threshold=0.5):
        result = self.pipeline(text, self.labels, threshold=threshold)
        return result
    
    def select_agent(self, text: str) -> Agent:
        result = self.classify_text(text)
        for agent in self.agents:
            if result["labels"][0] == agent.role:
                pretty_print(f"Selected agent: {agent.agent_name}", color="warning")
                return agent
        return None

if __name__ == "__main__":
    agents = [
        CoderAgent("deepseek-r1:14b", "agent1", "../prompts/coder_agent.txt", "server"),
        CasualAgent("deepseek-r1:14b", "agent2", "../prompts/casual_agent.txt", "server")
    ]
    router = AgentRouter(agents)
    
    texts = ["""
    Write a python script to check if the device on my network is connected to the internet
    """,
    """
    Hey could you search the web for the latest news on the stock market ?
    """,
    """
    hey can you give dating advice ?
    """
    ]

    for text in texts:
        print(text)
        results = router.classify_text(text)
        for result in results:
            print(result["label"], "=>", result["score"])
        agent = router.select_agent(text)
        print("Selected agent role:", agent.role)
