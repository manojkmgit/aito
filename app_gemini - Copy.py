import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai

# 1. UI CONFIGURATION
st.set_page_config(page_title="DocuChat (Gemini)", layout="wide")
# Start with the sidebar hidden
st.set_page_config(initial_sidebar_state="collapsed")
if st.button("Open Settings"):
    # Note: Streamlit doesn't have a direct 'st.sidebar.show()' function yet,
    # but you can toggle it by rerunning the script with a different config.
    st.write("Settings opened!")
st.title("🤖 Chat with your Document (Free Gemini Version)")

# 2. SIDEBAR: API KEY
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.markdown("[Get a Free Key Here](https://aistudio.google.com/app/apikey)")

    if api_key:
        # Configure the Google library with your key
        genai.configure(api_key=api_key)

# 3. MAIN UI
col1, col2 = st.columns(2)

with col1:
    st.header("1. The Source")
    source_text = st.text_area("Paste your document text here:", height=300)

with col2:
    st.header("2. The Question")
    question = st.text_input("What do you want to know?")
    
    if st.button("Get Answer"):
        if not api_key:
            st.error("Please enter your API Key in the sidebar.")
        elif not source_text:
            st.error("Please paste some text first.")
        elif not question:
            st.error("Please ask a question.")
        else:
            with st.spinner("Thinking..."):
                try:
                    # 4. THE AI ENGINEERING PART
                    # Select the model (Gemini 1.5 Flash is fast and free-tier eligible)
                    model = genai.GenerativeModel('gemini-2.5-flash-lite')
                    
                    # Create the prompt with context (RAG)
                    prompt = f"""
                    Context:
                    {source_text}
                    
                    Question:
                    {question}
                    
                    Answer the question using ONLY the context above.
                    """
                    
                    # Generate content
                    response = model.generate_content(prompt)
                    
                    # 5. DISPLAY RESULT
                    st.success("Answer:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"Error: {e}")