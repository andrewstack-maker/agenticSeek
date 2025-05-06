# AgenticSeek: 類似 Manus 但基於 Deepseek R1 Agents 的本地模型。

<p align="center">
<img align="center" src="./media/whale_readme.jpg">
<p>

--------------------------------------------------------------------------------
[English](./README.md) | 繁體中文 | [日本語](./README_JP.md)


*一个 **100% 本地替代 Manus AI** 的方案，这款支持语音的 AI 助理能够自主浏览网页、编写代码和规划任务，同时将所有数据保留在您的设备上。专为本地推理模型量身打造，完全在您自己的硬件上运行，确保完全的隐私保护和零云端依赖。*

[![Visit AgenticSeek](https://img.shields.io/static/v1?label=Website&message=AgenticSeek&color=blue&style=flat-square)](https://fosowl.github.io/agenticSeek.html) ![License](https://img.shields.io/badge/license-GPL--3.0-green) [![Discord](https://img.shields.io/badge/Discord-Join%20Us-7289DA?logo=discord&logoColor=white)](https://discord.gg/8hGDaME3TC) [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/fosowl.svg?style=social&label=Update%20%40Fosowl)](https://x.com/Martin993886460)

### 为什么选择 AgenticSeek？

* 🔒 完全本地化与隐私保护 - 所有功能都在您的设备上运行 — 无云端服务，无数据共享。您的文件、对话和搜索始终保持私密。

* 🌐 智能网页浏览 - AgenticSeek 能够自主浏览互联网 — 搜索、阅读、提取信息、填写网页表单 — 全程无需人工操作。

* 💻 自主编码助手 - 需要代码？它可以编写、调试并运行 Python、C、Go、Java 等多种语言的程序 — 全程无需监督。

* 🧠 智能代理选择 - 您提问，它会自动选择最适合该任务的代理。就像拥有一个随时待命的专家团队。

* 📋 规划与执行复杂任务 - 从旅行规划到复杂项目 — 它能将大型任务分解为步骤，并利用多个 AI 代理完成工作。

* 🎙️ 语音功能 - 清晰、快速、未来感十足的语音与语音转文本功能，让您能像科幻电影中一样与您的个人 AI 助手对话。

https://github.com/user-attachments/assets/4bd5faf6-459f-4f94-bd1d-238c4b331469

> 🛠️ **目前還在開發階段** – 歡迎任何貢獻者加入我們！

---

## **安裝**

確保已安裝了 Chrome driver，Docker 和 Python 3.10（或更新）。

我们强烈建议您使用 Python 3.10 进行设置，否则可能会发生依赖错误。

有關於 Chrome driver 的問題，請參見 **Chromedriver** 部分。

### 1️⃣ **複製儲存庫與設置環境變數**

```sh
git clone https://github.com/Fosowl/agenticSeek.git
cd agenticSeek
mv .env.example .env
```

### 2️ **建立虛擬環境**

```sh
python3 -m venv agentic_seek_env
source agentic_seek_env/bin/activate     
# On Windows: agentic_seek_env\Scripts\activate
```

### 3️⃣ **安裝所需套件**

**自動安裝:**

```sh
./install.sh
```

** 若要让文本转语音（TTS）功能支持中文，你需要安装 jieba（中文分词库）和 cn2an（中文数字转换库）：**

```
pip3 install jieba cn2an
```

**手動安裝:**


**注意：对于任何操作系统，请确保您安装的 ChromeDriver 与您已安装的 Chrome 版本匹配。运行 `google-chrome --version`。如果您的 Chrome 版本 > 135，请参阅已知问题**

- *Linux*:

更新软件包列表：`sudo apt update`

安装依赖项：`sudo apt install -y alsa-utils portaudio19-dev python3-pyaudio libgtk-3-dev libnotify-dev libgconf-2-4 libnss3 libxss1`

安装与您的 Chrome 浏览器版本匹配的 ChromeDriver：
`sudo apt install -y chromium-chromedriver`

安装 requirements：`pip3 install -r requirements.txt`

- *Macos*:

更新 brew：`brew update`

安装 chromedriver：`brew install --cask chromedriver`

安装 portaudio：`brew install portaudio`

升级 pip：`python3 -m pip install --upgrade pip`

升级 wheel：`pip3 install --upgrade setuptools wheel`

安装 requirements：`pip3 install -r requirements.txt`

- *Windows*:

安装 pyreadline3：`pip install pyreadline3`

手动安装 portaudio（例如，通过 vcpkg 或预编译的二进制文件），然后运行：`pip install pyaudio`

从以下网址手动下载并安装 chromedriver：https://sites.google.com/chromium.org/driver/getting-started

将 chromedriver 放置在包含在您的 PATH 中的目录中。

安装 requirements：`pip3 install -r requirements.txt`

## 在本地機器上運行 AgenticSeek

**建議至少使用 Deepseek 14B 以上參數的模型，較小的模型難以使用助理功能並且很快就會忘記上下文之間的關係。**

**本地运行助手**

启动你的本地提供者，例如使用 ollama：

```sh
ollama serve
```

请参阅下方支持的本地提供者列表。

修改 config.ini 文件以设置 provider_name 为支持的提供者，并将 provider_model 设置为该提供者支持的 LLM。我们推荐使用具有推理能力的模型，如 *Qwen* 或 *Deepseek*。

请参见 README 末尾的 **FAQ** 部分了解所需硬件。

```sh
[MAIN]
is_local = True # 无论是在本地运行还是使用远程提供者。
provider_name = ollama # 或 lm-studio, openai 等..
provider_model = deepseek-r1:14b # 选择适合您硬件的模型
provider_server_address = 127.0.0.1:11434
agent_name = Jarvis # 您的 AI 助手的名称
recover_last_session = True # 是否恢复之前的会话
save_session = True # 是否记住当前会话
speak = True # 文本转语音
listen = False # 语音转文本，仅适用于命令行界面
work_dir = /Users/mlg/Documents/workspace # AgenticSeek 的工作空间。
jarvis_personality = False # 是否使用更"贾维斯"风格的性格，不推荐在小型模型上使用
languages = en zh # 语言列表，文本转语音将默认使用列表中的第一种语言
[BROWSER]
headless_browser = True # 是否使用无头浏览器，只有在使用网页界面时才推荐使用。
stealth_mode = True # 使用无法检测的 selenium 来减少浏览器检测
```

**本地提供者列表**

| 提供者      | 本地? | 描述                                                   |
|-------------|--------|-------------------------------------------------------|
| ollama      | 是     | 使用 ollama 作为 LLM 提供者，轻松本地运行 LLM         |
| lm-studio   | 是     | 使用 LM Studio 本地运行 LLM（将 `provider_name` 设置为 `lm-studio`）|
| openai      | 否     | 使用兼容的 API                                        |

下一步： [Start services and run AgenticSeek](#Start-services-and-Run)  

---

## **Run with an API （透過 API 執行）**

設定 `config.ini`。

```sh
[MAIN]
is_local = False
provider_name = openai
provider_model = gpt-4o
provider_server_address = 127.0.0.1:5000
```

警告：確保 `config.ini` 沒有行尾空格。

如果使用基於本機的 openai-based api 則把 `is_local` 設定為 `True`。

同時更改你的 IP 為 openai-based api 的 IP。

下一步： [Start services and run AgenticSeek](#Start-services-and-Run)  

---

## Start services and Run
(启动服务并运行)

如果需要，请激活你的 Python 环境。
```sh
source agentic_seek_env/bin/activate
```

启动所需的服务。这将启动 `docker-compose.yml` 中的所有服务，包括：
- searxng
- redis（由 redis 提供支持）
- 前端

```sh
sudo ./start_services.sh # MacOS
start ./start_services.cmd # Windows
```

**选项 1:** 使用 CLI 界面运行。

```sh
python3 cli.py
```

**选项 2:** 使用 Web 界面运行。

注意：目前我們建議您使用 CLI 界面。Web 界面仍在積極開發中。

启动后端服务。

```sh
python3 api.py
```

访问 `http://localhost:3000/`，你应该会看到 Web 界面。

请注意，目前 Web 界面不支持消息流式传输。


*如果你不知道如何開始，請參閱 **Usage** 部分*

---

## Usage （使用方法）

为确保 agenticSeek 在中文环境下正常工作，请确保在 config.ini 中设置语言选项。
languages = en zh
更多信息请参阅 Config 部分

確定所有的核心檔案都啟用了，也就是執行過這條命令 `./start_services.sh` 然後你就可以使用 `python3 cli.py` 來啟動 AgenticSeek 了！

```sh
sudo ./start_services.sh
python3 cli.py
```

當你看到執行後顯示 `>>> `
這表示一切運作正常，AgenticSeek 正在等待你給他任何指令。
你也可以透過設定 `config.ini` 內的 `listen = True` 來啟用語音轉文字。

要退出時，只要和他說 `goodbye` 就可以退出！

以下是一些用法：

### Coding/Bash

> *在 Golang 中幫助我進行矩陣乘法*

> *使用 nmap 掃描我的網路，找出是否有任何可疑裝置連接*

> *用 Python 製作一個貪食蛇遊戲*

### 網路搜尋

> *進行網路搜尋，找出日本從事尖端人工智慧研究的酷炫科技新創公司*

> *你能在網路上找到誰創造了 AgenticSeek 嗎？*

> *你能在哪個網站上找到便宜的 RTX 4090 嗎？*

### 檔案瀏覽與搜尋

> *嘿，你能找到我遺失的 million_dollars_contract.pdf 在哪裡嗎？*

> *告訴我我的磁碟還剩下多少空間*

> *尋找並閱讀 README.md，並按照安裝說明進行操作*

### 日常聊天

> *告訴我關於法國的事*

> *人生的意義是什麼？*

> *我應該在鍛鍊前還是鍛鍊後服用肌酸？*


當你把指令送出後，AgenticSeek 會自動調用最能提供幫助的助理，去完成你交辦的工作和指令。

但也有可能出現怪怪的情況，或是你要找飛機機票，他跑去教你如何一步步做出一台飛機（開玩笑的，但真的可能出現），因為這是一個早期專案，我們會努力教導他、完善他的！

所以我們希望你在使用時，能明確地表明你希望他要怎麼做，下面給你一個範例！

你該說：
- 进行网络搜索，找出哪些国家最适合独自旅行


而不是說：
- 你知道哪些国家适合独自旅行？

---


---

## **在本地執行屬於你的 LLM 伺服器** 

如果你有一台功能強大的電腦或伺服器，但你想透過筆記型電腦使用它，那麼你可以選擇在遠端伺服器上執行 LLM。

### 1️⃣  **設定並啟動伺服器腳本** 

在運行 AI 模型的「伺服器」上，取得 IP 位址

```sh
ip a | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1
```

注意：請在 Windows 或 MacOS，分別使用 `ipconfig` 與 `ifconfig` 來尋找 IP 位址。

**如果你希望使用基於 Openai 的服務，請按照 *透過 API 執行* 部分進行。**

複製儲存庫並且進入 `server/` 資料夾。

```sh
git clone --depth 1 https://github.com/Fosowl/agenticSeek.git
cd agenticSeek/server/
```

安裝伺服器所需的套件：

```sh
pip3 install -r requirements.txt
```

執行伺服器腳本。

```sh
python3 app.py --provider ollama --port 3333
```

您可以選擇使用 `ollama` 或 `llamacpp` 作為 LLM 的服務框架。

### 2️⃣ **執行** 

在你的電腦上：

- 更改 `config.ini`
    - `provider_name = server`
    - `provider_model = deepseek-r1:14b`
    - `provider_server_address = {你執行模型的電腦的 IP 位址}`

```sh
[MAIN]
is_local = False
provider_name = server
provider_model = deepseek-r1:14b
provider_server_address = x.x.x.x:3333
```


---

## 語音轉文字

请注意，目前语音转文字功能仅支持英语。

預設狀況下，語音轉文字功能是停用的。若要啟用它，請在 `config.ini` 檔案中，將 `listen` 選項設為 `True`：

```
listen = True
```

啟用後 AgenticSeek 會聆聽你是否呼喚他，他才會開始聽你說的話，你可以在 *config.ini* 內去設定，要怎麼叫他。

```
agent_name = Friday
```

為了獲得比較好的結果，我們建議使用常見的英文名稱（如 “John” 或 “Emma”）作為他的名字。

當你看到程式開始執行時，請大聲說出他的名字，就可以喚醒 AgenticSeek 去聆聽！（如：Friday）

清楚說出你的需求。

用確認短句結束你說的話，以通知 AgenticSeek 繼續。確認短句的範例包括：
```
"do it", "go ahead", "execute", "run", "start", "thanks", "would ya", "please", "okay?", "proceed", "continue", "go on", "do that", "go it", "do you understand?"
```

## Config

Config 範例：
```
[MAIN]
is_local = True
provider_name = ollama
provider_model = deepseek-r1:1.5b
provider_server_address = 127.0.0.1:11434
agent_name = Friday
recover_last_session = False
save_session = False
speak = False
listen = False
work_dir =  /Users/mlg/Documents/ai_folder
jarvis_personality = False
languages = en zh
[BROWSER]
headless_browser = False
stealth_mode = False
```

**說明**:
- is_local
    - True：在本地運行。
    - False：在遠端伺服器運行。
- provider_name
    - 框架類型
        - `ollama`, `server`, `lm-studio`, `deepseek-api`
- provider_model
    - 運行的模型
        - `deepseek-r1:1.5b`, `deepseek-r1:14b`
- provider_server_address
    - 伺服器 IP
        - `127.0.0.1:11434`
- agent_name
    - AgenticSeek 的名字，用作TTS的觸發單詞。
        - `Friday`
- recover_last_session
    - True：從上個對話繼續。
    - False：重啟對話。
- save_session
    - True：儲存對話紀錄。
    - False：不保存。
- speak
    - True：啟用語音輸出。
    - False：關閉語音輸出。
- listen
    - True：啟用語音輸入。
    - False：關閉語音輸入。
- work_dir
    - AgenticSeek 擁有能存取與交互的工作目錄。
- jarvis_personality
    > 就是那個鋼鐵人的 JARVIS 
    - True：啟用 JARVIS 個性。
    - False：關閉 JARVIS 個性。
- headless_browser
    - True：前景瀏覽器。（很酷，推薦使用他 XD）
    - False：背景執行瀏覽器。
- stealth_mode
    -  隱私模式，但需要你自己安裝反爬蟲擴充功能。
- languages
    -  支持的语言列表。用于代理路由系统。语言列表越长，下载的模型越多。

## 框架

下表顯示了可用的框架：

| 框架  | 本地? | 描述|
|-|-|-|
| ollama | 可 | 使用 ollama 框架去執行本地模型 |
| server | 可 | 本地伺服器執行模型遠端調用 |
| lm-studio | 可 | 使用 LM Studio 在本地運行 LLM（設定provider_name為lm-studio）|
| openai | 不可 | 使用 ChatGPT API（無法保證隱私）|
| deepseek-api | 不可 | 使用 Deepseek API (無法保證隱私)|
| huggingface | 不可 | 使用 Hugging-Face API (無法保證隱私)|

若要選擇框架，請變更 `config.ini` 文件：

```
is_local = False
provider_name = openai
provider_model = gpt-4o
provider_server_address = 127.0.0.1:5000
```
`is_local`: 對於任何本地運行的 LLM 都應該為 True，否則為 False。

`provider_name`: 透過名稱選擇要使用的框架，請參閱上面的框架清單。

`provider_model`: 設定 AgenticSeek 使用的模型。

`provider_server_address`: 如果不使用雲端 API，則可以將其設定為任何內容。

# Known issues （已知問題）

## Chromedriver Issues

**已知問題 #1:** *chromedriver mismatch*

`Exception: Failed to initialize browser: Message: session not created: This version of ChromeDriver only supports Chrome version 113
Current browser version is 134.0.6998.89 with binary path`

如果你的瀏覽器和 chromedriver 版本不一樣，就會發生這種情況。

你可以透過以下連結下載最新版本：

https://developer.chrome.com/docs/chromedriver/downloads

如果您使用的是 Chrome 版本 115 或更新版本，請前往：

https://googlechromelabs.github.io/chrome-for-testing/

下載與你的作業系統相符的 chromedriver 版本。

![alt text](./media/chromedriver_readme.png)

如果有其他問題，請提供盡量詳細的敘述到 Issues 上，盡可能包含當前環境和問題是怎麼發生的。

## FAQ

**Q: 我需要什麼硬體？**  

| 模型大小  | GPU  | 備註                                               |
|-----------|--------|-----------------------------------------------------------|
| 7B        | 8GB Vram | ⚠️ 不推薦。性能較差，經常出現幻覺，規劃代理可能會失敗。 |
| 14B        | 12 GB VRAM (例如 RTX 3060) | ✅ 適用於簡單任務。可能在網頁瀏覽和規劃任務上表現不佳。 |
| 32B        | 24+ GB VRAM (例如 RTX 4090) | 🚀 大多數任務成功，但可能仍在任務規劃上有困難。 |
| 70B+        | 48+ GB Vram (例如 mac studio) | 💪 表現優異。建議用於高級使用情境。 |

**Q：為什麼選擇 Deepseek R1 而不是其他模型？**

就其尺寸而言，Deepseek R1 在推理和使用方面表現出色。我們認為非常適合我們的需求，其他模型也很好用，但 Deepseek 是我們最後選定的模型。

**Q：我在執行時 `cli.py` 時出現錯誤。我該怎麼辦？**

1. 確保 Ollama 正在運行（ollama serve）
2. 你 `config.ini` 內 `provider_name` 的框架選擇正確。
3. 依賴套件已安裝
4. 如果均無效，請隨時提出 Issues，同樣盡可能包含當前環境和問題是怎麼發生的。

**Q：它真的是 100% 本地運行嗎？**

是的，透過 Ollama 或其他框架，所有語音轉文字、LLM 和文字轉語音模型都在本地運行。
*但你能選擇非本地執行（OpenAI 或其他 API），同樣也是可以的*


**Q：我有 Manus 為甚麼還要用 AgenticSeek？**

這是我們因為興趣做的一個小 Side-Project，他特別的點在於是一個全部本地化的模型，而且可以像鋼鐵人裡面一樣與 `Jarvis` 對話，聽起來就超級酷的吧！隨著 Manus 的進化，我們也相應的加入更多功能！

**Q：它比 Manus 好在哪裡？**

不不不，AgenticSeek 和 Manus 是不同取向的東西，我們優先考慮的是本地執行和隱私，而不是基於雲端。這是一個與 Manus 相比起來更有趣且易使用的方案！

**Q: 是否支持中文以外的语言？**

DeepSeek R1 天生会说中文

但注意：代理路由系统只懂英文，所以必须通过 config.ini 的 languages 参数（如 languages = en zh）告诉系统：

如果不设置中文？后果可能是：你让它写代码，结果跳出来个"医生代理"（虽然我们根本没有这个代理... 但系统会一脸懵圈！）

实际上会下载一个小型翻译模型来协助任务分配

## 貢獻

我們正在尋找開發者來改善 AgenticSeek！你可以在 Issues 查看未解決的問題或和我們討論更酷的新功能！

[![Star History Chart](https://api.star-history.com/svg?repos=Fosowl/agenticSeek&type=Date)](https://www.star-history.com/#Fosowl/agenticSeek&Date)

[Contribution guide](./docs/CONTRIBUTING.md)

## 维护者:

 > [Fosowl](https://github.com/Fosowl) | 巴黎时间 | （有时很忙）

 > [https://github.com/antoineVIVIES](https://github.com/antoineVIVIES) | 台北时间 | （经常很忙）

 > [steveh8758](https://github.com/steveh8758) | 台北时间 | （总是很忙）