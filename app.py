import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
from google import genai as google_genai
from google.genai import types
from PIL import Image
from io import BytesIO

# 1. PAGE CONFIG
st.set_page_config(page_title="AI Pro App", layout="wide")

# 2. SESSION STATE INITIALIZATION
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["GEMINI_API_KEY"]

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("Main Menu")
    selected = option_menu(
        menu_title=None, # Set to None to hide the title inside the menu
        options=["Home", "Chat Bot", "Image Lab", "Vision Assistant", "Image Lab 3", "Settings"], 
        icons=["house", "robot", "palette", "brush", "bucket", "gear"], 
        menu_icon="cast", 
        default_index=0,
    )
    
    st.info("Tip: Enter your API key in Settings before using the Chat Bot.")

# --- NAVIGATION LOGIC ---

if selected == "Home":
    st.title("Welcome to your AI Workspace")
    st.write("Select a tool from the left sidebar to get started.")
elif selected == "Chat Bot":
    st.title("🤖 Document Chat")
    
    if not st.session_state.api_key:
        st.warning("Please go to Settings and enter your API Key.")
    else:
        genai.configure(api_key=st.session_state.api_key)
        
        col1, col2 = st.columns(2)
        with col1:
            source_text = st.text_area("Paste Document Content:", height=400)
        with col2:
            question = st.text_input("Ask a question:")
            if st.button("Run AI"):
                if source_text and question:
                    with st.spinner("Processing..."):
                        try:
                            model = genai.GenerativeModel('gemini-2.5-flash-lite')
                            prompt = f"Context: {source_text}\n\nQuestion: {question}"
                            response = model.generate_content(prompt)
                            st.info(response.text)
                        except Exception as e:
                            st.error(f"Error: {e}")
elif selected == "Image Lab":
    st.title("🎨 Image Generator")
    
    if not st.session_state.api_key:
        st.warning("Please go to Settings and enter your API Key.")
    else:
        # First, let's list available models
        if st.button("Show Available Models"):
            try:
                client = google_genai.Client(api_key=st.session_state.api_key)
                models = client.models.list()
                st.write("Available models:")
                for model in models:
                    st.write(f"- {model.name}")
            except Exception as e:
                st.error(f"Error listing models: {e}")
        
        st.divider()
        img_prompt = st.text_input("Describe the image you want to create:")
        model_name = st.text_input("Model name:", value="imagen-2-generate-001")
        
        if st.button("Generate Image"):
            if img_prompt:
                with st.spinner("Drawing..."):
                    try:
                        client = google_genai.Client(api_key=st.session_state.api_key)
                        response = client.models.generate_images(
                            model=model_name,
                            prompt=img_prompt
                        )
                        # Display the first generated image
                        st.image(response.generated_images[0].image.image_bytes)
                    except Exception as e:
                        st.error(f"Error generating image: {e}")
elif selected == "Vision Assistant":
    st.title("🎨 Nano Banana Image Lab")
    if not st.session_state.api_key:
        st.warning("Please enter your API Key in Settings.")
    else:
        st.title("👁️ Vision Assistant")
        st.write("Analyze images using Gemini's eyes.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        with col2:
            camera_photo = st.camera_input("Take Photo")
        with col3:
            camera_photo = st.camera_input("Show Photo")

        source = uploaded_file or camera_photo

        if source:
            img = Image.open(source)
            st.image(img, width=400)
            user_task = st.text_input("What should the AI do?", "Describe this image.")
            client = google_genai.Client(api_key=st.session_state.api_key)
            if st.button("Run Analysis"):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[user_task, img]
                )
                st.success(response.text)
# 4. IMAGE LAB (MULTIMODAL)
elif selected == "Image Lab 2":
    st.title("🎨 Nano Banana Image Lab")
    if not st.session_state.api_key:
        st.warning("Please enter your API Key in Settings.")
    else:
        client = google_genai.Client(api_key=st.session_state.api_key)
        img_prompt = st.text_input("Describe the image (e.g., 'Generate an image of a cybernetic cat')")

        if st.button("Create Image"):
            with st.spinner("Generating multimodal response..."):
                try:
                    # NANO BANANA METHOD: Requesting Image Modality
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=img_prompt,
                        config=types.GenerateContentConfig(
                            response_modalities=["TEXT", "IMAGE"]
                        )
                    )

                    # Loop through parts to find the image
                    for part in response.candidates[0].content.parts:
                        if part.text:
                            st.write(part.text)
                        if part.inline_data:
                            # Convert bytes to displayable image
                            st.image(part.inline_data.data, caption="Generated by Gemini")
                except Exception as e:
                    st.error(f"Error: {e}")
elif selected == "Image Lab 3":
    st.title("🎨 Image Description Generator")
    if not st.session_state.api_key:
        st.warning("Please enter your API Key in Settings.")
    else:
        client = google_genai.Client(api_key=st.session_state.api_key)
        
        st.info("📝 Note: Free tier generates detailed descriptions. Upload or describe images for analysis.")
        
        # Option 1: Generate image descriptions
        img_prompt = st.text_input("What kind of image would you like described?")
        
        if st.button("Generate Description"):
            if img_prompt:
                with st.spinner("Generating..."):
                    try:
                        model = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=f"Create a detailed, vivid description of: {img_prompt}\n\nInclude colors, mood, composition, and style."
                        )
                        if model.text:
                            st.write(model.text)
                    except Exception as e:
                        st.error(f"Generation failed: {e}")
elif selected == "Settings":
    st.header("⚙️ Configuration")
    key_input = st.text_input("Enter Gemini API Key", value=st.session_state.api_key, type="password")
    if st.button("Save Key"):
        st.session_state.api_key = key_input
        st.success("Key saved for this session!")




# Initialize the client with your API Key
# client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

def generate_ai_image(prompt):
    print(f"Generating: {prompt}...")
    
    # We use the 'imagen-3.0' model for high-quality images
    response = client.models.generate_images(
        model='imagen-3.0-generate-001',
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1" # You can use "16:9", "4:3", etc.
        )
    )

    # Images are returned as bytes; we use PIL to open/save them
    for i, generated_image in enumerate(response.generated_images):
        img = Image.open(BytesIO(generated_image.image.image_bytes))
        img.show() # Opens the image on your Windows PC
        img.save(f"generated_output_{i}.png")

# Run it
# generate_ai_image("A futuristic workspace for a Python developer, neon lights, 4k")