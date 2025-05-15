
# AI-Powered Cost Calculator (Prototype v1)
# Note: This is a Python (Streamlit-based) app that mirrors your Excel logic with AI inputs.

import streamlit as st
import pandas as pd
import numpy as np

# --- Constants (mocked for now, real logic can be inserted from your Excel formulas) ---
HOURLY_RATES = {
    "Social Monitoring": 14.63,
    "Analysis": 16.07,
    "Executive Report": 16.70,
    "Print Monitoring": 13.67
}

SETUP_HOURS = {
    "Print": {5: 1, 15: 3, 30: 8},
    "Online": {5: 1, 15: 3, 30: 8}
}

COST_PER_KEYWORD = 2.5  # Example: internal multiplier logic
COST_PER_PLATFORM = 1.8  # Per platform complexity factor
COST_PER_ALERT = 0.75   # Daily alert labor load per month

# --- Page Config ---
st.set_page_config(page_title="CARMA AI Cost Estimator", layout="wide")
st.title("🤖 CARMA AI-Powered Cost Estimator")

# --- User Inputs ---
st.sidebar.header("📝 Input Configuration")
service_type = st.sidebar.selectbox("Service Type", list(HOURLY_RATES.keys()))
keywords = st.sidebar.slider("Number of Keywords", 1, 50, 15)
platforms = st.sidebar.multiselect("Select Platforms", ["Facebook", "Instagram", "TikTok", "LinkedIn", "YouTube"])
duration_months = st.sidebar.selectbox("Coverage Duration (Months)", [3, 6, 12])
daily_alerts = st.sidebar.slider("Number of Daily Alerts", 0, 10, 3)
extra_hours = st.sidebar.slider("Additional Manual Hours (if needed)", 0, 20, 0)

# --- Setup Cost ---
def calculate_setup_cost(media_type, keyword_count):
    tier = min(keyword_count, 30)
    if tier <= 5:
        setup_hour = SETUP_HOURS[media_type][5]
    elif tier <= 15:
        setup_hour = SETUP_HOURS[media_type][15]
    else:
        setup_hour = SETUP_HOURS[media_type][30]
    return setup_hour * 36.38

# --- Monthly Cost ---
def calculate_monthly_cost(service, alerts, platforms, keywords, extra_hours):
    hourly_rate = HOURLY_RATES.get(service, 0)
    base_hours = (alerts * COST_PER_ALERT + keywords * COST_PER_KEYWORD + len(platforms) * COST_PER_PLATFORM)
    total_hours = base_hours + extra_hours
    return total_hours * hourly_rate

# --- Quote Calculation ---
setup_cost = calculate_setup_cost("Print", keywords)
monthly_cost = calculate_monthly_cost(service_type, daily_alerts, platforms, keywords, extra_hours)
total_cost = setup_cost + (monthly_cost * duration_months)

# --- Output ---
st.subheader("📊 Cost Breakdown")
st.write(f"**Setup Cost:** ${setup_cost:,.2f}")
st.write(f"**Monthly Cost:** ${monthly_cost:,.2f}")
st.write(f"**Total Project Cost ({duration_months} months):** ${total_cost:,.2f}")

# --- AI Prompt Preview ---
st.markdown("---")
st.subheader("🧠 Natural Language Summary")
st.info(f"You're quoting a {duration_months}-month {service_type} package, tracking {keywords} keywords across {len(platforms)} platforms with {daily_alerts} alerts/day. Manual extra hours added: {extra_hours}.")

# --- Export ---
st.download_button("📥 Export as CSV", pd.DataFrame.from_dict({
    "Setup Cost": [setup_cost],
    "Monthly Cost": [monthly_cost],
    "Total Cost": [total_cost]
}).to_csv(index=False), file_name="carma_quote.csv")
