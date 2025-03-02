
import time
import ollama
from ollama import chat
import requests
import subprocess
import ipaddress
import platform
from dotenv import load_dotenv, set_key
from openai import OpenAI
import os

class Provider:
    def __init__(self, provider_name, model, server_address = "127.0.0.1:5000"):
        self.provider_name = provider_name.lower()
        self.model = model
        self.server = self.check_address_format(server_address)
        self.available_providers = {
            "ollama": self.ollama_fn,
            "server": self.server_fn,
            "openai": self.openai_fn
        }
        self.api_key = None
        self.unsafe_providers = ["openai"]
        if self.provider_name not in self.available_providers:
            raise ValueError(f"Unknown provider: {provider_name}")
        if self.provider_name in self.unsafe_providers:
            print("Warning: you are using an API provider. You data will be sent to the cloud.")
            self.get_api_key(self.provider_name)
        elif self.server != "":
            print("Provider initialized at ", self.server)

    def get_api_key(self, provider):
        load_dotenv()
        api_key_var = f"{provider.upper()}_API_KEY"
        api_key = os.getenv(api_key_var)
        if not api_key:
            api_key = input(f"Please enter your {provider} API key: ")
            set_key(".env", api_key_var, api_key)
            load_dotenv()
        return api_key

    def check_address_format(self, address):
        """
        Validate if the address is valid IP.
        """
        try:
            ip, port = address.rsplit(":", 1)
            ipaddress.ip_address(ip)
            if not port.isdigit() or not (0 <= int(port) <= 65535):
                raise ValueError("Port must be a number between 0 and 65535.")
        except ValueError as e:
            raise Exception(f"Invalid address format: {e}")
        return address

    def respond(self, history, verbose = True):
        """
        Use the choosen provider to generate text.
        """
        llm = self.available_providers[self.provider_name]
        thought = llm(history, verbose)
        return thought

    def is_ip_online(self, ip_address):
        """
        Check if an IP address is online by sending a ping request.
        """
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', ip_address]
        try:
            output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
            if output.returncode == 0:
                return True
            else:
                return False
        except subprocess.TimeoutExpired:
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def server_fn(self, history, verbose = False):
        """
        Use a remote server wit LLM to generate text.
        """
        thought = ""
        route_start = f"http://{self.server}/generate"

        if not self.is_ip_online(self.server.split(":")[0]):
            raise Exception(f"Server is offline at {self.server}")

        requests.post(route_start, json={"messages": history})
        is_complete = False
        while not is_complete:
            response = requests.get(f"http://{self.server}/get_updated_sentence")
            thought = response.json()["sentence"]
            is_complete = bool(response.json()["is_complete"])
            time.sleep(2)
        return thought

    def ollama_fn(self, history, verbose = False):
        """
        Use local ollama server to generate text.
        """
        thought = ""
        try:
            stream = chat(
                model=self.model,
                messages=history,
                stream=True,
            )
            for chunk in stream:
              if verbose:
                print(chunk['message']['content'], end='', flush=True)
              thought += chunk['message']['content']
        except ollama.ResponseError as e:
            if e.status_code == 404:
                ollama.pull(self.model)
            if "refused" in str(e):
                raise Exception("Ollama connection failed. is the server running ?")
            raise e
        return thought

    def openai_fn(self, history, verbose=False):
        """
        Use openai to generate text.
        """
        api_key = self.get_api_key("openai")
        client = OpenAI(api_key=api_key)
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=history
            )
            thought = response.choices[0].message.content
            if verbose:
                print(thought)
            return thought
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")

    def test_fn(self, history, verbose = True):
        """
        This function is used to conduct tests.
        """
        thought = """
        This is a test response from the test provider.
        Change provider to 'ollama' or 'server' to get real responses.

        ```python
        print("Hello world from python")
        ```

        ```bash
        echo "Hello world from bash"
        ```
        """
        return thought

if __name__ == "__main__":
    provider = Provider("openai", "gpt-4o-mini")
    print(provider.respond(["user", "Hello, how are you?"]))
