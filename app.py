import streamlit as st
import pandas as pd
from engine import run_simulation
st.title("🚀 TCP Congestion Control Simulator")
st.write("Compare how different TCP algorithms react to network traffic jams and packet loss in real time.")
st.sidebar.header("Network Settings")
algorithm = st.sidebar.selectbox("Choose TCP Algorithm", ["Tahoe", "Reno"])
ticks = st.sidebar.slider("Simulation Duration (Ticks)", 50, 500, 200)
loss_rate = st.sidebar.slider("Packet Loss Rate (%)", 0.0, 20.0, 5.0) / 100.0
if st.button("Run Simulation"):
    data = run_simulation(ticks=ticks, loss_rate=loss_rate, algorithm=algorithm)
    df = pd.DataFrame(data)
    st.subheader(f"Results for TCP {algorithm}")
    st.line_chart(df.set_index("Tick")[["CongestionWindow", "Ssthresh"]])
    st.success("Simulation complete! Notice the 'sawtooth' pattern — when packet loss occurs, Tahoe drops back to 1, while Reno handles it more smoothly.")