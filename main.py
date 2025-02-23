#!/usr/bin python3

import sys
import signal
import argparse

from sources.llm_provider import Provider
from sources.interaction import Interaction
from sources.code_agent import CoderAgent


parser = argparse.ArgumentParser(description='Deepseek AI assistant')
parser.add_argument('--speak', action='store_true',
                help='Make AI use text-to-speech')
args = parser.parse_args()

def handleInterrupt(signum, frame):
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, handler=handleInterrupt)

    #local_provider = Provider("ollama", "deepseek-r1:14b", None)
    server_provider = Provider(provider_name="server",
                               model="deepseek-r1:14b",
                               server_address="192.168.1.100:5000")

    agent = CoderAgent(model="deepseek-r1:14b",
                       name="jarvis",
                       prompt_path="prompts/coder_agent.txt",
                       provider=server_provider)

    interaction = Interaction([agent], tts_enabled=args.speak)
    while interaction.is_active:
        interaction.get_user()
        interaction.think()
        interaction.show_answer()

if __name__ == "__main__":
    main()
