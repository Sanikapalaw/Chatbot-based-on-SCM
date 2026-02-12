import streamlit as st
import requests

st.set_page_config(page_title="SCM AI Assistant", page_icon="🚚")

st.title("🚚 SCM AI Assistant")

# 1. Access the API Key
api_key = st.secrets["GROQ_API_KEY"]
url = "https://api.groq.com/openai/v1/chat/completions"
SYSTEM_PROMPT = "You are a Supply Chain Management assistant. Answer simply and professionally."

# 2. Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# 3. Display Chat History (skipping the system prompt)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. Define the API Interaction Logic
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
        res.raise_for_status() 
        data = res.json()
        
        if "choices" in data:
            answer = data["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": answer})
            return answer
        else:
            return f"API Error: {data.get('error', 'Unknown error format')}"

    except requests.exceptions.RequestException as e:
        return f"Connection Error: {str(e)}"

# 5. Handle User Input
user_input = st.chat_input("Ask about supply chain logistics, inventory, etc...")

if user_input:
    # Immediately show the user's message
    with st.chat_message("user"):
        st.write(user_input)

    # Get the AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."): # Added a nice loading spinner
            reply = ask_ai(user_input)
            st.write(reply)
