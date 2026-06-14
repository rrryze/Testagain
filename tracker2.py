import streamlit as st
import pandas as pd
import requests
import json

# --- CODE CONFIGURATION ---
st.set_page_config(
    page_title="Kingsman: Spoils of War", 
    page_icon="🕶️", 
    layout="wide"
)

# 🔗 AUTOMATED GOOGLE CLOUD BACKEND ENGINE
API_URL = "https://script.google.com/macros/s/AKfycbyRLOGgw_YMn6lm8gCTpLb0HI1YROqnP1wePZw44a1vZdirZzOjeYXM--WupDJeQ7wZ/exec"
DEFAULT_POOL = ["Harry (Galahad)", "Eggsy (Galahad II)", "Roxy (Lancelot)", "Merlin"]

@st.cache_data(ttl=2)  # Re-scans cloud backend data every 2 seconds automatically
def load_cloud_names(url):
    """Fetches real-time names from the cloud Google Sheet backend API."""
    try:
        # Appending a dummy timestamp parameter breaks downstream proxy caching
        response = requests.get(f"{url}?timestamp={pd.Timestamp.now().timestamp()}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Flatten out the 2D array returned from Google Sheet column data
            names = [str(row[0]).strip() for row in data if row and str(row[0]).strip() != ""]
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

# Fill empty slots to prevent column breakdown if sheet yields short entries
while len(agent_pool) < 4:
    agent_pool.append(f"Operative {len(agent_pool) + 1}")

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

# Render the stylized MVP cards using cloud data shared among the 3 users
for i, agent in enumerate(agent_pool[:4]):
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
    st.info("⚡ Authenticated Session Active (Shared Matrix Admin).")
    
    # 🛠️ EDIT NAMES DIRECTLY IN APP
    st.markdown("#### ⚙️ MVP's Today")
    
    new_names = []
    edit_cols = st.columns(4)
    
    # Open up direct input fields populated with current cloud data
    for i in range(4):
        with edit_cols[i]:
            edited_name = st.text_input(f"Operative {i+1} Name", value=agent_pool[i], key=f"agent_edit_{i}")
            new_names.append(edited_name)
            
    if st.button("Update MVP List"):
        if any(name.strip() == "" for name in new_names):
            st.error("❌ Error: Agent names cannot be blank.")
        else:
            # Re-map any running scheduler instances locally
            for old_name, new_name in zip(agent_pool, new_names):
                if old_name != new_name:
                    st.session_state.schedule_db.loc[st.session_state.schedule_db["Agent"] == old_name, "Agent"] = new_name
            
            # Pushes the updated array to the Google Sheet backend
            if write_names_to_cloud(API_URL, new_names):
                st.success("💾 Cloud Sync Complete! All admins will see these updated names instantly.")
                st.cache_data.clear()  # Clear cache to force a fresh data fetch on rerun
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
