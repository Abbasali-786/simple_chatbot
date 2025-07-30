import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq client
client = Groq(api_key=api_key)

# Streamlit UI
st.set_page_config(page_title="Groq Chatbot", layout="centered")
st.title("🤖 Simple chat bot ")

# Initialize session state to store messages
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display previous messages
for message in st.session_state.chat_history[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Show user message
    st.chat_message("user").markdown(prompt)

    # Append user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Make API call
    with st.spinner("Thinking..."):
        chat_completion = client.chat.completions.create(
            messages=st.session_state.chat_history,
            model="gemma2-9b-it",
        )
        response = chat_completion.choices[0].message.content

    # Show assistant message
    st.chat_message("assistant").markdown(response)

    # Add response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
