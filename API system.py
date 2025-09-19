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
