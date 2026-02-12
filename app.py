import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SCM Gemini Assistant", page_icon="🚚")

st.title("🚚 SCM AI Assistant (Gemini)")

# ---------------- GEMINI CONFIG ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- SYSTEM PROMPT ----------------
SYSTEM_PROMPT = """
You are a Supply Chain Management expert assistant.
Keep conversation continuous and remember previous context.
Explain logistics, inventory, warehouse and supply chain
concepts in simple professional language.
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

# ---------------- FUNCTION FOR RESPONSE ----------------
def generate_response(user_text):

    st.session_state.messages.append(
        {"role": "user", "content": user_text}
    )

    # Build conversation history
    history = ""
    for m in st.session_state.messages:
        history += f"{m['role']}: {m['content']}\n"

    response = model.generate_content(history)
    reply = response.text

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
