
# 🚀 agenticSeek: Local AI Assistant Powered by DeepSeek Agents  

**A fully local AI assistant** using a swarm of DeepSeek agents, capable of:  
✅ **Code execution** (Python, Bash)  
✅ **Web browsing**  
✅ **Speech-to-text & text-to-speech**  
✅ **Self-correcting code execution**  

> 🛠️ **Work in Progress** – Looking for contributors! 🚀  

---

## 🌟 Why?  

-  **Privacy-first**: Runs 100% locally – **no data leaves your machine**  
- ️ **Voice-enabled**: Speak and interact naturally
-  **Self-correcting**: Automatically fixes its own code
- **Multi-agent**: Use a swarm of agents to answer complex questions
-  **Web browsing (not implemented yet)**: Browse the web and search the internet  
-  **Knowledge base (not implemented yet)**: Use a knowledge base to answer questions  

---

## Installation  

### 1️⃣ **Install Dependencies**  
Make sure you have [Ollama](https://ollama.com/) installed, then run:  
```sh
pip3 install -r requirements.txt
```

### 2️⃣ **Download Models**  

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
- Will try to fix code by itself
- Fast text-to-speech using kokoro.
- Speech-to-text using distil-whisper/distil-medium.en
- Web browsing (not implemented yet)
- Knowledge base RAG (not implemented yet)