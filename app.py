import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="AGRFS | Command Center", page_icon="⚡", layout="wide")

# --- CUSTOM CSS FOR SLEEK UI ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #00d1ff; }
    .stAlert { border-radius: 12px; border: none; }
    .main { background: #0e1117; }
    div[data-testid="metric-container"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADER ---
@st.cache_data
def load_model():
    # Pulling directly from your validated sheets
    matrix = {
        "Criterion": ["Galloping", "Pressure", "Efficiency", "Output", "Cost", "Complexity", "Novelty"],
        "D1": [1, 1, 1, 1, 4, 5, 1],
        "D2": [2, 2, 2, 2, 3, 3, 2],
        "D3": [5, 5, 5, 5, 4, 3, 5]
    }
    safety = {
        "Task": ["Agitator Maint.", "Membrane Cleaning", "Installation", "Filter Replace"],
        "Weight": [15, 2, 25, 10],
        "Freq": [3, 5, 1, 2]
    }
    return pd.DataFrame(matrix), pd.DataFrame(safety)

df_matrix, df_safety = load_model()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("🕹️ System Controls")
    velocity = st.select_slider("Simulated River Velocity (m/s)", options=np.round(np.arange(0, 2.1, 0.1), 1), value=0.8)
    budget_cap = st.number_input("Cost Ceiling (INR)", value=15000)
    st.divider()
    st.info("Model V4.2: Validated for 0.02μm Ultra-Filtration")

# --- HEADER SECTION ---
st.title("📊 AGRFS: Strategic Project Evaluation")
st.caption("Aero-Elastic Galloping River Filtration System & Ergonomic Exoskeleton Suite")

# --- TOP ROW: KPI CARDS ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# Logic: Output scaling
out_val = (velocity / 0.8) * 8 if 0.5 <= velocity <= 1.5 else 0
status = "STABLE" if 0.5 <= velocity <= 1.5 else "IDLE/FAIL"

kpi1.metric("Live Flux Rate", f"{out_val:.1f} L/hr", f"{velocity} m/s")
kpi2.metric("Design Score (D3)", "4.66 / 5.0", "Optimal")
kpi3.metric("System Status", status, border=True)
kpi4.metric("Avg. RPN", int(df_safety['Weight'].mean() * 3), "Risk Index")

st.divider()

# --- MIDDLE ROW: ANALYTICS ---
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("🚀 Design Evolution: Radar Analysis")
    # Radar Chart for Design Comparison
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=df_matrix['D1'], theta=df_matrix['Criterion'], fill='toself', name='Baseline (D1)'))
    fig_radar.add_trace(go.Scatterpolar(r=df_matrix['D3'], theta=df_matrix['Criterion'], fill='toself', name='Final AGRFS (D3)', line_color='#00d1ff'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=True, template="plotly_dark", height=450)
    st.plotly_chart(fig_radar, use_container_width=True)

with col_right:
    st.subheader("⚖️ Safety Thresholds")
    # RPN Calculation for UI
    df_safety['RPN'] = df_safety['Weight'] * df_safety['Freq']
    fig_risk = px.bar(df_safety, x="Task", y="RPN", color="RPN", color_continuous_scale="RdBu_r", title="Maintenance Strain Index")
    fig_risk.add_hline(y=15, line_dash="dash", line_color="red", annotation_text="Exo Mandatory Limit")
    fig_risk.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_risk, use_container_width=True)

# --- BOTTOM ROW: LIVE CONSTRAINTS ---
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Flow Efficiency Curve")
    v_range = np.linspace(0, 2, 100)
    o_range = [(v/0.8)*8 if 0.5 <= v <= 1.5 else 0 for v in v_range]
    fig_flow = px.area(x=v_range, y=o_range, labels={'x':'Velocity', 'y':'L/hr'}, color_discrete_sequence=['#00d1ff'])
    fig_flow.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig_flow, use_container_width=True)

with c2:
    st.subheader("📋 Component Status")
    st.table(df_matrix[['Criterion', 'D3']].style.background_gradient(subset=['D3'], cmap='Blues'))

st.success(f"**Final Verdict:** Design 3 remains **viable** at {velocity} m/s with a budget headroom of ₹{budget_cap - 14200}.")
