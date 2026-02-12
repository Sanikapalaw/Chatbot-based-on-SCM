import streamlit as st

st.set_page_config(page_title="SCM Interactive Bot", page_icon="🚚")

# 1. Initialize the Knowledge Base
scm_faq = {
    "What is the Bullwhip Effect?": "The bullwhip effect is when small changes in consumer demand cause larger and larger swings in inventory orders as you move up the supply chain.",
    "What is JIT (Just-In-Time)?": "JIT is an inventory strategy to increase efficiency by receiving goods only as they are needed in the production process, reducing storage costs.",
    "What is Safety Stock?": "Safety stock is extra inventory held as a buffer to prevent stockouts caused by unpredictable demand or supply delays.",
    "What is 3PL (Third-Party Logistics)?": "3PL is outsourcing your distribution, warehousing, and fulfillment to a specialized service provider like FedEx or DHL.",
    "What is Reverse Logistics?": "Reverse logistics is the process of moving goods from their final destination back to the seller for returns, recycling, or disposal."
}

# 2. Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.first_run = True

# 3. Greeting Logic
if st.session_state.first_run:
    greeting = "How can I help you today? Please select an SCM topic below or type your own question!"
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.session_state.first_run = False

# 4. Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Display 5 Clickable Options
st.write("### Quick Questions:")
cols = st.columns(1) # You can change this to 2 or 3 for a grid look
selected_question = None

for question in scm_faq.keys():
    if st.button(question, use_container_width=True):
        selected_question = question

# 6. Process the Choice or Manual Input
user_input = st.chat_input("Or type your own question here...")

# If they clicked a button, treat it as their input
final_input = selected_question if selected_question else user_input

if final_input:
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": final_input})
    
    # Generate Answer
    answer = scm_faq.get(final_input, "I'm sorry, I'm still learning! Try clicking one of the 5 options above.")
    
    # Add Assistant Message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    
    # Rerun to show the new messages immediately
    st.rerun()
