
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
    
    def process(self, prompt, speech_module) -> str:
        raise NotImplementedError("Browser agent is not implemented yet")

if __name__ == "__main__":
    browser = Browser()