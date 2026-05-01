"""
VayalAI (வயல் AI) - Farmer's Intelligent Field Assistant
Multi-page interactive app with voice input, crop recommendations, weed alerts, and more
"""

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import re
import plotly.graph_objects as go
import plotly.express as px
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
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

/* Farm background */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
                url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=1932&auto=format');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Glass morphism cards */
.glass-card {
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 1.5rem;
    margin: 0.5rem 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    transition: transform 0.3s;
}
.glass-card:hover {
    transform: translateY(-5px);
}

.green-card {
    background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%);
    color: white;
    border-radius: 20px;
    padding: 1.5rem;
    margin: 0.5rem 0;
}

.success-card {
    background: linear-gradient(135deg, #D8F3DC 0%, #95D5B2 100%);
    border-radius: 16px;
    padding: 1rem;
    color: #1B4332;
    border-left: 4px solid #2D6A4F;
}

.weed-alert {
    background: linear-gradient(135deg, #DC2F02 0%, #9D0208 100%);
    color: white;
    padding: 1rem;
    border-radius: 16px;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.02); opacity: 0.95; }
    100% { transform: scale(1); opacity: 1; }
}

.nav-button {
    background: rgba(45, 106, 79, 0.15);
    border: 2px solid #2D6A4F;
    border-radius: 12px;
    padding: 0.8rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
    margin: 0.3rem 0;
}
.nav-button:hover {
    background: rgba(45, 106, 79, 0.3);
    transform: translateX(5px);
}
.nav-button-active {
    background: #2D6A4F;
    color: white;
}

.voice-btn {
    background: linear-gradient(135deg, #52B788 0%, #2D6A4F 100%);
    color: white;
    border: none;
    padding: 14px 28px;
    border-radius: 40px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    transition: all 0.3s;
}
.voice-btn:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 12px rgba(45,106,79,0.4);
}

.progress-bar {
    background: #E8F5E9;
    border-radius: 10px;
    height: 8px;
    overflow: hidden;
}
.progress-fill {
    background: #2D6A4F;
    height: 100%;
    border-radius: 10px;
    transition: width 0.5s;
}

.crop-icon {
    font-size: 3rem;
    text-align: center;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #2D6A4F;
}

.footer {
    text-align: center;
    color: rgba(255,255,255,0.7);
    padding: 1.5rem;
    margin-top: 2rem;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: rgba(27, 67, 50, 0.95);
    backdrop-filter: blur(10px);
}
[data-testid="stSidebar"] * {
    color: white !important;
}
[data-testid="stSidebar"] .stSlider label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ============ SESSION STATE INITIALIZATION ============
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'farmer_name' not in st.session_state:
    st.session_state.farmer_name = ""
if 'village' not in st.session_state:
    st.session_state.village = ""
if 'farm_size' not in st.session_state:
    st.session_state.farm_size = 5.0
if 'soil_type' not in st.session_state:
    st.session_state.soil_type = "Loamy"
if 'season' not in st.session_state:
    st.session_state.season = "Kharif"
if 'planted_crops' not in st.session_state:
    st.session_state.planted_crops = []
if 'observations' not in st.session_state:
    st.session_state.observations = []
if 'voice_temp' not in st.session_state:
    st.session_state.voice_temp = 32
if 'voice_moist' not in st.session_state:
    st.session_state.voice_moist = 350
if 'show_voice_success' not in st.session_state:
    st.session_state.show_voice_success = False

# ============ SIDEBAR NAVIGATION ============
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="font-size: 2rem; margin: 0;">🌾 VayalAI</h1>
        <p style="font-size: 0.8rem; opacity: 0.8;">வயல் AI</p>
        <p style="font-size: 0.7rem;">Farmer's Field Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation buttons
    pages = ["🏠 Home", "🌱 Crop Advisor", "💧 Irrigation", "🚨 Weed Alert", "📊 My Farm", "🎯 Profit Calc", "📓 Farm Diary"]
    
    for p in pages:
        if st.button(p, use_container_width=True, key=f"nav_{p}"):
            st.session_state.page = p.replace("🏠 ", "").replace("🌱 ", "").replace("💧 ", "").replace("🚨 ", "").replace("📊 ", "").replace("🎯 ", "").replace("📓 ", "")
            st.rerun()
    
    st.markdown("---")
    
    # Farmer info display
    if st.session_state.farmer_name:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); border-radius: 12px; padding: 0.8rem; margin-top: 1rem;">
            <small>👨‍🌾 Farmer</small><br>
            <strong>{st.session_state.farmer_name}</strong><br>
            <small>📍 {st.session_state.village}</small>
        </div>
        """, unsafe_allow_html=True)

# ============ VOICE INPUT COMPONENT ============
def voice_input_component():
    st.markdown("""
    <div id="voice-container">
        <button id="voice-btn" class="voice-btn">
            🎤 Click and Speak (English or Tamil)
        </button>
        <div id="voice-status" style="font-size: 12px; text-align: center; margin-top: 8px;"></div>
    </div>
    
    <script>
        const voiceBtn = document.getElementById('voice-btn');
        const voiceStatus = document.getElementById('voice-status');
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (SpeechRecognition) {
            let currentLang = 'en-US';
            
            function startRecognition(lang) {
                currentLang = lang;
                const recognition = new SpeechRecognition();
                recognition.lang = lang;
                recognition.continuous = false;
                recognition.interimResults = false;
                
                recognition.onstart = () => {
                    voiceStatus.innerHTML = '🔴 Listening... Speak sensor values';
                    voiceStatus.style.color = '#ff6b6b';
                };
                
                recognition.onresult = (event) => {
                    const text = event.results[0][0].transcript;
                    voiceStatus.innerHTML = '✅ Recognized: ' + text;
                    voiceStatus.style.color = '#90be6d';
                    
                    const numbers = text.match(/\\d+/g);
                    if (numbers && numbers.length >= 2) {
                        const params = new URLSearchParams();
                        params.set('v_temp', numbers[0]);
                        params.set('v_moist', numbers[1]);
                        window.parent.location.hash = '?' + params.toString();
                        setTimeout(() => { window.parent.location.reload(); }, 800);
                    }
                };
                
                recognition.onerror = () => {
                    voiceStatus.innerHTML = '❌ Try again. Speak clearly.';
                };
                
                recognition.start();
            }
            
            voiceBtn.onclick = () => {
                const langChoice = confirm('English? Click OK. Tamil? Click Cancel.');
                if (langChoice) {
                    startRecognition('en-US');
                } else {
                    startRecognition('ta-IN');
                }
            };
        } else {
            voiceStatus.innerHTML = '❌ Voice not supported. Use Chrome.';
            voiceBtn.disabled = true;
        }
    </script>
    """, unsafe_allow_html=True)
    
    # Process voice parameters
    query_params = st.query_params
    if query_params:
        if 'v_temp' in query_params:
            st.session_state.voice_temp = float(query_params['v_temp'])
            st.session_state.show_voice_success = True
        if 'v_moist' in query_params:
            st.session_state.voice_moist = int(query_params['v_moist'])

# ============ CROP RECOMMENDATION ENGINE ============
def recommend_crop(temp, moisture, rainfall, season, soil):
    crops = {
        'Rice': {'temp': (25,35), 'moist': (300,600), 'rain': (150,250), 'season': 'Kharif', 'icon': '🌾', 'days': 120},
        'Wheat': {'temp': (15,25), 'moist': (250,450), 'rain': (50,150), 'season': 'Rabi', 'icon': '🌿', 'days': 110},
        'Sugarcane': {'temp': (25,35), 'moist': (300,500), 'rain': (100,250), 'season': 'Year-round', 'icon': '🎋', 'days': 365},
        'Cotton': {'temp': (25,35), 'moist': (250,400), 'rain': (50,150), 'season': 'Kharif', 'icon': '🌼', 'days': 160},
        'Groundnut': {'temp': (25,35), 'moist': (200,350), 'rain': (40,120), 'season': 'Kharif', 'icon': '🥜', 'days': 105},
        'Maize': {'temp': (20,30), 'moist': (250,450), 'rain': (60,180), 'season': 'Kharif', 'icon': '🌽', 'days': 100},
        'Turmeric': {'temp': (20,35), 'moist': (300,500), 'rain': (100,200), 'season': 'Year-round', 'icon': '🪴', 'days': 240},
        'Chilli': {'temp': (20,30), 'moist': (250,400), 'rain': (60,120), 'season': 'Kharif', 'icon': '🌶️', 'days': 90}
    }
    
    scores = {}
    for crop, data in crops.items():
        score = 0
        if data['temp'][0] <= temp <= data['temp'][1]: score += 25
        if data['moist'][0] <= moisture <= data['moist'][1]: score += 25
        if data['rain'][0] <= rainfall <= data['rain'][1]: score += 25
        if data['season'] == season or data['season'] == 'Year-round': score += 15
        if soil in ['Loamy', 'Black']: score += 10
        scores[crop] = min(score, 95)
    
    best_crop = max(scores, key=scores.get)
    return best_crop, scores[best_crop], crops[best_crop]

# ============ IRRIGATION DECISION ============
def get_irrigation(moisture, temp):
    if moisture < 200:
        return "🚨 WATER NOW", "Critical", 20, "#DC2F02"
    elif moisture < 300:
        return "⚠️ Water Soon", "High", 12, "#E85D04"
    elif moisture < 400:
        return "✅ Normal", "Medium", 8, "#F48C06"
    else:
        return "💚 Optimal", "Low", 0, "#2D6A4F"

# ============ WEED ALERT ============
def get_weed_status(last_check_days):
    if last_check_days >= 10:
        return "CRITICAL", "Weeds detected! Remove immediately", "#DC2F02"
    elif last_check_days >= 7:
        return "WARNING", "Weed growth detected. Remove within 2 days", "#E85D04"
    elif last_check_days >= 4:
        return "MONITOR", "Check for weeds soon", "#F48C06"
    else:
        return "GOOD", "No weed issues", "#2D6A4F"

# ============ SENSOR INPUT SECTION ============
def sensor_inputs():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        temp = st.slider("🌡️ Temperature (°C)", 15, 45, st.session_state.voice_temp)
    with col2:
        moisture = st.slider("💧 Soil Moisture", 0, 1023, st.session_state.voice_moist)
    with col3:
        humidity = st.slider("💨 Humidity (%)", 20, 95, 65)
    with col4:
        rainfall = st.slider("☔ Rainfall (mm)", 0, 350, 120)
    
    return temp, moisture, humidity, rainfall

# ============ PAGE: HOME ============
def page_home():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <h1>🌾 Welcome to VayalAI</h1>
        <p style="font-size: 1.1rem;">Your intelligent farming assistant powered by AI</p>
        """, unsafe_allow_html=True)
        
        if not st.session_state.farmer_name:
            st.subheader("👨‍🌾 Tell us about yourself")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                name = st.text_input("Farmer Name")
                village = st.text_input("Village/District")
            with col_f2:
                size = st.number_input("Farm Size (acres)", 0.5, 100.0, 5.0)
                soil = st.selectbox("Soil Type", ["Loamy", "Clay", "Sandy", "Black", "Laterite"])
            
            season_options = ["Kharif (June-Nov)", "Rabi (Oct-Mar)", "Zaid (Mar-Jun)"]
            season = st.selectbox("Current Season", season_options)
            
            if st.button("🌱 Start Farming with VayalAI", use_container_width=True):
                st.session_state.farmer_name = name
                st.session_state.village = village
                st.session_state.farm_size = size
                st.session_state.soil_type = soil
                st.session_state.season = season.split(" ")[0]
                st.success("✅ Welcome! Explore all features in sidebar.")
                st.rerun()
        else:
            st.markdown(f"""
            <div class="success-card">
                <strong>👨‍🌾 Welcome back, {st.session_state.farmer_name}!</strong><br>
                📍 {st.session_state.village} | 🧪 {st.session_state.soil_type} Soil | 🌾 {st.session_state.farm_size} acres
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🎯 Quick Actions")
            q1, q2, q3, q4 = st.columns(4)
            with q1:
                if st.button("🌱 Crop Advice", use_container_width=True):
                    st.session_state.page = "Crop Advisor"
                    st.rerun()
            with q2:
                if st.button("💧 Irrigation", use_container_width=True):
                    st.session_state.page = "Irrigation"
                    st.rerun()
            with q3:
                if st.button("🚨 Weed Alert", use_container_width=True):
                    st.session_state.page = "Weed Alert"
                    st.rerun()
            with q4:
                if st.button("📊 My Farm", use_container_width=True):
                    st.session_state.page = "My Farm"
                    st.rerun()
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 4rem;">🌾</div>
            <h3>Voice Input Ready</h3>
            <p>Click below and say:<br>
            "Temperature 32, moisture 280"</p>
        </div>
        """, unsafe_allow_html=True)
        voice_input_component()
        
        if st.session_state.show_voice_success:
            st.success(f"🎤 Voice applied: {st.session_state.voice_temp}°C, {st.session_state.voice_moist} moisture")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Features grid
    st.markdown("### ✨ Features")
    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("🌱", "Crop Advisor", "AI-powered crop recommendations"),
        ("💧", "Smart Irrigation", "Water scheduling based on soil"),
        ("🚨", "Weed Alerts", "Timely weed removal reminders"),
        ("📊", "Profit Calculator", "Estimate your earnings")
    ]
    for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 1rem;">
                <div style="font-size: 2.5rem;">{icon}</div>
                <strong>{title}</strong><br>
                <small>{desc}</small>
            </div>
            """, unsafe_allow_html=True)

# ============ PAGE: CROP ADVISOR ============
def page_crop_advisor():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h1>🌱 AI Crop Advisor</h1>", unsafe_allow_html=True)
    st.markdown("Get personalized crop recommendations based on your farm conditions")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Voice input
    col_v1, col_v2, col_v3 = st.columns([1, 2, 1])
    with col_v2:
        voice_input_component()
    
    # Sensor inputs
    temp, moisture, humidity, rainfall = sensor_inputs()
    
    # Get recommendation
    crop, confidence, crop_data = recommend_crop(temp, moisture, rainfall, st.session_state.season, st.session_state.soil_type)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""
        <div class="green-card" style="text-align: center;">
            <div style="font-size: 5rem;">{crop_data['icon']}</div>
            <h1 style="font-size: 2.5rem;">{crop}</h1>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {confidence}%;"></div>
            </div>
            <p>{confidence}% Match Confidence</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"🌾 Plant {crop} in my field", use_container_width=True):
            new_crop = {
                'name': crop,
                'planted_date': datetime.now().strftime("%Y-%m-%d"),
                'days_to_harvest': crop_data['days'],
                'status': 'Growing'
            }
            st.session_state.planted_crops.append(new_crop)
            st.success(f"✅ {crop} added to your farm! Check 'My Farm' page.")
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div class="success-card">
            <strong>📋 Why {crop}?</strong><br><br>
            • Temperature {temp}°C is ideal (optimal {crop_data['temp'][0]}-{crop_data['temp'][1]}°C)<br>
            • Soil moisture {moisture} matches requirements<br>
            • Rainfall {rainfall}mm is suitable<br>
            • {st.session_state.season} season is perfect<br>
            • {st.session_state.soil_type} soil works well
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="glass-card">
            <strong>📊 Crop Details</strong><br>
            🌾 Days to harvest: {crop_data['days']} days<br>
            💧 Water need: {"High" if confidence > 80 else "Medium"}<br>
            🌡️ Best season: {crop_data['season']}<br>
            💰 Expected yield: {random.randint(20, 45)} quintals/acre
        </div>
        """, unsafe_allow_html=True)
    
    # Alternative crops
    st.markdown("### 🔄 Alternative Crops You Can Consider")
    alts = ['Wheat', 'Maize', 'Groundnut']
    alt_cols = st.columns(3)
    for col, alt in zip(alt_cols, alts):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 2rem;">{'🌾' if alt == 'Wheat' else '🌽' if alt == 'Maize' else '🥜'}</div>
                <strong>{alt}</strong><br>
                <small>Alternative option</small>
            </div>
            """, unsafe_allow_html=True)

# ============ PAGE: IRRIGATION ============
def page_irrigation():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h1>💧 Smart Irrigation Manager</h1>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    voice_input_component()
    
    temp, moisture, humidity, rainfall = sensor_inputs()
    
    action, urgency, duration, color = get_irrigation(moisture, temp)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""
        <div style="background: {color}; border-radius: 20px; padding: 1.5rem; text-align: center; color: white;">
            <div style="font-size: 3rem;">💧</div>
            <h1>{action}</h1>
            <p>Urgency: {urgency}</p>
            <p style="font-size: 1.5rem; font-weight: bold;">{duration} minutes</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Manual pump control
        if st.button("💧 Activate Water Pump", use_container_width=True):
            st.success(f"✅ Pump activated for {duration} minutes")
        
        if st.button("⏰ Set Daily Schedule", use_container_width=True):
            st.success("Daily watering reminder set for 6:00 AM")
    
    with col2:
        st.markdown(f"""
        <div class="success-card">
            <strong>📋 Watering Schedule</strong><br><br>
            • Today: {action}<br>
            • Best time: 5:00 AM - 7:00 AM<br>
            • Duration: {duration} minutes<br>
            • Frequency: {"Daily" if moisture < 350 else "Every 2 days"}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="glass-card">
            <strong>💡 Water Saving Tips</strong><br>
            • Water early morning to reduce evaporation<br>
            • Use drip irrigation for 40% water savings<br>
            • Mulching helps retain soil moisture
        </div>
        """, unsafe_allow_html=True)
    
    # Weekly schedule
    st.markdown("### 📅 Weekly Watering Plan")
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    schedule_data = []
    for i, day in enumerate(days):
        if moisture < 350:
            schedule_data.append({'Day': day, 'Water': '✅ Yes', 'Duration': f'{duration} min', 'Time': '6:00 AM'})
        else:
            schedule_data.append({'Day': day, 'Water': '✅ Yes' if i % 2 == 0 else '⏸️ Skip', 'Duration': f'{duration} min' if i % 2 == 0 else '-', 'Time': '6:00 AM' if i % 2 == 0 else '-'})
    
    st.dataframe(pd.DataFrame(schedule_data), use_container_width=True, hide_index=True)

# ============ PAGE: WEED ALERT ============
def page_weed_alert():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h1>🚨 Weed Management System</h1>", unsafe_allow_html=True)
    st.markdown("Timely weed removal can increase yield by up to 40%")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        last_check = st.number_input("Days since last weed check", min_value=0, max_value=30, value=7)
    
    status, message, color = get_weed_status(last_check)
    
    if status == "CRITICAL" or status == "WARNING":
        st.markdown(f"""
        <div class="weed-alert">
            <h3>⚠️ {status} - {message}</h3>
            <p>Weeds compete with crops for water, nutrients, and sunlight.</p>
            <p><strong>Action required:</strong> Remove weeds within {2 if status == 'WARNING' else 1} days</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-card">
            <h3>✅ {status} - {message}</h3>
            <p>Your field looks healthy! Keep monitoring regularly.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Weed removal tips
    st.markdown("### 🛠️ Weed Removal Guide")
    
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.markdown("""
        <div class="glass-card">
            <strong>📅 Best Time</strong><br>
            Early morning or evening<br>
            Avoid midday heat
        </div>
        """, unsafe_allow_html=True)
    with col_t2:
        st.markdown("""
        <div class="glass-card">
            <strong>🛠️ Methods</strong><br>
            Manual removal<br>
            Mulching<br>
            Natural herbicides
        </div>
        """, unsafe_allow_html=True)
    with col_t3:
        st.markdown("""
        <div class="glass-card">
            <strong>⏱️ Time Needed</strong><br>
            2-3 hours per acre<br>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("✅ Mark Weeds Removed Today", use_container_width=True):
        st.success("Great! Weed removal recorded. Next check in 7 days.")

# ============ PAGE: MY FARM ============
def page_my_farm():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h1>📊 My Farm Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("Track your planted crops and farm health")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Farm summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Farm Size", f"{st.session_state.farm_size} acres", delta="Cultivable")
    with col2:
        st.metric("Planted Crops", len(st.session_state.planted_crops), delta="Growing")
    with col3:
        st.metric("Soil Type", st.session_state.soil_type)
    
    # Planted crops
    st.markdown("### 🌾 My Planted Crops")
    
    if st.session_state.planted_crops:
        for i, crop in enumerate(st.session_state.planted_crops):
            col_c1, col_c2, col_c3, col_c4 = st.columns([2, 2, 2, 1])
            with col_c1:
                st.markdown(f"**{crop['name']}**")
            with col_c2:
                st.markdown(f"Planted: {crop['planted_date']}")
            with col_c3:
                st.markdown(f"Status: ✅ {crop['status']}")
            with col_c4:
                if st.button(f"Update", key=f"update_{i}"):
                    st.info("Growth tracking coming soon")
    else:
        st.info("No crops planted yet. Go to 'Crop Advisor' to plant your first crop!")
    
    # Soil health gauge
    st.markdown("### 🧪 Soil Health Monitor")
    
    soil_health = random.randint(65, 95)
    st.markdown(f"""
    <div class="glass-card">
        <div class="progress-bar">
            <div class="progress-fill" style="width: {soil_health}%;"></div>
        </div>
        <p>Soil Health Score: {soil_health}% - {'Excellent' if soil_health > 80 else 'Good'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("### 📋 Recommendations")
    if soil_health < 80:
        st.info("💡 Add organic compost to improve soil health")
    else:
        st.success("✅ Soil health is excellent! Keep up good practices.")

# ============ PAGE: PROFIT CALCULATOR ============
def page_profit_calculator():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h1>💰 Profit Calculator</h1>", unsafe_allow_html=True)
    st.markdown("Estimate your potential earnings")
    st.markdown('</div>', unsafe_allow_html=True)
    
    acres = st.number_input("Farm Size (acres)", 1, 100, int(st.session_state.farm_size))
    
    profit_data = {
        'Rice': 42000, 'Wheat': 38000, 'Sugarcane': 75000, 'Cotton': 48000,
        'Groundnut': 35000, 'Maize': 40000, 'Turmeric': 120000, 'Chilli': 65000
    }
    
    st.markdown("### 📊 Profit per Acre by Crop")
    
    cols = st.columns(4)
    crops_list = list(profit_data.keys())
    for i, col in enumerate(cols):
        with col:
            if i < len(crops_list):
                crop = crops_list[i]
                profit = profit_data[crop]
                total = profit * acres
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <div style="font-size: 2rem;">{'🌾' if crop=='Rice' else '🌿' if crop=='Wheat' else '🎋' if crop=='Sugarcane' else '🌼' if crop=='Cotton' else '🥜' if crop=='Groundnut' else '🌽' if crop=='Maize' else '🪴'}</div>
                    <strong>{crop}</strong><br>
                    <span style="font-size: 1.5rem; color: #2D6A4F;">₹{total:,}</span><br>
                    <small>₹{profit:,}/acre</small>
                </div>
                """, unsafe_allow_html=True)
    
    st.info("💰 Profit estimates based on average market prices. Actual profits may vary.")

# ============ PAGE: FARM DIARY ============
def page_farm_diary():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h1>📓 Farm Diary</h1>", unsafe_allow_html=True)
    st.markdown("Record your daily observations")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # New observation
    st.markdown("### ✍️ Add Today's Observation")
    observation = st.text_area("What's happening in your farm?", height=100,
                               placeholder="e.g., Leaves turning yellow, new growth seen, pest spotted...")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Observation", use_container_width=True):
            if observation:
                st.session_state.observations.append({
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'note': observation
                })
                st.success("✅ Observation saved!")
                st.rerun()
    
    # Past observations
    st.markdown("### 📜 Past Observations")
    if st.session_state.observations:
        for obs in reversed(st.session_state.observations[-10:]):
            st.markdown(f"""
            <div class="glass-card" style="margin: 0.5rem 0;">
                <small>📅 {obs['date']}</small>
                <p>{obs['note']}</p>
            </div>
            """, unsafe_allow
