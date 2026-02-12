import streamlit as st
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SCM AI Assistant", page_icon="🚚")

st.title("🚚 Supply Chain AI Assistant")

# ---------------- OPENAI CLIENT ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- SYSTEM ROLE ----------------
SYSTEM_PROMPT = """
You are an expert Supply Chain Management assistant.
Keep conversation natural and continuous.
Remember previous discussion context.
Explain SCM concepts simply and professionally.
"""

# ---------------- SESSION MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ---------------- DISPLAY CHAT HISTORY ----------------
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- FUNCTION TO GET AI RESPONSE ----------------
def generate_response(user_text):

    # save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_text}
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # save assistant reply
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
    "What are important SCM KPIs?",
    "Explain demand forecasting in logistics"
]

cols = st.columns(2)

for i, question in enumerate(suggestions):
    if cols[i % 2].button(question):

        with st.chat_message("user"):
            st.markdown(question)

        reply = generate_response(question)

        with st.chat_message("assistant"):
            st.markdown(reply)
