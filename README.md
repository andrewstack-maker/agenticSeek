
# AgenticSeek: Fully local AI Assistant Powered by Deepseek R1 Agents.

**A fully local AI assistant** using AI agents. The goal of the project is to create a truly Jarvis like assistant using reasoning model such as deepseek R1. 

> 🛠️ **Work in Progress** – Looking for contributors! 🚀  
---

## Features:

-  **Privacy-first**: Runs 100% locally – **no data leaves your machine**  
- ️ **Voice-enabled**: Speak and interact naturally
- **Coding abilities**: Code in Python, Bash, C, Golang, and soon more
-  **Trial-and-error**: Automatically fixes code or command upon execution failure
- **Agent routing**: Select the best agent for the task
- **Multi-agent**: For complex tasks, divide and conquer with multiple agents
- ***Tools:**: All agents have their respective tools ability. Basic search, flight API, files explorer, etc...
-  **Web browsing (not implemented yet)**: Browse the web autonomously to conduct task.

---

## Installation  

### 1️⃣ **Install Dependencies**  
```sh
pip3 install -r requirements.txt
```

### 2️⃣ **Download Models**  

Make sure you have [Ollama](https://ollama.com/) installed.

Download the `deepseek-r1:7b` model from [DeepSeek](https://deepseek.com/models)

```sh
ollama pull deepseek-r1:7b
```

### 3️⃣ **Run the Assistant (Ollama)**  

Start the ollama server
```sh
ollama serve
```

Change the config.ini file to set the provider_name to `ollama` and provider_model to `deepseek-r1:7b`

```sh
[MAIN]
is_local = True
provider_name = ollama
provider_model = deepseek-r1:7b
```

Run the assistant:

```sh
python3 main.py
```

### 4️⃣ **Alternative: Run the LLM on your own server**  


On your "server" that will run the AI model, get the ip address

```sh
ip a | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1
```

Clone the repository and then, run the script `stream_llm.py` in `server/`

```sh
python3 stream_llm.py
```

Now on your personal computer:

Clone the repository.

Change the `config.ini` file to set the `provider_name` to `server` and `provider_model` to `deepseek-r1:7b`.
Set the `provider_server_address` to the ip address of the machine that will run the model.

```sh
[MAIN]
is_local = False
provider_name = server
provider_model = deepseek-r1:14b
provider_server_address = x.x.x.x:5000
```

Run the assistant:

```sh
python3 main.py
```

## Provider

Currently the only provider are :
- ollama -> Use ollama running on your computer. Ollama program for running locally large language models.
- server -> A custom script that allow you to have the LLM model run on another machine. Currently it use ollama but we'll switch to other options soon.
- openai -> Use ChatGPT API (not private).
- deepseek -> Deepseek API (not private).

To select a provider change the config.ini:

```
is_local = False
provider_name = openai
provider_model = gpt-4o
provider_server_address = 127.0.0.1:5000
```
is_local: should be True for any locally running LLM, otherwise False.
provider_name: Select the provider to use by its name, see the provider list above.
provider_model: Set the model to use by the agent.
provider_server_address: can be set to anything if you are not using the server provider.


## Current capabilities

- All running locally
- Reasoning with deepseek R1
- Code execution capabilities (Python, Golang, C, etc..)
- Shell control capabilities in bash
- Will try to fix errors by itself
- Routing system, select the best agent for the task
- Fast text-to-speech using kokoro.
- Speech to text.
- Memory compression (reduce history as interaction progresses using summary model) 
- Recovery: recover and save session from filesystem.
