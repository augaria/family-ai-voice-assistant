# Family AI Voice Assistant Core

## Project Overview

**Family AI Voice Assistant Core** is a core library for home smart speakers based on large language models (LLM). This project provides a modular solution to support the development and deployment of home voice assistants. It offers a runtime framework, module interface definitions, and features like Tools Manager, logging, and Telemetry.

## Design

The project adopts a modular design aimed at achieving flexible functionality expansion and maintenance. By defining clear interfaces, each module can be developed independently and dynamically loaded and bound through configuration files. The core library coordinates the interaction of each module to ensure stable system operation.

## Main Architecture

### Module Overview

The `clients` directory defines abstract interfaces for various functional modules of the smart speaker:

- **AssistantClient**: Core control logic of the smart speaker, coordinating and invoking various modules.
- **WakerClient**: Wake-up detection interface for activating the voice assistant.
- **GreetingClient**: Responsible for generating greetings.
- **ListeningClient**: Listens to user voice input.
- **RecognitionClient**: Speech recognition interface that converts speech to text.
- **PlaySoundClient**: Plays audio files.
- **LLMClient**: Handles natural language generation tasks.
- **ChatSessionClient**: Manages conversation sessions with users, maintaining dialogue state.
- **SpeechClient**: Text-to-speech interface for voice output.
- **ClientManager**: Client manager responsible for registering and retrieving module instances.
- **HistoryStoreClient**: Manages the storage of conversation history.
- **FileStoreClient**: File storage interface for storing audio files to specified locations.

![alt text](../../screenshots/architecture.svg)

### Other Features

#### Logging

Provides a unified logging function for easy debugging and system monitoring.

#### Telemetry

Responsible for monitoring system performance and usage, collecting and analyzing key metrics.

#### Tools Engine

Manages and registers Tools Calling for LLM, supporting dynamic expansion and invocation.

#### Configs

Configuration management module that loads and parses configuration information from files, supporting dynamic configuration of clients and functional modules.

## Usage Guide

### Environment Preparation

1. **Python**: Ensure Python 3.9 or above is installed, or create a Python environment using conda.
2. **Install package**:

```bash
pip install family-ai-voice-assistant-core
```

### Example Code

You can directly use `family-ai-voice-assistant-impl`, which provides common implementations for each module, or customize your own implementation by referring to this project.

Steps:

1. Implement the following interfaces:
    - VoiceWaker (optional, built-in keyboard wake-up and interactive enter wake-up)
    - PlaySoundClient
    - RecognitionClient
    - LLMClient
    - SpeechClient

Example:

```python
from dataclasses import dataclass

from family_ai_voice_assistant.core.clients import VoiceWaker
from family_ai_voice_assistant.core.configs import ConfigManager
from family_ai_voice_assistant.core.configs import Config

@dataclass
class MyWakerConfig(Config):
    api_key: str = None

class MyWaker(VoiceWaker):

    def __init__(self):
        config = ConfigManager().get_instance(MyWakerConfig)
        if config is None:
            raise ValueError("MyWakerConfig is not set.")
        waker = WakerAPI(config.api_key)

    def check(self) -> bool:
        return waker.wake()
```

2. [optional] For each newly implemented client, define the corresponding config type. Refer to existing config types [/configs](family_ai_voice_assistant/core/configs/). Each config type corresponds to a section of the same name in config.yaml during parsing.

3. Provide a config.yaml file containing the necessary information for running each module and set the path for config.yaml.

config.yaml

```yaml
# Other sections

mywaker:
  api_key: xxxxxx

# Other sections
```

main.py

```python
from family_ai_voice_assistant.core import set_yaml_config_path

set_yaml_config_path("config.yaml")
```

4. Use ClientSelector to bind client types and config types. If no config is needed, map to None.

```python
from family_ai_voice_assistant.core.client_register import (
    ClientSelector
)

ClientSelector().map_play_sound_config(None, MyPlaySound)
ClientSelector().map_voice_waker_config(MyVoiceWakerConfig, MyVoiceWaker)
ClientSelector().map_recognition_config(MyRecognitionConfig, MyRecognition) 
ClientSelector().map_llm_config(MyLLMConfig, MyLLM)
ClientSelector().map_speech_config(MySpeechConfig, MySpeech)
```

5. Use ClientRegistor to identify which clients need to be instantiated and registered to ClientManager by reading config.yaml.

```python
from family_ai_voice_assistant.core.client_register import (
    ClientRegistor,
    ClientSelector
)

ClientRegistor().register_clients_from_selector()
```

6. Run the assistant. The assistant acts as an orchestrator, retrieving each module's instance from ClientManager at runtime and invoking the corresponding interfaces.

```python
assistant = ClientRegistor().get_assistant()
assistant.run()
```

Below is a simple startup example:

main.py

```python
import argparse
from family_ai_voice_assistant.core import set_yaml_config_path
from family_ai_voice_assistant.core.client_register import (
    ClientRegistor,
    ClientSelector
)

parser = argparse.ArgumentParser(description="Start the Family AI Assistant.")
parser.add_argument('config', type=str, help='the config file path')
args = parser.parse_args()

set_yaml_config_path(args.config)

def map_configs_to_clients():
    ClientSelector().map_play_sound_config(None, MyPlaySound)
    ClientSelector().map_voice_waker_config(MyVoiceWakerConfig, MyVoiceWaker)
    ClientSelector().map_recognition_config(MyRecognitionConfig, MyRecognition) 
    ClientSelector().map_llm_config(MyLLMConfig, MyLLM)
    ClientSelector().map_speech_config(MySpeechConfig, MySpeech)

def main():
    map_configs_to_clients()
    ClientRegistor().register_clients_from_selector()
    assistant = ClientRegistor().get_assistant()
    assistant.run()

if __name__ == "__main__":
    main()
```

Execute:

```bash
python main.py <path to config.yaml>
```

For a real example, refer to the entry code of `family-ai-voice-assistant-impl` [basic_entry.py](../family-ai-voice-assistant-impl/family_ai_voice_assistant/basic_entry.py).

## Other Features

### File Server

The command `family_ai_voice_assistant_file_server` can start a service to receive uploaded files, suitable for deployment on an internal network storage server such as NAS, to receive and store audio files. It can be used with the built-in RestFileStore.

Example:

NAS side, IP: 192.168.1.200

```bash
pip install family-ai-voice-assistant-core

family_ai_voice_assistant_file_server --root /home/username/data/assistant --port 5100 &
```

Assistant side

config.yaml

```yaml
filestore:
  destination: http://192.168.1.200:5100/files/upload
```

### Assistant API

Two implementations of Assistant are built-in. The default is BasicAssistant. AssistantWithApi extends BasicAssistant by providing an API that allows chatting with the Assistant, making it easy to embed the Assistant into other applications.

Example:

Assistant side, IP: 192.168.1.240

config.yaml

```yaml
assistantapi:
  port: 10000 # any available port
```

On the client side, call this API according to the protocol: [chat_request.py](family_ai_voice_assistant/core/contracts/chat_request.py),

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"question": "Why is the sky blue?", "speak_answer": false}'  \
     http://192.168.1.240:10000/chat
```

Or use the built-in interactive command-line client:

```bash
pip install family-ai-voice-assistant-core

family_ai_voice_assistant_console --host 192.168.1.240 --port 10000 [--speak]
```
