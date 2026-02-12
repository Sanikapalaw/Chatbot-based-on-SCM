import streamlit as st

st.set_page_config(page_title="Dynamic SCM Bot", page_icon="🚚")

# 1. UPDATED Knowledge Base with missing branches
scm_branches = {
    "START": ("How can I help you today? Select a major supply chain area to explore:", 
              ["Procurement", "Inventory", "Logistics"]),
    
    # PROCUREMENT BRANCH
    "Procurement": ("Procurement is about sourcing goods. What specifically interests you?", 
                    ["Vendor Selection", "Negotiation Tips", "Purchase Orders"]),
    "Vendor Selection": ("Choosing the right vendor involves looking at cost, quality, and reliability. Always check their lead times!", ["Back to Procurement", "Home"]),
    "Negotiation Tips": ("Good negotiation is about 'win-win'. Focus on long-term partnerships rather than just the lowest price.", ["Back to Procurement", "Home"]),
    "Purchase Orders": ("A PO is a legally binding document sent by a buyer to a seller indicating types, quantities, and agreed prices.", ["Back to Procurement", "Home"]),

    # INVENTORY BRANCH
    "Inventory": ("Inventory management balances cost and availability. Want to learn about:", 
                  ["JIT Strategy", "Safety Stock", "ABC Analysis"]),
    "JIT Strategy": ("Just-In-Time (JIT) reduces waste by receiving goods only as needed. It requires high supplier reliability.", ["Back to Inventory", "Home"]),
    "Safety Stock": ("Safety stock is your 'insurance' inventory for demand spikes or supply delays.", ["Back to Inventory", "Home"]),
    "ABC Analysis": ("ABC Analysis divides inventory into three categories: A (high value), B (moderate), and C (low value).", ["Back to Inventory", "Home"]),
    
    # LOGISTICS BRANCH
    "Logistics": ("Logistics covers movement and storage. Choose a sub-topic:", 
                  ["3PL Services", "Route Optimization", "Reverse Logistics"]),
    "3PL Services": ("3PL providers handle your shipping and warehousing so you can focus on sales.", ["Back to Logistics", "Home"]),
    "Route Optimization": ("This uses math to find the shortest, fastest, and cheapest way to deliver goods.", ["Back to Logistics", "Home"]),
    "Reverse Logistics": ("This is the process of handling returns, recycling, and refurbishing goods.", ["Back to Logistics", "Home"]),

    "Home": ("Returning to start...", ["Procurement", "Inventory", "Logistics"])
}

# Mapping for "Back" buttons
back_map = {
    "Back to Procurement": "Procurement",
    "Back to Inventory": "Inventory", 
    "Back to Logistics": "Logistics"
}

# 2. Initialize State
if "current_step" not in st.session_state:
    st.session_state.current_step = "START"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Handle Button Clicks
def handle_click(choice):
    next_step = back_map.get(choice, choice)
    
    # Check if the step exists before moving to avoid the KeyError
    if next_step in scm_branches:
        st.session_state.current_step = next_step
        answer, _ = scm_branches[next_step]
        st.session_state.messages.append({"role": "user", "content": choice})
        st.session_state.messages.append({"role": "assistant", "content": answer})
    else:
        st.session_state.messages.append({"role": "assistant", "content": "I'm still learning about that topic!"})

# 4. UI Layout
st.title("🚚 Dynamic SCM Assistant")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Display Dynamic Buttons
# Using .get() to provide a fallback and prevent the KeyError crash
current_data = scm_branches.get(st.session_state.current_step, scm_branches["START"])
current_text, options = current_data

if st.session_state.current_step == "START" and not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write(current_text)

st.write("---")
st.write("### Choose an option to continue:")
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
