
import os
import requests
import dotenv

dotenv.load_dotenv()

if __name__ == "__main__":
    from tools import Tools
else:
    from sources.tools.tools import Tools

class webSearch(Tools):
    def __init__(self, api_key: str = None):
        """
        A tool to perform a Google search and return information from the first result.
        """
        super().__init__()
        self.tag = "web_search"
        self.api_key = api_key or os.getenv("SERPAPI_KEY")  # Requires a SerpApi key

    def execute(self, blocks: str, safety: bool = True) -> str:
        if self.api_key is None:
            return "Error: No SerpApi key provided."
        for block in blocks:
            query = block.strip()
            if not query:
                return "Error: No search query provided."

            try:
                url = "https://serpapi.com/search"
                params = {
                    "q": query,
                    "api_key": self.api_key,
                    "num": 1,
                    "output": "json"
                }
                response = requests.get(url, params=params)
                response.raise_for_status()

                data = response.json()
                if "organic_results" in data and len(data["organic_results"]) > 0:
                    first_result = data["organic_results"][0]
                    title = first_result.get("title", "No title")
                    snippet = first_result.get("snippet", "No snippet available")
                    link = first_result.get("link", "No link available")
                    return f"Title: {title}\nSnippet: {snippet}\nLink: {link}"
                else:
                    return "No results found for the query."
            except requests.RequestException as e:
                return f"Error during web search: {str(e)}"
            except Exception as e:
                return f"Unexpected error: {str(e)}"
        return "No search performed"

    def execution_failure_check(self, output: str) -> bool:
        return output.startswith("Error") or "No results found" in output

    def interpreter_feedback(self, output: str) -> str:
        if self.execution_failure_check(output):
            return f"Web search failed: {output}"
        return f"Web search result:\n{output}"


if __name__ == "__main__":
    search_tool = webSearch(api_key=os.getenv("SERPAPI_KEY"))
    query = "when did covid start"
    result = search_tool.execute(query, safety=True)
    feedback = search_tool.interpreter_feedback(result)
    print(feedback)