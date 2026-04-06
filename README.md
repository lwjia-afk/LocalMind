# LocalMind

A lightweight local AI chat framework built on top of [Ollama](https://ollama.com). LocalMind provides a clean abstraction layer for interacting with locally-hosted LLMs, with conversation history management and structured logging.

## Architecture

```
LocalMind/
├── LLM/
│   ├── LLMClient/
│   │   ├── LLMClientInterface.py   # Abstract base class for LLM clients
│   │   └── OllamaClient.py         # Ollama API implementation
│   └── LLMResult.py                # Response data class
├── models/
│   ├── Message.py                  # Chat message data class
│   └── Role.py                     # Role enum (user/system/assistant/tool)
├── LLMChatManager.py               # Conversation manager with history
├── ConfigManager.py                # YAML config loader
├── LogManager.py                   # Logging setup (console + rotating file)
├── config.yaml                     # Configuration file
└── hello_llm.py                    # Entry point / usage example
```

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally
- A model pulled in Ollama (default: `qwen2.5:7b`)

## Setup

**1. Install dependencies**

```bash
pip install requests pyyaml
```

**2. Pull a model in Ollama**

```bash
ollama pull qwen2.5:7b
```

**3. Configure `config.yaml`**

```yaml
llm:
  ollama:
    model: qwen2.5:7b
    temperature: 0.7
    generate_url: http://localhost:11434/api/chat

logging:
  level: INFO
  file: logs/localmind.log
```

**4. Run**

```bash
python hello_llm.py
```

## Usage

```python
from LLM import OllamaClient
from LLMChatManager import LLMChatManager
from LogManager import LogManager
from ConfigManager import ConfigManager

ConfigManager.load_config()
LogManager.init()

llm = OllamaClient()
chat = LLMChatManager(llm, system_prompt="You are a helpful assistant.")

print(chat.ask("Hello!"))
print(chat.ask("Tell me more."))  # conversation history is maintained
```

## Extending with a Custom LLM Client

Implement `LLMClientInterface` to add support for other LLM backends:

```python
from LLM.LLMClient.LLMClientInterface import LLMClientInterface
from LLM.LLMResult import LLMResult

class MyLLMClient(LLMClientInterface):
    def generate(self, messages: list) -> LLMResult:
        # call your LLM API here
        return LLMResult(text="response", raw={})
```

## Windows Note

If you see `UnicodeEncodeError` with Chinese or non-ASCII characters, add the following to your `.vscode/launch.json`:

```json
"env": {
    "PYTHONUTF8": "1"
}
```
