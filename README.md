
# AgenticSeek: Manus-like AI powered by Deepseek R1 Agents.


**A fully local alternative to Manus AI**, a voice-enabled AI assistant that codes, explores your filesystem, browse the web and correct it's mistakes all without sending a byte of data to the cloud. Built with reasoning models like DeepSeek R1, this autonomous agent runs entirely on your hardware, keeping your data private.

[![Visit AgenticSeek](https://img.shields.io/static/v1?label=Website&message=AgenticSeek&color=blue&style=flat-square)](https://fosowl.github.io/agenticSeek.html) ![License](https://img.shields.io/badge/license-GPL--3.0-green) ![Discord](https://img.shields.io/badge/Discord-Join%20Us-7289DA?logo=discord&logoColor=white)
> 🛠️ **Work in Progress** – Looking for contributors!

![alt text](./media/whale_readme.jpg)



## Features:

- **100% Local**: No cloud, runs on your hardware. Your data stays yours.

- **Voice interaction**: Voice-enabled natural interaction.

- **Filesystem interaction**: Use bash to navigate and manipulate your files effortlessly.

- **Code what you ask**: Can write, debug, and run code in Python, C, Golang and more languages on the way.

- **Autonomous**: If a command flops or code breaks, it retries and fixes it by itself.

- **Agent routing**: Automatically picks the right agent for the job.

- **Divide and Conquer**: For big tasks, spins up multiple agents to plan and execute.

- **Tool-Equipped**: From basic search to flight APIs and file exploration, every agent has it's own tools.

- **Memory**: Remembers what’s useful, your preferences and past sessions conversation.

- **Web Browsing**: Autonomous web navigation is underway. (See it on browser branch)

---

## **Installation**

### 1️⃣ **Clone the repository**

```sh
git clone https://github.com/Fosowl/agenticSeek.git
cd agenticSeek
```

### 2️ **Create a virtual env**

```sh
python3 -m venv agentic_seek_env
source agentic_seek_env/bin/activate      # On Windows: agentic_seek_env\Scripts\activate
```

### 3️⃣ **Install Dependencies**

```sh
pip3 install -r requirements.txt
```

## Run locally on your machine

**We recommend using at least Deepseek 14B, smaller models struggle with tool use and forget quickly the context.**

### 1️⃣ **Download Models**  

Make sure you have [Ollama](https://ollama.com/) installed.

Download the `deepseek-r1:7b` model from [DeepSeek](https://deepseek.com/models)

```sh
ollama pull deepseek-r1:7b
```

### 2️ **Run the Assistant (Ollama)**  

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

---

## **Run the LLM on your own server**  

If you have a powerful computer or a server that you can use, but you want to use it from your laptop you have the options to run the LLM on a remote server. 

### 1️⃣  **Set up and start the server scripts** 

On your "server" that will run the AI model, get the ip address

```sh
ip a | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1
```

Note: For Windows or macOS, use ipconfig or ifconfig respectively to find the IP address.

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

## **Run with an API**  

Clone the repository.

Set the desired provider in the `config.ini`

```sh
[MAIN]
is_local = False
provider_name = openai
provider_model = gpt4-o
provider_server_address = 127.0.0.1:5000 # can be set to anything, not used
```

Run the assistant:

```sh
python3 main.py
```

---

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

## FAQ
**Q: What hardware do I need?**  

7B Model: GPU with 8GB VRAM.
14B Model: 12GB GPU (e.g., RTX 3060).
32B Model: 24GB+ VRAM.

**Q: Why Deepseek R1 over other models?**  

Deepseek R1 excels at reasoning and tool use for its size. We think it’s a solid fit for our needs other models work fine, but Deepseek is our primary pick.

**Q: I get an error running `main.py`. What do I do?**  

Ensure Ollama is running (`ollama serve`), your `config.ini` matches your provider, and dependencies are installed. If none work feel free to raise an issue.

**Q: How to join the discord ?**

Ask in the Community section for an invite.

**Q: Can it really run 100% locally?**  

Yes with Ollama or Server providers, all speech to text, LLM and text to speech model run locally. Non-local options (OpenAI or others API) are optional.

**Q: How come it is older than manus ?**

we started this a fun side project to make a fully local, Jarvis-like AI. However, with the rise of Manus, we saw the opportunity to redirected some tasks to make yet another alternative.

**Q: How is it better than manus  ?**

It's not but we prioritizes local execution and privacy over cloud based approach. It’s a fun, accessible alternative!

## Contribute

We’re looking for developers to improve AgenticSeek! Check out open issues or discussion.

## Authors:
 > [Fosowl](https://github.com/Fosowl)
 > [steveh8758](https://github.com/steveh8758) 
