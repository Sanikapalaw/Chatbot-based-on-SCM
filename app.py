import streamlit as st

st.set_page_config(page_title="SCM Expert (No API)", page_icon="🚚")

st.title("🚚 SCM Expert Bot")
st.markdown("This bot runs locally and does **not** require an API key.")

# 1. Your 10 Question-and-Answer Knowledge Base
scm_knowledge = {
    "what is scm": "Supply Chain Management (SCM) is the oversight of materials, information, and finances as they move from supplier to manufacturer to wholesaler to retailer to consumer.",
    "jit": "Just-in-Time (JIT) is an inventory strategy that aligns raw-material orders from suppliers directly with production schedules to increase efficiency.",
    "bullwhip effect": "The bullwhip effect is a distribution channel phenomenon where demand fluctuations at the retail level cause progressively larger fluctuations at the wholesale, distributor, and manufacturer levels.",
    "safety stock": "Safety stock is extra inventory held to prevent stockouts caused by fluctuations in supply and demand.",
    "lead time": "Lead time is the latency between the initiation and completion of a process (e.g., the time from order placement to delivery).",
    "3pl": "3PL (Third-Party Logistics) is outsourcing e-commerce logistics processes to a third-party business, including inventory management, warehousing, and fulfillment.",
    "abc analysis": "ABC analysis is an inventory categorization technique that divides items into three categories (A, B, and C) based on their importance and value.",
    "procurement": "Procurement is the act of obtaining goods or services, typically for business purposes.",
    "reverse logistics": "Reverse logistics is the process of moving goods from their typical final destination for the purpose of capturing value, or proper disposal.",
    "logistics": "Logistics is the part of the supply chain that plans, implements, and controls the efficient flow and storage of goods and services."
}

# 2. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your offline SCM assistant. Ask me about JIT, Lead Time, or the Bullwhip Effect!"}
    ]

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle User Input
if user_input := st.chat_input("Ask a question..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Simple Logic: Check if any keyword from our dictionary is in the user's input
    user_query = user_input.lower()
    response = "I'm sorry, I only know the 10 core SCM concepts right now. Try asking about 'JIT', 'Safety Stock', or 'Bullwhip Effect'!"
    
    for key in scm_knowledge:
        if key in user_query:
            response = scm_knowledge[key]
            break

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# 5. Sidebar Utility
with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
