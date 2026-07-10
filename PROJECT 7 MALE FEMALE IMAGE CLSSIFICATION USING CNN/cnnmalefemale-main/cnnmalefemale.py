import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Gender Classification",
    page_icon="🧠",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
background:#F4F8FC;
}

.title{
text-align:center;
font-size:42px;
font-weight:700;
color:#1565C0;
}

.subtitle{
text-align:center;
font-size:18px;
color:#555;
margin-bottom:25px;
}

.result-card{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0px 4px 12px rgba(0,0,0,.1);
}

footer{
visibility:hidden;
}

</style>
""",unsafe_allow_html=True)

# --------------------------------------------------
# Load Model
# --------------------------------------------------

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("male_female_modeli.keras")

model=load_model()

IMG_SIZE=150

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
"""
<div class="title">
🧠 AI Gender Classification
</div>

<div class="subtitle">
Upload a facial image and let the Deep Learning model predict whether it belongs to a Male or Female.
</div>
""",
unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# Upload
# --------------------------------------------------

uploaded_file=st.file_uploader(
    "📤 Upload Image",
    type=["jpg","jpeg","png"]
)

if uploaded_file:

    image=Image.open(uploaded_file).convert("RGB")

    col1,col2=st.columns([1,1])

    with col1:

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

    img=image.resize((IMG_SIZE,IMG_SIZE))
    img=np.array(img)/255.0
    img=np.expand_dims(img,axis=0)

    prediction=model.predict(img,verbose=0)

    prob=float(prediction[0][0])

    if prob>=0.5:

        label="👨 Male"
        confidence=prob*100

    else:

        label="👩 Female"
        confidence=(1-prob)*100

    with col2:

        st.markdown('<div class="result-card">',unsafe_allow_html=True)

        st.subheader("Prediction")

        st.success(label)

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

        st.progress(confidence/100)

        st.info("The prediction confidence represents the probability assigned by the CNN model.")

        st.markdown("</div>",unsafe_allow_html=True)

st.divider()

st.markdown(
"""
<center>

### 📌 Technologies Used

Python • TensorFlow • Keras • Streamlit • Pillow • NumPy

</center>
""",
unsafe_allow_html=True
)
