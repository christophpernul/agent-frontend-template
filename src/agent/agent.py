"""
AI agent that processes user requests and sends meaningful responses to the user.
"""

from dataclasses import dataclass
from agents import Agent, Runner, SQLiteSession

from src.constants import AGENT_NAME
from src.agent.prompts import SYSTEM_PROMPT


@dataclass
class AgentResponse:
    """Represents the expected response from the agent."""
    answer: str



class AIAgent:
    """AI Agent class."""

    def __init__(self, trace_id: str, llm_name: str):
        self.agent = Agent(
            name=AGENT_NAME,
            model=llm_name,
            instructions=self._get_system_message(),
            tools=[],
        )
        self.session = SQLiteSession(trace_id)

    @staticmethod
    def _get_system_message() -> str:
        """Get the system message for the AI agent."""
        return SYSTEM_PROMPT

    async def process_request(self, user_message: str) -> str:
        """
        Process a user's request and return a response.

        Args:
            user_message: The user's request

        Returns:
            Response from the AI agent
        """
        # Send the message directly to the agent
        response = await Runner.run(self.agent,
                                    user_message,
                                    session=self.session,
                                    )
        return response.final_output
