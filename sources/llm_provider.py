
import time
import ollama
from ollama import chat
import requests
import subprocess
import ipaddress
import platform

class Provider:
    def __init__(self, provider_name, model, server_address = "127.0.0.1:5000"):
        self.provider_name = provider_name.lower()
        self.model = model
        self.server = self.check_address_format(server_address)
        self.available_providers = {
            "ollama": self.ollama_fn,
            "server": self.server_fn,
            "test": self.test_fn

        }
        if self.server != "":
            print("Provider initialized at ", self.server)
        else:
            print("Using localhost as provider")

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

    def server_fn(self, history, verbose = True):
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
            # TODO add real time streaming to stdout
            is_complete = bool(response.json()["is_complete"])
            time.sleep(2)
        return thought

    def ollama_fn(self, history, verbose = True):
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

    def test_fn(self, history, verbose = True):
        """
        Test function to generate text.
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
