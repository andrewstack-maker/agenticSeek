import os
import asyncio

from sources.utility import pretty_print, animate_thinking
from sources.agents.agent import Agent
from sources.tools.mcpFinder import MCP_finder

# NOTE MCP agent is an active work in progress, not functional yet.

class McpAgent(Agent):

    def __init__(self, name, prompt_path, provider, verbose=False):
        """
        The mcp agent is a special agent for using MCPs.
        MCP agent will be disabled if the user does not explicitly set the MCP_FINDER_API_KEY in environment variable.
        """
        super().__init__(name, prompt_path, provider, verbose, None)
        keys = self.get_api_keys()
        self.tools = {
            "mcp_finder": MCP_finder(keys["mcp_finder"]),
            # add mcp tools here
        }
        self.role = "mcp"
        self.type = "mcp_agent"
        self.enabled = True
    
    def get_api_keys(self) -> dict:
        """
        Returns the API keys for the tools.
        """
        api_key_mcp_finder = os.getenv("MCP_FINDER_API_KEY")
        if not api_key_mcp_finder or api_key_mcp_finder == "":
            pretty_print("MCP Finder API key not found. Please set the MCP_FINDER_API_KEY environment variable.", color="failure")
            pretty_print("MCP Finder disabled.", color="failure")
            self.enabled = False
        return {
            "mcp_finder": api_key_mcp_finder
        }
    
    def expand_prompt(self, prompt):
        """
        Expands the prompt with the tools available.
        """
        tools_name = self.get_tools_name()
        tools_str = ", ".join(tools_name)
        prompt += f"""
        You can use the following tools and MCPs:
        {tools_str}
        """
        return prompt
    
    async def process(self, prompt, speech_module) -> str:
        if self.enabled == False:
            return "MCP Agent is disabled."
        prompt = self.expand_prompt(prompt)
        self.memory.push('user', prompt)
        working = True
        while working == True:
            animate_thinking("Thinking...", color="status")
            answer, reasoning = await self.llm_request()
            exec_success, _ = self.execute_modules(answer)
            answer = self.remove_blocks(answer)
            self.last_answer = answer
            self.status_message = "Ready"
            if len(self.blocks_result) == 0:
                working = False
        return answer, reasoning

if __name__ == "__main__":
    pass