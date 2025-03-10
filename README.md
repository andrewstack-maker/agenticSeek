
# AgenticSeek: Local AI Assistant Powered by Deepseek R1 Agents.

**A fully local alternative to Manus AI**, a voice-enabled AI assistant that codes, explores your filesystem, and correct it's mistakes all without sending a byte of data to the cloud. The goal of the project is to create a truly Jarvis like assistant using reasoning model such as deepseek R1. 

> 🛠️ **Work in Progress** – Looking for contributors! 🚀  
---

## Features:

- **Privacy-first**: Runs 100% locally – **no data leaves your machine**  
- ️**Voice-enabled**: Speak and interact naturally
- **Filesystem interaction**: Use bash to interact with your filesystem.
- **Coding abilities**: Code in Python, C, Golang, and soon more
- **Trial-and-error**: If a command or code fails, the assistant retries to fixes it automatically, saving you time.
- **Agent routing**: Select the best agent for the task
- **Multi-agent (On Dev branch)**: For complex tasks, divide and conquer with multiple agents
- **Tools:**: All agents have their respective tools ability. Basic search, flight API, files explorer, etc...
- **Web browsing (not implemented yet | Hight priority task)**: Browse the web autonomously to conduct task.
- **Memory&Recovery**: Compress conversation over time to retain useful information, recover conversation session.

---

## Run locally

**We recommend using at least Deepseek 14B—smaller models struggle with tool use and memory retention.**

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

## **Alternative: Run the LLM on your own server**  

### 1️⃣  **Set up and start the server scripts** 

On your "server" that will run the AI model, get the ip address

```sh
ip a | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1
```

Clone the repository and then, run the script `stream_llm.py` in `server/`

```sh
python3 stream_llm.py
```

### 2️⃣ **Run it** 

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

## Providers

The table below show the available providers:

| Provider  | Local? | Description                                               |
|-----------|--------|-----------------------------------------------------------|
| Ollama    | Yes    | Run LLMs locally with ease using ollama as a LLM provider |
| Server    | Yes    | Host the model on another machine, run your local machine |
| OpenAI    | No     | Use ChatGPT API (non-private)                             |
| Deepseek  | No     | Deepseek API (non-private)                                |
| HuggingFace| No    | Hugging-Face API (non-private)                            |


To select a provider change the config.ini:

```
is_local = False
provider_name = openai
provider_model = gpt-4o
provider_server_address = 127.0.0.1:5000
```
`is_local`: should be True for any locally running LLM, otherwise False.

`provider_name`: Select the provider to use by its name, see the provider list above.

`provider_model`: Set the model to use by the agent.

`provider_server_address`: can be set to anything if you are not using the server provider.

## Current contributor:

Fosowl 🇫🇷
steveh8758 🇹🇼
