"""
Chainlit chat interface that wraps the AI Agent into a Chainlit chat functionality.
"""

from agents import gen_trace_id, trace

from src.agent.openai_agent_sdk import AIAgent
from src.agent.langgraph_agent import AIAgent as AIAgentLangGraph
from src.constants import APPLICATION_NAME


class ChatInterface:
    """Chat interface for a Chainlit App with an AI Agent."""

    def __init__(
        self,
        llm_api_key: str,
        llm_name: str,
        llm_api_base_url: str = None,
    ):
        self.trace_id = gen_trace_id()
        # self.agent = AIAgent(
        #     trace_id=self.trace_id,
        #     llm_api_key=llm_api_key,
        #     llm_name=llm_name,
        #     llm_api_base_url=llm_api_base_url,
        # )
        self.agent = AIAgentLangGraph(self.trace_id)

    async def setup(self):
        """Langgraph only!"""
        await self.agent.setup()

    async def run(
        self, message: str, history: list[dict] = None
    ) -> tuple[str, list[dict]]:
        """
        Process a chat message and return the agent's response.

        Args:
            message: User's message
            history: Chat history in messages format

        Returns:
            Tuple of (response, updated_history)
        """
        if history is None:
            history = []

        if not message.strip():
            return "", history

        try:
            with trace(APPLICATION_NAME, trace_id=self.trace_id):
                # TODO: OpenAI specific!
                print(
                    f"View trace: https://platform.openai.com/traces/trace?trace_id={self.trace_id}"
                )
                # yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
                # response = await self.agent.process_request(message)
                response = await self.agent.run_superstep(
                    message, history
                )  # langgraph only!
        except Exception as e:
            print(f"Error processing request: {e}")
            response = "I'm sorry, I encountered an error processing your request. Please try again."

        # Update history with messages format
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})

        return response, history
