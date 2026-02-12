import streamlit as st

st.set_page_config(page_title="Dynamic SCM Bot", page_icon="🚚")

# 1. Define the Branching Knowledge Base
# Format: { "Trigger": ("Answer", ["Follow-up 1", "Follow-up 2", ...]) }
scm_branches = {
    "START": ("How can I help you today? Select a major supply chain area to explore:", 
              ["Procurement", "Inventory", "Logistics"]),
    
    "Procurement": ("Procurement is about sourcing goods. What specifically interests you?", 
                    ["Vendor Selection", "Negotiation Tips", "Purchase Orders"]),
    
    "Inventory": ("Inventory management balances cost and availability. Want to learn about:", 
                  ["JIT Strategy", "Safety Stock", "ABC Analysis"]),
    
    "Logistics": ("Logistics covers movement and storage. Choose a sub-topic:", 
                  ["3PL Services", "Route Optimization", "Reverse Logistics"]),
    
    # Deep Branches (Level 2)
    "JIT Strategy": ("Just-In-Time (JIT) reduces waste by receiving goods only as needed. It requires high supplier reliability.", ["Back to Inventory", "Home"]),
    "Safety Stock": ("Safety stock is your 'insurance' inventory for demand spikes.", ["Back to Inventory", "Home"]),
    "3PL Services": ("3PL providers handle your shipping and warehousing so you can focus on sales.", ["Back to Logistics", "Home"]),
    "Home": ("Returning to start...", ["Procurement", "Inventory", "Logistics"])
}

# Mapping for "Back" buttons to keep it clean
back_map = {"Back to Inventory": "Inventory", "Back to Logistics": "Logistics"}

# 2. Initialize State
if "current_step" not in st.session_state:
    st.session_state.current_step = "START"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Handle Button Clicks
def handle_click(choice):
    # Determine the next step
    next_step = back_map.get(choice, choice)
    st.session_state.current_step = next_step
    
    # Add to chat history
    answer, _ = scm_branches.get(next_step, ("I'm not sure about that.", []))
    st.session_state.messages.append({"role": "user", "content": choice})
    st.session_state.messages.append({"role": "assistant", "content": answer})

# 4. UI Layout
st.title("🚚 Dynamic SCM Assistant")

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Display Dynamic Buttons
current_text, options = scm_branches[st.session_state.current_step]

if st.session_state.current_step == "START":
    with st.chat_message("assistant"):
        st.write(current_text)

st.write("---")
st.write("### Choose an option:")
cols = st.columns(len(options))

for i, option in enumerate(options):
    with cols[i]:
        if st.button(option, key=option):
            handle_click(option)
            st.rerun()

# 6. Sidebar Reset
with st.sidebar:
    if st.button("Restart Bot"):
        st.session_state.current_step = "START"
        st.session_state.messages = []
        st.rerun()
