"""
AI agent that processes user requests and sends meaningful responses to the user.
"""

import asyncio
from dataclasses import dataclass
from agents import Agent, trace, Runner

from src.constants import AGENT_NAME
from src.prompts import SYSTEM_PROMPT


@dataclass
class AgentResponse:
    """Represents the expected response from the agent."""
    answer: str



class AIAgent:
    """AI Agent class."""

    def __init__(self, openai_api_key: str):
        self.agent = Agent(
            name=AGENT_NAME,
            model="gpt-4o-mini",
            instructions=self._get_system_message()
        )

    def _get_system_message(self) -> str:
        """Get the system message for the AI agent."""
        return SYSTEM_PROMPT

    async def _process_request(self, user_message: str) -> str:
        """
        Process a user's request and return a response.

        Args:
            user_message: The user's request

        Returns:
            Response from the AI agent
        """
        # Send the message directly to the agent
        with trace(AGENT_NAME):
            response = await Runner.run(self.agent, user_message)
        return response.final_output

    def chat_with_agent(self, message: str, history: list[dict]) -> tuple[str, list[dict]]:
        """
        Process a chat message and return the agent's response.

        Args:
            message: User's message
            history: Chat history in messages format

        Returns:
            Tuple of (response, updated_history)
        """
        if not message.strip():
            return "", history

        # Process the message with the agent
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            response = loop.run_until_complete(self._process_request(message))
        finally:
            loop.close()

        # Update history with messages format
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})

        return "", history