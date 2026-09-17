from __future__ import annotations

import streamlit as st

from darukaa_assignment.reasoning.recommender import build_recommendation

st.set_page_config(page_title="Darukaa Biodiversity Intelligence", page_icon="🌱")
st.title("Darukaa Biodiversity Intelligence")
st.caption("Evidence-backed land restoration recommendations")

with st.form("metrics_form"):
    message = st.text_area(
        "Question",
        value="How can I improve biodiversity on this farm?",
    )
    st.subheader("Site metrics")
    soc = st.number_input("Soil organic carbon (%)", value=0.0)
    ph = st.number_input("Soil pH", value=7.0)
    rainfall = st.number_input("Annual rainfall (mm)", value=0.0)
    land_use = st.text_input("Land use")
    region = st.text_input("Region")
    moisture = st.number_input("Soil moisture index", value=0.0)
    submitted = st.form_submit_button("Generate recommendation")

if submitted:
    metrics = {
        "soc": soc,
        "ph": ph,
        "rainfall": rainfall,
        "land_use": land_use,
        "region": region,
        "moisture": moisture,
    }
    missing = [name for name in ("soc", "ph", "rainfall", "land_use", "region") if not metrics[name]]
    if missing:
        st.warning("Please provide: " + ", ".join(missing))
    else:
        try:
            recommendation, grouped_sources = build_recommendation(message, metrics)
        except ValueError as error:
            st.error(str(error))
        else:
            st.subheader("Recommendation")
            st.write(recommendation.recommendation)
            st.write("**Mechanism:** " + recommendation.mechanism)
            st.write("**Impacted metrics:** " + ", ".join(recommendation.impacted_metrics))
            st.write("**Expected change:** " + recommendation.expected_change)
            st.write("**Time horizon:** " + recommendation.time_horizon)
            st.write("**Confidence:** " + recommendation.confidence)
            st.subheader("Evidence")
            for source in grouped_sources:
                with st.expander(f"{source['title']} ({len(source['matches'])} matches)"):
                    st.write(f"{source['source_org']} | {source['year']} | {source['domain']}")
                    st.write(source["url"])
                    for match in source["matches"][:2]:
                        st.caption(match)
