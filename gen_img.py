from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Initialize the client with your API Key
client = genai.Client(api_key="AIzaSyCdQ8Ig3vcwvp73Krey-JaRtLbyNZuEA3E")

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
generate_ai_image("A futuristic workspace for a Python developer, neon lights, 4k")