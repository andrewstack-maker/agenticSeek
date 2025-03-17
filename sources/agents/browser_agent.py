import re
import time

from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.tools.searxSearch import searxSearch
from sources.browser import Browser

class BrowserAgent(Agent):
    def __init__(self, model, name, prompt_path, provider):
        """
        The Browser agent is an agent that navigate the web autonomously in search of answer
        """
        super().__init__(model, name, prompt_path, provider)
        self.tools = {
            "web_search": searxSearch(),
        }
        self.role = "deep research and web search"
        self.browser = Browser()
        self.browser.go_to("https://github.com/")
        self.search_history = []
        self.navigable_links = []
        self.notes = []
    

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

    def make_newsearch_prompt(self, user_prompt: str, search_result: dict):
        search_choice = self.stringify_search_results(search_result)
        return f"""
        Based on the search result:
        {search_choice}
        Your goal is to find accurate and complete information to satisfy the user’s request.
        User request: {user_prompt}
        To proceed, choose a relevant link from the search results. Announce your choice by saying: "I want to navigate to <link>."
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
        You must choose a link (write it down) to navigate to, or go back.
        For exemple you can say: i want to go to www.wikipedia.org/cats
        Always end with a sentence that summarize when useful information is found for exemple:
        Summary: According to https://karpathy.github.io/ LeCun net is the earliest real-world application of a neural net"
        Do not say "according to this page", always write down the whole link.
        If a website does not have usefull information say Error, for exemple:
        Error: This forum does not discus anything that can answer the user query
        Do not explain your choice, be short, concise.
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
        results_unvisited = []
        for res in search_result:
            if res["link"] not in self.search_history:
                results_unvisited.append(res) 
        return results_unvisited

    def jsonify_search_results(self, results_string):
        result_blocks = results_string.split("\n\n")
        parsed_results = []
        for block in result_blocks:
            if not block.strip():
                continue
            lines = block.split("\n")
            result_dict = {}
            for line in lines:
                if line.startswith("Title:"):
                    result_dict["title"] = line.replace("Title:", "").strip()
                elif line.startswith("Snippet:"):
                    result_dict["snippet"] = line.replace("Snippet:", "").strip()
                elif line.startswith("Link:"):
                    result_dict["link"] = line.replace("Link:", "").strip()
            if result_dict:
                parsed_results.append(result_dict)
        return parsed_results 
    
    def stringify_search_results(self, results_arr):
        return '\n\n'.join([f"Link: {res['link']}" for res in results_arr])
    
    def save_notes(self, text):
        lines = text.split('\n')
        for line in lines:
            if "summary:" in line.lower():
                self.notes.append(line)
    
    def conclude_prompt(self, user_query):
        search_note = '\n -'.join(self.notes)
        return f"""
        Following a web search about:
        {user_query}
        Write a conclusion based on these notes:
        {search_note}
        """

    def process(self, user_prompt, speech_module) -> str:
        complete = False

        animate_thinking(f"Searching...", color="status")
        search_result_raw = self.tools["web_search"].execute([user_prompt], False)
        search_result = self.jsonify_search_results(search_result_raw)
        search_result = search_result[:10] # until futher improvement
        prompt = self.make_newsearch_prompt(user_prompt, search_result)
        unvisited = [None]
        while not complete:
            answer, reasoning = self.llm_decide(prompt)
            self.save_notes(answer)
            if "REQUEST_EXIT" in answer:
                complete = True
                break
            links = self.extract_links(answer)
            if len(links) == 0 or "GO_BACK" in answer:
                unvisited = self.select_unvisited(search_result)
                prompt = self.make_newsearch_prompt(user_prompt, unvisited)
                pretty_print(f"Going back to results. Still {len(unvisited)}", color="warning")
                links = []
                continue
            if len(unvisited) == 0:
                break
            animate_thinking(f"Navigating to {links[0]}", color="status")
            speech_module.speak(f"Navigating to {links[0]}")
            self.browser.go_to(links[0])
            self.search_history.append(links[0])
            page_text = self.browser.get_text()
            self.navigable_links = self.browser.get_navigable()
            prompt = self.make_navigation_prompt(user_prompt, page_text)

        speech_module.speak(answer)
        self.browser.close()
        prompt = self.conclude_prompt(user_prompt)
        answer, reasoning = self.llm_request(prompt)
        pretty_print(answer, color="output")
        return answer, reasoning

if __name__ == "__main__":
    browser = Browser()