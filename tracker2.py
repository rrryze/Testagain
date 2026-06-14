import streamlit as st
import pandas as pd
from datetime import datetime, time

# --- CODE CONFIGURATION ---
st.set_page_config(
    page_title="Kingsman: Spoils of War", 
    page_icon="🕶️", 
    layout="wide"
)

# --- INITIALIZE DATABASE (SESSION STATE) ---
if "schedule_db" not in st.session_state:
    st.session_state.schedule_db = pd.DataFrame(
        columns=["Agent", "Mission Title", "Date", "Start Time", "End Time", "Risk Level"]
    )

# --- EMULATED THEME STYLING ---
st.markdown("""
    <style>
    .kingsman-title { text-align: center; color: #D4AF37; font-weight: bold; font-family: 'Georgia', serif; }
    .status-card { background-color: #1E293B; padding: 15px; border-radius: 8px; border-left: 5px solid #D4AF37; }
    </style>
""", unsafe_allowed_html=True)

st.markdown("<h1 class='kingsman-title'>🕶️ KINGSMAN: SPOILS OF WAR</h1>", unsafe_allowed_html=True)
st.markdown("<h4 style='text-align: center; color: #888;'>Tactical 4-Agent Deployment Scheduler</h4>", unsafe_allowed_html=True)
st.divider()

# --- SIDEBAR: MISSION BRIEFING & INPUT ---
st.sidebar.header("🗺️ Assign New Objective")
agent_pool = ["Harry (Galahad)", "Eggsy (Galahad II)", "Roxy (Lancelot)", "Merlin"]

with st.sidebar.form(key="mission_form", clear_on_submit=True):
    selected_agent = st.selectbox("Assign Operative", agent_pool)
    mission_name = st.text_input("Objective / Mission Name", placeholder="e.g., Golden Circle Extraction")
    mission_date = st.date_input("Target Date", min_value=datetime.today())
    
    col1, col2 = st.columns(2)
    start_t = col1.time_input("Commence Time", value=time(9, 0))
    end_t = col2.time_input("Extraction Time", value=time(17, 0))
    
    risk_level = st.select_slider("Threat Matrix Level", options=["Low", "Medium", "High", "Critical"])
    submit_button = st.form_submit_button(label="Lock in Schedule")

# --- DATABASE LOGIC & CONFLICT MANAGEMENT ---
if submit_button:
    if not mission_name:
        st.sidebar.error("❌ Operational Error: Mission Title cannot be blank.")
    elif start_t >= end_t:
        st.sidebar.error("❌ Temporal Paradox: Extraction must happen AFTER commencement.")
    else:
        # Cross-reference existing records for schedule overlap
        overlap = False
        existing_records = st.session_state.schedule_db[
            (st.session_state.schedule_db["Agent"] == selected_agent) & 
            (st.session_state.schedule_db["Date"] == mission_date)
        ]
        
        for _, row in existing_records.iterrows():
            if not (end_t <= row["Start Time"] or start_t >= row["End Time"]):
                overlap = True
                break
                
        if overlap:
            st.sidebar.error(f"⚠️ Conflict Detected! {selected_agent} is already deployed during those hours.")
        else:
            # Append new clean schedule entry
            new_mission = pd.DataFrame([{
                "Agent": selected_agent,
                "Mission Title": mission_name,
                "Date": mission_date,
                "Start Time": start_t,
                "End Time": end_t,
                "Risk Level": risk_level
            }])
            st.session_state.schedule_db = pd.concat([st.session_state.schedule_db, new_mission], ignore_index=True)
            st.sidebar.success(f"⚡ Mission logged for {selected_agent}!")

# --- MAIN INTERFACE: OPERATIONAL DASHBOARD ---
st.subheader("📊 Active Operative Manifest")
live_cols = st.columns(4)

for i, agent in enumerate(agent_pool):
    with live_cols[i]:
        agent_tasks = st.session_state.schedule_db[st.session_state.schedule_db["Agent"] == agent]
        task_count = len(agent_tasks)
        
        st.markdown(f"""
        <div class='status-card'>
            <h4>{agent}</h4>
            <p>Active Commitments: <b>{task_count}</b></p>
        </div>
        """, unsafe_allowed_html=True)

st.markdown("### 📋 Master Timeline Ledger")
if st.session_state.schedule_db.empty:
    st.info("The ledger is currently clear. No ops are scheduled for today.")
else:
    # Format and present data clearly
    display_df = st.session_state.schedule_db.copy()
    display_df["Date"] = display_df["Date"].apply(lambda x: x.strftime('%Y-%m-%d'))
    display_df["Start Time"] = display_df["Start Time"].apply(lambda x: x.strftime('%H:%M'))
    display_df["End Time"] = display_df["End Time"].apply(lambda x: x.strftime('%H:%M'))
    
    st.dataframe(display_df, use_container_width=True)
    
    if st.button("Clear All Data Logs"):
        st.session_state.schedule_db = pd.DataFrame(columns=["Agent", "Mission Title", "Date", "Start Time", "End Time", "Risk Level"])
        st.rerun()
