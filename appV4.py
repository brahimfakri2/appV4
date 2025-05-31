import streamlit as st
import requests
import os

# ========================
# Page Configuration
# ========================
st.set_page_config(page_title="🦙 Local GPT Assistant", layout="wide")
st.title("🤖 Welcome to Your Local GPT Assistant")
st.markdown("Ask me anything — powered by Together.ai using open-source LLaMA models.")

# ========================
# Chat History Setup
# ========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ========================
# Styled Chat Bubbles
# ========================
st.markdown("""
<style>
.chat-bubble {
    padding: 0.75em 1em;
    border-radius: 1em;
    margin: 0.5em;
    max-width: 75%;
    word-wrap: break-word;
    font-size: 1rem;
    line-height: 1.4;
}
.user {
    background-color: #DCF8C6;
    margin-left: auto;
    text-align: right;
}
.bot {
    background-color: #F1F0F0;
    margin-right: auto;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# ========================
# Display Default Message
# ========================
if not st.session_state.chat_history:
    st.info("💡 You haven't started chatting yet. Ask your first question below!")

# ========================
# Show Chat History
# ========================
for sender, msg in st.session_state.chat_history:
    role = "user" if sender == "You" else "bot"
    label = "🧑 You" if sender == "You" else "🤖 Assistant"
    html = f'<div class="chat-bubble {role}"><b>{label}:</b> {msg}</div>'
    st.markdown(html, unsafe_allow_html=True)

# ========================
# Chat Input
# ========================
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", placeholder="Ask your assistant anything...")
    submit_button = st.form_submit_button(label="Send")

# ========================
# API Call to Together.ai
# ========================
if submit_button and user_input:
    st.session_state.chat_history.append(("You", user_input))

    # 🔐 Set your API key securely
    TOGETHER_API_KEY = "19dc8da67a1db369caae9e661346716d30e01875c4ac1a7c3d303af34e46152f"

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers=headers,
            json=data
        )

        if response.status_code != 200:
            result = f"[Error {response.status_code}] {response.text}"
            st.error(result)
        else:
            result = response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        result = f"[Request failed: {str(e)}]"
        st.error(result)

    st.session_state.chat_history.append(("Assistant", result))
    st.rerun()



