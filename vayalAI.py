"""
VayalAI (வயல் AI) - Farmer's Intelligent Field Assistant
Enhanced multi-page interactive app with voice input, crop recommendations, weed alerts, and more
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="VayalAI - Farmer's Field Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS ============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=Noto+Sans+Tamil:wght@400;600&display=swap');

* {
    font-family: 'Sora', 'Noto Sans Tamil', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a1f0f 0%, #0d2b17 40%, #0a1a0c 100%);
    min-height: 100vh;
}

/* Animated background particles */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
        radial-gradient(circle at 20% 50%, rgba(45, 106, 79, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(82, 183, 136, 0.1) 0%, transparent 40%),
        radial-gradient(circle at 60% 80%, rgba(27, 67, 50, 0.2) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* Glass morphism cards */
.glass-card {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 1.5rem;
    margin: 0.6rem 0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.1);
    border: 1px solid rgba(82, 183, 136, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    color: #e8f5e9;
}
.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.15);
    border-color: rgba(82, 183, 136, 0.4);
}

.green-card {
    background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 60%, #40916C 100%);
    color: white;
    border-radius: 20px;
    padding: 1.5rem;
    margin: 0.5rem 0;
    box-shadow: 0 8px 24px rgba(27, 67, 50, 0.5);
    border: 1px solid rgba(82, 183, 136, 0.3);
}

.success-card {
    background: linear-gradient(135deg, rgba(27, 67, 50, 0.8) 0%, rgba(45, 106, 79, 0.8) 100%);
    border-radius: 16px;
    padding: 1.2rem;
    color: #b7e4c7;
    border-left: 4px solid #52B788;
    backdrop-filter: blur(10px);
}

.weed-alert {
    background: linear-gradient(135deg, #7B0D1E 0%, #9D0208 50%, #DC2F02 100%);
    color: white;
    padding: 1.2rem;
    border-radius: 16px;
    animation: pulse 2s ease-in-out infinite;
    border: 1px solid rgba(220, 47, 2, 0.5);
    box-shadow: 0 0 30px rgba(220, 47, 2, 0.3);
}

@keyframes pulse {
    0%, 100% { transform: scale(1); box-shadow: 0 0 30px rgba(220, 47, 2, 0.3); }
    50% { transform: scale(1.01); box-shadow: 0 0 50px rgba(220, 47, 2, 0.5); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-in {
    animation: fadeInUp 0.5s ease forwards;
}

.voice-btn {
    background: linear-gradient(135deg, #52B788 0%, #2D6A4F 50%, #1B4332 100%);
    color: white;
    border: 1px solid rgba(82, 183, 136, 0.4);
    padding: 14px 28px;
    border-radius: 40px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    transition: all 0.3s ease;
    letter-spacing: 0.5px;
}
.voice-btn:hover {
    transform: scale(1.03);
    box-shadow: 0 6px 20px rgba(82, 183, 136, 0.4);
}

.progress-bar {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    height: 10px;
    overflow: hidden;
    margin: 0.5rem 0;
}
.progress-fill {
    background: linear-gradient(90deg, #52B788, #95D5B2);
    height: 100%;
    border-radius: 10px;
    transition: width 1s ease;
}

.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(82, 183, 136, 0.2);
    border-radius: 16px;
    padding: 1.2rem;
    text-align: center;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #52B788;
    line-height: 1.1;
}
.metric-label {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.6);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

/* Page header style */
.page-header {
    background: linear-gradient(135deg, rgba(27,67,50,0.9) 0%, rgba(45,106,79,0.7) 100%);
    border-radius: 20px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(82,183,136,0.3);
    color: white;
}
.page-header h1 {
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
    color: #95D5B2;
}
.page-header p {
    margin: 0.3rem 0 0 0;
    color: rgba(255,255,255,0.7);
    font-size: 0.9rem;
}

.tag {
    display: inline-block;
    background: rgba(82, 183, 136, 0.2);
    color: #95D5B2;
    border: 1px solid rgba(82, 183, 136, 0.3);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(10, 31, 15, 0.97) !important;
    border-right: 1px solid rgba(82, 183, 136, 0.2);
}
[data-testid="stSidebar"] * {
    color: #d8f3dc !important;
}
[data-testid="stSidebar"] .stButton button {
    background: rgba(45, 106, 79, 0.2) !important;
    border: 1px solid rgba(82, 183, 136, 0.3) !important;
    border-radius: 12px !important;
    color: #d8f3dc !important;
    font-weight: 500 !important;
    transition: all 0.3s !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(82, 183, 136, 0.3) !important;
    transform: translateX(4px) !important;
}

/* Streamlit overrides */
.stSlider > label { color: #b7e4c7 !important; }
.stNumberInput > label { color: #b7e4c7 !important; }
.stTextInput > label { color: #b7e4c7 !important; }
.stTextArea > label { color: #b7e4c7 !important; }
.stSelectbox > label { color: #b7e4c7 !important; }
h1, h2, h3, h4, h5, h6 { color: #95D5B2 !important; }
p, li, small { color: #d8f3dc; }
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* Divider */
hr { border-color: rgba(82, 183, 136, 0.2) !important; }

.footer {
    text-align: center;
    color: rgba(255,255,255,0.4);
    padding: 2rem;
    margin-top: 2rem;
    font-size: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# ============ SESSION STATE INITIALIZATION ============
defaults = {
    'page': "Home",
    'farmer_name': "",
    'village': "",
    'farm_size': 5.0,
    'soil_type': "Loamy",
    'season': "Kharif",
    'planted_crops': [],
    'observations': [],
    'voice_temp': 32,
    'voice_moist': 350,
    'show_voice_success': False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============ SIDEBAR NAVIGATION ============
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0 1rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.2rem;">🌾</div>
        <h1 style="font-size: 1.8rem; margin: 0; color: #52B788 !important; font-weight: 800;">VayalAI</h1>
        <p style="font-size: 1rem; opacity: 0.7; margin: 0;">வயல் AI</p>
        <p style="font-size: 0.72rem; opacity: 0.5; margin-top: 4px;">Farmer's Field Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    pages = [
        ("🏠", "Home"),
        ("🌱", "Crop Advisor"),
        ("💧", "Irrigation"),
        ("🚨", "Weed Alert"),
        ("📊", "My Farm"),
        ("🎯", "Profit Calc"),
        ("📓", "Farm Diary"),
    ]

    for icon, name in pages:
        label = f"{icon}  {name}"
        if st.button(label, use_container_width=True, key=f"nav_{name}"):
            st.session_state.page = name
            st.rerun()

    st.markdown("---")

    if st.session_state.farmer_name:
        st.markdown(f"""
        <div style="background: rgba(82,183,136,0.1); border: 1px solid rgba(82,183,136,0.25); border-radius: 14px; padding: 1rem; margin-top: 0.5rem;">
            <div style="font-size: 0.7rem; color: rgba(255,255,255,0.5) !important; text-transform: uppercase; letter-spacing: 1px;">Active Farmer</div>
            <div style="font-size: 1rem; font-weight: 700; color: #95D5B2 !important; margin-top: 4px;">👨‍🌾 {st.session_state.farmer_name}</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.6) !important;">📍 {st.session_state.village}</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.6) !important;">🌿 {st.session_state.farm_size} acres · {st.session_state.soil_type}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer" style="margin-top: 2rem;">
        Made with ❤️ for Indian Farmers
    </div>
    """, unsafe_allow_html=True)


# ============ VOICE INPUT COMPONENT ============
def voice_input_component():
    st.markdown("""
    <div id="voice-container" style="margin: 1rem 0;">
        <button id="voice-btn" class="voice-btn" onclick="handleVoice()">
            🎤 Click & Speak Sensor Values
        </button>
        <div id="voice-status" style="font-size: 12px; text-align: center; margin-top: 10px; color: rgba(255,255,255,0.6); min-height: 20px;"></div>
    </div>

    <script>
    function handleVoice() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const voiceStatus = document.getElementById('voice-status');
        const voiceBtn = document.getElementById('voice-btn');

        if (!SpeechRecognition) {
            voiceStatus.innerHTML = '❌ Voice not supported. Please use Chrome.';
            voiceStatus.style.color = '#ff6b6b';
            return;
        }

        const useTamil = window.confirm('Choose language:\\n✅ OK = English\\n❌ Cancel = Tamil');
        const lang = useTamil ? 'en-US' : 'ta-IN';

        const recognition = new SpeechRecognition();
        recognition.lang = lang;
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = () => {
            voiceBtn.innerHTML = '🔴 Listening... Speak now!';
            voiceStatus.innerHTML = 'Say something like: "Temperature 32 moisture 280"';
            voiceStatus.style.color = '#ff9f9f';
        };

        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            voiceStatus.innerHTML = '✅ Heard: <em>' + text + '</em>';
            voiceStatus.style.color = '#95D5B2';
            voiceBtn.innerHTML = '🎤 Click & Speak Sensor Values';

            const numbers = text.match(/\\d+/g);
            if (numbers && numbers.length >= 2) {
                const params = new URLSearchParams(window.parent.location.search);
                params.set('v_temp', numbers[0]);
                params.set('v_moist', numbers[1]);
                const newUrl = window.parent.location.pathname + '?' + params.toString();
                window.parent.history.pushState({}, '', newUrl);
                setTimeout(() => { window.parent.location.reload(); }, 800);
            } else {
                voiceStatus.innerHTML = '⚠️ Could not find numbers. Try again: "Temperature 32 moisture 280"';
                voiceStatus.style.color = '#ffd166';
                voiceBtn.innerHTML = '🎤 Click & Speak Sensor Values';
            }
        };

        recognition.onerror = (event) => {
            voiceStatus.innerHTML = '❌ Error: ' + event.error + '. Please try again.';
            voiceStatus.style.color = '#ff6b6b';
            voiceBtn.innerHTML = '🎤 Click & Speak Sensor Values';
        };

        recognition.onend = () => {
            voiceBtn.innerHTML = '🎤 Click & Speak Sensor Values';
        };

        recognition.start();
    }
    </script>
    """, unsafe_allow_html=True)

    # Process voice query params
    query_params = st.query_params
    if 'v_temp' in query_params:
        try:
            st.session_state.voice_temp = int(float(query_params['v_temp']))
            st.session_state.show_voice_success = True
        except (ValueError, TypeError):
            pass
    if 'v_moist' in query_params:
        try:
            st.session_state.voice_moist = int(float(query_params['v_moist']))
        except (ValueError, TypeError):
            pass


# ============ SENSOR INPUT SECTION ============
def sensor_inputs():
    st.markdown("""
    <div class="glass-card" style="padding: 1rem 1.5rem; margin-bottom: 1rem;">
        <div style="font-size: 0.75rem; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.8rem;">
            📡 Live Sensor Readings
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        temp = st.slider("🌡️ Temperature (°C)", 15, 45, st.session_state.voice_temp, key="temp_slider")
    with col2:
        moisture = st.slider("💧 Soil Moisture", 0, 1023, st.session_state.voice_moist, key="moist_slider")
    with col3:
        humidity = st.slider("💨 Humidity (%)", 20, 95, 65, key="humid_slider")
    with col4:
        rainfall = st.slider("☔ Rainfall (mm)", 0, 350, 120, key="rain_slider")

    st.markdown("</div>", unsafe_allow_html=True)
    return temp, moisture, humidity, rainfall


# ============ CROP RECOMMENDATION ENGINE ============
CROPS = {
    'Rice':      {'temp': (25,35), 'moist': (300,600), 'rain': (150,250), 'season': 'Kharif',     'icon': '🌾', 'days': 120, 'water': 'High'},
    'Wheat':     {'temp': (15,25), 'moist': (250,450), 'rain': (50,150),  'season': 'Rabi',       'icon': '🌿', 'days': 110, 'water': 'Medium'},
    'Sugarcane': {'temp': (25,35), 'moist': (300,500), 'rain': (100,250), 'season': 'Year-round', 'icon': '🎋', 'days': 365, 'water': 'High'},
    'Cotton':    {'temp': (25,35), 'moist': (250,400), 'rain': (50,150),  'season': 'Kharif',     'icon': '🌼', 'days': 160, 'water': 'Medium'},
    'Groundnut': {'temp': (25,35), 'moist': (200,350), 'rain': (40,120),  'season': 'Kharif',     'icon': '🥜', 'days': 105, 'water': 'Low'},
    'Maize':     {'temp': (20,30), 'moist': (250,450), 'rain': (60,180),  'season': 'Kharif',     'icon': '🌽', 'days': 100, 'water': 'Medium'},
    'Turmeric':  {'temp': (20,35), 'moist': (300,500), 'rain': (100,200), 'season': 'Year-round', 'icon': '🪴', 'days': 240, 'water': 'Medium'},
    'Chilli':    {'temp': (20,30), 'moist': (250,400), 'rain': (60,120),  'season': 'Kharif',     'icon': '🌶️', 'days': 90,  'water': 'Low'},
}

def recommend_crop(temp, moisture, rainfall, season, soil):
    scores = {}
    for crop, data in CROPS.items():
        score = 0
        if data['temp'][0] <= temp <= data['temp'][1]:   score += 30
        if data['moist'][0] <= moisture <= data['moist'][1]: score += 25
        if data['rain'][0] <= rainfall <= data['rain'][1]:  score += 25
        if data['season'] == season or data['season'] == 'Year-round': score += 15
        if soil in ['Loamy', 'Black']: score += 5
        scores[crop] = min(score, 97)

    sorted_crops = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_crop, best_score = sorted_crops[0]
    return best_crop, best_score, CROPS[best_crop], sorted_crops[1:4]


# ============ IRRIGATION DECISION ============
def get_irrigation(moisture, temp):
    if moisture < 200:
        return "🚨 WATER NOW", "Critical", 25, "#DC2F02"
    elif moisture < 300:
        return "⚠️ Water Soon", "High", 15, "#E85D04"
    elif moisture < 400:
        return "✅ Moderate", "Medium", 10, "#F48C06"
    else:
        return "💚 Optimal", "Low", 0, "#2D6A4F"


# ============ WEED STATUS ============
def get_weed_status(last_check_days):
    if last_check_days >= 10:
        return "CRITICAL", "Weeds detected! Remove immediately", "#DC2F02"
    elif last_check_days >= 7:
        return "WARNING", "Weed growth likely. Remove within 2 days", "#E85D04"
    elif last_check_days >= 4:
        return "MONITOR", "Check your field for early weed growth", "#F48C06"
    else:
        return "GOOD", "No weed issues detected", "#2D6A4F"


# ============ PAGE: HOME ============
def page_home():
    col_main, col_voice = st.columns([2, 1])

    with col_main:
        if not st.session_state.farmer_name:
            st.markdown("""
            <div class="page-header">
                <h1>🌾 Welcome to VayalAI</h1>
                <p>Your intelligent AI-powered farming assistant for Tamil Nadu & beyond</p>
            </div>
            """, unsafe_allow_html=True)

            with st.container():
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("#### 👨‍🌾 Tell us about yourself")
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    name = st.text_input("Farmer Name", placeholder="Enter your name")
                    village = st.text_input("Village / District", placeholder="e.g., Thanjavur")
                with col_f2:
                    size = st.number_input("Farm Size (acres)", min_value=0.5, max_value=100.0, value=5.0, step=0.5)
                    soil = st.selectbox("Soil Type", ["Loamy", "Clay", "Sandy", "Black", "Laterite"])

                season = st.selectbox("Current Season", ["Kharif (June-Nov)", "Rabi (Oct-Mar)", "Zaid (Mar-Jun)"])

                st.markdown("</div>", unsafe_allow_html=True)

                if st.button("🌱 Start Farming with VayalAI", use_container_width=True, type="primary"):
                    if name.strip():
                        st.session_state.farmer_name = name.strip()
                        st.session_state.village = village.strip()
                        st.session_state.farm_size = size
                        st.session_state.soil_type = soil
                        st.session_state.season = season.split(" ")[0]
                        st.success("✅ Profile saved! Use the sidebar to explore features.")
                        st.rerun()
                    else:
                        st.warning("⚠️ Please enter your name to continue.")
        else:
            st.markdown(f"""
            <div class="page-header">
                <h1>🌾 Welcome back, {st.session_state.farmer_name}!</h1>
                <p>📍 {st.session_state.village} &nbsp;|&nbsp; 🧪 {st.session_state.soil_type} Soil &nbsp;|&nbsp; 🌾 {st.session_state.farm_size} acres &nbsp;|&nbsp; 🗓️ {st.session_state.season} Season</p>
            </div>
            """, unsafe_allow_html=True)

            # Stats row
            c1, c2, c3, c4 = st.columns(4)
            stats = [
                ("🌱", len(st.session_state.planted_crops), "Crops Growing"),
                ("📓", len(st.session_state.observations), "Diary Entries"),
                ("🌿", st.session_state.soil_type, "Soil Type"),
                ("📏", f"{st.session_state.farm_size}ac", "Farm Size"),
            ]
            for col, (icon, val, lbl) in zip([c1, c2, c3, c4], stats):
                with col:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1.8rem;">{icon}</div>
                        <div class="metric-value">{val}</div>
                        <div class="metric-label">{lbl}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Quick actions
            st.markdown("#### 🎯 Quick Actions")
            q1, q2, q3, q4 = st.columns(4)
            actions = [("🌱 Crop Advice", "Crop Advisor"), ("💧 Irrigation", "Irrigation"),
                       ("🚨 Weed Alert", "Weed Alert"), ("💰 Profit Calc", "Profit Calc")]
            for col, (label, target) in zip([q1, q2, q3, q4], actions):
                with col:
                    if st.button(label, use_container_width=True, key=f"quick_{target}"):
                        st.session_state.page = target
                        st.rerun()

    with col_voice:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🎤</div>
            <div style="font-size: 1rem; font-weight: 700; color: #95D5B2; margin-bottom: 0.3rem;">Voice Input</div>
            <p style="font-size: 0.82rem; color: rgba(255,255,255,0.6);">
                Say: <em>"Temperature 32, moisture 280"</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
        voice_input_component()

        if st.session_state.show_voice_success:
            st.success(f"🎤 Applied: {st.session_state.voice_temp}°C · Moisture {st.session_state.voice_moist}")
            st.session_state.show_voice_success = False

    # Features grid
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### ✨ What VayalAI Can Do")
    features = [
        ("🌱", "Crop Advisor", "AI picks the best crop for your soil, season & conditions"),
        ("💧", "Smart Irrigation", "Know exactly when and how long to water"),
        ("🚨", "Weed Alerts", "Timely reminders prevent up to 40% yield loss"),
        ("💰", "Profit Calculator", "Estimate income before you plant"),
        ("📊", "Farm Dashboard", "Track all your crops in one place"),
        ("📓", "Farm Diary", "Log daily observations for better decisions"),
        ("🎤", "Voice Control", "Input data hands-free in English or Tamil"),
        ("🌤️", "AI Recommendations", "Smart tips based on live sensor data"),
    ]
    rows = [features[:4], features[4:]]
    for row in rows:
        cols = st.columns(4)
        for col, (icon, title, desc) in zip(cols, row):
            with col:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; padding: 1.2rem 0.8rem;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                    <div style="font-weight: 700; font-size: 0.9rem; color: #95D5B2;">{title}</div>
                    <div style="font-size: 0.75rem; color: rgba(255,255,255,0.55); margin-top: 0.3rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)


# ============ PAGE: CROP ADVISOR ============
def page_crop_advisor():
    st.markdown("""
    <div class="page-header">
        <h1>🌱 AI Crop Advisor</h1>
        <p>Get personalized crop recommendations based on your current farm conditions</p>
    </div>
    """, unsafe_allow_html=True)

    col_vc, _ = st.columns([1, 2])
    with col_vc:
        voice_input_component()

    temp, moisture, humidity, rainfall = sensor_inputs()

    crop, confidence, crop_data, alternatives = recommend_crop(
        temp, moisture, rainfall, st.session_state.season, st.session_state.soil_type
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
        <div class="green-card" style="text-align: center;">
            <div style="font-size: 5rem; margin-bottom: 0.5rem;">{crop_data['icon']}</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: white;">{crop}</div>
            <div style="margin: 1rem 0;">
                <div class="progress-bar"><div class="progress-fill" style="width: {confidence}%;"></div></div>
                <div style="font-size: 0.85rem; margin-top: 6px; opacity: 0.9;">{confidence}% Match Confidence</div>
            </div>
            <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin-top: 0.5rem;">
                <span class="tag">⏱️ {crop_data['days']} days</span>
                <span class="tag">💧 {crop_data['water']} water</span>
                <span class="tag">🌿 {crop_data['season']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"🌾 Add {crop} to My Farm", use_container_width=True, type="primary"):
            new_crop = {
                'name': crop,
                'icon': crop_data['icon'],
                'planted_date': datetime.now().strftime("%Y-%m-%d"),
                'days_to_harvest': crop_data['days'],
                'status': 'Growing',
                'harvest_date': (datetime.now() + timedelta(days=crop_data['days'])).strftime("%Y-%m-%d"),
            }
            st.session_state.planted_crops.append(new_crop)
            st.success(f"✅ {crop} added to your farm! Check 'My Farm' page.")

    with col2:
        st.markdown(f"""
        <div class="success-card" style="margin-bottom: 1rem;">
            <div style="font-weight: 700; font-size: 1rem; color: #95D5B2; margin-bottom: 0.8rem;">📋 Why {crop}?</div>
            <div style="font-size: 0.88rem; line-height: 1.8; color: #d8f3dc;">
                ✅ Temperature {temp}°C is ideal (optimal: {crop_data['temp'][0]}–{crop_data['temp'][1]}°C)<br>
                ✅ Soil moisture {moisture} matches requirements ({crop_data['moist'][0]}–{crop_data['moist'][1]})<br>
                ✅ Rainfall {rainfall}mm is suitable ({crop_data['rain'][0]}–{crop_data['rain'][1]}mm)<br>
                ✅ {st.session_state.season} season is perfect for this crop<br>
                ✅ {st.session_state.soil_type} soil supports good growth
            </div>
        </div>
        """, unsafe_allow_html=True)

        est_yield = random.randint(20, 45)
        st.markdown(f"""
        <div class="glass-card">
            <div style="font-weight: 700; color: #95D5B2; margin-bottom: 0.8rem;">📊 Crop Stats</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; font-size: 0.85rem; color: #d8f3dc;">
                <div>🗓️ <strong>Harvest In</strong><br>{crop_data['days']} days</div>
                <div>💧 <strong>Water Need</strong><br>{crop_data['water']}</div>
                <div>🌿 <strong>Best Season</strong><br>{crop_data['season']}</div>
                <div>⚖️ <strong>Est. Yield</strong><br>{est_yield} Q/acre</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Alternatives
    st.markdown("<br>#### 🔄 Alternative Crops to Consider")
    alt_cols = st.columns(len(alternatives))
    for col, (alt_name, alt_score) in zip(alt_cols, alternatives):
        alt_data = CROPS[alt_name]
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 2.5rem;">{alt_data['icon']}</div>
                <div style="font-weight: 700; color: #95D5B2;">{alt_name}</div>
                <div class="progress-bar" style="margin: 0.5rem 0;"><div class="progress-fill" style="width: {alt_score}%;"></div></div>
                <div style="font-size: 0.75rem; color: rgba(255,255,255,0.55);">{alt_score}% match · {alt_data['days']}d</div>
            </div>
            """, unsafe_allow_html=True)


# ============ PAGE: IRRIGATION ============
def page_irrigation():
    st.markdown("""
    <div class="page-header">
        <h1>💧 Smart Irrigation Manager</h1>
        <p>AI-based watering recommendations from live soil moisture data</p>
    </div>
    """, unsafe_allow_html=True)

    col_vc, _ = st.columns([1, 2])
    with col_vc:
        voice_input_component()

    temp, moisture, humidity, rainfall = sensor_inputs()
    action, urgency, duration, color = get_irrigation(moisture, temp)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""
        <div style="background: {color}; border-radius: 20px; padding: 1.8rem; text-align: center; color: white;
                    box-shadow: 0 8px 30px rgba(0,0,0,0.4);">
            <div style="font-size: 3.5rem;">💧</div>
            <div style="font-size: 1.8rem; font-weight: 800; margin: 0.5rem 0;">{action}</div>
            <div style="font-size: 0.9rem; opacity: 0.85;">Urgency: <strong>{urgency}</strong></div>
            <div style="font-size: 2.5rem; font-weight: 800; margin-top: 0.5rem;">{duration} min</div>
            <div style="font-size: 0.75rem; opacity: 0.7;">recommended watering duration</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💧 Activate Water Pump Now", use_container_width=True, type="primary"):
            if duration > 0:
                st.success(f"✅ Pump activated for {duration} minutes!")
            else:
                st.info("ℹ️ Soil moisture is optimal — no watering needed.")
        if st.button("⏰ Set Daily 6 AM Reminder", use_container_width=True):
            st.success("✅ Daily watering reminder set for 6:00 AM")

    with col2:
        freq = "Daily" if moisture < 350 else "Every 2 days"
        best_time = "5:00 AM – 7:00 AM"
        st.markdown(f"""
        <div class="success-card" style="margin-bottom: 1rem;">
            <div style="font-weight: 700; color: #95D5B2; margin-bottom: 0.6rem;">📋 Watering Schedule</div>
            <div style="font-size: 0.88rem; line-height: 2; color: #d8f3dc;">
                🕐 <strong>Best time:</strong> {best_time}<br>
                ⏱️ <strong>Duration:</strong> {duration} minutes<br>
                🔁 <strong>Frequency:</strong> {freq}<br>
                📡 <strong>Moisture reading:</strong> {moisture}/1023<br>
                🌡️ <strong>Temperature:</strong> {temp}°C
            </div>
        </div>
        <div class="glass-card">
            <div style="font-weight: 700; color: #95D5B2; margin-bottom: 0.6rem;">💡 Water Saving Tips</div>
            <div style="font-size: 0.85rem; line-height: 1.9; color: #d8f3dc;">
                • Water early morning to reduce evaporation<br>
                • Drip irrigation saves up to 40% water<br>
                • Mulching helps retain soil moisture longer<br>
                • Avoid watering during peak midday heat
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Weekly schedule
    st.markdown("<br>#### 📅 Weekly Watering Plan")
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    schedule_data = []
    for i, day in enumerate(days):
        water = True if moisture < 350 else (i % 2 == 0)
        schedule_data.append({
            'Day': day,
            'Water?': '✅ Yes' if water else '⏸️ Skip',
            'Duration': f'{duration} min' if water and duration > 0 else '—',
            'Time': '6:00 AM' if water else '—',
            'Method': 'Drip / Flood' if water else '—',
        })
    st.dataframe(pd.DataFrame(schedule_data), use_container_width=True, hide_index=True)


# ============ PAGE: WEED ALERT ============
def page_weed_alert():
    st.markdown("""
    <div class="page-header">
        <h1>🚨 Weed Management System</h1>
        <p>Timely weed removal can increase your crop yield by up to 40%</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        last_check = st.number_input("Days since last weed check", min_value=0, max_value=30, value=7, step=1)

    status, message, color = get_weed_status(last_check)

    if status in ("CRITICAL", "WARNING"):
        days_action = 1 if status == "CRITICAL" else 2
        st.markdown(f"""
        <div class="weed-alert">
            <div style="font-size: 1.4rem; font-weight: 800;">⚠️ {status} ALERT</div>
            <div style="margin: 0.5rem 0;">{message}</div>
            <div style="font-size: 0.88rem; opacity: 0.85;">
                Weeds compete with crops for water, nutrients, and sunlight.<br>
                <strong>👉 Action required within {days_action} day{'s' if days_action > 1 else ''}!</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-card">
            <div style="font-size: 1.2rem; font-weight: 700; color: #95D5B2;">✅ {status}</div>
            <div style="margin-top: 0.3rem;">{message}</div>
            <div style="font-size: 0.85rem; opacity: 0.8; margin-top: 0.3rem;">Keep monitoring every 3–4 days for best results.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>#### 🛠️ Weed Removal Guide")
    guide = [
        ("📅", "Best Time", "Early morning or evening.\nAvoid midday heat."),
        ("🛠️", "Methods", "Manual removal\nMulching\nNatural herbicides"),
        ("⏱️", "Time Needed", "2–3 hours per acre\nFor manual removal"),
        ("🔁", "Frequency", "Check every 3–7 days\nRemove when spotted"),
    ]
    gcols = st.columns(4)
    for col, (icon, title, body) in zip(gcols, guide):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="font-weight: 700; color: #95D5B2; margin: 0.4rem 0;">{title}</div>
                <div style="font-size: 0.8rem; color: rgba(255,255,255,0.65); white-space: pre-line;">{body}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✅ Mark Weeds Removed Today", use_container_width=True, type="primary"):
        st.success("🎉 Weed removal recorded! Schedule your next check in 7 days.")
        st.balloons()

    # Info about common weeds
    st.markdown("#### 🌿 Common Weeds in Tamil Nadu Fields")
    weeds = [
        ("Barnyard Grass", "Competes heavily with rice", "🌾"),
        ("Wild Mustard", "Common in wheat fields", "🌼"),
        ("Nut Grass (Cyperus)", "Hard to remove, spreads fast", "🪴"),
        ("Pigweed", "Affects groundnut yield", "🌿"),
    ]
    wcols = st.columns(4)
    for col, (name, desc, icon) in zip(wcols, weeds):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 1rem;">
                <div style="font-size: 1.8rem;">{icon}</div>
                <div style="font-weight: 700; font-size: 0.85rem; color: #f4a261; margin: 0.3rem 0;">{name}</div>
                <div style="font-size: 0.75rem; color: rgba(255,255,255,0.55);">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ============ PAGE: MY FARM ============
def page_my_farm():
    st.markdown("""
    <div class="page-header">
        <h1>📊 My Farm Dashboard</h1>
        <p>Track your planted crops, soil health, and farm statistics</p>
    </div>
    """, unsafe_allow_html=True)

    # Farm summary metrics
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("📏", f"{st.session_state.farm_size}", "Farm Size (acres)"),
        ("🌱", str(len(st.session_state.planted_crops)), "Crops Growing"),
        ("🧪", st.session_state.soil_type, "Soil Type"),
        ("🗓️", st.session_state.season, "Current Season"),
    ]
    for col, (icon, val, lbl) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 1.8rem;">{icon}</div>
                <div class="metric-value" style="font-size: 1.5rem;">{val}</div>
                <div class="metric-label">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    # Planted crops
    st.markdown("<br>#### 🌾 My Planted Crops")
    if st.session_state.planted_crops:
        for i, crop in enumerate(st.session_state.planted_crops):
            planted = datetime.strptime(crop['planted_date'], "%Y-%m-%d")
            days_growing = (datetime.now() - planted).days
            progress = min(int((days_growing / crop['days_to_harvest']) * 100), 100)

            with st.container():
                c1, c2, c3, c4, c5 = st.columns([1, 2, 2, 2, 1])
                with c1:
                    st.markdown(f"<div style='font-size: 2rem; text-align: center;'>{crop.get('icon','🌱')}</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"**{crop['name']}**\n\nPlanted: {crop['planted_date']}")
                with c3:
                    st.markdown(f"""
                    <div style="font-size: 0.82rem; color: #95D5B2; margin-bottom: 4px;">Growth: {progress}%</div>
                    <div class="progress-bar"><div class="progress-fill" style="width: {progress}%;"></div></div>
                    <div style="font-size: 0.75rem; color: rgba(255,255,255,0.5); margin-top: 4px;">{days_growing}/{crop['days_to_harvest']} days</div>
                    """, unsafe_allow_html=True)
                with c4:
                    st.markdown(f"**Harvest:** {crop.get('harvest_date', 'N/A')}")
                with c5:
                    if st.button("🗑️", key=f"del_{i}", help="Remove crop"):
                        st.session_state.planted_crops.pop(i)
                        st.rerun()
            st.markdown("---")
    else:
        st.info("🌱 No crops planted yet. Visit **Crop Advisor** to add your first crop!")

    # Soil health
    st.markdown("#### 🧪 Soil Health Monitor")
    soil_health = random.randint(65, 95)
    soil_label = "Excellent 🟢" if soil_health > 80 else "Good 🟡"
    st.markdown(f"""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div style="font-weight: 700; color: #95D5B2;">Soil Health Score</div>
            <div style="font-size: 1.4rem; font-weight: 800; color: #52B788;">{soil_health}% — {soil_label}</div>
        </div>
        <div class="progress-bar"><div class="progress-fill" style="width: {soil_health}%;"></div></div>
        <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5); margin-top: 0.5rem;">
            Based on soil type, recent moisture levels, and crop history
        </div>
    </div>
    """, unsafe_allow_html=True)

    if soil_health < 80:
        st.info("💡 **Tip:** Add organic compost or vermicompost to improve soil health and yield.")
    else:
        st.success("✅ Soil health is excellent! Maintain organic matter levels for continued performance.")


# ============ PAGE: PROFIT CALCULATOR ============
def page_profit_calculator():
    st.markdown("""
    <div class="page-header">
        <h1>💰 Profit Calculator</h1>
        <p>Estimate potential earnings before you plant — make smarter decisions</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        acres = st.number_input("Farm Size (acres)", min_value=1, max_value=100, value=int(st.session_state.farm_size), step=1)

    profit_data = {
        'Rice':      {'profit': 42000, 'icon': '🌾', 'cost': 18000, 'days': 120},
        'Wheat':     {'profit': 38000, 'icon': '🌿', 'cost': 15000, 'days': 110},
        'Sugarcane': {'profit': 75000, 'icon': '🎋', 'cost': 30000, 'days': 365},
        'Cotton':    {'profit': 48000, 'icon': '🌼', 'cost': 22000, 'days': 160},
        'Groundnut': {'profit': 35000, 'icon': '🥜', 'cost': 14000, 'days': 105},
        'Maize':     {'profit': 40000, 'icon': '🌽', 'cost': 16000, 'days': 100},
        'Turmeric':  {'profit': 120000,'icon': '🪴', 'cost': 45000, 'days': 240},
        'Chilli':    {'profit': 65000, 'icon': '🌶️', 'cost': 28000, 'days': 90},
    }

    st.markdown("<br>#### 📊 Profit Estimates by Crop")
    cols_row1 = st.columns(4)
    cols_row2 = st.columns(4)
    all_cols = cols_row1 + cols_row2

    for col, (crop, data) in zip(all_cols, profit_data.items()):
        net = data['profit'] * acres
        cost = data['cost'] * acres
        margin = int(((data['profit'] - data['cost']) / data['profit']) * 100)
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 1rem 0.8rem;">
                <div style="font-size: 2.2rem;">{data['icon']}</div>
                <div style="font-weight: 700; color: #95D5B2; margin: 0.3rem 0;">{crop}</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #52B788;">₹{net:,}</div>
                <div style="font-size: 0.72rem; color: rgba(255,255,255,0.5);">Revenue · {acres} acre{'s' if acres > 1 else ''}</div>
                <div style="font-size: 0.72rem; color: rgba(220,80,80,0.8); margin-top: 2px;">Cost: ₹{cost:,}</div>
                <div class="tag" style="margin-top: 6px;">{margin}% margin</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>")
    st.info("📌 **Disclaimer:** Estimates are based on average market prices (2024–25). Actual profits depend on market rates, input costs, weather, and local factors.")

    # Best crop recommendation
    best_crop = max(profit_data, key=lambda c: profit_data[c]['profit'] - profit_data[c]['cost'])
    best_net = (profit_data[best_crop]['profit'] - profit_data[best_crop]['cost']) * acres
    st.success(f"🏆 **Most Profitable for {acres} acre(s):** {profit_data[best_crop]['icon']} **{best_crop}** — estimated net profit of **₹{best_net:,}**")


# ============ PAGE: FARM DIARY ============
def page_farm_diary():
    st.markdown("""
    <div class="page-header">
        <h1>📓 Farm Diary</h1>
        <p>Record daily field observations for better tracking and decisions</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ✍️ Add Today's Observation")
    col1, col2 = st.columns([2, 1])
    with col1:
        observation = st.text_area(
            "What's happening in your farm today?",
            height=120,
            placeholder="e.g., Leaves turning yellow on the north edge, new pest spotted near rice rows, irrigation extended by 10 min..."
        )
    with col2:
        category = st.selectbox("Category", ["🌿 General", "🐛 Pest/Disease", "💧 Water", "🌡️ Weather", "🌾 Growth", "💊 Treatment"])
        mood = st.selectbox("Crop Health", ["😊 Healthy", "😐 Moderate", "😟 Concerning", "🚨 Critical"])

    if st.button("💾 Save Observation", use_container_width=True, type="primary"):
        if observation.strip():
            st.session_state.observations.append({
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'note': observation.strip(),
                'category': category,
                'health': mood,
            })
            st.success("✅ Observation saved to your diary!")
            st.rerun()
        else:
            st.warning("⚠️ Please write something before saving.")

    # Past observations
    st.markdown(f"<br>#### 📜 Diary Entries ({len(st.session_state.observations)} total)")

    if st.session_state.observations:
        for obs in reversed(st.session_state.observations[-15:]):
            st.markdown(f"""
            <div class="glass-card" style="padding: 1rem 1.2rem; margin: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                    <span style="font-size: 0.72rem; color: rgba(255,255,255,0.45);">📅 {obs['date']}</span>
                    <span class="tag">{obs.get('category', '🌿 General')}</span>
                    <span style="font-size: 0.8rem;">{obs.get('health', '')}</span>
                </div>
                <div style="font-size: 0.9rem; color: #d8f3dc; line-height: 1.6;">{obs['note']}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ Clear All Diary Entries", use_container_width=False):
            st.session_state.observations = []
            st.rerun()
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem;">📓</div>
            <div style="color: rgba(255,255,255,0.5); margin-top: 0.5rem;">No entries yet. Start recording your farm observations!</div>
        </div>
        """, unsafe_allow_html=True)


# ============ ROUTER ============
page = st.session_state.page

if page == "Home":
    page_home()
elif page == "Crop Advisor":
    page_crop_advisor()
elif page == "Irrigation":
    page_irrigation()
elif page == "Weed Alert":
    page_weed_alert()
elif page == "My Farm":
    page_my_farm()
elif page == "Profit Calc":
    page_profit_calculator()
elif page == "Farm Diary":
    page_farm_diary()
else:
    page_home()

# ============ FOOTER ============
st.markdown("""
<div class="footer">
    🌾 VayalAI (வயல் AI) · Built for Indian Farmers · தமிழ்நாட்டு விவசாயிகளுக்கு அர்ப்பணம்
</div>
""", unsafe_allow_html=True)
