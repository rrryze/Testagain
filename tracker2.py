import streamlit as st
import datetime
from PIL import Image, ImageDraw, ImageFont
import io

# Set page configuration to dark mode defaults
st.set_page_config(page_title="Kingsman Tracker", layout="centered")

# 1. Custom Cyberpunk Active Neon Glow CSS Injection with Typewriter Fonts
st.markdown(
    """
    <style>
    /* Import Premium Retro Typewriter Font */
    @import url('https://googleapis.com');

    /* Hide Default Streamlit Menu Overlays */
    #MainMenu, footer, header {
        display: none !important;
    }
    
    /* Pitch Black Base Canvas & Global Gritty Typewriter Font Style */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], p, span, label, input, button, select, div, select option {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Special Elite', 'Courier New', Courier, monospace !important;
    }
    
    /* Active Pulsing Animation Keyframes for Real Neon Glow Effect */
    @keyframes neonPulseWhite {
        0%, 100% { text-shadow: 0 0 4px #fff, 0 0 10px #fff, 0 0 18px #fff, 0 0 30px #b0b0b0; }
        50% { text-shadow: 0 0 2px #fff, 0 0 6px #fff, 0 0 12px #fff, 0 0 20px #707070; }
    }
    
    @keyframes neonPulsePurple {
        0%, 100% { text-shadow: 0 0 4px #df80ff, 0 0 12px #c633ff, 0 0 25px #9900cc; }
        50% { text-shadow: 0 0 2px #df80ff, 0 0 8px #c633ff, 0 0 15px #660088; }
    }

    @keyframes neonPulseGreen {
        0%, 100% { 
            text-shadow: 0 0 4px rgba(163, 230, 53, 0.9);
            box-shadow: inset 0 0 10px rgba(163, 230, 53, 0.2), 0 0 8px rgba(163, 230, 53, 0.2);
        }
        50% { 
            text-shadow: 0 0 2px rgba(163, 230, 53, 0.6);
            box-shadow: inset 0 0 5px rgba(163, 230, 53, 0.1), 0 0 4px rgba(163, 230, 53, 0.1);
        }
    }

    /* Neon White Glowing Title with Pulsing Animation */
    .neon-title {
        color: #ffffff !important;
        font-size: 2.3rem !important;
        font-weight: bold !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 40px;
        font-family: 'Special Elite', monospace !important;
        animation: neonPulseWhite 3s infinite alternate;
    }
    
    /* Decent Spacing: Custom Container Box Wrapper */
    .schedule-card {
        background-color: #09090d !important;
        border: 1px solid #1f1f2e !important;
        border-radius: 10px;
        padding: 24px !important;
        margin-bottom: 30px !important; 
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.8);
        font-family: 'Special Elite', monospace !important;
    }

    /* Sidebar/Results Clean Result Entry Card */
    .result-card-box {
        background-color: #09090d !important;
        border-left: 3px solid #df80ff !important;
        padding: 14px !important;
        margin-bottom: 12px !important;
        border-radius: 4px;
        font-family: 'Special Elite', monospace !important;
    }
    
    /* Puppet Card Fragment Glowing Neon Purple */
    .neon-purple-item {
        color: #df80ff !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        margin-bottom: 6px;
        font-family: 'Special Elite', monospace !important;
        animation: neonPulsePurple 2.5s infinite alternate;
    }
    
    /* Date and Day Label Styling with Neon White Glow */
    .date-label-glow {
        color: #ffffff !important;
        font-size: 0.95rem !important;
        margin-bottom: 14px;
        letter-spacing: 0.5px;
        font-family: 'Special Elite', monospace !important;
        display: inline-block;
        animation: neonPulseWhite 2.5s infinite alternate;
    }

    /* Glowing Neon Green Recipient Box with Active Neon Borders */
    .neon-green-recipient {
        color: #a3e635 !important;
        font-size: 1.15rem !important;
        font-weight: bold !important;
        background-color: #0b0f05 !important;
        border: 1px solid #a3e635 !important;
        border-left: 5px solid #a3e635 !important;
        padding: 12px 16px;
        border-radius: 6px;
        margin-top: 8px;
        font-family: 'Special Elite', monospace !important;
        animation: neonPulseGreen 4s infinite alternate;
    }

    /* Force UI Dropdown components into Typewriter font */
    div[data-testid="stSelectbox"] label, div[data-testid="stTextInput"] label p {
        color: #a1a1aa !important;
        margin-bottom: 8px !important;
        font-family: 'Special Elite', monospace !important;
    }

    /* Cyberpunk Text Input Field Modifications */
    div[data-testid="stTextInput"] input {
        background-color: #0d0d13 !important;
        color: #ffffff !important;
        border: 1px solid #1f1f2e !important;
        font-family: 'Special Elite', monospace !important;
    }

    /* Custom Futuristic Style for Download and Search Buttons Container */
    div.stDownloadButton > button, div.stButton > button {
        background-color: #000000 !important;
        color: #a3e635 !important;
        border: 1px solid #a3e635 !important;
        font-family: 'Special Elite', monospace !important;
        font-weight: bold !important;
        border-radius: 4px !important;
        transition: all 0.3s ease !important;
        width: 100%;
        margin-top: 24px;
    }
    div.stDownloadButton > button:hover, div.stButton > button:hover {
        background-color: #a3e635 !important;
        color: #000000 !important;
        box-shadow: 0 0 12px #a3e635 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 2. Render Glowing White Title without leading Sword Icon
st.markdown('<div class="neon-title">Kingsman: Spoils or War ⚔️</div>', unsafe_allow_html=True)

# 3. Dynamic Date Engine Filtering Loop (Tue=1, Thu=3, Sun=6)
@st.cache_data
def get_scheduled_dates():
    start_date = datetime.date.today()
    end_date = datetime.date(2026, 12, 31)
    valid_dates = []
    current_date = start_date
    target_days = {1, 3, 6} 
    while current_date <= end_date:
        if current_date.weekday() in target_days: valid_dates.append(current_date)
        current_date += datetime.timedelta(days=1)
    return valid_dates

all_dates = get_scheduled_dates()
date_options = {d.strftime("%A, %B %d, %Y"): d for d in all_dates}

# 4. Provided Roster List (54 Names)
roster = [
    "Strix", "Sidstark", "Gaion", "Chantelleboo", "Jdee", 
    "Recently", "iM01", "xCross", "Mohoney09", "Neir", "Geralt", 
    "Jhann", "Jcav27", "Wiizzz", "HighONE", "MALMON", "Papi", 
    "Sprig", "Mirai01", "Koomi", "BuknoyNaKoyKoy", "MJOY", "iSnappy", 
    "Blebze", "Seraphier", "Kittypoo", "Ravensaur", "xSNAKE", "AkagamiShanks", 
    "Xylohero", "Balaraw", "Bolts", "Khier", "Meruem", "Eidikos", 
    "Dessy", "Despair", "Lizz", "CTRL", "Impaktita", "Adboot", 
    "Aetherling", "Ardel", "Eagleman", "eytsvn", "HINATA", "kevkev", 
    "MrJack", "RC", "STAR", "Stiffled", "Zz33"
]

# # 5. CONTROL GRID: Dropdown, Download PNG, and Search Entry Panel Side-by-Side
col_select, col_btn, col_search = st.columns([4, 3, 3])

with col_select:
    selected_label = st.selectbox("Select Scheduled Drop Date:", list(date_options.keys()))
    selected_date_obj = date_options[selected_label]

# Mathematical Loop Distribution System
date_index = all_dates.index(selected_date_obj) if selected_date_obj in all_dates else 0
start_index = (date_index * 4) % len(roster)
assigned_recipients = [roster[(start_index + step) % len(roster)] for step in range(4)]

# Function to draw a high-quality PNG layout matching the UI styles
def generate_schedule_image(date_str, recipients_list):
    img = Image.new("RGB", (1000, 950), color="#000000"); draw = ImageDraw.Draw(img)
    try: title_font, item_font, sub_font = ImageFont.load_default(size=36), ImageFont.load_default(size=24), ImageFont.load_default(size=20)
    except TypeError: title_font, item_font, sub_font = ImageFont.load_default(), ImageFont.load_default(), ImageFont.load_default()
    draw.text((500, 60), "KINGSMAN: SPOILS OR WAR ⚔️", fill="#ffffff", font=title_font, anchor="mm")
    draw.line([(100, 100), (900, 100)], fill="#1f1f2e", width=2)
    for idx, name in enumerate(recipients_list, start=1):
        by1 = 140 + ((idx - 1) * 190); by2 = by1 + 160
        draw.rectangle([(100, by1), (900, by2)], fill="#09090d", outline="#1f1f2e", width=2)
        draw.text((130, by1 + 25), "Puppet Card Fragment", fill="#df80ff", font=item_font)
        draw.text((130, by1 + 65), f"{date_str}", fill="#ffffff", font=sub_font)
        draw.rectangle([(130, by1 + 105), (870, by1 + 140)], fill="#0b0f05", outline="#a3e635", width=1)
        draw.text((145, by1 + 112), f"{idx}: {name}", fill="#a3e635", font=item_font)
    buf = io.BytesIO(); img.save(buf, format='PNG')
    return buf.getvalue()

png_data = generate_schedule_image(selected_label, assigned_recipients)

with col_btn:
    st.download_button(label="📥 DOWNLOAD PNG", data=png_data, file_name=f"kingsman_schedule_{selected_date_obj.isoformat()}.png", mime="image/png")

# Visible Main Search Tool placed right next to the control buttons
with col_search:
    search_query = st.text_input("Search Player Schedule:", placeholder="Type name here...", value="").strip()

st.write("---")

# 6. RENDER SEARCH RESULTS (If query exists)
if search_query:
    st.markdown(f"### 🔍 Search Results for: '{search_query}'", unsafe_allow_html=True)
    matches_found = 0
    for idx, d_obj in enumerate(all_dates):
        s_idx = (idx * 4) % len(roster)
        day_recipients = [roster[(s_idx + step) % len(roster)] for step in range(4)]
        if any(search_query.lower() in name.lower() for name in day_recipients):
            matches_found += 1
            formatted_d = d_obj.strftime("%A, %B %d, %Y")
            matching_positions = [str(step + 1) for step, name in enumerate(day_recipients) if search_query.lower() in name.lower()]
            pos_lbl = ", ".join(matching_positions)
            st.markdown(f'<div class="result-card-box"><div class="neon-purple-item">🔮 Puppet Card Fragment</div><div class="date-label-glow">📅 {formatted_d}</div><div class="neon-green-recipient">👤 Position: {pos_lbl}</div></div>', unsafe_allow_html=True)
    if matches_found == 0:
        st.markdown("<p style='color:#71717a;'>No drops scheduled for this player context.</p>", unsafe_allow_html=True)
    st.write("---")

# 7. Clean Card Slot Render Loop (Main Daily Display)
st.markdown("### 📅 Active Drop Schedule")
for i, recipient in enumerate(assigned_recipients, start=1):
    st.markdown(f'<div class="schedule-card"><div class="neon-purple-item">🔮 Puppet Card Fragment</div><div class="date-label-glow">📅 {selected_label}</div><div class="neon-green-recipient">👤 {i}: {recipient}</div></div>', unsafe_allow_html=True)
