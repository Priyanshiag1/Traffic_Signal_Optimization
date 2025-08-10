import streamlit as st
import os
from optimizer import run_optimization, manual_check

st.set_page_config(page_title="Traffic Optimizer", layout="centered")

# 🛑 App Title & Instructions
st.title("🚦 Traffic Signal Optimizer")
st.markdown("Use this tool to optimize green times based on selected cycle length and saturation rate.")

# 🎬 Show the traffic animation **below the title**
video_path = os.path.join(os.path.dirname(__file__), 'Traffic.mp4')
if os.path.exists(video_path):
    with open(video_path, 'rb') as video_file:
        video_bytes = video_file.read()
        st.video(video_bytes)  # This will display the animation
else:
    st.error(f"🚫 Video file not found: {video_path}")

# 🚧 User Inputs
cycle_time = st.slider("Set Cycle Length (sec)", min_value=120, max_value=400, value=240)
sat_rate = st.number_input("Saturation Flow Rate (vehicles/sec)", min_value=0.1, max_value=2.0, value=0.5)

# 🔁 Run Optimization
if st.button("Run Optimization"):
    opt_green, opt_served, phase_demand, green_phases = run_optimization(cycle_time, sat_rate)
    manual_check(opt_green, opt_served, phase_demand, green_phases, cycle_time, sat_rate)
