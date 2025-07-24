import streamlit as st
import requests

# OpenRouter API details
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"

# Custom CSS for chat interface
st.markdown(
    """
    <style>
    /* User message styling */
    .user-message {
        background-color: #0078D4;
        color: white;
        border-radius: 15px 15px 0 15px;
        padding: 10px;
        margin: 5px 0;
        max-width: 70%;
        margin-left: auto;
    }

    /* AI message styling */
    .ai-message {
        background-color: #F1F1F1;
        color: black;
        border-radius: 15px 15px 15px 0;
        padding: 10px;
        margin: 5px 0;
        max-width: 70%;
        margin-right: auto;
    }

    /* Chat container styling */
    .chat-container {
        display: flex;
        flex-direction: column;
        padding: 10px;
    }

    /* Streamlit chat input styling */
    .stChatInput {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: white;
        padding: 10px;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# Streamlit app title
st.title("🤖 AI For Your Medical Assistance")

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="chat-container"><div class="user-message">{message["content"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="chat-container"><div class="ai-message">{message["content"]}</div></div>',
            unsafe_allow_html=True,
        )

# Chat input
if prompt := st.chat_input("How can I help you?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(
        f'<div class="chat-container"><div class="user-message">{prompt}</div></div>',
        unsafe_allow_html=True,
    )

    # Prepare the request payload for OpenRouter
    payload = {
        "model": "openai/gpt-3.5-turbo",
        # "model":"deepseek/deepseek-r1-zero",# Specify the model
        "messages": st.session_state.messages + [
            {
                "role": "system",
                "content": "You are a helpful health advisor providing guidance on COVID-19. Respond in a concise, conversational tone.",
            }
        ],
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
    st.markdown(
        f'<div class="chat-container"><div class="ai-message">{ai_response}</div></div>',
        unsafe_allow_html=True,
    )
