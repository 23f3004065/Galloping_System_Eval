import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(page_title="AGRFS | Strategic DSS", page_icon="🛡️", layout="wide")

# --- EXPANSIVE UI STYLING ---
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .stMetric { border-radius: 15px; background-color: #161b22; border: 1px solid #30363d; padding: 20px; }
    .stExpander { border-radius: 12px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & PROJECT SCOPE ---
st.title("🛡️ AGRFS Strategic Command Center")
st.markdown("""
**The Problem:** Rural river communities lack decentralized, low-cost water purification.  
**The Solution:** An Aero-Elastic Galloping system that captures river kinetic energy to power a 0.02μm filtration unit.
""")

# --- GLOBAL LOGIC ENGINE ---
MIN_V = 0.5
MAX_V = 1.5
TARGET_LPH = 8.0

# Sidebar with Explanation tooltips
with st.sidebar:
    st.header("⚙️ Simulation Settings")
    sim_v = st.slider("River Velocity (m/s)", 0.0, 2.0, 0.8, help="Simulates real river flow. Cut-in is 0.5m/s.")
    sim_maint = st.slider("Monthly Maint. Cycles", 1, 10, 3, help="How often the membrane is cleaned.")
    
# Logic Calculations
is_active = MIN_V <= sim_v <= MAX_V
out_lph = (sim_v / 0.8) * TARGET_LPH if is_active else 0
rpn = 15 * sim_maint  # Weight(15kg) * Frequency
exo_status = "MANDATORY" if rpn >= 15 else "OPTIONAL"

# --- SECTION 1: DYNAMIC KPI DASHBOARD ---
st.subheader("🚀 Live Operational Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Filtration Flux", f"{out_lph:.2f} L/hr", f"{sim_v} m/s")
c2.metric("Safety Strain (RPN)", rpn, exo_status, delta_color="inverse" if rpn >= 15 else "normal")
c3.metric("System Health", "STABLE" if is_active else "OFFLINE")
c4.metric("Budget Headroom", "₹800", "Under ₹15K Cap")

# --- SECTION 2: THE "HOW IT WORKS" EXPLAINER ---
st.divider()
tab1, tab2, tab3 = st.tabs(["📊 Performance Analysis", "🧬 Mechanical Theory", "🧤 Ergonomic Safety"])

with tab1:
    st.subheader("Galloping Response Curve")
    v_ax = np.linspace(0, 2, 100)
    o_ax = np.where((v_ax >= MIN_V) & (v_ax <= MAX_V), (v_ax/0.8)*TARGET_LPH, 0)
    fig_p = px.area(x=v_ax, y=o_ax, labels={'x':'Velocity', 'y':'L/hr'}, title="System Output Sensitivity")
    fig_p.add_vline(x=sim_v, line_dash="dash", line_color="red")
    st.plotly_chart(fig_p, use_container_width=True)
    st.write("**Explanation:** The 'Hump' represents the optimal galloping zone. Outside 0.5-1.5 m/s, the system shuts down to prevent structural fatigue.")

with tab2:
    st.subheader("Design Selection Matrix (D1 vs D3)")
    # Pulling data from your Sheet 1 Matrix
    radar_data = pd.DataFrame(dict(
        r=[1, 1, 1, 4, 5, 1],
        theta=['Galloping','Pressure','Efficiency','Cost','Complexity','Novelty']))
    fig_r = px.line_polar(radar_data, r='r', theta='theta', line_close=True, title="Baseline Design (D1)")
    st.plotly_chart(fig_r, use_container_width=True)
    st.info("Design 3 (Final) improves 'Galloping' and 'Novelty' by 400% compared to Design 1.")

with tab3:
    st.subheader("Exoskeleton Justification")
    st.write(f"Current RPN: **{rpn}**. Standard safety limit: **15**.")
    st.progress(min(rpn/50, 1.0))
    st.write("""
    **Why the Exoskeleton?**  
    - Repetitive lifting of the 15kg agitator causes L5-S1 vertebrae compression.
    - The exoskeleton transfers load to the lower frame, reducing 'felt' RPN by 60%.
    """)

# --- SECTION 3: VIVA CHEAT SHEET ---
st.divider()
with st.expander("🎓 VIVA PREP: How to explain this to examiners"):
    st.markdown("""
    ### 1. What does the Excel do?
    It serves as the **Logic Anchor**. It stores hard engineering constants (like the 0.02μm pore size and ₹15,000 budget) and calculates the RPN (Risk Priority Number) for health safety.
    
    ### 2. How does the Dashboard improve the Excel?
    The Dashboard is a **Live Simulator**. While Excel is static, the Dashboard allows us to show 'What-If' scenarios—like how output drops to zero if the river slows down, or how maintenance frequency triggers a legal safety requirement for an exoskeleton.
    
    ### 3. Critical Talking Point: Poka-Yoke
    Design 3 includes 'Poka-Yoke' (Mistake Proofing). We added a mechanical stop to the agitator travel distance to ensure the user cannot over-compress the pump, extending system life to 5+ years.
    """)
