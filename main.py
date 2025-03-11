import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit app title
st.title("🤖 AI Chatbot Using LLM")

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

    # Generate AI response
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" if GPT-4 is not available
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        ai_response = response.choices[0].message.content
        st.markdown(ai_response)

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
