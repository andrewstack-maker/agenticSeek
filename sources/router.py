import os
import sys
import torch
from transformers import pipeline

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sources.agents.agent import Agent
from sources.agents.code_agent import CoderAgent
from sources.agents.casual_agent import CasualAgent
from sources.agents.planner_agent import PlannerAgent
from sources.agents.browser_agent import BrowserAgent
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

    def classify_text(self, text: str, threshold: float = 0.4) -> list:
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
                pretty_print(f"Selected agent: {agent.agent_name} (roles: {agent.role})", color="warning")
                return agent
        return None

if __name__ == "__main__":
    agents = [
        CasualAgent("deepseek-r1:14b", "jarvis", "../prompts/casual_agent.txt", None),
        BrowserAgent("deepseek-r1:14b", "browser", "../prompts/planner_agent.txt", None),
        CoderAgent("deepseek-r1:14b", "coder", "../prompts/coder_agent.txt", None)
    ]
    router = AgentRouter(agents)
    texts = [
        "Write a python script to check if the device on my network is connected to the internet",
        #"Peut tu écrire un script python qui vérifie si l'appareil sur mon réseau est connecté à internet?",
        #"写一个Python脚本，检查我网络上的设备是否连接到互联网",
        "Hey could you search the web for the latest news on the tesla stock market ?",
        #"嘿，你能搜索网页上关于股票市场的最新新闻吗？",
        #"Yo, cherche sur internet comment va tesla en bourse.",
        "I would like you to search for weather api and then make an app using this API",
        #"我想让你搜索天气API，然后用这个API做一个应用程序",
        #"J'aimerais que tu cherche une api météo et que l'utilise pour faire une application",
        "Plan a 3-day trip to New York, including flights and hotels.",
        #"计划一次为期3天的纽约之旅，包括机票和酒店。",
        #"Planifie un trip de 3 jours à Paris, y compris les vols et hotels.",
        "Find me the latest research papers on AI.",
        #"给我找最新的AI研究论文。",
        #"Trouve moi les derniers papiers de recherche en IA",
        "Help me write a C++ program to sort an array",
        #"帮我写一个C++程序来排序数组",
        #"Aide moi à faire un programme c++ pour trier une array.",
        "What’s the weather like today? Oh, and can you find a good weather app?",
        #"今天天气怎么样？哦，你还能找到一个好的天气应用程序吗？",
        #"La météo est comment aujourd'hui ? oh et trouve moi une bonne appli météo tant que tu y est.",
        "Can you debug this Java code? It’s not working.",
        #"你能调试这段Java代码吗？它不起作用。",
        #"Peut tu m'aider à debugger ce code java, ça marche pas",
        "What's the latest brainrot on the internet ?",
        #"互联网上最新的“脑残”是什么？",
        #"Quel est la dernière connerie sur internet ?",
        "i would like to setup a new AI project, index as mark2",
        #"我想建立一个新的 AI 项目，索引为 Mark2",
        #"Je voudrais configurer un nouveau projet d'IA, index Mark2",
        "Hey, can you find the old_project.zip file somewhere on my drive?",
        #"嘿，你能在我驱动器上找到old_project.zip文件吗？",
        #"Hé trouve moi le old_project.zip, il est quelque part sur mon disque.",
        "Tell me a funny story",
        #"给我讲一个有趣的故事",
        #"Raconte moi une histoire drole"
    ]
    for text in texts:
        print("Input text:", text)
        agent = router.select_agent(text)
        print()
