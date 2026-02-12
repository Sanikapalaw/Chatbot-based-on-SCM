import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(
    page_title="SCM AI Assistant", 
    page_icon="🚚", 
    layout="centered"
)

st.title("🚚 SCM AI Assistant")
st.markdown("Specialized intelligence for Logistics, Inventory, and Supply Chain Management.")

# 2. Secure API Configuration
# Pulls the key from Streamlit Cloud's "Secrets" manager
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key! Please go to App Settings > Secrets and add 'GEMINI_API_KEY'.")
    st.stop()

# 3. Model Initialization (Updated to 2.0 to avoid 404 errors)
# Gemini 2.0 Flash is the latest stable model for high-speed chat
model = genai.GenerativeModel(
    model_name='gemini-2.0-flash',
    system_instruction="You are a Supply Chain Management expert. Provide professional, concise, and data-driven advice on logistics and operations."
)

# 4. Session State for Chat Persistence
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    # persistent chat object manages the conversation history for you
    st.session_state.chat_session = model.start_chat(history=[])

# 5. Display Existing Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. User Input Logic
user_input = st.chat_input("Ask about demand forecasting, safety stock, or route optimization...")

if user_input:
    # Save and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and display Gemini response
    with st.chat_message("assistant"):
        with st.spinner("Processing SCM logic..."):
            try:
                # Uses the persistent session to maintain context
                response = st.session_state.chat_session.send_message(user_input)
                full_response = response.text
                
                st.markdown(full_response)
                
                # Save assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                # Handles potential API or safety filter errors gracefully
                st.error(f"Error: {str(e)}")

# 7. Sidebar Utilities
with st.sidebar:
    st.header("Control Panel")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    
    st.divider()
    st.caption("Engine: Gemini 2.0 Flash")
    st.caption("Status: Active & Stable")
