import json

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Aqua Predict — Live Demo", layout="wide")

with st.sidebar:
    st.title("💧 Aqua Predict")
    st.caption("Water Quality Prediction — live demo")
    st.markdown(
        "[Code on GitHub](https://github.com/Sreecharan-lagudu/"
        "Water-Quality-Prediction---ML-Pipeline-Project)"
    )
    st.markdown(
        "The full pipeline (PostgreSQL + FastAPI + Streamlit) runs locally — "
        "this demo serves the trained model directly."
    )

@st.cache_resource
def load_model():
    return joblib.load("water_quality_model.pkl")

@st.cache_data
def load_meta():
    with open("demo/ui_meta.json") as f:
        return json.load(f)

model = load_model()
meta = load_meta()
cats = meta.get("cats", {})
cols = meta["columns"]

st.header("🔬 Will this water pass the quality test?")
st.write("Enter sensor measurements below — the model predicts whether the sample is safe.")

def num_input(key, label, lo=0.0, hi=100.0, val=10.0, step=0.1):
    return st.number_input(label, min_value=float(lo), max_value=float(hi), value=float(val), step=step, key=key)

row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)
row5 = st.columns(3)
row6 = st.columns(3)
row7 = st.columns(3)

widgets = {}
grid = [row1, row2, row3, row4, row5, row6, row7]

numeric_specs = [
    ("pH", 0.0, 14.0, 7.0), ("Iron", 0.0, 5.0, 0.1), ("Nitrate", 0.0, 50.0, 5.0),
    ("Chloride", 0.0, 500.0, 50.0), ("Lead", 0.0, 1.0, 0.05), ("Zinc", 0.0, 10.0, 1.0),
    ("Turbidity", 0.0, 20.0, 2.0), ("Fluoride", 0.0, 5.0, 0.5), ("Copper", 0.0, 5.0, 0.5),
    ("Sulfate", 0.0, 500.0, 50.0), ("Conductivity", 0.0, 2000.0, 200.0), ("Chlorine", 0.0, 10.0, 1.0),
    ("Manganese", 0.0, 1.0, 0.05), ("Total Dissolved Solids", 0.0, 1000.0, 100.0),
    ("Water Temperature", 0.0, 40.0, 15.0), ("Air Temperature", -10.0, 50.0, 20.0),
    ("Day", 1, 31, 15),
]
cat_specs = ["Source", "Color", "Month"]
odor_key, tod_key = "Odor", "Time of Day"

cells = [c for r in grid for c in r]
idx = 0
for name, lo, hi, val in numeric_specs:
    with cells[idx % 3]:
        widgets[name] = num_input("n_" + name, name + ((" (mg/L)" if name not in ("pH", "Day", "Water Temperature", "Air Temperature") else "")), lo, hi, val)
    idx += 1

for name in cat_specs:
    with cells[idx % 3]:
        if name in cats:
            widgets[name] = st.selectbox(name, cats[name], key="c_" + name)
        else:
            widgets[name] = st.number_input(name, min_value=0, value=0, key="c_" + name)
    idx += 1

with cells[idx % 3]:
    if "odor_min" in meta:
        widgets[odor_key] = st.slider("Odor", meta["odor_min"], meta["odor_max"], meta["odor_min"], key="o_odor")
    else:
        widgets[odor_key] = st.number_input("Odor", 0.0, 100.0, 0.0, key="o_odor")
with cells[idx % 3]:
    if "tod_min" in meta:
        widgets[tod_key] = st.slider("Time of Day", meta["tod_min"], meta["tod_max"], meta["tod_min"], key="o_tod")
    else:
        widgets[tod_key] = st.number_input("Time of Day", 0.0, 24.0, 12.0, key="o_tod")

st.divider()

if st.button("🚰 Predict Water Quality", type="primary", use_container_width=True):
    # Encode categorical values exactly like training (alphabetical index)
    def enc(col, value):
        if col in cats:
            return cats[col].index(str(value))
        return value

    input_row = [enc(c, widgets[c]) if c in cat_specs or c in (odor_key, tod_key) and False else widgets[c] for c in cols]
    # (numeric widgets pass through unchanged; cat columns get encoded above)
    input_row = []
    for c in cols:
        if c in cat_specs:
            input_row.append(enc(c, widgets[c]))
        else:
            input_row.append(widgets[c])

    proba = model.predict_proba([input_row])[0]
    pred = int(model.classes_[proba.argmax()])

    c1, c2 = st.columns(2)
    with c1:
        if pred == 1:
            st.success(f"✅ **Prediction: SAFE** — passes the quality test")
        else:
            st.error(f"🚫 **Prediction: NOT SAFE** — fails the quality test")
        st.metric("Safe probability", f"{proba[1]:.1%}" if len(proba) > 1 else f"{proba[0]:.1%}")
        st.progress(proba[1] if len(proba) > 1 else 1 - proba[0])
    with c2:
        st.subheader("What the model looks at")
        importances = pd.Series(model.feature_importances_, index=cols).sort_values(ascending=True)
        st.bar_chart(importances.tail(10))
        st.caption("Top 10 features by RandomForest importance")
