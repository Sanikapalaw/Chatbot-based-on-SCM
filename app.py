import streamlit as st
import requests

st.set_page_config(page_title="SCM AI Assistant", page_icon="🚚")

st.title("🚚 SCM AI Assistant")

API_KEY = st.secrets["GEMINI_API_KEY"]

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

SYSTEM_PROMPT = "You are a Supply Chain Management assistant. Answer simply."

# -------- CHAT MEMORY --------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": SYSTEM_PROMPT}
    ]

# -------- SHOW CHAT --------
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------- RESPONSE FUNCTION --------
def ask_gemini(question):

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    payload = {
        "contents": [
            {
                "parts": [{"text": question}]
            }
        ]
    }

    response = requests.post(API_URL, json=payload)
    data = response.json()

    # simple safe read
    try:
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        reply = "Please try again."

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    return reply


# -------- USER INPUT --------
user_input = st.chat_input("Ask SCM question...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    answer = ask_gemini(user_input)

    with st.chat_message("assistant"):
        st.write(answer)

# -------- SUGGESTED QUESTIONS --------
st.divider()
st.subheader("Suggested Questions")

questions = [
    "What causes delivery delays?",
    "How to reduce logistics cost?",
    "What are SCM KPIs?",
    "Explain demand forecasting"
]

cols = st.columns(2)

for i, q in enumerate(questions):
    if cols[i % 2].button(q):
        with st.chat_message("user"):
            st.write(q)

        answer = ask_gemini(q)

        with st.chat_message("assistant"):
            st.write(answer)
