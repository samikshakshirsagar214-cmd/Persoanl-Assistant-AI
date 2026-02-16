import streamlit as st
import os

from graph import app, get_graph_image 
from langfuse.langchain import CallbackHandler

# Initialize Langfuse - reads from environment variables
# Required: LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST
langfuse_handler = CallbackHandler()

st.set_page_config(page_title="AI Assistant", layout="wide")

#  Graph Visualization
with st.sidebar:
    st.subheader("Agent Architecture")
    # This calls the function from graph.py
    st.image(get_graph_image(), caption="LangGraph Logic Flow")

st.title("🤖 Personal Assistant (Gemma:2b)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # Invoke with callbacks - traces will be sent to Langfuse
        response = app.invoke(
            {"messages": [("user", prompt)]},
            config={"callbacks": [langfuse_handler]}
        )
        
        answer = response["messages"][-1].content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        print(f"Error invoking app: {e}")