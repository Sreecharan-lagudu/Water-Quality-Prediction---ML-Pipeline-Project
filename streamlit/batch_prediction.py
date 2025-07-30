import streamlit as st
import pandas as pd
import joblib
import requests
from sklearn.preprocessing import LabelEncoder

# Load model and encoders
model = joblib.load("water_quality_model.pkl")
encoder_source = LabelEncoder().fit(["River", "Lake", "Groundwater", "Well"])
encoder_color = LabelEncoder().fit(["Clear", "Brown", "Yellow", "Green"])
encoder_odor = LabelEncoder().fit(["Odorless", "Foul", "Metallic"])
encoder_time = LabelEncoder().fit(["Morning", "Afternoon", "Evening", "Night"])

FASTAPI_SAVE_URL = "http://127.0.0.1:8000/save_predictions/"

def batch_prediction():
    st.header("Batch Prediction via CSV Upload")
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file is not None:
        original_data = pd.read_csv(uploaded_file)
        st.write("Preview of Uploaded Data:")
        st.dataframe(original_data)

        # Handle missing or unknown values
        original_data["Source"] = original_data["Source"].fillna("River")
        original_data["Color"] = original_data["Color"].fillna("Clear")
        original_data["Odor"] = original_data["Odor"].fillna("Odorless")
        original_data["Time of Day"] = original_data["Time of Day"].fillna("Morning")

        # Encode categorical columns
        input_data = original_data.copy()
        input_data["Source"] = encoder_source.transform(input_data["Source"])
        input_data["Color"] = encoder_color.transform(input_data["Color"])
        input_data["Odor"] = encoder_odor.transform(input_data["Odor"])
        input_data["Time of Day"] = encoder_time.transform(input_data["Time of Day"])

        if st.button("Predict Batch Data"):
            predictions = model.predict(input_data)
            original_data["Prediction"] = predictions
            st.write("Prediction Results:")
            st.dataframe(original_data)

            # Prepare payload for FastAPI
            batch_payloads = []
            for _, row in original_data.iterrows():
                payload = {
                    "ph": row["pH"], "iron": row["Iron"], "nitrate": row["Nitrate"],
                    "chloride": row["Chloride"], "lead": row["Lead"], "zinc": row["Zinc"],
                    "color": row["Color"], "turbidity": row["Turbidity"], "fluoride": row["Fluoride"],
                    "copper": row["Copper"], "odor": row["Odor"], "sulfate": row["Sulfate"],
                    "conductivity": row["Conductivity"], "chlorine": row["Chlorine"],
                    "manganese": row["Manganese"], "tds": row["Total Dissolved Solids"],
                    "source": row["Source"], "water_temp": row["Water Temperature"],
                    "air_temp": row["Air Temperature"], "month": row["Month"], "day": row["Day"],
                    "time_of_day": row["Time of Day"], "prediction": row["Prediction"],
                }
                batch_payloads.append(payload)

            try:
                response = requests.post(FASTAPI_SAVE_URL, json=batch_payloads)
                if response.status_code == 200:
                    st.info("Batch predictions saved to database successfully.")
                else:
                    st.error(f"Error saving batch predictions: {response.text}")
            except Exception as e:
                st.error(f"Error in sending batch predictions: {e}")