from typing import Annotated, TypedDict
import io
from PIL import Image

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from src.agent.langgraph_tools import tool_search


class State(TypedDict):
    messages: Annotated[list, add_messages]


memory = MemorySaver()
tools = [tool_search]

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    """Creates a chatbot node for langgraph."""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_conditional_edges("chatbot", tools_condition, "tools")
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile(checkpointer=memory)

image = Image.open(io.BytesIO(graph.get_graph().draw_mermaid_png()))
image.show()

config = {"configurable": {"thread_id": "1"}}


def chat(user_input: str, history):
    result = graph.invoke(
        {"messages": [{"role": "user", "content": user_input}]}, config=config
    )
    return result["messages"][-1].content


import gradio as gr

gr.ChatInterface(chat).launch()
