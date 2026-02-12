import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(
    page_title="SCM AI Assistant", 
    page_icon="🚚", 
    layout="centered"
)

st.title("🚚 SCM AI Assistant")
st.markdown("Your specialized assistant for Supply Chain, Logistics, and Inventory Management.")

# 2. Secure API Configuration
# This pulls the key from Streamlit Cloud's "Secrets" manager
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# 3. Model Initialization
# We use gemini-1.5-flash for speed and efficiency
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="You are a Supply Chain Management assistant. Answer simply, professionally, and provide actionable SCM insights."
)

# 4. Session State for Chat History
# This ensures the chat doesn't disappear when the app reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    # persistent chat object handles conversation memory
    st.session_state.chat_session = model.start_chat(history=[])

# 5. Display Existing Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. User Input Logic
user_input = st.chat_input("Ask a supply chain question (e.g., How to optimize safety stock?)")

if user_input:
    # Display user's message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and display AI response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            try:
                # Send message to the Gemini API
                response = st.session_state.chat_session.send_message(user_input)
                full_response = response.text
                
                st.markdown(full_response)
                
                # Save to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# 7. Sidebar Utilities
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    
    st.info("Powered by Google Gemini 1.5 Flash")
