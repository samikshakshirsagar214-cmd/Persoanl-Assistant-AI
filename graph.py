from langgraph.graph import StateGraph, MessagesState, START, END
from llm import get_llm

# 1. Get the LLM from shared llm.py
llm = get_llm()

# 2. Define the node function
def assistant(state: MessagesState):
    """The core logic that processes messages."""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 3. Build the Graph
workflow = StateGraph(MessagesState) # type: ignore

# Add the node to the graph
workflow.add_node("agent", assistant)

# --- THE CRITICAL FIXES ---
# Tell the graph where to begin
workflow.add_edge(START, "agent")

# Tell the graph where to stop
workflow.add_edge("agent", END)
# ---------------------------

# 4. Compile the graph into an executable 'app'
# This matches the name 'app' we used in ui.py
app = workflow.compile()

def get_graph_image():
    """Returns a PNG byte stream of the graph visualization."""
    try:
        # We use 'app' here to match the compiled variable
        return app.get_graph().draw_mermaid_png() # type: ignore
    except Exception as e:
        print(f"Graph visualization error: {e}")
        return None