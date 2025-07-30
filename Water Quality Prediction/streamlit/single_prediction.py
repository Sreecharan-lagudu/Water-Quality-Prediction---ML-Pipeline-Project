import streamlit as st
import joblib
import requests
from datetime import datetime
from sklearn.preprocessing import LabelEncoder

# Load model and encoders
model = joblib.load("water_quality_model.pkl")
encoder_source = LabelEncoder().fit(["River", "Lake", "Groundwater", "Well"])
encoder_color = LabelEncoder().fit(["Clear", "Brown", "Yellow", "Green"])
encoder_odor = LabelEncoder().fit(["Odorless", "Foul", "Metallic"])
encoder_time = LabelEncoder().fit(["Morning", "Afternoon", "Evening", "Night"])

FASTAPI_SAVE_URL = "http://127.0.0.1:8000/save_predictions/"

def single_prediction():
    st.header("Input Water Quality Parameters")

    # Numeric Input Fields
    ph = st.number_input("pH", min_value=0.0, max_value=14.0, step=0.1)
    iron = st.number_input("Iron (mg/L)", step=0.1)
    nitrate = st.number_input("Nitrate (mg/L)", step=0.1)
    chloride = st.number_input("Chloride (mg/L)", step=0.1)
    lead = st.number_input("Lead (mg/L)", step=0.1)
    zinc = st.number_input("Zinc (mg/L)", step=0.1)
    turbidity = st.number_input("Turbidity (NTU)", step=0.1)
    fluoride = st.number_input("Fluoride (mg/L)", step=0.1)
    copper = st.number_input("Copper (mg/L)", step=0.1)
    sulfate = st.number_input("Sulfate (mg/L)", step=0.1)
    conductivity = st.number_input("Conductivity (μS/cm)", step=1.0)
    chlorine = st.number_input("Chlorine (mg/L)", step=0.1)
    manganese = st.number_input("Manganese (mg/L)", step=0.1)
    tds = st.number_input("Total Dissolved Solids (mg/L)", step=1.0)
    water_temp = st.number_input("Water Temperature (°C)", step=0.1)
    air_temp = st.number_input("Air Temperature (°C)", step=0.1)
    month = st.slider("Month", 1, 12, 1)
    day = st.slider("Day", 1, 31, 1)

    # Categorical Input Fields
    source = st.selectbox("Source", ["River", "Lake", "Groundwater", "Well"])
    color = st.selectbox("Color", ["Clear", "Brown", "Yellow", "Green"])
    odor = st.selectbox("Odor", ["Odorless", "Foul", "Metallic"])
    time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night"])

    # Encode categorical values
    source_encoded = encoder_source.transform([source])[0]
    color_encoded = encoder_color.transform([color])[0]
    odor_encoded = encoder_odor.transform([odor])[0]
    time_encoded = encoder_time.transform([time_of_day])[0]

    # Prepare data for prediction
    input_data = [
        ph, iron, nitrate, chloride, lead, zinc, color_encoded, turbidity, fluoride,
        copper, odor_encoded, sulfate, conductivity, chlorine, manganese, tds,
        source_encoded, water_temp, air_temp, month, day, time_encoded,
    ]

    if st.button("Predict Water Quality"):
        prediction = model.predict([input_data])[0]
        st.success(f"Predicted Water Quality: {prediction:.2f}")

        # Prepare payload for FastAPI
        payload = {
            "ph": ph, "iron": iron, "nitrate": nitrate, "chloride": chloride,
            "lead": lead, "zinc": zinc, "color": color, "turbidity": turbidity,
            "fluoride": fluoride, "copper": copper, "odor": odor, "sulfate": sulfate,
            "conductivity": conductivity, "chlorine": chlorine, "manganese": manganese,
            "tds": tds, "source": source, "water_temp": water_temp, "air_temp": air_temp,
            "month": month, "day": day, "time_of_day": time_of_day, "prediction": prediction,
        }

        try:
            response = requests.post(FASTAPI_SAVE_URL, json=[payload])
            if response.status_code == 200:
                st.info("Prediction saved to database successfully.")
            else:
                st.error("Error saving prediction to database.")
        except Exception as e:
            st.error(f"Error: {e}")