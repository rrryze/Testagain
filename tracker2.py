import streamlit as st
import pandas as pd
import json
import os

# --- CODE CONFIGURATION ---
st.set_page_config(
    page_title="Kingsman: Spoils of War", 
    page_icon="🕶️", 
    layout="wide"
)

# --- HARD RECOVERY / STORAGE PATHS ---
DATA_FILE = "mvp_data.json"
DEFAULT_POOL = ["Harry (Galahad)", "Eggsy (Galahad II)", "Roxy (Lancelot)", "Merlin"]

def load_permanent_names():
    """Reads permanent configurations from file storage safely."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_POOL
    return DEFAULT_POOL

def save_permanent_names(names_list):
    """Writes updated configurations directly to persistent hardware storage."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(names_list, f)
    except Exception as e:
        st.error(f"Write Failure: {e}")

# --- INITIALIZE CORE PLATFORM DATABASE (SESSION STATE) ---
if "schedule_db" not in st.session_state:
    st.session_state.schedule_db = pd.DataFrame(
        columns=["Agent", "Mission Title", "Date", "Start Time", "End Time", "Risk Level"]
    )

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Fetch fresh or saved permanent configurations dynamically on runtime iteration
agent_pool = load_permanent_names()

# --- EMULATED THEME STYLING ---
st.markdown("""
    <style>
    .kingsman-title { text-align: center; color: #D4AF37; font-weight: bold; font-family: 'Georgia', serif; }
    .status-card { background-color: #1E293B; padding: 15px; border-radius: 8px; border-left: 5px solid #D4AF37; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='kingsman-title'>🕶️ KINGSMAN: SPOILS OF WAR</h1>", unsafe_allow_html=True)
st.divider()

# --- MAIN PAGE: MVP OVERVIEW PANEL ---
st.subheader("📊 MVP")
live_cols = st.columns(4)

# Render the stylized MVP cards with permanently loaded records
for i, agent in enumerate(agent_pool):
    with live_cols[i]:
        st.markdown(f"""
        <div class='status-card'>
            <h4>{agent}</h4>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# --- ADMIN ACCESS SECTION ---
st.markdown("### 🔐 Admin Access")

if not st.session_state.is_admin:
    # --- LOGIN INTERFACE ---
    with st.form(key="login_form"):
        col1, col2 = st.columns(2)
        username = col1.text_input("User", placeholder="Enter username")
        password = col2.text_input("Password", type="password", placeholder="Enter password")
        
        login_button = st.form_submit_button(label="Authenticate")
        
        if login_button:
            if username == "Kingsman" and password == "Admin":
                st.session_state.is_admin = True
                st.success("🔒 Access Granted. Welcome, Administrator.")
                st.rerun()
            else:
                st.error("❌ Access Denied. Invalid credentials.")
else:
    # --- AUTHENTICATED PANEL ---
    st.info("⚡ Authenticated Session Active.")
    
    # 🛠️ EDIT NAMES CAPABILITY
    st.markdown("#### ⚙️ MVP's Today")
    new_names = []
    edit_cols = st.columns(4)
    
    # Pre-populate input modules with the currently locked-in storage settings
    for i in range(4):
        with edit_cols[i]:
            current_name = agent_pool[i]
            edited_name = st.text_input(f"Operative {i+1} Name", value=current_name, key=f"agent_input_{i}")
            new_names.append(edited_name)
            
    # Apply roster updates straight to file storage
    if st.button("Update MVP List"):
        if any(name.strip() == "" for name in new_names):
            st.error("❌ Error: Agent names cannot be blank.")
        else:
            # Re-map backend parameters for consistency inside temporary deployment table
            for old_name, new_name in zip(agent_pool, new_names):
                if old_name != new_name:
                    st.session_state.schedule_db.loc[st.session_state.schedule_db["Agent"] == old_name, "Agent"] = new_name
            
            # Commit straight to the permanent hard disk array
            save_permanent_names(new_names)
            st.success("💾 Roster permanently locked into database architecture!")
            st.rerun()

    # --- DISCONNECT / RESET UTILITIES ---
    st.markdown("---")
    control_cols = st.columns(2)
    
    with control_cols[0]:  
        if st.button("Log Out of Admin Status"):
            st.session_state.is_admin = False
            st.rerun()
            
    with control_cols[1]:  
        if not st.session_state.schedule_db.empty:
            if st.button("Clear All Data Logs"):
                st.session_state.schedule_db = pd.DataFrame(columns=["Agent", "Mission Title", "Date", "Start Time", "End Time", "Risk Level"])
                st.rerun()
