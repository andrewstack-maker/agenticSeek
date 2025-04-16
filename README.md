<p align="center">
<img align="center" src="./media/whale_readme.jpg">
<p>

--------------------------------------------------------------------------------
English | [中文](./README_CHS.md) | [繁體中文](./README_CHT.md)  | [Français](./README_FR.md)

# AgenticSeek: Manus-like AI powered by Deepseek R1 Agents.


**A fully local alternative to Manus AI**, a voice-enabled AI assistant that codes, explores your filesystem, browse the web and correct it's mistakes all without sending a byte of data to the cloud. Built with reasoning models like DeepSeek R1, this autonomous agent runs entirely on your hardware, keeping your data private.

[![Visit AgenticSeek](https://img.shields.io/static/v1?label=Website&message=AgenticSeek&color=blue&style=flat-square)](https://fosowl.github.io/agenticSeek.html) ![License](https://img.shields.io/badge/license-GPL--3.0-green) [![Discord](https://img.shields.io/badge/Discord-Join%20Us-7289DA?logo=discord&logoColor=white)](https://discord.gg/4Ub2D6Fj) [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/fosowl.svg?style=social&label=Update%20%40Fosowl)](https://x.com/Martin993886460)

> 🛠️ **Work in Progress** – Looking for contributors!


https://github.com/user-attachments/assets/4bd5faf6-459f-4f94-bd1d-238c4b331469


> *Do a deep search of AI startup in Osaka and Tokyo, find at least 5, then save in the research_japan.txt file*

> *Can you make a tetris game in C ?*

> *I would like to setup a new project file index as mark2.*


## Features:

- **100% Local**: No cloud, runs on your hardware. Your data stays yours.

- **Filesystem interaction**: Use bash to navigate and manipulate your files effortlessly.

- **Autonomous Coding**: Can write, debug, and run code in Python, C, Golang and more languages on the way.

- **Agent routing**: Automatically picks the right agent for the job.

- **Planning**: For complex tasks, spins up multiple agents to plan and execute.

- **Autonomous Web Browsing**: Autonomous web navigation.

- **Memory**: Efficient memory and sessions management. 

---

## **Installation**

Make sure you have chrome driver, docker and python3.10 (or newer) installed.

For issues related to chrome driver, see the **Chromedriver** section.

### 1️⃣ **Clone the repository and setup**

```sh
git clone https://github.com/Fosowl/agenticSeek.git
cd agenticSeek
mv .env.example .env
```

### 2️ **Create a virtual env**

```sh
python3 -m venv agentic_seek_env
source agentic_seek_env/bin/activate     
# On Windows: agentic_seek_env\Scripts\activate
```

### 3️⃣ **Install package**

**Automatic Installation:**

```sh
./install.sh
```

**Manually:**

```sh
pip3 install -r requirements.txt
# or
python3 setup.py install
```


## Run locally on your machine

**We recommend using at the very least Deepseek 14B, smaller models will struggle with tasks especially for web browsing.**

### 1️⃣ **Download Models**  

Make sure you have [Ollama](https://ollama.com/) installed.

Download the `deepseek-r1:14b` model from [DeepSeek](https://deepseek.com/models)

```sh
ollama pull deepseek-r1:14b
```

### 2️ **Run the Assistant (Ollama)**  

Start the ollama server
```sh
ollama serve
```

Change the config.ini file to set the provider_name to `ollama` and provider_model to `deepseek-r1:14b`

NOTE: `deepseek-r1:14b`is an example, use a bigger model if your hardware allow it.

```sh
[MAIN]
is_local = True
provider_name = ollama
provider_model = deepseek-r1:14b
provider_server_address = 127.0.0.1:11434
```

start all services :

```sh
sudo ./start_services.sh # MacOS
start ./start_services.cmd # Window
```

Run the assistant:

```sh
python3 main.py
```

*See the **Usage** section if you don't understand how to use it*

*See the **Known issues** section if you are having issues*

*See the **Run with an API** section if your hardware can't run deepseek locally*

*See the **Config** section for detailled config file explanation.*

---

## Usage

Make sure the services are up and running with `./start_services.sh` and run the agenticSeek with `python3 main.py`

```sh
sudo ./start_services.sh
python3 main.py
```

You will be prompted with `>>> `
This indicate agenticSeek await you type for instructions.
You can also use speech to text by setting `listen = True` in the config.

To exit, simply say `goodbye`.

Here are some example usage:

### Coding/Bash

> *Make a snake game in python*

> *Show me how to multiply matrice in C*

> *Make a blackjack in golang*

### Web search

> *Do a web search to find cool tech startup in Japan working on cutting edge AI research*

> *Can you find on the internet who created agenticSeek?*

> *Can you use a fuel calculator online to estimate the cost of a Nice - Milan trip*

### File system

> *Hey can you find where is contract.pdf i lost it*

> *Show me how much space I have left on my disk*

> *Can you follow the readme and install project at /home/path/project*

### Casual

> *Tell me about Rennes, France*

> *Should I pursue a phd ?*

> *What's the best workout routine ?*


After you type your query, agenticSeek will allocate the best agent for the task.

Because this is an early prototype, the agent routing system might not always allocate the right agent based on your query.

Therefore, you should be very explicit in what you want and how the AI might proceed for example if you want it to conduct a web search, do not say:

`Do you know some good countries for solo-travel?`

Instead, ask:

`Do a web search and find out which are the best country for solo-travel`

---

## **Run the LLM on your own server**  

If you have a powerful computer or a server that you can use, but you want to use it from your laptop you have the options to run the LLM on a remote server. 

### 1️⃣  **Set up and start the server scripts** 

On your "server" that will run the AI model, get the ip address

```sh
ip a | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1
```

Note: For Windows or macOS, use ipconfig or ifconfig respectively to find the IP address.

**If you wish to use openai based provider follow the *Run with an API*  section.**

Clone the repository and enter the `server/`folder.


```sh
git clone --depth 1 https://github.com/Fosowl/agenticSeek.git
cd agenticSeek/server/
```

Install server specific requirements:

```sh
pip3 install -r requirements.txt
```

Run the server script.

```sh
python3 app.py --provider ollama --port 3333
```

You have the choice between using `ollama` and `llamacpp` as a LLM service.

### 2️⃣ **Run it** 

Now on your personal computer:

Change the `config.ini` file to set the `provider_name` to `server` and `provider_model` to `deepseek-r1:14b`.
Set the `provider_server_address` to the ip address of the machine that will run the model.

```sh
[MAIN]
is_local = False
provider_name = server
provider_model = deepseek-r1:14b
provider_server_address = x.x.x.x:3333
```

Run the assistant:

```sh
sudo ./start_services.sh # start_services.cmd on windows
python3 main.py
```

## **Run with an API**  

Set the desired provider in the `config.ini`

```sh
[MAIN]
is_local = False
provider_name = openai
provider_model = gpt-4o
provider_server_address = 127.0.0.1:5000
```

WARNING: Make sure there is not trailing space in the config.

Set `is_local` to True if using a local openai-based api.

Change the IP address if your openai-based api run on your own server.

Run the assistant:

```sh
sudo ./start_services.sh # start_services.cmd on windows
python3 main.py
```

---

## Speech to Text

The speech-to-text functionality is disabled by default. To enable it, set the listen option to True in the config.ini file:

```
listen = True
```

When enabled, the speech-to-text feature listens for a trigger keyword, which is the agent's name, before it begins processing your input. You can customize the agent's name by updating the `agent_name` value in the *config.ini* file:

```
agent_name = Friday
```

For optimal recognition, we recommend using a common English name like "John" or "Emma" as the agent name

Once you see the transcript start to appear, say the agent's name aloud to wake it up (e.g., "Friday").

Speak your query clearly.

End your request with a confirmation phrase to signal the system to proceed. Examples of confirmation phrases include:
```
"do it", "go ahead", "execute", "run", "start", "thanks", "would ya", "please", "okay?", "proceed", "continue", "go on", "do that", "go it", "do you understand?"
```

## Config

Example config:
```
[MAIN]
is_local = True
provider_name = ollama
provider_model = deepseek-r1:32b
provider_server_address = 127.0.0.1:11434
agent_name = Friday
recover_last_session = False
save_session = False
speak = False
listen = False
work_dir =  /Users/mlg/Documents/ai_folder
jarvis_personality = False
[BROWSER]
headless_browser = False
stealth_mode = False
```

**Explanation**:

- is_local -> Runs the agent locally (True) or on a remote server (False).
- provider_name -> The provider to use (one of: `ollama`, `server`, `lm-studio`, `deepseek-api`)
- provider_model -> The model used, e.g., deepseek-r1:32b.
- provider_server_address -> Server address, e.g., 127.0.0.1:11434 for local. Set to anything for non-local API.
- agent_name -> Name of the agent, e.g., Friday. Used as a trigger word for TTS.
- recover_last_session -> Restarts from last session (True) or not (False).
- save_session -> Saves session data (True) or not (False).
- speak -> Enables voice output (True) or not (False).
- listen -> listen to voice input (True) or not (False).
- work_dir -> Folder the AI will have access to. eg: /Users/user/Documents/.
- jarvis_personality -> Uses a JARVIS-like personality (True) or not (False). This simply change the prompt file.
- languages -> The list of supported language, needed for the llm router to work properly, avoid putting too many or too similar languages.
- headless_browser -> Runs browser without a visible window (True) or not (False).
- stealth_mode -> Make bot detector time harder. Only downside is you have to manually install the anticaptcha extension.

## Providers

The table below show the available providers:

| Provider  | Local? | Description                                               |
|-----------|--------|-----------------------------------------------------------|
| ollama    | Yes    | Run LLMs locally with ease using ollama as a LLM provider |
| server    | Yes    | Host the model on another machine, run your local machine |
| lm-studio  | Yes    | Run LLM locally with LM studio (set `provider_name` to `lm-studio`)|
| openai    | No     | Use ChatGPT API (non-private)                             |
| deepseek-api  | No     | Deepseek API (non-private)                                |
| huggingface| No    | Hugging-Face API (non-private)                            |

To select a provider change the config.ini:

```
is_local = False
provider_name = openai
provider_model = gpt-4o
provider_server_address = 127.0.0.1:5000
```
`is_local`: should be True for any locally running LLM, otherwise False.

`provider_name`: Select the provider to use by it's name, see the provider list above.

`provider_model`: Set the model to use by the agent.

`provider_server_address`: can be set to anything if you are not using the server provider.

# Known issues

## Chromedriver Issues

**Known error #1:** *chromedriver mismatch*

`Exception: Failed to initialize browser: Message: session not created: This version of ChromeDriver only supports Chrome version 113
Current browser version is 134.0.6998.89 with binary path`

This happen if there is a mismatch between your browser and chromedriver version.

You need to navigate to download the latest version:

https://developer.chrome.com/docs/chromedriver/downloads

If you're using Chrome version 115 or newer go to:

https://googlechromelabs.github.io/chrome-for-testing/

And download the chromedriver version matching your OS.

![alt text](./media/chromedriver_readme.png)

If this section is incomplete please raise an issue.

## FAQ

**Q: What hardware do I need?**  

| Model Size  | GPU  | Comment                                               |
|-----------|--------|-----------------------------------------------------------|
| 7B        | 8GB Vram | ⚠️ Not recommended. Performance is poor, frequent hallucinations, and planner agents will likely fail. |
| 14B        | 12 GB VRAM (e.g. RTX 3060) | ✅ Usable for simple tasks. May struggle with web browsing and planning tasks. |
| 32B        | 24+ GB VRAM (e.g. RTX 4090) | 🚀 Success with most tasks, might still struggle with task planning |
| 70B+        | 48+ GB Vram (eg. mac studio) | 💪 Excellent. Recommended for advanced use cases. |

**Q: Why Deepseek R1 over other models?**  

Deepseek R1 excels at reasoning and tool use for its size. We think it’s a solid fit for our needs other models work fine, but Deepseek is our primary pick.

**Q: I get an error running `main.py`. What do I do?**  

Ensure Ollama is running (`ollama serve`), your `config.ini` matches your provider, and dependencies are installed. If none work feel free to raise an issue.

**Q: Can it really run 100% locally?**  

Yes with Ollama or Server providers, all speech to text, LLM and text to speech model run locally. Non-local options (OpenAI or others API) are optional.

**Q: Why should I use AgenticSeek when I have Manus?**

This started as Side-Project we did out of interest about AI agents. What’s special about it is that we want to use local model and avoid APIs.
We draw inspiration from Jarvis and Friday (Iron man movies) to make it "cool" but for functionnality we take more inspiration from Manus, because that's what people want in the first place: a local manus alternative.
Unlike Manus, AgenticSeek prioritizes independence from external systems, giving you more control, privacy and avoid api cost.

## Contribute

We’re looking for developers to improve AgenticSeek! Check out open issues or discussion.

[Contribution guide](./docs/CONTRIBUTING.md)

[![Star History Chart](https://api.star-history.com/svg?repos=Fosowl/agenticSeek&type=Date)](https://www.star-history.com/#Fosowl/agenticSeek&Date)

## Maintainers:
 > [Fosowl](https://github.com/Fosowl)
 > [steveh8758](https://github.com/steveh8758) 
