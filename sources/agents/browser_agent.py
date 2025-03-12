import re
import time

from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.tools.webSearch import webSearch
from sources.browser import Browser
class BrowserAgent(Agent):
    def __init__(self, model, name, prompt_path, provider):
        """
        The casual agent is a special for casual talk to the user without specific tasks.
        """
        super().__init__(model, name, prompt_path, provider)
        self.tools = {
            "web_search": webSearch(),
        }
        self.role = "deep research and web search"
        self.browser = Browser()
        self.browser.goTo("https://github.com/")
    
    def make_init_prompt(self, user_prompt: str, search_result: str):
        return f"""
        Based on the search result:
        {search_result}
        Start browsing and find the information the user want.
        User: {user_prompt}
        You must choose a link to navigate to. Say i want to navigate to a <link>.
        """
    
    def extract_links(self, search_result: str):
        return re.findall(r'https?://[^\s]+', search_result)
    
    def make_navigation_prompt(self, user_prompt: str, page_text: str, navigable_links: list):
        format_links = "\n".join([f"[{i}] {link['text']} - {link['url']}" for i, link in enumerate(navigable_links)])
        return f"""
        \nYou are browsing the web. Not the user, you are the browser.

        Page content:
        {page_text}

        Navigable links:
        {format_links}


        You must choose a link to navigate to or do a new search.
        Remember, you seek the information the user want.
        The user query was : {user_prompt}
        If you want to do a new search, use the "web_search" tool.
        Exemple:
        ```web_search
        weather in tokyo
        ```
        If you have an answer and want to exit the browser, please say "REQUEST_EXIT".
        """
    
    def clean_links(self, links: list):
        links_clean = []
        for link in links:
            if link[-1] == '.':
                links_clean.append(link[:-1])
            else:
                links_clean.append(link)
        return links_clean
    
    def process(self, prompt, speech_module) -> str:
        complete = False

        animate_thinking(f"Searching...", color="status")
        search_result = self.tools["web_search"].execute([prompt], False)
        user_prompt = self.make_init_prompt(prompt, search_result)
        prompt = user_prompt
        while not complete:
            animate_thinking("Thinking...", color="status")
            self.memory.push('user', user_prompt)
            answer, reasoning = self.llm_request(prompt)
            pretty_print("-"*100)
            pretty_print(answer, color="output")
            pretty_print("-"*100)
            if "REQUEST_EXIT" in answer:
                complete = True
                break
            links = self.extract_links(answer)
            links_clean = self.clean_links(links)
            if len(links_clean) == 0:
                prompt = f"Please choose a link to navigate to or do a new search. Links found:\n{links_clean}"
                pretty_print("No links found, doing a new search.", color="warning")
                continue
            animate_thinking(f"Navigating to {links[0]}", color="status")
            speech_module.speak(f"Navigating to {links[0]}")
            self.browser.goTo(links[0])
            page_text = self.browser.getText()[:2048]
            navigable_links = self.browser.getNavigable()[:15]
            prompt = self.make_navigation_prompt(user_prompt, page_text, navigable_links)

        self.browser.close()
        return answer, reasoning

if __name__ == "__main__":
    browser = Browser()