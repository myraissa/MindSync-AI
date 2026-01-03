# app/streamlit_app.py
import streamlit as st
from pathlib import Path

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="MindSync AI - Mental Health Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SHARED STYLING (CSS) ====================
st.markdown("""
<style>
/* App background - same design as Chat */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(circle at 50% 50%, rgba(200,220,255,0.08) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}


/* Glass effect overlay */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(circle at 50% 50%, rgba(200,220,255,0.08) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d3561 0%, #1a1f3a 100%);
    border-right: 2px solid rgba(255,255,255,0.1);
}

[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p {
    color: white !important;
}

/* Main title */

[data-testid="stMarkdownContainer"] .main-title {
    font-size: 3em;
    font-weight: 800;
    text-align: center;
    color: #4a5abf;
    margin: 20px 0;
    color: #4a5abf; /* unique solid blue that complements sidebar */
    
}
.subtitle {
    font-size: 1.5em;
    text-align: center;
    opacity: 0.95;
    margin-bottom: 30px;
}

/* Feature cards */
.feature-card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px;
    padding: 30px;
    margin: 20px 0;
    text-align: center;
    transition: transform 0.3s ease;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}
.logo-container {
    text-align: center;
    margin-bottom: 30px;
    padding: 50px;
}
.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.3);
}

.feature-icon {
    font-size: 3em;
    margin-bottom: 15px;
}

/* Buttons */
.stButton button {
    width: 100%;
    border-radius: 15px;
    padding: 15px;
    font-size: 18px;
    font-weight: 600;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 25px rgba(102,126,234,0.4);
}

/* Floating animation */
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.floating {
    animation: float 3s ease-in-out infinite;
}
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
import os
with st.sidebar:
    # App logo
    try:
        logo_path = os.path.join(os.path.dirname(__file__), ".", "assets", "logo.png")
        st.image(logo_path)
    except Exception as e:
        st.markdown("<div class='logo-container'>MindSync AI</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # App information
    st.markdown("""
    ### About MindSync AI
    
    Smart mental health app using AI:
    
    - **Understands your emotions** through text analysis
    - **Deep conversations** with specialized AI
    - **Crisis detection** and rapid intervention
    - **Mood tracking** over time
    """)
    
    st.markdown("---")
    st.warning("⚠️ **Not a replacement for professional therapy**")
    
    st.markdown("---")
    st.error("""
    **🆘 Emergency Contacts:**
    - Tunisia: **80 101 080**
    - International: **116 123**
    """)

# ==================== MAIN CONTENT ====================
st.markdown("<h1 class='main-title floating'>MindSync AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your Intelligent Mental Health Companion 💙</p>", unsafe_allow_html=True)

st.markdown("---")

# ==================== FEATURE CARDS ====================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🏠</div>
        <h3>Dashboard</h3>
        <p>Get a comprehensive overview of your mental health, statistics, and progress</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Dashboard →", key="dash"):
        st.switch_page("pages/1_Dashboard.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <h3>Chat</h3>
        <p>Talk with an intelligent AI that understands your emotions and provides support</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Conversation →", key="chat"):
        st.switch_page("pages/2_Chat.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Mood Tracker</h3>
        <p>Track your mood over time with clear data visualizations</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Track Mood →", key="mood"):
        st.switch_page("pages/3_Mood_Tracker.py")

st.markdown("---")
