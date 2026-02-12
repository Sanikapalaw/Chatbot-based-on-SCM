import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SCM Gemini Assistant", page_icon="🚚")

st.title("🚚 SCM AI Assistant (Gemini)")

# ---------------- GEMINI CONFIG ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """
You are a Supply Chain Management expert assistant.
Keep conversation continuous and remember context.
Explain logistics and SCM topics simply.
"""

# ---------------- SESSION MEMORY ----------------
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(
        history=[
            {"role": "user", "parts": [SYSTEM_PROMPT]},
            {"role": "model", "parts": ["Understood. I will act as an SCM assistant."]}
        ]
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY CHAT HISTORY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- RESPONSE FUNCTION ----------------
def generate_response(user_text):

    response = st.session_state.chat.send_message(user_text)
    reply = response.text

    st.session_state.messages.append(
        {"role": "user", "content": user_text}
    )

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
