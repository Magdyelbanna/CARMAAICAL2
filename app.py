
import streamlit as st
import pandas as pd
import numpy as np

# --- Constants ---
HOURLY_RATES = {
    "Social Monitoring": 14.63,
    "Analysis": 16.07,
    "Executive Report": 16.70,
    "Print Monitoring": 13.67,
    "Online Media": 15.25
}

SETUP_HOURS = {
    "Print": {5: 1, 15: 3, 30: 8},
    "Online": {5: 1, 15: 3, 30: 8}
}

COST_PER_KEYWORD = 2.5
COST_PER_PLATFORM = 1.8
COST_PER_ALERT = 0.75

# --- Page Config ---
st.set_page_config(page_title="CARMA AI Cost Estimator", layout="wide")
st.title("🤖 CARMA AI-Powered Cost Estimator")

# --- Sidebar Inputs ---
st.sidebar.header("📝 Input Configuration")
region = st.sidebar.selectbox("Region", ["MENA", "GCC", "North Africa", "Global"])
country = st.sidebar.selectbox("Country (Print/Online)", ["UAE", "KSA", "Egypt", "Morocco", "Qatar"])
project_duration = st.sidebar.selectbox("Project Duration (months)", [3, 6, 12])
conversion_rate = st.sidebar.number_input("LCY Conversion Rate (e.g., 3.67 for AED to USD)", min_value=0.01, value=3.67)

service_type = st.sidebar.selectbox("Service Type", list(HOURLY_RATES.keys()))
keywords = st.sidebar.slider("Number of Keywords", 1, 50, 15)
platforms = st.sidebar.multiselect("Select Platforms", ["Facebook", "Instagram", "TikTok", "LinkedIn", "YouTube"])
languages = st.sidebar.multiselect("Languages (Online Media)", ["Arabic", "English", "French", "Urdu", "Hindi", "Russian", "Chinese"])
daily_alerts = st.sidebar.slider("Number of Daily Alerts", 0, 10, 3)
extra_hours = st.sidebar.slider("Additional Manual Hours", 0, 20, 0)

# --- Setup Cost Calculation ---
def calculate_setup_cost(media_type, keyword_count):
    tier = min(keyword_count, 30)
    if tier <= 5:
        setup_hour = SETUP_HOURS[media_type][5]
    elif tier <= 15:
        setup_hour = SETUP_HOURS[media_type][15]
    else:
        setup_hour = SETUP_HOURS[media_type][30]
    return setup_hour * 36.38

# --- Monthly Cost Calculation ---
def calculate_monthly_cost(service, alerts, platforms, keywords, extra_hours, language_count):
    hourly_rate = HOURLY_RATES.get(service, 0)
    base_hours = (
        alerts * COST_PER_ALERT +
        keywords * COST_PER_KEYWORD +
        len(platforms) * COST_PER_PLATFORM +
        language_count * 1.2
    )
    total_hours = base_hours + extra_hours
    return total_hours * hourly_rate

# --- Quote Calculation ---
setup_cost = calculate_setup_cost("Online" if service_type == "Online Media" else "Print", keywords)
monthly_cost = calculate_monthly_cost(service_type, daily_alerts, platforms, keywords, extra_hours, len(languages))
total_cost_usd = setup_cost + (monthly_cost * project_duration)
total_cost_lcy = total_cost_usd * conversion_rate

# --- Output ---
st.subheader("📊 Cost Breakdown")
st.write(f"**Region:** {region}")
st.write(f"**Country:** {country}")
st.write(f"**Project Duration:** {project_duration} months")
st.write(f"**Conversion Rate:** {conversion_rate}")
st.write(f"**Setup Cost (USD):** ${setup_cost:,.2f}")
st.write(f"**Monthly Cost (USD):** ${monthly_cost:,.2f}")
st.write(f"**Total Project Cost (USD):** ${total_cost_usd:,.2f}")
st.write(f"**Total Project Cost (LCY):** {total_cost_lcy:,.2f}")

# --- AI Summary ---
st.markdown("---")
st.subheader("🧠 Natural Language Summary")
st.info(
    f"You're quoting a {project_duration}-month {service_type} project in {country} ({region}), "
    f"tracking {keywords} keywords in {len(languages)} language(s) across {len(platforms)} platform(s), "
    f"with {daily_alerts} daily alerts and {extra_hours} manual hours. "
    f"Total cost in LCY: {total_cost_lcy:,.2f}."
)

# --- Export ---
st.download_button("📥 Export as CSV", pd.DataFrame.from_dict({
    "Region": [region],
    "Country": [country],
    "Service Type": [service_type],
    "Project Duration (months)": [project_duration],
    "Conversion Rate": [conversion_rate],
    "Setup Cost (USD)": [setup_cost],
    "Monthly Cost (USD)": [monthly_cost],
    "Total Cost (USD)": [total_cost_usd],
    "Total Cost (LCY)": [total_cost_lcy]
}).to_csv(index=False), file_name="carma_quote.csv")
