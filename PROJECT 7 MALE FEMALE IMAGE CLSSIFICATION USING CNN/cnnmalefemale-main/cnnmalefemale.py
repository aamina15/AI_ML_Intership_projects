import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Eye Gender Classification",
    page_icon="👁️",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
background:#F4F8FC;
}

/* Hide Streamlit Branding */

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

/* Main Heading */

.title{
text-align:center;
font-size:44px;
font-weight:700;
color:#1565C0;
margin-bottom:5px;
}

.subtitle{
text-align:center;
font-size:18px;
color:#555;
margin-bottom:25px;
}

/* Cards */

.card{
background:white;
padding:22px;
border-radius:18px;
box-shadow:0px 5px 18px rgba(0,0,0,.12);
margin-bottom:20px;
}

/* File Uploader */

[data-testid="stFileUploader"]{
border:2px dashed #2196F3;
border-radius:15px;
padding:18px;
background:white;
}

/* Metric */

[data-testid="stMetric"]{
background:white;
padding:10px;
border-radius:12px;
}

/* Progress */

.stProgress>div>div>div>div{
background:#1565C0;
}

/* Button */

.stButton>button{
background:linear-gradient(90deg,#1565C0,#42A5F5);
color:white;
border:none;
border-radius:10px;
font-size:17px;
font-weight:bold;
padding:12px;
width:100%;
}

</style>
""",unsafe_allow_html=True)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("male_female_modeli.keras")

model=load_model()

IMG_SIZE=150

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="title">
👁️ Eye Gender Classification
</div>

<div class="subtitle">
Deep Learning Based Gender Prediction using Eye Images
</div>
""",unsafe_allow_html=True)

st.divider()

# --------------------------------------------------
# PROJECT INFO
# --------------------------------------------------

c1,c2,c3=st.columns(3)

with c1:
    st.metric("Model","CNN")

with c2:
    st.metric("Input","Eye Image")

with c3:
    st.metric("Output","Male/Female")

st.divider()

# --------------------------------------------------
# FILE UPLOADER
# --------------------------------------------------

uploaded_file=st.file_uploader(
"📤 Upload an Eye Image",
type=["jpg","jpeg","png"]
)

if uploaded_file:

    image=Image.open(uploaded_file).convert("RGB")

    col1,col2=st.columns([1,1])

    with col1:

        st.markdown("<div class='card'>",unsafe_allow_html=True)

        st.image(
            image,
            caption="Uploaded Eye Image",
            use_container_width=True
        )

        st.markdown("</div>",unsafe_allow_html=True)

    img=image.resize((IMG_SIZE,IMG_SIZE))
    img=np.array(img)/255.0
    img=np.expand_dims(img,axis=0)

    prediction=model.predict(img,verbose=0)

    probability=float(prediction[0][0])
        # --------------------------------------------------
    # PREDICTION
    # --------------------------------------------------

    if probability >= 0.5:
        label = "👨 Male Eye"
        confidence = probability * 100
        male_prob = probability * 100
        female_prob = (1 - probability) * 100
    else:
        label = "👩 Female Eye"
        confidence = (1 - probability) * 100
        male_prob = probability * 100
        female_prob = (1 - probability) * 100

    # --------------------------------------------------
    # RESULT CARD
    # --------------------------------------------------

    with col2:

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("🤖 AI Prediction")

        st.success(label)

        st.metric(
            label="Prediction Confidence",
            value=f"{confidence:.2f}%"
        )

        st.progress(confidence / 100)

        st.write("### Probability")

        st.write(f"👨 Male : **{male_prob:.2f}%**")
        st.progress(male_prob / 100)

        st.write(f"👩 Female : **{female_prob:.2f}%**")
        st.progress(female_prob / 100)

        st.info(
            "The uploaded eye image has been analyzed using a Convolutional Neural Network (CNN)."
        )

        st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# ABOUT PROJECT
# --------------------------------------------------

st.divider()

st.markdown("""
<div class='card'>

<h3 style="color:#1565C0;">📖 About the Project</h3>

This application uses a <b>Convolutional Neural Network (CNN)</b> trained on eye images to classify whether the uploaded eye belongs to a <b>Male</b> or a <b>Female</b>. The uploaded image is automatically resized, normalized, and passed through the trained model to generate a prediction along with confidence scores.

<b>Workflow</b>

• Upload Eye Image<br>
• Image Preprocessing<br>
• CNN Model Prediction<br>
• Display Gender & Confidence

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TECHNOLOGIES
# --------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Framework", "TensorFlow")

with c2:
    st.metric("Frontend", "Streamlit")

with c3:
    st.metric("Language", "Python")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown("""
<div style='text-align:center;color:gray;'>

### 👁️ Eye Gender Classification

Built using ❤️ with Python • TensorFlow • Streamlit • NumPy • Pillow

</div>
""", unsafe_allow_html=True)
