import streamlit as st

# 1. Page & Branding
st.set_page_config(page_title="SCM Pro Assistant", page_icon="🚚", layout="centered")

st.title("🚚 SCM Professional Assistant")
st.markdown("---")

# 2. Professional Knowledge Base
scm_knowledge = {
    "Negotiation Tips": "Focus on win-win outcomes and long-term partnerships rather than just the lowest price.",
    "JIT Strategy": "Just-In-Time (JIT) reduces waste by receiving goods only as needed, requiring high supplier reliability.",
    "Safety Stock": "This is your 'insurance' inventory for demand spikes or supply delays.",
    "3PL Services": "Third-Party Logistics (3PL) providers handle shipping and warehousing so you can focus on core sales.",
    "Reverse Logistics": "The process of handling returns, recycling, and refurbishing goods efficiently."
}

# 3. Initialize Professional Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today? You can select a quick topic below or type your own question.", "avatar": "🤖"}
    ]

# 4. Sidebar Controls
with st.sidebar:
    st.header("⚙️ Settings")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = [{"role": "assistant", "content": "Chat cleared. How can I help?", "avatar": "🤖"}]
        st.rerun()
    st.info("Status: Local Mode (No API Required)")

# 5. Display Continuous Chat History with Avatars
for msg in st.session_state.messages:
    # Preset avatars for user and custom emoji for assistant
    avatar = msg.get("avatar") if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 6. Quick Action Buttons (The "Branching" Options)
st.write("---")
st.caption("Quick Topics:")
cols = st.columns(3)
quick_picks = list(scm_knowledge.keys())[:3] # Show first 3 as buttons

selected_button = None
for i, topic in enumerate(quick_picks):
    if cols[i].button(topic, use_container_width=True):
        selected_button = topic

# 7. Professional Chat Input
user_input = st.chat_input("Ask about logistics, inventory, or procurement...")

# Priority logic: Use button if clicked, otherwise use typed input
final_prompt = selected_button if selected_button else user_input

if final_prompt:
    # User Message
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.markdown(final_prompt)

    # Professional Response Logic
    with st.chat_message("assistant", avatar="🤖"):
        # Search dictionary for match, else provide a fallback
        response = scm_knowledge.get(final_prompt, "I'm specialized in core SCM areas. Try asking about JIT, 3PL, or Safety Stock!")
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "🤖"})
    
    # Rerun to clear the button state
    st.rerun()
