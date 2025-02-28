#!/usr/bin python3

import sys
import signal
import argparse
import configparser

from sources.llm_provider import Provider
from sources.interaction import Interaction
from sources.code_agent import CoderAgent


parser = argparse.ArgumentParser(description='Deepseek AI assistant')
parser.add_argument('--speak', action='store_true',
                help='Make AI use text-to-speech')
args = parser.parse_args()

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

    agent = CoderAgent(model=config["MAIN"]["provider_model"],
                       name=config["MAIN"]["agent_name"],
                       prompt_path="prompts/coder_agent.txt",
                       provider=provider)

    interaction = Interaction([agent], tts_enabled=config.getboolean('MAIN', 'speak'),
                                       recover_last_session=config.getboolean('MAIN', 'recover_last_session'))
    while interaction.is_active:
        interaction.get_user()
        interaction.think()
        interaction.show_answer()

if __name__ == "__main__":
    main()
