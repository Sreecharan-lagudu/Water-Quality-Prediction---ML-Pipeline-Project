import streamlit as st
import requests

FASTAPI_GET_URL = "http://127.0.0.1:8000/get_predictions/"

def past_predictions():
    st.header("Past Predictions")
    st.write("Select a date range to filter past predictions (leave empty to fetch all):")

    # Date inputs
    start = st.date_input("Start Date", value=None)
    end = st.date_input("End Date", value=None)

    # Build query parameters
    params = {}
    if start:
        params["start_date"] = start.isoformat()
    if end:
        params["end_date"] = end.isoformat()

    if st.button("Fetch Predictions"):
        try:
            response = requests.get(FASTAPI_GET_URL, params=params)
            if response.status_code == 200:
                predictions = response.json()
                if predictions:
                    st.dataframe(predictions)
                else:
                    st.info("No predictions found for the selected date range.")
            else:
                st.error("Error fetching predictions from database.")
        except Exception as e:
            st.error(f"Error: {e}")