from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langfuse.langchain import CallbackHandler
import os

# Define the state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define the LLM (Switching based on environment)
llm = ChatOllama(
    model="gemma:2b",
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)

# Define the node
def assistant(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# Build the Graph
builder = StateGraph(State)
builder.add_node("assistant", assistant)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)
graph = builder.compile()

# Observability Handler
langfuse_handler = CallbackHandler()