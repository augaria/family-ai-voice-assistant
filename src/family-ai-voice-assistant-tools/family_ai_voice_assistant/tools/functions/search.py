import requests
from typing import List, Dict

from serpapi.google_search import GoogleSearch
from bs4 import BeautifulSoup

from family_ai_voice_assistant.core.config import ConfigManager
from family_ai_voice_assistant.core.tools_engine import (
    tool_function
)
from family_ai_voice_assistant.core.logging import Loggers

from ..config.bulitin_tools_config import BuiltInFunctionsConfig


def config():
    return ConfigManager().get_instance(BuiltInFunctionsConfig)


@tool_function
def google_search(query: str):
    """
    Use Google API to search for specified keywords.

    :param query: Search keywords
    """

    params = {
        "engine": "google",
        "q": query,
        "google_domain": "google.com",
        "num": 10,
        "start": 0,
        "safe": "active",
        "api_key": config().google_search_api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]

    return parse_response(organic_results, "title", "link", 5)


@tool_function
def bing_news_search(query: str):
    """
    Use Bing API to search for news with specified keywords.

    :param query: Search keywords
    """
    return bing_search_base(
        f"{config().bing_search_endpoint}/news/search",
        query,
        5
    )


@tool_function
def bing_top_news():
    """
    Use Bing API to get top news.
    """
    return bing_search_base(
        f"{config().bing_search_endpoint}/news",
        None,
        10
    )


@tool_function
def bing_search(query: str):
    """
    Use Bing API to search for specified keywords.

    :param query: Search keywords
    """
    return bing_search_base(
        f"{config().bing_search_endpoint}/search",
        query,
        5
    )


def bing_search_base(endpoint: str, query: str, count: int = 5):

    params = {
        'mkt': 'zh-CN',
        'count': 2 * count,
        'offset': 0
    }
    if query is not None:
        params['q'] = query
    headers = {
        'Ocp-Apim-Subscription-Key': config().bing_subscription_key
    }

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        json_response = response.json()
        if 'webPages' in json_response:
            items = json_response['webPages']['value']
        else:
            items = json_response['value']
    except Exception as ex:
        raise ex

    return parse_response(items, "name", "url", count)


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
    count: int = 5
) -> Dict:
    if len(items) > 0:
        results = []
        valid_count = 0
        for item in items:
            title = item.get(title_key, "")
            link = item.get(link_key, "")
            content = fetch_webpage_content(link)
            if content is not None:
                results.append(
                    f"Title: {title}\nURL: {link}\nContent: {content}")
                valid_count += 1
                if valid_count == count:
                    break
        return {"result": "\n\n".join(results)}
    else:
        return {"result": "search failed"}
