import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- PAGE ARCHITECTURE ---
st.set_page_config(page_title="AGRFS | Industrial Command", page_icon="⚙️", layout="wide")

# --- INDUSTRIAL SLEEK THEME (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e1e1e1; }
    div[data-testid="stMetricValue"] { font-family: 'Courier New', monospace; color: #00f2ff; font-weight: bold; }
    .stMetric { background-color: #1a1f29; border: 1px solid #2d333b; border-radius: 8px; padding: 15px; }
    .plot-container { border: 1px solid #2d333b; border-radius: 12px; background-color: #161b22; }
    h1, h2, h3 { color: #ffffff; font-family: 'Inter', sans-serif; }
    .caption-text { font-size: 0.85rem; color: #8b949e; line-height: 1.4; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- GLOBAL DATA CONSTANTS ---
# Pulled from Sheet2_Constraints
MIN_V = 0.5
MAX_V = 1.5
NOMINAL_V = 0.8
TARGET_LPH = 8.0
BUDGET_CAP = 15000

# --- SIDEBAR: INDUSTRIAL CONTROL PANEL ---
with st.sidebar:
    st.title("🎛️ Parameters")
    st.markdown("---")
    
    with st.container():
        st.subheader("🌊 Environment")
        in_velo = st.slider("Flow Velocity (m/s)", 0.0, 2.5, 0.8, 0.05)
        in_turb = st.select_slider("Turbidity Level (NTU)", options=["Low (5)", "Med (50)", "High (200)"])
    
    with st.container():
        st.subheader("🔧 Operations")
        in_maint = st.number_input("Monthly Cycles", 1, 30, 4)
        in_labor = st.slider("Labor Rate (INR/hr)", 100, 1000, 350)
    
    with st.container():
        st.subheader("💰 Fiscal")
        in_fab = st.number_input("Fabrication Cost", 10000, 25000, 14200)

    st.markdown("---")
    st.caption("v4.2.0-stable | AGRFS-DSS")

# --- LOGIC ENGINE ---
# Flux Logic
is_active = MIN_V <= in_velo <= MAX_V
out_val = (in_velo / NOMINAL_V) * TARGET_LPH if is_active else 0.0
system_status = "STABLE" if is_active else ("CRITICAL FAIL" if in_velo > MAX_V else "IDLE")

# Safety Logic (RPN)
rpn = 15 * in_maint
exo_required = rpn >= 15

# Efficiency Logic
eff_score = 0.145 * (1 - (0.1 if in_turb == "High (200)" else 0))

# --- HEADER SECTION ---
st.header("⚡ AGRFS Industrial Monitoring & Selection Model")
st.write("Dynamic analysis of Aero-Elastic Galloping filtration performance and ergonomic safety logistics.")

# --- ROW 1: KPI RE-IMAGINED ---
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Net Flux Output", f"{out_val:.2f} L/hr", f"{in_velo} m/s")
k2.metric("Risk Priority (RPN)", rpn, "Exo Needed" if exo_required else "Safe", delta_color="inverse" if exo_required else "normal")
k3.metric("System Status", system_status)
k4.metric("Est. Annual OPEX", f"₹{(in_maint * in_labor * 12):,}")
k5.metric("Efficiency Ratio", f"{eff_score*100:.1f}%")

st.divider()

# --- ROW 2: PRIMARY ANALYTICS ---
c1, c2 = st.columns([1.5, 1])

with c1:
    st.subheader("📈 Response & Power Surface")
    v_range = np.linspace(0, 2.5, 150)
    o_range = np.where((v_range >= MIN_V) & (v_range <= MAX_V), (v_range/NOMINAL_V)*TARGET_LPH, 0)
    
    fig_main = go.Figure()
    fig_main.add_trace(go.Scatter(x=v_range, y=o_range, fill='tozeroy', name='Filtered Output', line=dict(color='#00f2ff', width=3)))
    fig_main.add_vline(x=in_velo, line_dash="dash", line_color="#ff4b4b")
    fig_main.update_layout(template="plotly_dark", height=450, xaxis_title="River Velocity (m/s)", yaxis_title="L/hr", margin=dict(t=20))
    st.plotly_chart(fig_main, use_container_width=True)
    st.markdown('<div class="caption-text"><b>Explainability:</b> The cyan region represents the aero-elastic operational window. Below 0.5 m/s, kinetic energy is insufficient to start oscillation. Above 1.5 m/s, the system enters a structural damping mode to protect internal seals.</div>', unsafe_allow_html=True)

with c2:
    st.subheader("🎯 Design Convergence")
    # Radar Chart Data
    categories = ['Galloping','Pressure','Efficiency','Cost','Complexity','Novelty']
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=[5,5,5,4,3,5], theta=categories, fill='toself', name='D3 (Final)', line_color='#00f2ff'))
    fig_radar.add_trace(go.Scatterpolar(r=[1,1,1,4,5,1], theta=categories, fill='toself', name='D1 (Baseline)', line_color='#ff4b4b'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), template="plotly_dark", height=450, margin=dict(t=50))
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('<div class="caption-text"><b>Explainability:</b> Comparison between the standard turbine (D1) and the Galloping system (D3). Note the 400% gain in efficiency and novelty at the cost of slight mechanical complexity.</div>', unsafe_allow_html=True)

# --- ROW 3: SAFETY & FISCAL ---
st.divider()
c3, c4 = st.columns(2)

with c3:
    st.subheader("🛡️ Ergonomic Fatigue Mapping")
    tasks = ["Agitator Maint.", "Membrane Scrub", "System Install", "Filter Replace"]
    weights = [15, 2, 25, 10]
    rpns = [w * in_maint for w in weights]
    
    fig_safety = px.bar(x=tasks, y=rpns, color=rpns, color_continuous_scale='Viridis', labels={'x':'Task', 'y':'RPN Score'})
    fig_safety.add_hline(y=15, line_dash="dot", line_color="red", annotation_text="Safety Threshold (15)")
    fig_safety.update_layout(template="plotly_dark", height=350)
    st.plotly_chart(fig_safety, use_container_width=True)
    st.markdown('<div class="caption-text"><b>Explainability:</b> RPN (Risk Priority Number) scales with Weight and Frequency. High-frequency maintenance (current input) pushes manual tasks above the safety limit, mandating exoskeleton intervention.</div>', unsafe_allow_html=True)

with c4:
    st.subheader("📉 Fiscal Sensitivity")
    # Budget tracking
    budget_usage = (in_fab / BUDGET_CAP) * 100
    st.write(f"Fabrication Cap Utilization: **{budget_usage:.1f}%**")
    st.progress(min(budget_usage/100, 1.0))
    
    # Financial breakdown table
    fin_data = {
        "Cost Head": ["Hardware Fab.", "Labor (Monthly)", "Energy Savings (Est.)"],
        "Value (INR)": [in_fab, in_maint * in_labor, "- ₹1,200"]
    }
    st.table(pd.DataFrame(fin_data))
    st.markdown('<div class="caption-text"><b>Explainability:</b> Financial viability is maintained if total utilization remains below 100%. The system provides a net-positive ROI by eliminating external power costs.</div>', unsafe_allow_html=True)
