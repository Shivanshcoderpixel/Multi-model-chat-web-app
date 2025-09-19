import os
import streamlit as st
import requests
from datetime import datetime

# Styling for chat bubbles
st.markdown("""
<style>
.chat-message {
    padding: 1rem;
    border-radius: 1rem;
    margin-bottom: 1rem;
    animation: fadeIn 0.3s ease-in;
}
.user-message {
    background-color: #d0e7ff;
    border-left: 4px solid #1a73e8;
}
.bot-message {
    background-color: #e8d7f7;
    border-left: 4px solid #7b1fa2;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
.model-badge {
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    padding: 0.2rem 0.6rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    margin-left: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = {
    "GPT-4": "openai/gpt-4",
    "GPT-3.5": "openai/gpt-3.5-turbo",
    "Llama 2": "llama2-13b-chat",
}

def query_openrouter(messages, model_id, temperature=0.7):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-app-url.com",
        "X-Title": "Multi-Model Chatbot"
    }
    payload = {
        "model": model_id,
        "messages": messages,
        "max_tokens": 512,
        "temperature": temperature,
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def test_api_connection():
    test_msg = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello."}]
    try:
        reply = query_openrouter(test_msg, MODELS["GPT-3.5"])
        return True, reply
    except Exception as e:
        return False, str(e)

def main():
    st.set_page_config(page_title="AI Chat Companion", layout="centered")
    st.title("AI Chat Companion")
    st.sidebar.header("Settings")
    model_name = st.sidebar.selectbox("Select AI Model", list(MODELS.keys()))
    model_id = MODELS[model_name]

    if not OPENROUTER_API_KEY:
        st.error("API key missing. Set OPENROUTER_API_KEY environment variable.")
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

    # Run API test once and show result
    if "api_test_done" not in st.session_state:
        success, result = test_api_connection()
        if success:
            st.success("API connection successful.")
        else:
            st.error(f"API connection failed: {result}")
        st.session_state.api_test_done = True

    # Display chat history
    for msg in st.session_state.messages[1:]:
        timestamp = msg.get("timestamp", "")
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You</strong> <small>({timestamp})</small><br>{msg['content']}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>AI Assistant</strong><span class="model-badge">{model_name}</span> <small>({timestamp})</small><br>{msg['content']}
            </div>""", unsafe_allow_html=True)

    user_input = st.text_input("Your message", key="input")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        with st.spinner("AI is typing..."):
            try:
                response = query_openrouter(st.session_state.messages, model_id)
            except Exception as e:
                st.error(f"Error: {e}")
                return
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        st.experimental_rerun()

    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
        st.experimental_rerun()

if __name__ == "__main__":
    main()
