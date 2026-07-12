"""
KGF 2 / Movie Review Sentiment Analysis App
--------------------------------------------
An end-to-end NLP app using Hugging Face Transformers to perform
sentiment analysis on movie reviews, with accuracy/F1 evaluation
against ground-truth labels.

Run locally:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import evaluate
from transformers import pipeline

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Movie Review Sentiment Analyzer",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 Movie Review Sentiment Analysis (KGF 2 / Dhurandhar 2)")
st.caption(
    "Powered by Hugging Face `distilbert-base-uncased-finetuned-sst-2-english`"
)

# ----------------------------------------------------------------------
# Cache the model so it only loads once per session
# ----------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading sentiment analysis model...")
def load_classifier():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
    )


@st.cache_resource(show_spinner=False)
def load_metrics():
    accuracy = evaluate.load("accuracy")
    f1 = evaluate.load("f1")
    return accuracy, f1


classifier = load_classifier()
accuracy_metric, f1_metric = load_metrics()

# ----------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------
mode = st.sidebar.radio(
    "Choose a mode",
    ["Single Review", "Batch CSV Analysis"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Model:** distilbert-base-uncased-finetuned-sst-2-english\n\n"
    "**Task:** Binary sentiment classification (POSITIVE / NEGATIVE)"
)

# ----------------------------------------------------------------------
# Mode 1: Single custom review
# ----------------------------------------------------------------------
if mode == "Single Review":
    st.subheader("Analyze a single review")

    default_review = "KGF 2 is an amazing movie with powerful action and excellent performance."
    review_text = st.text_area("Enter a movie review:", value=default_review, height=120)

    if st.button("Analyze Sentiment", type="primary"):
        if review_text.strip():
            with st.spinner("Analyzing..."):
                result = classifier(review_text)[0]
            label = result["label"]
            score = result["score"]

            col1, col2 = st.columns(2)
            with col1:
                if label == "POSITIVE":
                    st.success(f"Sentiment: {label} 😊")
                else:
                    st.error(f"Sentiment: {label} 😞")
            with col2:
                st.metric("Confidence", f"{score:.2%}")
        else:
            st.warning("Please enter a review first.")

# ----------------------------------------------------------------------
# Mode 2: Batch CSV analysis + evaluation
# ----------------------------------------------------------------------
else:
    st.subheader("Batch analysis from CSV")
    st.write(
        "Upload a CSV with a `Review` column (and optionally a `Class` column "
        "containing `POSITIVE`/`NEGATIVE` ground-truth labels for evaluation). "
        "The file should be semicolon-delimited (`;`), matching the original dataset format."
    )

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    delimiter = st.text_input("CSV delimiter", value=";")

    use_sample = st.checkbox("Use bundled sample dataset instead", value=not bool(uploaded_file))

    df = None
    if uploaded_file is not None and not use_sample:
        df = pd.read_csv(uploaded_file, delimiter=delimiter)
    elif use_sample:
        try:
            df = pd.read_csv("data/sample_reviews.csv", delimiter=";")
        except FileNotFoundError:
            st.warning("No bundled sample dataset found at data/sample_reviews.csv. Please upload a file.")

    if df is not None:
        if "Review" not in df.columns:
            st.error("CSV must contain a 'Review' column.")
        else:
            st.write("### Preview of uploaded data")
            st.dataframe(df.head())

            if st.button("Run Sentiment Analysis on Dataset", type="primary"):
                reviews = df["Review"].tolist()

                with st.spinner(f"Analyzing {len(reviews)} reviews..."):
                    predicted_labels = classifier(reviews)

                results_df = df.copy()
                results_df["Predicted Sentiment"] = [p["label"] for p in predicted_labels]
                results_df["Confidence"] = [round(p["score"], 4) for p in predicted_labels]

                st.write("### Results")
                st.dataframe(results_df)

                csv_out = results_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download results as CSV",
                    data=csv_out,
                    file_name="sentiment_results.csv",
                    mime="text/csv",
                )

                # Evaluation if ground-truth labels exist
                if "Class" in df.columns:
                    st.write("### Evaluation against ground truth")
                    real_labels = df["Class"].tolist()

                    references = [1 if label == "POSITIVE" else 0 for label in real_labels]
                    predictions = [1 if p["label"] == "POSITIVE" else 0 for p in predicted_labels]

                    acc_result = accuracy_metric.compute(
                        references=references, predictions=predictions
                    )["accuracy"]
                    f1_result = f1_metric.compute(
                        references=references, predictions=predictions
                    )["f1"]

                    col1, col2 = st.columns(2)
                    col1.metric("Accuracy", f"{acc_result:.2%}")
                    col2.metric("F1 Score", f"{f1_result:.2%}")
                else:
                    st.info(
                        "No 'Class' column found — skipping accuracy/F1 evaluation. "
                        "Add a 'Class' column with POSITIVE/NEGATIVE labels to enable it."
                    )

st.markdown("---")
st.caption("Adapted from the original 'Analyzing KGF 2 movie review with LLMs/GenAI' notebook.")
