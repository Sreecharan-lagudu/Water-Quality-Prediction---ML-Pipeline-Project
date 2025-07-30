import joblib
from sklearn.preprocessing import LabelEncoder

def load_model():
    return joblib.load("water_quality_model.pkl")

def load_encoders():
    encoder_source = LabelEncoder().fit(["River", "Lake", "Groundwater", "Well"])
    encoder_color = LabelEncoder().fit(["Clear", "Brown", "Yellow", "Green"])
    encoder_odor = LabelEncoder().fit(["Odorless", "Foul", "Metallic"])
    encoder_time = LabelEncoder().fit(["Morning", "Afternoon", "Evening", "Night"])
    return encoder_source, encoder_color, encoder_odor, encoder_time