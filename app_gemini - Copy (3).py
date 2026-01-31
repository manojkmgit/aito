import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Pro App", layout="wide")

# 2. SESSION STATE INITIALIZATION
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("Main Menu")
    selected = option_menu(
        menu_title=None, # Set to None to hide the title inside the menu
        options=["Home", "Chat Bot", "Settings"], 
        icons=["house", "robot", "gear"], 
        menu_icon="cast", 
        default_index=0,
    )
    
    st.info("Tip: Enter your API key in Settings before using the Chat Bot.")

# --- NAVIGATION LOGIC ---

if selected == "Home":
    st.title("Welcome to your AI Workspace")
    st.write("Select a tool from the left sidebar to get started.")

elif selected == "Settings":
    st.header("⚙️ Configuration")
    key_input = st.text_input("Enter Gemini API Key", value=st.session_state.api_key, type="password")
    if st.button("Save Key"):
        st.session_state.api_key = key_input
        st.success("Key saved for this session!")

elif selected == "Chat Bot":
    st.title("🤖 Document Chat with Memory")

    # 1. Initialize History in Session State if it doesn't exist
    if "chat_session" not in st.session_state:
        # We start a chat object and store it so it survives reruns
        genai.configure(api_key=st.session_state.api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        st.session_state.chat_session = model.start_chat(history=[])

    # 2. Layout
    source_text = st.text_area("Paste Document Content (Context):", height=200)
    
    # Display previous messages (Chat UI)
    for message in st.session_state.chat_session.history:
        with st.chat_message(message.role):
            st.markdown(message.parts[0].text)

    # 3. User Input
    if question := st.chat_input("Ask a follow-up question..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(question)

        # 4. Send message with context
        full_prompt = f"Context: {source_text}\n\nQuestion: {question}"
        
        with st.spinner("Thinking..."):
            response = st.session_state.chat_session.send_message(full_prompt)
            
            # Display AI response
            with st.chat_message("model"):
                st.markdown(response.text)