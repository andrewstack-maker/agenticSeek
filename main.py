#!/usr/bin python3

import sys
from colorama import Fore
import signal
import argparse

from sources.text_to_speech import Speech
from sources.code_agent import CoderAgent
from sources.utility import pretty_print
from sources.llm_provider import Provider

parser = argparse.ArgumentParser(description='Deepseek AI assistant')
parser.add_argument('--speak', action='store_true',
                help='Make AI use text-to-speech')
args = parser.parse_args()

def get_user_query() -> str:
    buffer = ""

    while buffer == "" or buffer.isascii() == False:
        buffer = input(f">>> ")
        if buffer == "exit":
            return None
    return buffer

def conversation_loop():
    speech_module = Speech()
    #local_provider = Provider("ollama", "deepseek-r1:14b", None)
    server_provider = Provider("server", "deepseek-r1:14b", "192.168.1.100:5000")

    agent = CoderAgent(model="deepseek-r1:14b",
                       name="Marcus the code agent",
                       prompt_path="prompts/coder_agent.txt",
                       provider=server_provider)

    while True:
        query = get_user_query()
        if query is None:
            break
        answer, reasoning = agent.answer(query, speech_module)
        pretty_print(answer, color="output")
        if args.speak:
            speech_module.speak(answer)

def handleInterrupt(signum, frame):
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, handler=handleInterrupt)
    conversation_loop()

if __name__ == "__main__":
    main()
