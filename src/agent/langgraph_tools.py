import os
import requests

from playwright.async_api import async_playwright
from langchain.tools import tool
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.agent_toolkits import (
    PlayWrightBrowserToolkit,
    FileManagementToolkit,
)

# from langchain_experimental.tools import PythonREPLTool


@tool("search")
def tool_search(query: str) -> str:
    """Useful for when you need more information from an online search."""
    serper = GoogleSerperAPIWrapper()
    return serper.run(query)


@tool("send_push_notification")
def tool_push_notification(message: str):
    """Use this tool when you want to send a push notification"""
    pushover_token = os.getenv("PUSHOVER_TOKEN")
    pushover_user = os.getenv("PUSHOVER_USER")
    pushover_url = "https://api.pushover.net/1/messages.json"

    print(f"Push: {message}")
    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    requests.post(pushover_url, data=payload)
    return "success"


async def playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright


def get_file_tools():
    toolkit = FileManagementToolkit(root_dir="sandbox")
    return toolkit.get_tools()


async def other_tools():
    file_tools = get_file_tools()

    wikipedia = WikipediaAPIWrapper()
    tool_wiki = WikipediaQueryRun(api_wrapper=wikipedia)

    # python_repl = PythonREPLTool()

    return file_tools + [tool_push_notification, tool_search, tool_wiki]
