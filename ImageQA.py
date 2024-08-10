import streamlit as st
from transformers import BlipProcessor, BlipForQuestionAnswering
from PIL import Image
import torch

# Load the BLIP VQA model and processor
model_name = "Salesforce/blip-vqa-base"
processor = BlipProcessor.from_pretrained(model_name)
model = BlipForQuestionAnswering.from_pretrained(model_name)

# Streamlit app
st.title("Visual Question Answering")

st.write("Upload an image and ask a question about it.")

# Upload an image
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image as soon as it's uploaded
if uploaded_image is not None:
    raw_image = Image.open(uploaded_image).convert('RGB')
    st.image(raw_image, caption="Uploaded Image", use_column_width=True)

# Ask a question
question = st.text_input("Ask a question about the image (e.g., 'What is in the image?')")

# Add "Enter" button
if st.button("Enter"):
    if uploaded_image is not None and question:
        # Process the image and question
        inputs = processor(raw_image, question, return_tensors="pt")

        # Move inputs to GPU if available
        if torch.cuda.is_available():
            model = model.to("cuda")
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        # Generate the answer using the model
        with torch.no_grad():
            generated_ids = model.generate(**inputs, max_length=50, num_beams=5, early_stopping=True)
            answer = processor.decode(generated_ids[0], skip_special_tokens=True)

        # Display the result
        st.write(f"**Question:** {question}")
        st.write(f"**Answer:** {answer}")
    else:
        st.write("Please upload an image and enter a question.")

# Add "Re-run" button
if st.button("Re-run"):
    st.experimental_rerun()

