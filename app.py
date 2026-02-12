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

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": st.session_state.messages
    }

    res = requests.post(url, headers=headers, json=payload)
    data = res.json()

    answer = data["choices"][0]["message"]["content"]

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    return answer


user_input = st.chat_input("Ask SCM question...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    reply = ask_ai(user_input)

    with st.chat_message("assistant"):
        st.write(reply)
