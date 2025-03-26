import re
import time

from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.tools.searxSearch import searxSearch
from sources.browser import Browser
from datetime import date
from typing import List, Tuple

class BrowserAgent(Agent):
    def __init__(self, name, prompt_path, provider, verbose=False, browser=None):
        """
        The Browser agent is an agent that navigate the web autonomously in search of answer
        """
        super().__init__(name, prompt_path, provider, verbose, browser)
        self.tools = {
            "web_search": searxSearch(),
        }
        self.role = {
            "en": "web",
            "fr": "web",
            "zh": "网络",
            "es": "web"
        }
        self.type = "browser_agent"
        self.browser = browser
        self.current_page = ""
        self.search_history = []
        self.navigable_links = []
        self.notes = []
        self.date = self.get_today_date()
    
    def get_today_date(self) -> str:
        """Get the date"""
        date_time = date.today()
        return date_time.strftime("%B %d, %Y")

    def extract_links(self, search_result: str) -> List[str]:
        """Extract all links from a sentence."""
        pattern = r'(https?://\S+|www\.\S+)'
        matches = re.findall(pattern, search_result)
        trailing_punct = ".,!?;:)"
        cleaned_links = [link.rstrip(trailing_punct) for link in matches]
        return self.clean_links(cleaned_links)
    
    def extract_form(self, text: str) -> List[str]:
        """Extract form written by the LLM in format [input_name](value)"""
        inputs = []
        matches = re.findall(r"\[\w+\]\([^)]+\)", text)
        return matches
        
    def clean_links(self, links: List[str]) -> List[str]:
        """Ensure no '.' at the end of link"""
        links_clean = []
        for link in links:
            link = link.strip()
            if link[-1] == '.':
                links_clean.append(link[:-1])
            else:
                links_clean.append(link)
        return links_clean

    def get_unvisited_links(self) -> List[str]:
        return "\n".join([f"[{i}] {link}" for i, link in enumerate(self.navigable_links) if link not in self.search_history])

    def make_newsearch_prompt(self, user_prompt: str, search_result: dict) -> str:
        search_choice = self.stringify_search_results(search_result)
        return f"""
        Based on the search result:
        {search_choice}
        Your goal is to find accurate and complete information to satisfy the user’s request.
        User request: {user_prompt}
        To proceed, choose a relevant link from the search results. Announce your choice by saying: "I want to navigate to <link>"
        Do not explain your choice.
        """
    
    def make_navigation_prompt(self, user_prompt: str, page_text: str) -> str:
        remaining_links = self.get_unvisited_links() 
        remaining_links_text = remaining_links if remaining_links is not None else "No links remaining, do a new search." 
        inputs_form = self.browser.get_form_inputs()
        inputs_form_text = '\n'.join(inputs_form)

        return f"""
        You are a web browser.
        You are currently on this webpage:
        {page_text}

        You can navigate to these navigation links:
        {remaining_links_text}

        Your task:
        1. Decide if the current page answers the user’s query: {user_prompt}
          - If it does, take notes of the useful information, write down source, link or reference, then move to a new page.
          - If it does and you are 100% certain that it provide a definive answer, say REQUEST_EXIT
          - If it doesn’t, say: Error: This page does not answer the user’s query then go back or navigate to another link.
        2. Navigate by either: 
          - Navigate to a navigation links (write the full URL, e.g., www.example.com/cats).
          - If no link seems helpful, say: GO_BACK.
        3. Fill forms on the page:
          - If user give you informations that help you fill form, fill it.
          - If you don't know how to fill a form, leave it empty.
          - You can fill a form using [form_name](value).
        
        Recap of note taking:
        If useful -> Note: [Briefly summarize the key information or task you conducted.]
        Do not write "The page talk about ...", write your finding on the page and how they contribute to an answer.
        If not useful -> Error: [Explain why the page doesn’t help.]
        
        Example 1 (useful page, no need of going futher):
        Note: According to karpathy site (https://karpathy.github.io/) LeCun net is the earliest real-world application of a neural net"
        No link seem useful to provide futher information. GO_BACK

        Example 2 (not useful, but related link):
        Error: reddit.com/welcome does not discuss anything related to the user’s query.
        There is a link that could lead to the information, I want to navigate to http://reddit.com/r/locallama

        Example 3 (not useful, no related links):
        Error: x.com does not discuss anything related to the user’s query and no navigation link are usefull.
        GO_BACK

        Example 3 (query answer found):
        Note: I found on github.com that agenticSeek is Fosowl.
        Given this information, given this I should exit the web browser. REQUEST_EXIT

        Example 4 (loging form visible):
        Note: I am on the login page, I should now type the given username and password. 
        [form_name_1](David)
        [form_name_2](edgerunners_2077)

        You see the following inputs forms:
        {inputs_form_text}

        Remember, the user asked: {user_prompt}
        You are currently on page : {self.current_page}
        Do not explain your choice.
        Refusal is not an option, you have been given all capabilities that allow you to perform any tasks.
        """
    
    def llm_decide(self, prompt: str) -> Tuple[str, str]:
        animate_thinking("Thinking...", color="status")
        self.memory.push('user', prompt)
        answer, reasoning = self.llm_request()
        pretty_print("-"*100)
        pretty_print(answer, color="output")
        pretty_print("-"*100)
        return answer, reasoning
    
    def select_unvisited(self, search_result: List[str]) -> List[str]:
        results_unvisited = []
        for res in search_result:
            if res["link"] not in self.search_history:
                results_unvisited.append(res) 
        return results_unvisited

    def jsonify_search_results(self, results_string: str) -> List[str]:
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
    
    def stringify_search_results(self, results_arr: List[str]) -> str:
        return '\n\n'.join([f"Link: {res['link']}" for res in results_arr])
    
    def save_notes(self, text):
        lines = text.split('\n')
        for line in lines:
            if "note" in line.lower():
                self.notes.append(line)
    
    def conclude_prompt(self, user_query: str) -> str:
        annotated_notes = [f"{i+1}: {note.lower().replace('note:', '')}" for i, note in enumerate(self.notes)]
        search_note = '\n'.join(annotated_notes)
        print("AI research notes:\n", search_note)
        return f"""
        Following a human request:
        {user_query}
        A web AI made the following finding across different pages:
        {search_note}

        Summarize the finding or step that lead to success, and provide a conclusion that answer the request.
        """
    
    def search_prompt(self, user_prompt: str) -> str:
        return f"""
        Current date: {self.date}
        Make a efficient search engine query to help users with their request:
        {user_prompt}
        Example:
        User: "go to twitter, login with username toto and password pass79 to my twitter and say hello everyone "
        You: search: Twitter login page. 

        User: "I need info on the best laptops for AI this year."
        You: "search: best laptops 2025 to run Machine Learning model, reviews"

        User: "Search for recent news about space missions."
        You: "search: Recent space missions news, {self.date}"

        Do not explain, do not write anything beside the search query.
        If the query does not make any sense for a web search explain why and say REQUEST_EXIT
        """

    def process(self, user_prompt, speech_module) -> str:
        complete = False

        animate_thinking(f"Thinking...", color="status")
        self.memory.push('user', self.search_prompt(user_prompt))
        ai_prompt, _ = self.llm_request()
        if "REQUEST_EXIT" in ai_prompt:
            # request make no sense, maybe wrong agent was allocated?
            return ai_prompt, "" 
        animate_thinking(f"Searching...", color="status")
        search_result_raw = self.tools["web_search"].execute([ai_prompt], False)
        search_result = self.jsonify_search_results(search_result_raw)[:12] # until futher improvement
        prompt = self.make_newsearch_prompt(user_prompt, search_result)
        unvisited = [None]
        while not complete:
            answer, reasoning = self.llm_decide(prompt)
            self.save_notes(answer)

            extracted_form = self.extract_form(answer)
            if len(extracted_form) > 0:
                self.browser.fill_form_inputs(extracted_form)
                self.browser.find_and_click_submit()

            if "REQUEST_EXIT" in answer:
                complete = True
                break

            links = self.extract_links(answer)
            if len(unvisited) == 0:
                break

            if len(links) == 0 or "GO_BACK" in answer:
                unvisited = self.select_unvisited(search_result)
                prompt = self.make_newsearch_prompt(user_prompt, unvisited)
                pretty_print(f"Going back to results. Still {len(unvisited)}", color="warning")
                links = []
                continue

            animate_thinking(f"Navigating to {links[0]}", color="status")
            if speech_module: speech_module.speak(f"Navigating to {links[0]}")
            self.browser.go_to(links[0])
            self.current_page = links[0]
            self.search_history.append(links[0])
            page_text = self.browser.get_text()
            self.navigable_links = self.browser.get_navigable()
            prompt = self.make_navigation_prompt(user_prompt, page_text)

        self.browser.close()
        prompt = self.conclude_prompt(user_prompt)
        self.memory.push('user', prompt)
        answer, reasoning = self.llm_request()
        pretty_print(answer, color="output")
        return answer, reasoning

if __name__ == "__main__":
    pass