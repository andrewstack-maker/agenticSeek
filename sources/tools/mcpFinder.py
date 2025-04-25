import os
import requests
from urllib.parse import urljoin
from typing import Dict, Any, Optional

if __name__ == "__main__":
    from tools import Tools
else:
    from sources.tools.tools import Tools

class MCP_finder(Tools):
    """
    Tool
    """
    def __init__(self, api_key: str = None):
        super().__init__()
        self.tag = "mcp"
        self.base_url = "https://registry.smithery.ai"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                     data: Optional[Dict] = None) -> Dict[str, Any]:
        url = urljoin(self.base_url.rstrip(), endpoint)
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError(f"API request failed: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Network error: {str(e)}")

    def list_mcp_servers(self, page: int = 1, page_size: int = 5000) -> Dict[str, Any]:
        params = {"page": page, "pageSize": page_size}
        return self._make_request("GET", "/servers", params=params)

    def get_mcp_server_details(self, qualified_name: str) -> Dict[str, Any]:
        endpoint = f"/servers/{qualified_name}"
        return self._make_request("GET", endpoint)
    
    def find_mcp_servers(self, query: str) -> Dict[str, Any]:
        """
        Finds a specific MCP server by its name.
        Args:
            query (str): a name or string that more or less matches the MCP server name.
        Returns:
            Dict[str, Any]: The details of the found MCP server or an error message.
        """
        mcps = self.list_mcp_servers()
        matching_mcp = []
        for mcp in mcps.get("servers", []):
            name = mcp.get("qualifiedName", "")
            if query.lower() in name.lower():
                details = {
                    "name": name,
                    "description": mcp.get("description", "No description available"),
                    "params": mcp.get("connections", [])
                }
                matching_mcp.append(details)
        return matching_mcp
    
    def execute(self, blocks: list, safety:bool = False) -> str:
        if not blocks or not isinstance(blocks, list):
            return "Error: No blocks provided\n"

        output = ""
        for block in blocks:
            block_clean = block.strip().lower().replace('\n', '')
            try:
                matching_mcp_infos = self.find_mcp_servers(block_clean)
            except requests.exceptions.RequestException as e:
                output += "Connection failed. Is the API in environement?\n"
                continue
            except Exception as e:
                output += f"Error: {str(e)}\n"
                continue
            if matching_mcp_infos == []:
                output += f"Error: No MCP server found for query '{block}'\n"
                continue
            for mcp_infos in matching_mcp_infos:
                output += f"Name: {mcp_infos['name']}\n"
                output += f"Description: {mcp_infos['description']}\n"
                output += f"Params: {', '.join(mcp_infos['params'])}\n"
                output += "-------\n"
        return output.strip()

    def execution_failure_check(self, output: str) -> bool:
        output = output.strip().lower()
        if not output:
            return True
        if "error" in output or "not found" in output:
            return True
        return False

    def interpreter_feedback(self, output: str) -> str:
        """
        Not really needed for this tool (use return of execute() directly)
        """
        if not output:
            return "No output generated."
        return output.strip()

if __name__ == "__main__":
    api_key = os.getenv("MCP_FINDER")
    tool = MCP_finder(api_key)
    result = tool.execute(["""
news
"""], False)
    print(result)