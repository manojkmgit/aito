import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu

# 1. PAGE CONFIG (Hide sidebar by default for a cleaner look)
st.set_page_config(page_title="AI Pro App", layout="wide", initial_sidebar_state="collapsed")

# 2. TOP NAVIGATION MENU
selected = option_menu(
    menu_title=None, 
    options=["Home", "Chat Bot", "Settings"], 
    icons=["house", "robot", "gear"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal",
)

# 3. INITIALIZE SESSION STATE (To remember the API key across tabs)
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# --- TAB: SETTINGS ---
if selected == "Settings":
    st.header("⚙️ Configuration")
    key_input = st.text_input("Enter Gemini API Key", value=st.session_state.api_key, type="password")
    if st.button("Save Key"):
        st.session_state.api_key = key_input
        st.success("Key saved for this session!")

# --- TAB: HOME ---
elif selected == "Home":
    st.title("Welcome to your AI Workspace")
    st.write("Use the menu above to configure your key or start chatting with documents.")

# --- TAB: CHAT BOT ---
elif selected == "Chat Bot":
    st.title("🤖 Document Chat")
    
    if not st.session_state.api_key:
        st.warning("Please go to the 'Settings' tab and enter your API Key first.")
    else:
        # Configure Gemini
        genai.configure(api_key=st.session_state.api_key)
        
        col1, col2 = st.columns(2)
        with col1:
            source_text = st.text_area("Paste Document Content:", height=300)
        with col2:
            question = st.text_input("Ask a question about the document:")
            if st.button("Run AI"):
                if source_text and question:
                    with st.spinner("Analyzing..."):
                        try:
                            model = genai.GenerativeModel('gemini-2.0-flash') # Using the updated model
                            prompt = f"Context: {source_text}\n\nQuestion: {question}\n\nAnswer based only on context."
                            response = model.generate_content(prompt)
                            st.info(response.text)
                        except Exception as e:
                            st.error(f"Error: {e}")
                else:
                    st.error("Please provide both text and a question.")