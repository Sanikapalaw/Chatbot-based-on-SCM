import streamlit as st
import requests

st.set_page_config(page_title="SCM AI Assistant", page_icon="🚚")

st.title("🚚 SCM AI Assistant")

api_key = st.secrets["GROQ_API_KEY"]

url = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = "You are a Supply Chain Management assistant. Answer simply and professionally."

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# show chat
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

def ask_ai(question):
    st.session_state.messages.append({"role": "user", "content": question})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": st.session_state.messages
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status() # This will trigger the 'except' block if the API returns an error
        data = res.json()
        
        # Check if 'choices' is actually in the response
        if "choices" in data:
            answer = data["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": answer})
            return answer
        else:
            return f"API Error: {data.get('error', 'Unknown error occurred')}"

    except requests.exceptions.RequestException as e:
        return f"Connection Error: {str(e)}"

