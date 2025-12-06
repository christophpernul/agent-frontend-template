import os
import requests

from agents import function_tool


@function_tool
def push_notification_tool(message: str):
    """Use this tool when you want to send a push notification"""
    pushover_token = os.getenv("PUSHOVER_TOKEN")
    pushover_user = os.getenv("PUSHOVER_USER")
    pushover_url = "https://api.pushover.net/1/messages.json"

    print(f"Push: {message}")
    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    requests.post(pushover_url, data=payload)
    return "success"
