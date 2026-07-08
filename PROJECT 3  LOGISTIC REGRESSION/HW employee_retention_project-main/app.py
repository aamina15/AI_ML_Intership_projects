import streamlit as st
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Employee Retention Prediction",
    page_icon="👨‍💼",
    layout="centered"
)
st.title("👨‍💼 Employee Retention Prediction")

st.markdown("""
**Name:** Aamina Hasan  
**Branch:** Computer Science Engineering (CSE)  
**Room No.:** 612
""")

st.write("Predict whether an employee will leave the company.")

# -----------------------------------
# Load Dataset
# -----------------------------------

df = pd.read_csv("HR_comma_sep.csv")

encoder = LabelEncoder()
df["salary"] = encoder.fit_transform(df["salary"])

st.subheader("Dataset")
st.dataframe(df)

# -----------------------------------
# Train Model
# -----------------------------------

X = df[[
    "satisfaction_level",
    "average_montly_hours",
    "promotion_last_5years",
    "salary"
]]

y = df["left"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    train_size=0.8,
    random_state=42
)

model = LogisticRegression()

model.fit(X_train, y_train)

# -----------------------------------
# User Input
# -----------------------------------

st.subheader("Enter Employee Details")

satisfaction = st.number_input(
    "Satisfaction Level",
    min_value=0.00,
    max_value=1.00,
    value=0.50,
    step=0.01
)

hours = st.number_input(
    "Average Monthly Hours",
    min_value=90,
    max_value=320,
    value=200
)

promotion = st.selectbox(
    "Promotion in Last 5 Years",
    [0,1]
)

salary = st.selectbox(
    "Salary",
    ["Low","Medium","High"]
)

salary_value = {
    "Low":0,
    "Medium":1,
    "High":2
}

# -----------------------------------
# Prediction
# -----------------------------------

if st.button("Predict"):

    prediction = model.predict([[
        satisfaction,
        hours,
        promotion,
        salary_value[salary]
    ]])[0]

    if prediction == 1:
        st.error("❌ Employee is likely to leave the company.")
    else:
        st.success("✅ Employee is likely to stay with the company.")

# -----------------------------------
# Model Accuracy
# -----------------------------------

accuracy = model.score(X_test, y_test)

st.subheader("Model Accuracy")

st.write(f"Accuracy: **{accuracy:.2%}**")
