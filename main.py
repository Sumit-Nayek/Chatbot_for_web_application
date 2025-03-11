import streamlit as st
import requests

# OpenRouter API details
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Streamlit app title
st.title("🤖 AI Chatbot Using OpenRouter")

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How can I help you?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the request payload for OpenRouter
    payload = {
        "model": "deepseek/deepseek-r1-zero:free",  # Specify the model
        "messages": st.session_state.messages,
    }

    # Make the API request to OpenRouter
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        ai_response = response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        ai_response = "Sorry, I couldn't process your request. Please try again."

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)
