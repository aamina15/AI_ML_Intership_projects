import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Price Outlier Detection",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Price Outlier Detection using Percentiles")

# Read CSV directly from the project folder
df = pd.read_csv("AB_NYC_2019.csv")   # Change filename if needed

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Dataset Shape")
col1, col2 = st.columns(2)
col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])

st.subheader("Price Statistics (Before Cleaning)")
st.dataframe(df["price"].describe())

# Calculate thresholds
min_threshold, max_threshold = df["price"].quantile([0.01, 0.999])

st.subheader("Threshold Values")
c1, c2 = st.columns(2)
c1.metric("1st Percentile", round(min_threshold, 2))
c2.metric("99.9th Percentile", round(max_threshold, 2))

# Remove outliers
df2 = df[(df["price"] > min_threshold) & (df["price"] < max_threshold)]

st.subheader("Dataset After Removing Outliers")
st.dataframe(df2.head())

st.metric("Rows After Cleaning", df2.shape[0])

st.subheader("Price Statistics (After Cleaning)")
st.dataframe(df2["price"].describe())

# Histogram before cleaning
st.subheader("Histogram Before Cleaning")
fig1, ax1 = plt.subplots(figsize=(8,4))
ax1.hist(df["price"], bins=40)
ax1.set_xlabel("Price")
ax1.set_ylabel("Frequency")
st.pyplot(fig1)

# Histogram after cleaning
st.subheader("Histogram After Cleaning")
fig2, ax2 = plt.subplots(figsize=(8,4))
ax2.hist(df2["price"], bins=40)
ax2.set_xlabel("Price")
ax2.set_ylabel("Frequency")
st.pyplot(fig2)

# Show cleaned dataset
st.subheader("Cleaned Dataset")
st.dataframe(df2)

# Download button
csv = df2.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇ Download Cleaned Dataset",
    csv,
    "cleaned_house_data.csv",
    "text/csv"
)
