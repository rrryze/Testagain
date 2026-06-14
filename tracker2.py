import streamlit as st
import pandas as pd
import requests
import io

# --- CODE CONFIGURATION ---
st.set_page_config(
    page_title="Kingsman: Spoils of War", 
    page_icon="🕶️", 
    layout="wide"
)

# 🔗 ACTIVE CLOUD SOURCE OF TRUTH
CLOUD_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS71WEaocX8sg-a-x5vHje7861yhW0ciPKvlaoFV7SFHKBqLnes43gvi_I0wiShGb6ir-7EG023HYJE/pub?output=csv"
DEFAULT_POOL = ["Harry (Galahad)", "Eggsy (Galahad II)", "Roxy (Lancelot)", "Merlin"]

@st.cache_data(ttl=5)  # Caches data for 5 seconds so multiple refreshes don't hit rate limits
def load_cloud_names(url):
    """Fetches locked configurations directly from the shared Google Sheet cloud matrix."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            
            # Use the first column values as the agent names
            if not df.empty and len(df) >= 4:
                return df.iloc[:4, 0].dropna().tolist()
            elif not df.empty:
                return df.iloc[:, 0].dropna().tolist()
    except Exception:
        return DEFAULT_POOL
    return DEFAULT_POOL

# --- INITIALIZE INTERNAL STRUCTURES ---
if "schedule_db" not in st.session_state:
    st.session_state.schedule_db = pd.DataFrame(
        columns=["Agent", "Mission Title", "Date", "Start Time", "End Time", "Risk Level"]
    )

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Fetch fresh cloud configurations simultaneously for all active dashboard administrators
agent_pool = load_cloud_names(CLOUD_SHEET_CSV_URL)

# Ensure we always have exactly 4 slots filled to prevent interface layout breaking
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
    st.info("⚡ Authenticated Session Active.")
    
    # 🛠️ EDIT NAMES CAPABILITY
    st.markdown("#### ⚙️ MVP's Today")
    
    # Inform the admins exactly how this deployment sync operates
    st.warning(
        "📝 **Cloud Management Notice:** Because you are using a shared cloud-published spreadsheet, "
        "any of the 3 admins can change names directly on the Google Sheet. The web app will update automatically."
    )
    
    edit_cols = st.columns(4)
    for i in range(4):
        with edit_cols[i]:
            st.text_input(f"Current Live Name {i+1}", value=agent_pool[i], disabled=True, key=f"agent_view_{i}")
            
    st.markdown(
        f'<a href="https://google.com" target="_blank">'
        f'<button style="background-color: #D4AF37; color: black; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold;">'
        f'🔗 Open Google Sheet to Edit Names'
        f'</button></a>', 
        unsafe_allow_html=True
    )

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
