import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Male/Female Classifier",
    page_icon="🧑",
    layout="centered"
)

# -------------------------
# Load Model
# -------------------------
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model("male_female_modeli.keras")

model = load_my_model()

IMG_SIZE = 150

# -------------------------
# Title
# -------------------------
st.title("🧑 Male / Female Image Classifier")
st.write("Upload a face image to predict whether it is Male or Female.")

# -------------------------
# Upload Image
# -------------------------
uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(image, caption="Uploaded Image", use_container_width=True)

    # -------------------------
    # Preprocess Image
    # -------------------------
    img = image.resize((IMG_SIZE, IMG_SIZE))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    # -------------------------
    # Prediction
    # -------------------------
    prediction = model.predict(img)

    probability = float(prediction[0][0])

    if probability >= 0.5:
        label = "Male"
        confidence = probability * 100
    else:
        label = "Female"
        confidence = (1 - probability) * 100

    # -------------------------
    # Display Result
    # -------------------------
    st.success(f"Prediction: **{label}**")
    st.write(f"Confidence: **{confidence:.2f}%**")%**")
