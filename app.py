import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SCM AI Assistant", page_icon="🚚")

st.title("🚚 SCM AI Assistant (Gemini API)")

API_KEY = st.secrets["GEMINI_API_KEY"]

API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

SYSTEM_PROMPT = """
You are a Supply Chain Management expert assistant.
Keep conversation continuous and remember context.
Explain logistics and SCM topics simply and professionally.
"""

# ---------------- SESSION MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": SYSTEM_PROMPT}
    ]

# ---------------- DISPLAY CHAT HISTORY ----------------
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- GEMINI RESPONSE FUNCTION ----------------
def generate_response(user_text):

    st.session_state.messages.append(
        {"role": "user", "content": user_text}
    )

    # Build conversation history
    contents = []
    for msg in st.session_state.messages:
        contents.append({
            "role": "user" if msg["role"] == "user" else "model",
            "parts": [{"text": msg["content"]}]
        })

    payload = {
        "contents": contents
    }

    response = requests.post(API_URL, json=payload)
    result = response.json()

    reply = result["candidates"][0]["content"]["parts"][0]["text"]

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    return reply


# ---------------- USER INPUT ----------------
user_input = st.chat_input("Ask SCM question...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    reply = generate_response(user_input)

    with st.chat_message("assistant"):
        st.markdown(reply)


# ---------------- SUGGESTED QUESTIONS ----------------
st.divider()
st.subheader("Suggested Questions")

suggestions = [
    "What causes delivery delays?",
    "How to reduce logistics cost?",
    "What are SCM KPIs?",
    "Explain demand forecasting"
]

cols = st.columns(2)

for i, question in enumerate(suggestions):
    if cols[i % 2].button(question):

        with st.chat_message("user"):
            st.markdown(question)

        reply = generate_response(question)

        with st.chat_message("assistant"):
            st.markdown(reply)
