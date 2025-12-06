import os
import requests

from langchain.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper


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
