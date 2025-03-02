
# 🚀 agenticSeek: Local AI Assistant Powered by DeepSeek Agents  

**A fully local AI assistant** using Deepseek R1 agents.

> 🛠️ **Work in Progress** – Looking for contributors! 🚀  
---

## Features:

-  **Privacy-first**: Runs 100% locally – **no data leaves your machine**  
- ️ **Voice-enabled**: Speak and interact naturally
- **Coding abilities**: Code in Python, Bash, C, Golang, and soon more
-  **Self-correcting**: Automatically fixes errors by itself
- **Agent routing**: Select the best agent for the task
- **Multi-agent**: For complex tasks, divide and conquer with multiple agents
-  **Web browsing (not implemented yet)**: Browse the web and search the internet  

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

### 4️⃣ **Alternative: Run the Assistant (Own Server)**  

On the other machine that will run the model execute the script in stream_llm.py


```sh
python3 stream_llm.py
```

Get the ip address of the machine that will run the model

```sh
ip a | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1
```

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

## Current capabilities

- All running locally
- Reasoning with deepseek R1
- Code execution capabilities (Python, Golang, C)
- Shell control capabilities in bash
- Will try to fix errors by itself
- Routing system, select the best agent for the task
- Fast text-to-speech using kokoro.
- Memory compression (reduce history as interaction progresses using summary model) 
- Recovery: recover last session from memory

## UNDER DEVELOPMENT

- Web browsing
- Knowledge base RAG
- Graphical interface
- Speech-to-text using distil-whisper/distil-medium.en
