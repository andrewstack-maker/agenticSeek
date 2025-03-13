#!/usr/bin python3

import sys
import signal
import argparse
import configparser

from sources.llm_provider import Provider
from sources.interaction import Interaction
from sources.agents import Agent, CoderAgent, CasualAgent, FileAgent, PlannerAgent, BrowserAgent

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

    agents = [
        CasualAgent(model=config["MAIN"]["provider_model"],
                       name=config["MAIN"]["agent_name"],
                       prompt_path="prompts/casual_agent.txt",
                       provider=provider),
        CoderAgent(model=config["MAIN"]["provider_model"],
                       name="coder",
                       prompt_path="prompts/coder_agent.txt",
                       provider=provider),
        FileAgent(model=config["MAIN"]["provider_model"],
                       name="File Agent",
                       prompt_path="prompts/file_agent.txt",
                       provider=provider),
        PlannerAgent(model=config["MAIN"]["provider_model"],
                       name="Planner",
                       prompt_path="prompts/planner_agent.txt",
                       provider=provider),
        BrowserAgent(model=config["MAIN"]["provider_model"],
                       name="Browser",
                       prompt_path="prompts/browser_agent.txt",
                       provider=provider)
    ]

    interaction = Interaction(agents, tts_enabled=config.getboolean('MAIN', 'speak'),
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
