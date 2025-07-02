import streamlit as st
import requests
import numpy as np

st.set_page_config(page_title="Shlok", layout="centered")

st.title("Cosmic Radiation Origin and Risks")

# --- Intro Section ---
st.subheader("🔬 Understanding Cosmic Radiation Risks")
st.markdown("""
Cosmic radiation is a form of high-energy radiation that originates from outside Earth’s atmosphere.  
There are two main types relevant to space missions:
- **Galactic Cosmic Rays (GCRs)**: Constant background radiation from deep space.
- **Solar Energetic Particles (SEPs)**: Burst-like radiation from solar flares and CMEs.

These can cause:
- Cellular damage  
- Increased cancer risk  
- Radiation sickness on long missions

The solar cycle affects the intensity of this radiation, as shown below:
""")

# --- Solar Cycle Image from NOAA ---
st.image("https://services.swpc.noaa.gov/json/solar-cycle/cycle_update.png", caption="NOAA Solar Cycle Status", use_column_width=True)

st.divider()  # visual break before calculator

# --- Radiation Risk Calculator Section ---
st.subheader("🧮 Radiation Risk Calculator")
st.info("This tool estimates the radiation dose and cancer risk for a space mission based on real-time solar particle flux and selected shielding.")

# Inputs
mission_days = st.slider("Mission Duration (days)", 1, 1000, 180)
shielding_material = st.selectbox("Shielding Material", ["None", "Aluminum", "Polyethylene"])

# Real-time proton flux from NOAA
url = "https://services.swpc.noaa.gov/json/goes/primary/differential-proton-flux-1-day.json"

try:
    data = requests.get(url).json()
    flux = float(data[-1]['flux'])  # protons/cm²/s/sr
    st.success(f"Live Proton Flux (≥10 MeV): {flux:.2e} protons/cm²/s/sr")
except:
    flux = 100  # fallback if API fails
    st.warning("Unable to fetch live data. Using default flux: 100 p/cm²/s/sr")

# Simplified dose model
base_dose_per_day = flux * 0.00005  # empirical approximation
shield_factors = {'None': 1.0, 'Aluminum': 0.7, 'Polyethylene': 0.5}
daily_dose = base_dose_per_day * shield_factors[shielding_material]
total_dose = daily_dose * mission_days  # in mSv

# Cancer risk estimate
risk_percent = (total_dose / 1000) * 5  # linear ERR model

st.metric("☢ Estimated Total Dose (mSv)", f"{total_dose:.2f}")
st.metric("⚠ Estimated Cancer Risk", f"{risk_percent:.2f} %")

st.caption("ICRP model: 5% risk increase per 1 Sv of exposure. Not for clinical use.")
