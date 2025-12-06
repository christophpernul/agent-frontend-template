"""
AI agent that processes user requests and sends meaningful responses to the user.
"""

from openai import AsyncOpenAI
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel

from src.constants import AGENT_NAME
from src.agent.prompts import SYSTEM_PROMPT


class AIAgent:
    """AI Agent class."""

    def __init__(
        self,
        trace_id: str,
        llm_api_key: str,
        llm_name: str,
        llm_api_base_url: str = None,
    ):
        if llm_name.startswith("gpt"):
            model = llm_name
        elif llm_name.startswith("gemini"):
            gemini_client = AsyncOpenAI(base_url=llm_api_base_url, api_key=llm_api_key)
            model = OpenAIChatCompletionsModel(
                model=llm_name, openai_client=gemini_client
            )
        else:
            raise RuntimeError(
                f"Model not known, make sure it is either an OpenAI or a Gemini model, got: {llm_name}"
            )

        self.agent = Agent(
            name=AGENT_NAME,
            model=model,
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
        response = await Runner.run(
            self.agent,
            user_message,
            session=self.session,
        )
        return response.final_output
