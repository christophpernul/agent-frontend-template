from typing import Annotated, TypedDict, Any
import io
from PIL import Image
import asyncio

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.agent.langgraph_tools import playwright_tools, other_tools


class State(TypedDict):
    """Langgraph state object."""

    messages: Annotated[list[Any], add_messages]
    # additional_state_parameter: str


class AIAgent:
    def __init__(self, trace_id: str):
        self.tools = None
        self.llm_with_tools = None
        self.graph = None
        self.agent_id = trace_id
        self.memory = MemorySaver()
        self.browser = None
        self.playwright = None

    async def setup(self):
        self.tools, self.browser, self.playwright = await playwright_tools()
        self.tools += await other_tools()
        worker_llm = ChatOpenAI(model="gpt-4o-mini")
        self.llm_with_tools = worker_llm.bind_tools(self.tools)
        await self.build_graph()

    async def build_graph(self):
        # Set up Graph Builder with State
        graph_builder = StateGraph(State)

        # Add nodes
        graph_builder.add_node("worker", self.worker)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        # Add edges
        graph_builder.add_conditional_edges("worker", tools_condition, "tools")
        graph_builder.add_edge("tools", "worker")
        graph_builder.add_edge(START, "worker")

        # Compile the graph
        self.graph = graph_builder.compile(checkpointer=self.memory)

    def show_graph(self):
        image = Image.open(io.BytesIO(self.graph.get_graph().draw_mermaid_png()))
        image.show()

    async def run_superstep(self, message, history):
        config = {"configurable": {"thread_id": self.agent_id}}

        state = {
            "messages": message,
            # "additional_state_parameter": "something",
        }
        result = await self.graph.ainvoke(state, config=config)
        user = {"role": "user", "content": message}
        reply = {"role": "assistant", "content": result["messages"][-1].content}
        # return history + [user, reply]
        return result["messages"][-1].content

    def cleanup(self):
        if self.browser:
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.browser.close())
                if self.playwright:
                    loop.create_task(self.playwright.stop())
            except RuntimeError:
                # If no loop is running, do a direct run
                asyncio.run(self.browser.close())
                if self.playwright:
                    asyncio.run(self.playwright.stop())

    def worker(self, state: State) -> dict[str, Any]:
        """Creates a chatbot node for langgraph."""
        # system_message = f"""Here you can dynamically add sth from state, {state['additional_state_parameter']}."""
        #
        # # Add in the system message
        # found_system_message = False
        messages = state["messages"]
        # for message in messages:
        #     if isinstance(message, SystemMessage):
        #         message.content = system_message
        #         found_system_message = True
        #
        # if not found_system_message:
        #     messages = [SystemMessage(content=system_message)] + messages

        response = self.llm_with_tools.invoke(messages)
        return {
            "messages": [response],
        }

    # def worker_router(self, state: State) -> str:
    #     """Special router to decide between tools or evaluator calls."""
    #     last_message = state["messages"][-1]
    #
    #     if hasattr(last_message, "tool_calls") and last_message.tool_calls:
    #         return "tools"
    #     else:
    #         return "evaluator"

    def format_conversation(self, messages: list[Any]) -> str:
        conversation = "Conversation history:\n\n"
        for message in messages:
            if isinstance(message, HumanMessage):
                conversation += f"User: {message.content}\n"
            elif isinstance(message, AIMessage):
                text = message.content or "[Tools use]"
                conversation += f"Assistant: {text}\n"
        return conversation
