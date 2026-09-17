from __future__ import annotations

import streamlit as st

st.title("Darukaa Biodiversity Intelligence")

st.write("Enter land and biodiversity metrics, or ask a question about the site.")

with st.form("metrics_form"):
    soc = st.number_input("Soil organic carbon (%)", value=0.0)
    rainfall = st.number_input("Annual rainfall (mm)", value=0.0)
    land_use = st.text_input("Land use")
    region = st.text_input("Region")
    submitted = st.form_submit_button("Generate recommendation")

if submitted:
    st.success(
        "Recommendation workflow ready. Connect the backend reasoning and retrieval pipeline here."
    )
    st.json({
        "soc": soc,
        "rainfall": rainfall,
        "land_use": land_use,
        "region": region,
    })
