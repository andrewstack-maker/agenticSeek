import os
import sys
import torch
from transformers import pipeline
# adaptive-classifier==0.0.10
from adaptive_classifier import AdaptiveClassifier

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from sources.agents.agent import Agent
from sources.agents.code_agent import CoderAgent
from sources.agents.casual_agent import CasualAgent
from sources.agents.planner_agent import FileAgent
from sources.agents.browser_agent import BrowserAgent
from sources.language import LanguageUtility
from sources.utility import pretty_print

class AgentRouter:
    """
    AgentRouter is a class that selects the appropriate agent based on the user query.
    """
    # TODO add adaptive-classifier==0.0.10 to requirements.txt
    def __init__(self, agents: list):
        self.agents = agents
        self.lang_analysis = LanguageUtility()
        self.pipelines = {
            "bart": pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        }
        self.classifier = self.load_llm_router()
        self.learn_few_shots_en()

    def load_llm_router(self) -> AdaptiveClassifier:
        """
        Load the LLM router model.
        returns:
            AdaptiveClassifier: The loaded model
        exceptions:
            Exception: If the safetensors fails to load
        """
        path = "../llm_router" if __name__ == "__main__" else "./llm_router"
        try:
            classifier = AdaptiveClassifier.from_pretrained(path)
        except Exception as e:
            raise Exception("Failed to load the routing model. Please run the dl_safetensors.sh script inside llm_router/ directory to download the model.")
        return classifier

    def get_device(self) -> str:
        if torch.backends.mps.is_available():
            return "mps"
        elif torch.cuda.is_available():
            return "cuda:0"
        else:
            return "cpu"

    def learn_few_shots_en(self) -> None:
        """
        Few shot learning for the LLM router.
        Use the build in add_examples method of the AdaptiveClassifier.
        """
        few_shots = [
            ("Write a python script to check if the device on my network is connected to the internet", "coding"),
            ("Hey could you search the web for the latest news on the tesla stock market ?", "web"),
            ("I would like you to search for weather api", "web"),
            ("Plan a 3-day trip to New York, including flights and hotels.", "web"),
            ("Find on the web the latest research papers on AI.", "web"),
            ("Can you debug this Java code? It’s not working.", "code"),
            ("Can you browse the web and find me a 4090 for cheap?", "web"),
            ("i would like to setup a new AI project, index as mark2", "files"),
            ("Hey, can you find the old_project.zip file somewhere on my drive?", "files"),
            ("Tell me a funny story", "talk"),
            ("Can you locate the backup folder I created last month on my system?", "files"),
            ("Share a random fun fact about space.", "talk"),
            ("Write a script to rename all files in a directory to lowercase.", "files"),
            ("Could you check if the presentation.pdf file exists in my downloads?", "files"),
            ("Tell me about the weirdest dream you’ve ever heard of.", "talk"),
            ("Search my drive for a file called vacation_photos_2023.jpg.", "files"),
            ("Help me organize my desktop files into folders by type.", "files"),
            ("What’s your favorite movie and why?", "talk"),
            ("Search my drive for a file named budget_2024.xlsx", "files"),
            ("Write a Python function to sort a list of dictionaries by key", "code"),
            ("Find the latest updates on quantum computing on the web", "web"),
            ("Check if the folder ‘Work_Projects’ exists on my desktop", "files"),
            ("Create a bash script to monitor CPU usage", "code"),
            ("Search online for the best budget smartphones of 2025", "web"),
            ("What’s the strangest food combination you’ve heard of?", "talk"),
            ("Move all .txt files from Downloads to a new folder called Notes", "files"),
            ("Debug this C++ code that keeps crashing", "code"),
            ("can you browse the web to find out who fosowl is ?", "web"),
            ("Find the file ‘important_notes.txt’", "files"),
            ("Find out the latest news on the upcoming Mars mission", "web"),
            ("Write a Java program to calculate the area of a circle", "code"),
            ("Search the web for the best ways to learn a new language", "web"),
            ("Locate the file ‘presentation.pptx’ in my Documents folder", "files"),
            ("Write a Python script to download all images from a webpage", "code"),
            ("Search the web for the latest trends in AI and machine learning", "web"),
            ("Tell me about a time when you had to solve a difficult problem", "talk"),
            ("Organize all image files on my desktop into a folder called ‘Pictures’", "files"),
            ("Generate a Ruby script to calculate Fibonacci numbers up to 100", "code"),
            ("Find out what device are connected to my network", "code"),
            ("Show me how much disk space is left on my drive", "code"),
            ("Look up recent posts on X about climate change", "web"),
            ("Find the photo I took last week named sunset_beach.jpg", "files"),
            ("Write a JavaScript snippet to fetch data from an API", "code"),
            ("Search the web for tutorials on machine learning with Python", "web"),
            ("Locate the file ‘meeting_notes.docx’ in my Documents folder", "files"),
            ("Write a Python script to scrape a website’s title and links", "code"),
            ("Search the web for the latest breakthroughs in fusion energy", "web"),
            ("Tell me about a historical event that sounds too wild to be true", "talk"),
            ("Organize all image files on my desktop into a folder called ‘Pictures’", "files"),
            ("Generate a Ruby script to calculate Fibonacci numbers up to 100", "code"),
            ("Find recent X posts about SpaceX’s next rocket launch", "web"),
            ("What’s the funniest misunderstanding you’ve seen between humans and AI?", "talk"),
            ("Check if ‘backup_032025.zip’ exists anywhere on my drive", "files" ),
            ("Create a shell script to automate backups of a directory", "code"),
            ("Look up the top AI conferences happening in 2025 online", "web"),
            ("Write a C# program to simulate a basic calculator", "code"),
            ("Browse the web for open-source alternatives to Photoshop", "web"),
            ("Hey how are you", "talk"),
            ("Write a Python script to ping a website", "code"),
            ("Search the web for the latest iPhone release", "web"),
            ("What’s the weather like today?", "web"),
            ("Hi, how’s your day going?", "talk"),
            ("Can you find a file called resume.docx on my drive?", "files"),
            ("Write a simple Java program to print 'Hello World'", "code"),
            ("Tell me a quick joke", "talk"),
            ("Search online for the best coffee shops in Seattle", "web"),
            ("Check if ‘project_plan.pdf’ exists in my Downloads folder", "files"),
            ("What’s your favorite color?", "talk"),
            ("Write a bash script to list all files in a directory", "code"),
            ("Find recent X posts about electric cars", "web"),
            ("Hey, you doing okay?", "talk"),
            ("Locate the file ‘family_photo.jpg’ on my system", "files"),
            ("Search the web for beginner guitar lessons", "web"),
            ("Write a Python function to reverse a string", "code"),
            ("What’s the weirdest animal you know of?", "talk"),
            ("Organize all .pdf files on my desktop into a ‘Documents’ folder", "files"),
            ("Browse the web for the latest space mission updates", "web"),
            ("Hey, what’s up with you today?", "talk"),
            ("Write a JavaScript function to add two numbers", "code"),
            ("Find the file ‘notes.txt’ in my Documents folder", "files"),
            ("Tell me something random about the ocean", "talk"),
            ("Search the web for cheap flights to Paris", "web"),
            ("Check if ‘budget.xlsx’ is on my drive", "files"),
            ("Write a Python script to count words in a text file", "code"),
            ("How’s it going today?", "talk"),
            ("Find recent X posts about AI advancements", "web"),
            ("Move all .jpg files from Downloads to a ‘Photos’ folder", "files"),
            ("Search online for the best laptops of 2025", "web"),
            ("What’s the funniest thing you’ve heard lately?", "talk"),
            ("Write a Ruby script to generate random numbers", "code"),
            ("Hey, how’s everything with you?", "talk"),
            ("Locate ‘meeting_agenda.docx’ in my system", "files"),
            ("Search the web for tips on growing indoor plants", "web"),
            ("Write a C++ program to calculate the sum of an array", "code"),
            ("Tell me a fun fact about dogs", "talk"),
            ("Check if the folder ‘Old_Projects’ exists on my desktop", "files"),
            ("Browse the web for the latest gaming console reviews", "web"),
            ("Hi, how are you feeling today?", "talk"),
            ("Write a Python script to check disk space", "code"),
            ("Find the file ‘vacation_itinerary.pdf’ on my drive", "files"),
            ("Search the web for news on renewable energy", "web"),
            ("What’s the strangest thing you’ve learned recently?", "talk"),
            ("Organize all video files into a ‘Videos’ folder", "files"),
            ("Write a shell script to delete temporary files", "code"),
            ("Hey, how’s your week been so far?", "talk"),
            ("Search online for the top movies of 2025", "web"),
            ("Locate ‘taxes_2024.xlsx’ in my Documents folder", "files"),
            ("Tell me about a cool invention from history", "talk"),
            ("Write a Java program to check if a number is even or odd", "code"),
            ("Find recent X posts about cryptocurrency trends", "web"),
            ("Hey, you good today?", "talk"),
            ("Search the web for easy dinner recipes", "web"),
            ("Check if ‘photo_backup.zip’ exists on my drive", "files"),
            ("Write a Python script to rename files with a timestamp", "code"),
            ("What’s your favorite thing about space?", "talk"),
            ("Browse the web for the latest fitness trends", "web"),
            ("Move all .docx files to a ‘Work’ folder", "files"),
        ]
        texts = [text for text, _ in few_shots]
        labels = [label for _, label in few_shots]
        self.classifier.clear_memory()
        self.classifier.add_examples(texts, labels)

    def llm_router(self, text: str) -> tuple:
        """
        Inference of the LLM router model.
        Args:
            text: The input text
        """
        predictions = self.classifier.predict(text)
        predictions = [pred for pred in predictions if pred[0] not in ["HIGH", "LOW"]]
        predictions = sorted(predictions, key=lambda x: x[1], reverse=True)
        return predictions[0]
    
    def router_vote(self, text: str, labels: list) -> str:
        """
        Vote between the LLM router and BART model.
        Args:
            text: The input text
            labels: The labels to classify
        Returns:
            str: The selected label
        """
        result_bart = self.pipelines['bart'](text, labels, threshold=0.3)
        result_llm_router = self.llm_router(text)
        bart, confidence_bart = result_bart['labels'][0], result_bart['scores'][0]
        llm_router, confidence_llm_router = result_llm_router[0], result_llm_router[1]
        confidence_bart *= 0.8 # was always a bit too confident 
        print("BART:", bart, "LLM Router:", llm_router)
        print("Confidence BART:", confidence_bart, "Confidence LLM Router:", confidence_llm_router)
        if confidence_bart > confidence_llm_router:
            return bart
        else:
            return llm_router
    
    def classify_text(self, text: str, threshold: float = 0.4) -> list:
        """
        Classify the text using the LLM router and BART model.
        """
        first_sentence = None
        lang = "en"
        for line in text.split("\n"):
            first_sentence = line.strip()
            break
        if first_sentence is None:
            first_sentence = text
        try:
            lang = self.lang_analysis.detect_language(first_sentence)
            labels = [agent.role[lang] for agent in self.agents]
            result = self.router_vote(first_sentence, labels)
        except Exception as e:
            raise e
        return result, lang
    
    def select_agent(self, text: str) -> Agent:
        """
        Select the appropriate agent based on the text.
        Args:
            text (str): The text to select the agent from
        Returns:
            Agent: The selected agent
        """
        if len(self.agents) == 0:
            return self.agents[0]
        result, lang = self.classify_text(text)
        for agent in self.agents:
            if result == agent.role[lang]:
                pretty_print(f"Selected agent: {agent.agent_name} (roles: {agent.role[lang]})", color="warning")
                return agent
        pretty_print(f"Error choosing agent. Routing system is not multilingual yet.", color="failure")
        pretty_print(f"选择代理时出错。路由系统尚不支持多语言", color="failure")
        pretty_print(f"エージェントの選択エラー。ルーティングシステムはまだ多言語に対応していません", color="failure")
        pretty_print(f"Erreur lors du choix de l'agent. Le système de routage n'est pas encore multilingue.", color="failure")
        pretty_print(f"Error al elegir agente. El sistema de enrutamiento aún no es multilingüe.", color="failure")

        return None

if __name__ == "__main__":
    agents = [
        CasualAgent("jarvis", "../prompts/casual_agent.txt", None),
        BrowserAgent("browser", "../prompts/planner_agent.txt", None),
        CoderAgent("coder", "../prompts/coder_agent.txt", None),
        FileAgent("file", "../prompts/coder_agent.txt", None)
    ]
    router = AgentRouter(agents)
    texts = [
        "hi",
        #"你好",
        #"Bonjour",
        "Write a python script to check if the device on my network is connected to the internet",
        # "Peut tu écrire un script python qui vérifie si l'appareil sur mon réseau est connecté à internet?",
        # "写一个Python脚本，检查我网络上的设备是否连接到互联网",
        "Hey could you search the web for the latest news on the tesla stock market ?",
        # "嘿，你能搜索网页上关于股票市场的最新新闻吗？",
        # "Yo, cherche sur internet comment va tesla en bourse.",
        "I would like you to search for weather api and then make an app using this API",
        # "我想让你搜索天气API，然后用这个API做一个应用程序",
        # "J'aimerais que tu cherche une api météo et que l'utilise pour faire une application",
        "Plan a 3-day trip to New York, including flights and hotels.",
        # "计划一次为期3天的纽约之旅，包括机票和酒店。",
        # "Planifie un trip de 3 jours à Paris, y compris les vols et hotels.",
        "Find on the web the latest research papers on AI.",
        # "在网上找到最新的人工智能研究论文。",
        # "Trouve moi les derniers articles de recherche sur l'IA sur internet",
        "Help me write a C++ program to sort an array",
        "Tell me what France been up to lately",
        # "告诉我法国最近在做什么",
        # "Dis moi ce que la France a fait récemment",
        "Who is Sergio Pesto ?",
        # "谁是Sergio Pesto？",
        # "Qui est Sergio Pesto ?",
        # "帮我写一个C++程序来排序数组",
        # "Aide moi à faire un programme c++ pour trier une array.",
        "What’s the weather like today? Oh, and can you find a good weather app?",
        # "今天天气怎么样？哦，你还能找到一个好的天气应用程序吗？",
        # "La météo est comment aujourd'hui ? oh et trouve moi une bonne appli météo tant que tu y est.",
        "Can you debug this Java code? It’s not working.",
        # "你能调试这段Java代码吗？它不起作用。",
        # "Peut tu m'aider à debugger ce code java, ça marche pas",
        #"Can you browse the web and find me a 4090 for cheap?",
        #"你能浏览网页，为我找一个便宜的4090吗？",
        #"Peut tu chercher sur internet et me trouver une 4090 pas cher ?",
        #"Hey, can you find the old_project.zip file somewhere on my drive?",
        #"嘿，你能在我驱动器上找到old_project.zip文件吗？",
        #"Hé trouve moi le old_project.zip, il est quelque part sur mon disque.",
        "Tell me a funny story",
        "给我讲一个有趣的故事",
        "Raconte moi une histoire drole"
    ]
    for text in texts:
        print("Input text:", text)
        agent = router.select_agent(text)
        print()
