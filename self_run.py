
#!/usr/bin python3

"""
self_run.py is a script for automatically creating prompts, and saving history as training data.
"""

import sys
import argparse
import configparser
import asyncio

from sources.llm_provider import Provider
from sources.interaction import Interaction
from sources.agents import Agent, CoderAgent, CasualAgent, FileAgent, PlannerAgent, BrowserAgent, McpAgent
from sources.browser import Browser, create_driver

import warnings
warnings.filterwarnings("ignore")

config = configparser.ConfigParser()
config.read('config.ini')

def copy_conversations_folder():
    source_path = "conversations/"
    destination_path = "training_data/"
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    for filename in os.listdir(source_path):
        source_file = os.path.join(source_path, filename)
        destination_file = os.path.join(destination_path, filename)
        shutil.copy2(source_file, destination_file)
        print(f"Copied {source_file} to {destination_file}")

def get_random_query(provider):
    prompt = """
You are an expert in crafting queries for AgenticSeek, a AI assistant that autonomously browses the web, writes code, plans tasks, and manages files. It supports tasks like web searches, coding in Python/C/Go/Java, file operations, task planning.
Queries must be explicit, specifying actions like "search the web," "write code," or "save to a file," as AgenticSeek's agent routing may not infer vague intents.

Generate a single realistic user query for AgenticSeek. The query should:

Be concise and explicit about the desired action (e.g., web search, coding, file management).
Align with AgenticSeek’s capabilities (web browsing, coding, task planning, file operations).
Include a specific output where relevant (e.g., save to a file with a clear name and path).
Reflect a practical use case (e.g., research, programming, personal tasks).
Be formatted as a single sentence.
Example Query:
Search the web for the best hiking trails in Colorado and save a list of three trails with their locations in hiking_trails.txt in /home/project
    """
    history = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
    thought = provider.respond(history)
    return thought

async def self_runner():
    provider = Provider(provider_name=config["MAIN"]["provider_name"],
                        model=config["MAIN"]["provider_model"],
                        server_address=config["MAIN"]["provider_server_address"],
                        is_local=config.getboolean('MAIN', 'is_local'))

    browser = Browser(
        create_driver(headless=True, stealth_mode=False),
        anticaptcha_manual_install=False
    )

    agents = [
        CasualAgent(name=config["MAIN"]["agent_name"],
                    prompt_path=f"prompts/base/casual_agent.txt",
                    provider=provider, verbose=False),
        CoderAgent(name="coder",
                   prompt_path=f"prompts/base/coder_agent.txt",
                   provider=provider, verbose=False),
        FileAgent(name="File Agent",
                  prompt_path=f"prompts/base/file_agent.txt",
                  provider=provider, verbose=False),
        BrowserAgent(name="Browser",
                     prompt_path=f"prompts/base/browser_agent.txt",
                     provider=provider, verbose=False, browser=browser),
        PlannerAgent(name="Planner",
                     prompt_path=f"prompts/base/planner_agent.txt",
                     provider=provider, verbose=False, browser=browser)
    ]

    interaction = Interaction(agents,
                              tts_enabled=False,
                              stt_enabled=False,
                              recover_last_session=False,
                              langs=['en']
                            )
    print("Start self-running for training data generation...")
    try:
        while interaction.is_active:
            query = get_random_query(provider)
            print(f"Generated query: {query}")
            interaction.set_query(query)
            if await interaction.think():
                interaction.show_answer()
    except Exception as e:
        if config.getboolean('MAIN', 'save_session'):
            interaction.save_session()
            copy_conversations_folder()
        raise e
    finally:
        if config.getboolean('MAIN', 'save_session'):
            interaction.save_session()
            copy_conversations_folder()

if __name__ == "__main__":
    asyncio.run(self_runner())