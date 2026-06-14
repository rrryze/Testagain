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

# 🔗 AUTOMATED GOOGLE CLOUD BACKEND ENGINE - UNTOUCHED & PRESERVED
API_URL = "https://script.google.com/macros/s/AKfycbyRLOGgw_YMn6lm8gCTpLb0HI1YROqnP1wePZw44a1vZdirZzOjeYXM--WupDJeQ7wZ/exec"
DEFAULT_POOL = ["Kafra's still searching", "Kafra's still searching", "Kafra's still searching", "Kafra's still searching"]

@st.cache_data(ttl=2)  # Re-scans cloud backend data every 2 seconds automatically
def load_cloud_names(url):
    """Fetches real-time names from the cloud Google Sheet backend API and cleans raw arrays."""
    try:
        response = requests.get(f"{url}?timestamp={pd.Timestamp.now().timestamp()}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            names = []
            for row in data:
                if isinstance(row, list) and len(row) > 0:
                    val = str(row).strip()
                else:
                    val = str(row).strip()
                
                # Definitive cleanup string filter to violently strip brackets and raw quotes
                val = val.replace("[", "").replace("]", "").replace("'", "").replace('"', '')
                
                if val != "":
                    names.append(val)
                    
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
        clean_list = [str(n).replace("[", "").replace("]", "").replace("'", "").replace('"', '') for n in names_list]
        response = requests.post(url, data=json.dumps(clean_list), timeout=5)
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
    agent_pool.append("Kafra's still searching")

# --- CUSTOM CSS: TYPEWRITER FONTS + ANIMATED HIGH-INTENSITY NEON GLOW ENGINE ---
st.markdown("""
    <style>
    /* ⌨️ GLOBAL TYPEWRITER OVERRIDE */
    html, body, [class*="st-"], p, h1, h2, h3, h4, h5, h6, label, input, button {
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* 🧠 MAIN LAYOUT STYLING */
    .status-card { 
        background-color: #0F172A; 
        padding: 20px; 
        border-radius: 10px; 
        border: 1px solid #1E293B;
        border-left: 5px solid #D4AF37; 
        min-height: 120px; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* ⚪ ANIMATED NEON WHITE GLOW: MAIN TITLE (PULSING) */
    .neon-title { 
        text-align: center; 
        color: #FFFFFF; 
        font-weight: bold; 
        font-size: 2.5rem;
        margin-bottom: 10px;
        animation: whitePulse 3s infinite alternate;
    }

    /* 🔮 ANIMATED NEON PURPLE GLOW: LOOT TITLE (CYBERPUNK FLICKER) */
    .neon-purple-loot { 
        color: #E0B0FF; 
        font-size: 0.9rem; 
        font-weight: bold; 
        margin-bottom: 8px; 
        text-transform: uppercase; 
        letter-spacing: 2px;
        animation: purpleFlicker 4s infinite;
    }

    /* 🟢 ANIMATED NEON GREEN GLOW: NAME MATRIX (BREATHING WAVE) */
    .neon-green-name { 
        margin-top: 5px; 
        font-weight: bold; 
        font-size: 1.3rem;
        color: #E8FFEA; 
        display: inline-block;
        animation: greenBreathing 2.5s infinite ease-in-out alternate;
    }
    
    /* 🎬 SEARCHING DOTS CSS ANIMATION */
    .loading-dots span {
        animation-name: blink;
        animation-duration: 1.4s;
        animation-iteration-count: infinite;
        animation-fill-mode: both;
        font-weight: bold;
        color: #00FF66;
        text-shadow: 0 0 5px #00FF66, 0 0 10px #00FF66;
    }
    .loading-dots span:nth-child(2) { animation-delay: .2s; }
    .loading-dots span:nth-child(3) { animation-delay: .4s; }

    /* ==========================================
       🌟 NEON ENGINE TIMELINE ANIMATIONS (KEYFRAMES)
       ========================================== */

    /* 1. White Title Pulsing Loop */
    @keyframes whitePulse {
        0% {
            text-shadow: 0 0 4px #fff, 0 0 10px #fff, 0 0 18px #fff, 0 0 30px #B0B0B0;
        }
        100% {
            text-shadow: 0 0 8px #fff, 0 0 20px #fff, 0 0 35px #fff, 0 0 60px #fff;
        }
    }

    /* 2. Purple Loot Neon Sign Flicker */
    @keyframes purpleFlicker {
        0%, 18%, 22%, 25%, 53%, 57%, 100% {
            text-shadow: 0 0 4px #D800FF, 0 0 10px #D800FF, 0 0 18px #D800FF;
        }
        20%, 24%, 55% {
            text-shadow: none;
            opacity: 0.7;
        }
    }

    /* 3. Green Name Dynamic Breathing */
    @keyframes greenBreathing {
        0% {
            text-shadow: 0 0 3px #00FF66, 0 0 8px #00FF66;
            transform: scale(0.99);
        }
        100% {
            text-shadow: 0 0 8px #00FF66, 0 0 20px #00FF66, 0 0 30px #00FF66;
            transform: scale(1.01);
        }
    }

    /* 4. Falling Text Dots */
    @keyframes blink {
        0% { opacity: .2; }
        20% { opacity: 1; }
        100% { opacity: .2; }
    }
    </style>
""", unsafe_allow_html=True)

# Render the High-Intensity White Neon Header Title
st.markdown("<h1 class='neon-title'>⚔️ KINGSMAN: SPOILS OF WAR</h1>", unsafe_allow_html=True)
st.divider()

# --- MAIN PAGE: MVP LOOT DISTRIBUTION PANEL ---
st.subheader("📊 MVP Loot Distribution")  
live_cols = st.columns(4)

# Render the stylized MVP cards with animated searching tags and neon layers
for i, agent in enumerate(agent_pool[:4]):
    with live_cols[i]:
        if agent == "Kafra's still searching":
            display_html = """
            <div class='status-card'>
                <div class='neon-purple-loot'>Pup. Card Fragment</div>
                <h4 class='neon-green-name'>Kafra's still searching<span class='loading-dots'><span>.</span><span>.</span><span>.</span></span></h4>
            </div>
            """
        else:
            display_html = f"""
            <div class='status-card'>
                <div class='neon-purple-loot'>Pup. Card Fragment</div>
                <h4 class='neon-green-name'>{agent}</h4>
            </div>
            """
        st.markdown(display_html, unsafe_allow_html=True)

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
