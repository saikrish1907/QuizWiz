import streamlit as st
import google.generativeai as genai
from apikey import gemini_open_apikey
from PIL import Image
import base64

genai.configure(api_key=gemini_open_apikey)

generation_config = {
  "temperature": 1.35,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# Setting the page config
st.set_page_config(layout="wide")

# Set the logo 
st.image('logo.png', width=200)

# Title of your page
st.title("The AI QuizWhiz 🤖")

# Sub header -- Descripiton of what the page does
st.subheader("Fast and precise AI-driven quiz answers 💡")

# Get input of what the title of the blog and keywords to generate the article/blog

with st.sidebar:
  st.title('Input the quiz image')
  uploaded_image = st.file_uploader("Upload an image", type=["png", "jpeg", "jpg"])
  submit = st.button('Generate Answer')

if submit:
  # Open the uploaded image file
  image = Image.open(uploaded_image)
  
  # Display the image
  st.image(image, caption='Quiz Image', use_column_width=True)
  
  # If you need the image data, you can get it using getvalue()
  image_bytes = uploaded_image.getvalue()

    # Encode the image as base64 for the request (if required by the API)
  encoded_image = base64.b64encode(image_bytes).decode('utf-8')

  # Create the files structure with mime_type and data
  files = [{
      "mime_type": "image/jpeg",  # Update this if your image is of a different type
      "data": encoded_image,
  }]

  # Structure the prompt parts correctly
  prompt_parts = [
        {
            "mime_type": files[0]['mime_type'],
            "data": files[0]['data']
        },
        {"text": "Please provide the correct option from the below image."}
    ]
  response = model.generate_content(prompt_parts)
  st.write(response.text)
