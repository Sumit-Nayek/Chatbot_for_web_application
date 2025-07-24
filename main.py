import streamlit as st
from openai import OpenAI

# Initialize OpenAI client for OpenRouter
OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", None)
if not OPENROUTER_API_KEY:
    st.error("API key not found. Please set OPENROUTER_API_KEY in Streamlit secrets.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

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

## Mannual button to clear the chat history
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.success("Chat history cleared!")
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

    # Prepare messages for OpenRouter, including system prompt
    messages = st.session_state.messages + [
        {
            "role": "system",
            "content": "You are a helpful health advisor providing guidance on COVID-19. Respond in a concise, conversational tone.",
        }
    ]

    # Make the API request to OpenRouter using OpenAI client
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost:8501",  # Replace with your site URL
                "X-Title": "Medical Assistance App",      # Replace with your app name
            },
            model="deepseek/deepseek-r1:free",  # Use the model you want
            messages=messages,
        )
        ai_response = completion.choices[0].message.content
    except Exception as e:
        st.error(f"API request failed: {str(e)}")
        ai_response = "Sorry, I couldn't process your request. Please try again."

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    st.markdown(
        f'<div class="chat-container"><div class="ai-message">{ai_response}</div></div>',
        unsafe_allow_html=True,
    )
