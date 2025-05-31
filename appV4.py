import streamlit as st
import requests


# ========================
# Welcome & Page Settings
# ========================
st.set_page_config(page_title="🦙 Your Local GPT Assistant", layout="wide")

st.title("🤖 Welcome to Your Local GPT Assistant")
st.markdown("Ask me anything — I'm running locally with no internet needed!")

# ========================
# Session State Setup
# ========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ========================

# ========================
# Chat Bubble Styling
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
# Display Chat History
# ========================
if not st.session_state.chat_history:
    st.info("💡 You haven't started chatting yet. Ask your first question below!")

for sender, msg in st.session_state.chat_history:
    css_class = "user" if sender == "You" else "bot"
    label = "🧑 You" if sender == "You" else "🤖 Assistant"
    html = f'<div class="chat-bubble {css_class}"><b>{label}:</b> {msg}</div>'
    st.markdown(html, unsafe_allow_html=True)

# ========================
# Chat Input
# ========================
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", placeholder="Ask your assistant anything...")
    submit_button = st.form_submit_button(label="Send")

# ========================
# Process Submission
# ========================
if submit_button and user_input:
    st.session_state.chat_history.append(("You", user_input))

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",  # Replace with your model name if different
                "prompt": user_input,
                "stream": False
            }
        )

        if response.status_code != 200:
            result = f"[Error {response.status_code}] {response.text}"
            st.error(result)
        else:
            data = response.json()
            result = data.get("response", "[No response from model]")

    except Exception as e:
        result = f"[Request failed: {str(e)}]"
        st.error(result)

    st.session_state.chat_history.append(("Assistant", result))
    st.rerun()


