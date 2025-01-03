import requests
from typing import List, Dict, Union

from serpapi.google_search import GoogleSearch
from bs4 import BeautifulSoup

from family_ai_voice_assistant.core.configs import ConfigManager
from family_ai_voice_assistant.core.tools_engine import (
    tool_function
)
from family_ai_voice_assistant.core.logging import Loggers

from ..configs.bulitin_tools_config import BuiltInToolsConfig


def config():
    return ConfigManager().get_instance(BuiltInToolsConfig)


@tool_function
def google_search(query: str) -> Union[List[Dict], str]:
    """
    Use Google API to search for specified keywords.

    :param query: Search keywords
    """
    api_key = config().google_search_api_key
    if not api_key or api_key == "":
        error_msg = "Google API key not found"
        Loggers().tool.error(error_msg)
        return error_msg

    params = {
        "engine": "google",
        "q": query,
        "google_domain": "google.com",
        "num": 10,
        "start": 0,
        "safe": "active",
        "api_key": api_key
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]

        return parse_response(organic_results, "title", "link", "snippet")
    except Exception as ex:
        error_msg = f"search tool failed: {ex}"
        Loggers().tool.error(error_msg)
        return error_msg


@tool_function
def bing_news_search(query: str) -> Union[List[Dict], str]:
    """
    Use Bing API to search for news with specified keywords.

    :param query: Search keywords
    """
    return bing_search_base(
        f"{config().bing_search_endpoint}/news/search",
        query,
        "description",
        10
    )


@tool_function
def bing_top_news() -> Union[List[Dict], str]:
    """
    Use Bing API to get top news.
    """
    return bing_search_base(
        f"{config().bing_search_endpoint}/news",
        None,
        "description",
        10
    )


@tool_function
def bing_search(query: str) -> Union[List[Dict], str]:
    """
    Use Bing API to search for specified keywords.

    :param query: Search keywords
    """
    return bing_search_base(
        f"{config().bing_search_endpoint}/search",
        query,
        "snippet",
        10
    )


def bing_search_base(
    endpoint: str,
    query: str,
    snippet_key: str,
    count: int = 10
) -> Union[List[Dict], str]:

    api_key = config().bing_subscription_key
    if not api_key or api_key == "":
        error_msg = "Bing API key not found"
        Loggers().tool.error(error_msg)
        return error_msg

    params = {
        'mkt': 'zh-CN',
        'count': count,
        'offset': 0,
        'safeSearch': 'Strict',
        'setLang': 'zh-hans'
    }
    if query is not None:
        params['q'] = query
    headers = {
        'Ocp-Apim-Subscription-Key': api_key
    }

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        json_response = response.json()
        if 'webPages' in json_response:
            items = json_response['webPages']['value']
        else:
            items = json_response['value']
        return parse_response(items, "name", "url", snippet_key)
    except Exception as ex:
        error_msg = f"search tool failed: {ex}"
        Loggers().tool.error(error_msg)
        return error_msg


def fetch_webpage_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p')
        content = ' '.join(p.get_text() for p in paragraphs)
        return content
    except requests.RequestException as e:
        Loggers().tool.warning(f"search tool failed to fetch {url}: {e}")
        return None


def parse_response(
    items: List[Dict],
    title_key: str,
    link_key: str,
    snippet_key: str,
    include_web_content: bool = False
) -> Union[List[Dict], str]:
    if len(items) > 0:
        results = []
        for item in items:
            record = {
                "title": item.get(title_key, ""),
                "link": item.get(link_key, ""),
                "snippet": item.get(snippet_key, "")
            }
            if include_web_content:
                record["content"] = fetch_webpage_content(record["link"])
            results.append(record)
        return results
    else:
        return "search failed"
