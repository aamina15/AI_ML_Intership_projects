import streamlit as st
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Insurance Sales Prediction",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Project 3: Insurance Sales Prediction")
st.write("Predict whether a person will buy insurance using Logistic Regression.")

# -----------------------------------
# Load Dataset
# -----------------------------------
df = pd.read_csv("insurance_data.csv")

st.subheader("Insurance Dataset")
st.dataframe(df)

# -----------------------------------
# Train Model
# -----------------------------------
X = df[['age']]
y = df['bought_insurance']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    train_size=0.8,
    random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

# -----------------------------------
# User Input
# -----------------------------------
st.subheader("Enter Person's Age")

age = st.number_input(
    "Age (Years)",
    min_value=10,
    max_value=100,
    value=30,
    step=1
)

# -----------------------------------
# Prediction
# -----------------------------------
if st.button("Predict Insurance"):

    prediction = model.predict([[age]])[0]
    probability = model.predict_proba([[age]])[0][1]

    if prediction == 1:
        st.success("✅ This person is likely to BUY insurance.")
    else:
        st.error("❌ This person is NOT likely to buy insurance.")

    st.write(f"**Probability of buying insurance:** {probability:.2%}")

# -----------------------------------
# Model Information
# -----------------------------------
st.subheader("Model Details")

st.write("Coefficient:", model.coef_[0][0])
st.write("Intercept:", model.intercept_[0])

# -----------------------------------
# Model Accuracy
# -----------------------------------
accuracy = model.score(X_test, y_test)
st.subheader("Model Accuracy")
st.write(f"Accuracy: **{accuracy:.2%}**")
