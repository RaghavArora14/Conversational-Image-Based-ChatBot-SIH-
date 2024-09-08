import google.generativeai as genai
import PIL.Image
import os
import streamlit as st

# Set the API key for Google Generative AI
os.environ["API_KEY"] = 'AIzaSyA9DSaPu4a5mU5yrc2lMcoU_f06aLf8ScI'
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

st.title("Gemini Chatbot with Image Support")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

# Image Upload Section
uploaded_file = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png",'webp'])

if uploaded_file is not None:
    # Load the uploaded image and display it
    st.session_state.uploaded_image = PIL.Image.open(uploaded_file)
    st.image(st.session_state.uploaded_image, caption="Uploaded Image", use_column_width=True)

# Display chat messages
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Prepare the messages for the API call
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        # If an image is uploaded, include it in the API call
        if st.session_state.uploaded_image:
            response = model.generate_content([messages[-1]["content"], st.session_state.uploaded_image], stream=True)
        else:
            response = model.generate_content(messages[-1]["content"], stream=True)

        # Stream the response
        for chunk in response:
            full_response += chunk.text
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Add a button to clear the conversation
if st.button("Clear Conversation"):
    st.session_state.messages = []
    st.session_state.uploaded_image = None
