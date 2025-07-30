import streamlit as st
from single_prediction import single_prediction
from batch_prediction import batch_prediction
from past_predictions import past_predictions

# Page Config
st.set_page_config(page_title="Aqua Predict", layout="centered")

# Initializing session state for mode
if "mode" not in st.session_state:
    st.session_state.mode = None

# Navigation buttons 
st.sidebar.header("Menu")
if st.sidebar.button("Home"):
    st.session_state.mode = None  # Reset to main page
if st.sidebar.button("Single Prediction"):
    st.session_state.mode = "Single Prediction"
if st.sidebar.button("Batch Prediction"):
    st.session_state.mode = "Batch Prediction"
if st.sidebar.button("Past Predictions"):
    st.session_state.mode = "Past Predictions"

# Display main page content only if no mode is selected
if st.session_state.mode is None:
    st.title("Aqua Predict")

# ----- Single Prediction Mode -----
if st.session_state.mode == "Single Prediction":
    single_prediction()

# ----- Batch Prediction Mode -----
elif st.session_state.mode == "Batch Prediction":
    batch_prediction()

# ----- View Past Predictions Mode -----
elif st.session_state.mode == "Past Predictions":
    past_predictions()