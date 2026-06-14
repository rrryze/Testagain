import streamlit as st
import pandas as pd
import requests
import json

# --- CODE CONFIGURATION ---
st.set_page_config(
    page_title="Kingsman: Spoils of War", 
    page_icon="⚔️", 
    layout="wide"
)

# 🔗 AUTOMATED GOOGLE CLOUD BACKEND ENGINE
API_URL = "https://google.com"
DEFAULT_POOL = ["Kafra's still searching..", "Kafra's still searching..", "Kafra's still searching..", "Kafra's still searching.."]

@st.cache_data(ttl=2)  # Re-scans cloud backend data every 2 seconds automatically
def load_cloud_names(url):
    """Fetches real-time names from the cloud Google Sheet backend API."""
    try:
        response = requests.get(f"{url}?timestamp={pd.Timestamp.now().timestamp()}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            names = [str(row).strip() for row in data if row and str(row).strip() != ""]
            if len(names) >= 4:
                return names[:4]
            elif len(names) > 0:
                return names
    except Exception:
        return DEFAULT_POOL
    return DEFAULT_POOL

def write_names_to_cloud(url, names_list):
    """Pushes new admin-edited names up to the live Google Sheet cloud architecture."""
    try:
        response = requests.post(url, data=json.dumps(names_list), timeout=5)
        if response.status_code == 200:
            return True
    except Exception as e:
        st.error(f"Cloud update bottleneck: {e}")
    return False

# --- INITIALIZE DATABASE & LOCAL STATES ---
if "schedule_db" not in st.session_state:
    st.session_state.schedule_db = pd.DataFrame(
        columns=["Agent", "Mission Title", "Date", "Start Time", "End Time", "Risk Level"]
    )

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Load shared cloud array live from the spreadsheet server
agent_pool = load_cloud_names(API_URL)

while len(agent_pool) < 4:
    agent_pool.append("Kafra's still searching..")

# --- EMULATED THEME STYLING ---
st.markdown("""
    <style>
    .kingsman-title { text-align: center; color: #D4AF37; font-weight: bold; font-family: 'Georgia', serif; }
    .status-card { background-color: #1E293B; padding: 15px; border-radius: 8px; border-left: 5px solid #D4AF37; }
    .loot-title { color: #888; font-size: 0.85rem; font-weight: bold; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }
    .agent-name { margin-top: 0px; font-weight: bold; color: #FFFFFF; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='kingsman-title'>⚔️ KINGSMAN: SPOILS OF WAR</h1>", unsafe_allow_html=True)
st.divider()

# --- MAIN PAGE: MVP LOOT DISTRIBUTION PANEL ---
st.subheader("📊 MVP Loot Distribution")  
live_cols = st.columns(4)

# Render the stylized MVP cards with the loot title inside the box
for i, agent in enumerate(agent_pool[:4]):
    with live_cols[i]:
        st.markdown(f"""
        <div class='status-card'>
            <div class='loot-title'>Pup. Card Fragment</div>
            <h4 class='agent-name'>{agent}</h4>
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
    st.info("⚡ Authenticated Session Active (Shared Matrix Admin).")
    
    # 🛠️ EDIT NAMES DIRECTLY IN APP
    st.markdown("#### ⚙️ MVP's Today")
    
    new_names = []
    edit_cols = st.columns(4)
    
    for i in range(4):
        with edit_cols[i]:
            edited_name = st.text_input(f"Operative {i+1} Name", value=agent_pool[i], key=f"agent_edit_{i}")
            new_names.append(edited_name)
            
    if st.button("Update MVP List"):
        if any(name.strip() == "" for name in new_names):
            st.error("❌ Error: Agent names cannot be blank.")
        else:
            for old_name, new_name in zip(agent_pool, new_names):
                if old_name != new_name:
                    st.session_state.schedule_db.loc[st.session_state.schedule_db["Agent"] == old_name, "Agent"] = new_name
            
            if write_names_to_cloud(API_URL, new_names):
                st.success("💾 Cloud Sync Complete! All admins will see these updated names instantly.")
                st.cache_data.clear()
                st.rerun()

    # --- DISCONNECT / RESET UTILITIES ---
    st.markdown("---")
    control_cols = st.columns(2)
    
    with control_cols:  
        if st.button("Log Out of Admin Status"):
            st.session_state.is_admin = False
            st.rerun()
            
    with control_cols:  
        if not st.session_state.schedule_db.empty:
            if st.button("Clear All Data Logs"):
                st.session_state.schedule_db = pd.DataFrame(columns=["Agent", "Mission Title", "Date", "Start Time", "End Time", "Risk Level"])
                st.rerun()
