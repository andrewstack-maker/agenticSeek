#!/usr/bin python3

import sys
import signal
import argparse
import configparser

from sources.llm_provider import Provider
from sources.interaction import Interaction
from sources.agents import Agent, CoderAgent, CasualAgent, FileAgent, PlannerAgent, BrowserAgent
from sources.browser import Browser, create_driver

import warnings
warnings.filterwarnings("ignore")

config = configparser.ConfigParser()
config.read('config.ini')

def handleInterrupt(signum, frame):
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, handler=handleInterrupt)

    if config.getboolean('MAIN', 'is_local'):
        provider = Provider(config["MAIN"]["provider_name"], config["MAIN"]["provider_model"], config["MAIN"]["provider_server_address"])
    else:
        provider = Provider(provider_name=config["MAIN"]["provider_name"],
                                   model=config["MAIN"]["provider_model"],
                                   server_address=config["MAIN"]["provider_server_address"])

    browser = Browser(create_driver(), headless=False)

    agents = [
        CasualAgent(name=config["MAIN"]["agent_name"],
                    prompt_path="prompts/casual_agent.txt",
                    provider=provider, verbose=False),
        CoderAgent(name="coder",
                   prompt_path="prompts/coder_agent.txt",
                   provider=provider, verbose=False),
        FileAgent(name="File Agent",
                  prompt_path="prompts/file_agent.txt",
                  provider=provider, verbose=False),
        BrowserAgent(name="Browser",
                     prompt_path="prompts/browser_agent.txt",
                     provider=provider, verbose=False, browser=browser),
        # Planner agent is experimental, might work poorly, especially with model < 32b
        PlannerAgent(name="Planner",
                     prompt_path="prompts/planner_agent.txt",
                     provider=provider, verbose=False, browser=browser)
    ]

    interaction = Interaction(agents,
                              tts_enabled=config.getboolean('MAIN', 'speak'),
                              stt_enabled=config.getboolean('MAIN', 'listen'),
                              recover_last_session=config.getboolean('MAIN', 'recover_last_session'))
    try:
        while interaction.is_active:
            interaction.get_user()
            interaction.think()
            interaction.show_answer()
    except Exception as e:
        if config.getboolean('MAIN', 'save_session'):
            interaction.save_session()
        raise e
    finally:
        if config.getboolean('MAIN', 'save_session'):
            interaction.save_session()


if __name__ == "__main__":
    main()
