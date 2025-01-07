# Family AI Voice Assistant Tools

Family AI Voice Assistant Tools is a package that provides built-in tools for the Family AI Voice Assistant, designed to interface with large language models for tool calling. This package offers functionalities such as search, retrieving current time, weather information, and collecting new vocabulary words in both English and Chinese for educational purposes. Note that MongoDB support is required for vocabulary collection. Also, serve as a reference for customized toolkits.

## Requirements

- Python 3.9 or higher
- [Optional] MongoDB for vocabulary features

## Tool Definition

To define a tool, follow these steps:

### 1. Tool Decorator: `@tool_function`

The `@tool_function` decorator is essential for registering a function as a tool. It signals the tool manager to recognize the function as a tool that can be called by LLM.

```python
from family_ai_voice_assistant.core.tools_engine import (
    tool_function
)
```

### 2. Function Definition

Define your tool as a standard Python function. Ensure that the function name is descriptive of its purpose. Use Python type annotations for parameters and return values, as the tool manager uses these to determine parameter types.

### 3. Docstring

The docstring of the tool is crucial. It serves multiple purposes:
- **Description**: Begin with a brief description of what the tool does.
- **Parameters**: Describe each parameter. The tool manager uses this to understand what each parameter does. Use the format `:param <name>: <description>`.

### Example

Here’s an example of how to define a tool:

```python
@tool_function
def example_tool(param1: str, param2: int) -> Dict:
    """
    Perform an example operation.

    :param param1: Description of the first parameter.
    :param param2: Description of the second parameter.
    """

    # Tool implementation

    return {"result": "success"}
```




## Builtin Tools

Introduction to all Builtin Tools. Parameters will be automatically filled in by the LLM based on their descriptions. The Config section outlines the configuration needed to use the Tool.

Define `builtintools` section in config.yaml, according to [BuiltInToolsConfig](family_ai_voice_assistant/tools/configs/bulitin_tools_config.py)

```yaml
# builtin tools
builtintools:
  mongo_connection_str: mongodb://localhost:27017/
  mongo_database: xxxxxx
  english_word_list_collection: english_word_list
  chinese_phrase_list_collection: chinese_phrase_list
  memo_list_collection: memo_list
  google_search_api_key: xxxxxx
  # bing_subscription_key: xxxxxx
  # bing_search_endpoint: https://api.bing.microsoft.com/v7.0
  amap_api_key: xxxxxx
  default_city_adcode: 110000 # Beijing
```


### core.py

#### 1. `get_time_and_timezone`
- **Functionality**: Retrieves the current time and timezone.
- **Parameters**: None
- **Returns**: `Dict[str, str]` containing `time` and `timezone`.

#### 2. `switch_language`
- **Functionality**: Switches the conversation language.
- **Parameters**: 
  - `language: Language` (optional) - `CHS` for Chinese, `EN` for English.
- **Returns**: None

#### 3. `exit_program`
- **Functionality**: Exits the program after the last message.
- **Parameters**: None
- **Returns**: None

---

### executors.py

#### 1. `execute_bash_script`
- **Functionality**: Executes a Linux bash shell script.
- **Parameters**: 
  - `script: str` - The bash script content.
- **Returns**: `str` - Output of the script or error message.

#### 2. `execute_python_code`
- **Functionality**: Executes Python code using `exec()`.
- **Parameters**: 
  - `code: str` - The Python code content.
- **Returns**: `str` - Local variables after execution or error message.

---

### local_apis.py

#### 1. `add_to_english_word_list`
- **Functionality**: Adds a new English word to the vocabulary list.
- **Parameters**: 
  - `english_word: str`
  - `part_of_speech: str`
  - `chinese_explanation: str`
  - `example_sentence: str`
- **Returns**: `str` - Result of addition.
- **Config**:
  - mongo_connection_str
  - mongo_database
  - english_word_list_collection

#### 2. `review_english_words`
- **Functionality**: Retrieves English words for review. Select the words that hasn't been reviewed for the longest time.
- **Parameters**: 
  - `count: int` (default 3) - Number of words to review.
- **Returns**: `List[Dict[str, Any]]`
- **Config**:
  - mongo_connection_str
  - mongo_database
  - english_word_list_collection

#### 3. `count_english_word_list`
- **Functionality**: Counts the English words in the list.
- **Parameters**: None
- **Returns**: `int`
- **Config**:
  - mongo_connection_str
  - mongo_database
  - english_word_list_collection

#### 4. `add_to_chinese_phrase_list`
- **Functionality**: Adds a new Chinese phrase to the list.
- **Parameters**: 
  - `phrase: str`
  - `pinyin: str`
  - `explanation: str`
  - `example_sentence: str`
  - `source: str` (optional)
- **Returns**: `str` - Result of addition.
- **Config**:
  - mongo_connection_str
  - mongo_database
  - chinese_phrase_list_collection

#### 5. `review_chinese_phrases`
- **Functionality**: Retrieves Chinese phrases for review. Select the phrases that hasn't been reviewed for the longest time.
- **Parameters**: 
  - `count: int` (default 3) - Number of phrases to review.
- **Returns**: `List[Dict[str, Any]]`
- **Config**:
  - mongo_connection_str
  - mongo_database
  - chinese_phrase_list_collection

#### 6. `count_chinese_phrase_list`
- **Functionality**: Counts the Chinese phrases in the list.
- **Parameters**: None
- **Returns**: `int`
- **Config**:
  - mongo_connection_str
  - mongo_database
  - chinese_phrase_list_collection

#### 7. `add_to_memo`
- **Functionality**: Adds a memo to the list.
- **Parameters**: 
  - `date: str` - Format `%Y-%m-%d`
  - `content: str`
  - `hour: str` (optional)
- **Returns**: `str` - Result of addition.
- **Config**:
  - mongo_connection_str
  - mongo_database
  - memo_list_collection

#### 8. `get_memos`
- **Functionality**: Retrieves memos for a specific date.
- **Parameters**: 
  - `date: str` - Format `%Y-%m-%d`
- **Returns**: `List[Dict[str, Any]]`
- **Config**:
  - mongo_connection_str
  - mongo_database
  - memo_list_collection

#### 9. `count_down_timer`
- **Functionality**: Starts a countdown timer.
- **Parameters**: 
  - `seconds: int`
  - `message: str` (optional)
- **Returns**: `Any`

#### 10. `alarm_timer`
- **Functionality**: Sets an alarm for a specific time.
- **Parameters**: 
  - `target_time_str: str` - Format `%H:%M:%S`
  - `message: str` (optional)
- **Returns**: `Any`

---

### web_apis.py

#### 1. `get_weather_info`
- **Functionality**: Retrieves weather information using Amap API.
- **Parameters**: 
  - `city_adcode: str` (optional)
  - `extensions: str` (default `'base'`)
- **Returns**: `Union[Dict, str]`
- **Config**:
  - amap_api_key
  - default_city_adcode

---

### search.py

#### 1. `google_search`
- **Functionality**: Performs a Google search.
- **Parameters**: 
  - `query: str`
- **Returns**: `Union[List[Dict], str]`
- **Config**:
  - google_search_api_key

#### 2. `bing_news_search`
- **Functionality**: Searches for news using Bing API.
- **Parameters**: 
  - `query: str`
- **Returns**: `Union[List[Dict], str]`
- **Config**:
  - bing_subscription_key
  - bing_search_endpoint

#### 3. `bing_top_news`
- **Functionality**: Retrieves top news using Bing API.
- **Parameters**: None
- **Returns**: `Union[List[Dict], str]`
- **Config**:
  - bing_subscription_key
  - bing_search_endpoint

#### 4. `bing_search`
- **Functionality**: Performs a Bing search.
- **Parameters**: 
  - `query: str`
- **Returns**: `Union[List[Dict], str]`
- **Config**:
  - bing_subscription_key
  - bing_search_endpoint

---

### combination_tools.py

#### 1. `daily_report`
- **Functionality**: Generates a daily report, including date, weather, memos, english words to review, chinese phrases to review, famous saying, top news.
- **Parameters**: 
  - `famous_saying: str`
- **Returns**: `Union[Dict, str]`
- **Config**:
  - mongo_connection_str
  - mongo_database
  - english_word_list_collection
  - chinese_phrase_list_collection
  - memo_list_collection
  - amap_api_key
  - default_city_adcode
  - google_search_api_key
  - bing_subscription_key
  - bing_search_endpoint

--- 
