import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AGRFS | Intelligence Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM MODERN STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .status-card { padding: 20px; border-radius: 10px; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🌊 AGRFS Intelligence Hub")
st.write("Aero-Elastic Galloping River Filtration System | Engineering DSS")
st.divider()

# --- SIDEBAR: DYNAMIC CONTROLS ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/water-filter.png", width=80)
    st.header("Control Panel")
    
    # Input group for River conditions
    with st.expander("🌍 River Environment", expanded=True):
        velocity = st.slider("Current Velocity (m/s)", 0.0, 2.0, 0.8, step=0.05)
        turbidity = st.select_slider("Inlet Water Quality", options=["Low", "Medium", "High"])

    # Input group for Maintenance
    with st.expander("🛠️ Operational Parameters", expanded=True):
        maint_freq = st.number_input("Maintenance Cycles / Month", 1, 15, 3)
        labor_cost = st.slider("Local Labor Rate (INR/hr)", 100, 500, 250)

# --- LOGIC ENGINE (Derived from Sheet 2 & 3) ---
# Hard constants from your Validated Model
MIN_VELO = 0.5
MAX_VELO = 1.5
TARGET_LPH = 8.0
AGITATOR_KG = 15

# Calculate Live Output
if velocity < MIN_VELO:
    output = 0.0
    status = "🔴 SYSTEM IDLE (Below Cut-in)"
elif velocity > MAX_VELO:
    output = 0.0
    status = "⚠️ CRITICAL FAILURE (Structural Risk)"
else:
    output = (velocity / 0.8) * TARGET_LPH
    status = "🟢 OPERATIONAL (Optimal Galloping)"

# Calculate Safety (RPN)
rpn = AGITATOR_KG * maint_freq
exo_needed = rpn >= 15

# --- TOP ROW: KPI METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Live Purification", f"{output:.2f} L/hr", delta=f"{output-8:.1f} vs Target")
m2.metric("Safety Index (RPN)", rpn, delta="Exo Required" if exo_needed else "Manual OK", delta_color="inverse" if exo_needed else "normal")
m3.metric("System Efficiency", "14.2%", help="Calculated kinetic capture efficiency")
m4.metric("Est. Monthly OPEX", f"₹{maint_freq * labor_cost}")

st.divider()

# --- MIDDLE ROW: INTERACTIVE VISUALS ---
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Performance Response Curve")
    v_axis = np.linspace(0, 2, 100)
    # Vectorized logic for the curve
    o_axis = np.where((v_axis >= MIN_VELO) & (v_axis <= MAX_VELO), (v_axis/0.8)*TARGET_LPH, 0)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=v_axis, y=o_axis, fill='tozeroy', name='Output (L/hr)', line=dict(color='#00d1ff', width=3)))
    fig.add_vline(x=velocity, line_dash="dash", line_color="white", annotation_text="Current")
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20), height=400,
                      xaxis_title="River Velocity (m/s)", yaxis_title="Filtered Water (L/hr)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("System Status")
    st.markdown(f"### {status}")
    if exo_needed:
        st.warning("🚨 **Mandatory:** Upper Body Exoskeleton required for maintenance at this frequency to prevent musculoskeletal strain.")
    else:
        st.success("✅ Maintenance tasks within ergonomic limits for manual labor.")
    
    # Progress bar for Budget Control
    progress = min(100, int((15000/15000)*100)) # Placeholder for real-time budget tracking
    st.write(f"Fabrication Budget Utilization: **₹15,000 / ₹15,000**")
    st.progress(progress)

# --- BOTTOM ROW: DATA TABLES ---
st.divider()
with st.expander("📂 View Underlying Model Data (Sheet 1: Matrix)"):
    # Modern styled dataframe
    matrix_data = {
        "Criterion": ["Galloping Response", "Pressure Consistency", "Energy Efficiency", "Fabricability", "Mechanical Novelty"],
        "D1 (Baseline)": [1, 1, 1, 4, 1],
        "D3 (Final AGRFS)": [5, 5, 5, 4, 5]
    }
    st.dataframe(pd.DataFrame(matrix_data), use_container_width=True)

st.caption("Developed for TIET ECE / IITM Data Science | Model V4.2 Validated for Brahma-River Specs.")