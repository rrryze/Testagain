import streamlit as st
import pandas as pd

# --- CODE CONFIGURATION ---
st.set_page_config(
    page_title="Kingsman: Spoils of War", 
    page_icon="🕶️", 
    layout="wide"
)

DEFAULT_POOL = ["Peter", "James", "Matthew", "Nathanael"]

# --- INITIALIZE NATIVE CLOUD KEY-VALUE STORE ---
# st.kv_store automatically synchronizes data globally across all 3 admins over the cloud.
if "mvp_names" not in st.kv_store:
    st.kv_store["mvp_names"] = DEFAULT_POOL

if "schedule_db" not in st.session_state:
    st.session_state.schedule_db = pd.DataFrame(
        columns=["Agent", "Mission Title", "Date", "Start Time", "End Time", "Risk Level"]
    )

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Fetch fresh cloud configurations simultaneously for all active dashboard administrators
agent_pool = st.kv_store["mvp_names"]

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
            # Re-map any running scheduler instances
            for old_name, new_name in zip(agent_pool, new_names):
                if old_name != new_name:
                    st.session_state.schedule_db.loc[st.session_state.schedule_db["Agent"] == old_name, "Agent"] = new_name
            
            # Pushes the updated array directly to the secure built-in Streamlit Cloud Database
            st.kv_store["mvp_names"] = new_names
            st.success("💾 Cloud Sync Complete! All admins will see these updated names instantly.")
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
