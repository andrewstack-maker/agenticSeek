import re
import time

from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.tools.webSearch import webSearch
from sources.browser import Browser
class BrowserAgent(Agent):
    def __init__(self, model, name, prompt_path, provider):
        """
        The Browser agent is an agent that navigate the web autonomously in search of answer
        """
        super().__init__(model, name, prompt_path, provider)
        self.tools = {
            "web_search": webSearch(),
        }
        self.role = "deep research and web search"
        self.browser = Browser()
        self.browser.go_to("https://github.com/")
        self.search_history = []
        self.navigable_links = []
        self.ai_notes = []
    

    def extract_links(self, search_result: str):
        pattern = r'(https?://\S+|www\.\S+)'
        matches = re.findall(pattern, search_result)
        trailing_punct = ".,!?;:"
        cleaned_links = [link.rstrip(trailing_punct) for link in matches]
        return self.clean_links(cleaned_links)
        
    def clean_links(self, links: list):
        links_clean = []
        for link in links:
            link = link.strip()
            if link[-1] == '.':
                links_clean.append(link[:-1])
            else:
                links_clean.append(link)
        return links_clean

    def get_unvisited_links(self):
        return "\n".join([f"[{i}] {link}" for i, link in enumerate(self.navigable_links) if link not in self.search_history])

    def make_newsearch_prompt(self, user_prompt: str, search_result: str):
        return f"""
        Based on the search result: {search_result}
        Your goal is to find accurate and complete information to satisfy the user’s request.
        User request: {user_prompt}
        To proceed, choose a relevant link from the search results. Announce your choice by saying: "I want to navigate to <link>."
        For example: "I want to navigate to geohot.github.io."
        Do not explain your choice.
        """
    
    def make_navigation_prompt(self, user_prompt: str, page_text: str):
        remaining_links = self.get_unvisited_links() 
        remaining_links_text = remaining_links if remaining_links is not None else "No links remaining, proceed with a new search." 
        return f"""
        \nYou are currently browsing the web. Not the user, you are the browser.

        Page content:
        {page_text}

        You can navigate to these links:
        {remaining_links}

        If no link seem appropriate, please say "GO_BACK".
        Remember, you seek the information the user want.
        The user query was : {user_prompt}
        If you found a clear answer, please say "REQUEST_EXIT".
        You must choose a link to navigate to, go back or exit.
        Do not explain your choice.
        """
    
    def llm_decide(self, prompt):
        animate_thinking("Thinking...", color="status")
        self.memory.push('user', prompt)
        answer, reasoning = self.llm_request(prompt)
        pretty_print("-"*100)
        pretty_print(answer, color="output")
        pretty_print("-"*100)
        return answer, reasoning
    
    def select_unvisited(self, search_result):
        results_arr = search_result.split('\n\n') 
        results_unvisited = []
        for res in results_arr:
            for his in self.search_history:
                if his not in res:
                    results_unvisited.append(res) 
        return results_unvisited
    
    def process(self, user_prompt, speech_module) -> str:
        complete = False

        animate_thinking(f"Searching...", color="status")
        search_result = self.tools["web_search"].execute([user_prompt], False)
        prompt = self.make_newsearch_prompt(user_prompt, search_result)
        while not complete:
            answer, reasoning = self.llm_decide(prompt)
            if "REQUEST_EXIT" in answer:
                complete = True
                break
            links = self.extract_links(answer)
            if len(links) == 0 or "GO_BACK" in answer:
                search_result_unvisited = self.select_unvisited(search_result)
                prompt = self.make_newsearch_prompt(user_prompt, search_result)
                pretty_print("No links found, doing a new search.", color="warning")
                continue
            animate_thinking(f"Navigating to {links[0]}", color="status")
            speech_module.speak(f"Navigating to {links[0]}")
            self.browser.go_to(links[0])
            page_text = self.browser.get_text()
            self.search_history.append(links[0])
            self.navigable_links = self.browser.get_navigable()
            prompt = self.make_navigation_prompt(user_prompt, page_text)

        speech_module.speak(answer)
        self.browser.close()
        return answer, reasoning

if __name__ == "__main__":
    browser = Browser()