# app/pages/1_🏠_Dashboard.py
import streamlit as st
import sys
from pathlib import Path
import os
# Add project path
sys.path.append(str(Path(__file__).parent.parent.parent))

from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.services.data_storage_service import DataStorageService
# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Dashboard - MindSync AI",
    layout="wide"
)

# ==================== STYLING (Same CSS) ====================
st.markdown("""
<style>
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
.logo-container {
    text-align: center;
    margin-bottom: 30px;
    padding: 50px;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d3561 0%, #1a1f3a 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.metric-card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.metric-value {
    font-size: 2.5em;
    font-weight: bold;
    margin: 10px 0;
}

.metric-label {
    font-size: 1.2em;
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)
# ==================== INITIALIZE DATA STORAGE ====================
if 'user_id' not in st.session_state:
    st.session_state.user_id = "demo_user"

if 'data_storage' not in st.session_state:
    st.session_state.data_storage = DataStorageService(user_id=st.session_state.user_id)

data_storage = st.session_state.data_storage

# ==================== SIDEBAR ====================
with st.sidebar:
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
        st.image(logo_path)
    except Exception as e:
        st.markdown("<div class='logo-container'>MindSync AI</div>", unsafe_allow_html=True)
    
    st.markdown("### Dashboard Settings")
    time_range_map = {
        "Last 7 days": 7,
        "Last 30 days": 30,
        "Last 3 months": 90,
        "Full year": 365
    }
    time_range = st.selectbox(
        "Select time period:",
        list(time_range_map.keys())
    )
    selected_days = time_range_map[time_range]
    
    st.markdown("---")
    st.info("💡 **Tip:** Use Dashboard to monitor your progress over time")
    
    st.markdown("---")
    if st.button("Refresh Data"):
        st.rerun()

# ==================== LOAD REAL DATA ====================
statistics = data_storage.get_statistics()
avg_mood = data_storage.get_average_mood_score(days=7)
streak_days = data_storage.get_streak_days()
dominant_emotion = data_storage.get_dominant_emotion(days=7)

# Calculate improvement
prev_mood = data_storage.get_average_mood_score(days=14)
if prev_mood > 0:
    mood_change = ((avg_mood - prev_mood) / prev_mood) * 100
else:
    mood_change = 0

# ==================== TITLE ====================
st.markdown("# Dashboard - Overview")
st.markdown("### Welcome to your control panel!")
st.markdown("---")

# ==================== KEY METRICS ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_convos = statistics.get('total_conversations', 0)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Conversations</div>
        <div class="metric-value">{total_convos}</div>
        <div style="color:#4ade80;">Total interactions</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    arrow = "↑" if mood_change > 0 else "↓" if mood_change < 0 else "→"
    color = "#4ade80" if mood_change > 0 else "#ff6b6b" if mood_change < 0 else "#fbbf24"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Average Mood</div>
        <div class="metric-value">{avg_mood}/10</div>
        <div style="color:{color};">{arrow} {abs(mood_change):.1f}% from last week</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # Map emotion to emoji
    emotion_emoji = {
        'Joy': '😊',
        'Neutral': '😐',
        'Sadness': '😔',
        'Anger': '😡',
        'Fear': '😰'
    }
    emoji = emotion_emoji.get(dominant_emotion, '😐')
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Dominant Emotion</div>
        <div class="metric-value">{emoji} {dominant_emotion}</div>
        <div style="opacity:0.8;">Most common this week</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Streak</div>
        <div class="metric-value">{streak_days} days</div>
        <div style="color:#fbbf24;">Keep it up! 💪</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================== CHARTS ====================
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📈 Emotion Evolution")
    
    # Get REAL emotion timeline data
    emotions_data = data_storage.get_emotion_timeline(days=selected_days)
    
    if not emotions_data.empty:
        fig = px.line(emotions_data, x='Date', y=['Joy', 'Sadness', 'Anger', 'Fear', 'Neutral'],
                      labels={'value': 'Percentage', 'variable': 'Emotions'},
                      color_discrete_map={
                          'Joy': '#FFD700',
                          'Sadness': '#4169E1',
                          'Anger': '#DC143C',
                          'Fear': '#9370DB',
                          'Neutral': '#808080'
                      })
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(255,255,255,0.1)',
            font_color='white',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📝 No emotion data yet. Start chatting to see your emotion trends!")

with col_right:
    st.markdown("### 🎭 Emotion Distribution")
    
    # Get REAL emotion distribution
    emotion_dist = data_storage.get_emotion_distribution(days=7)
    
    if not emotion_dist.empty and emotion_dist['Count'].sum() > 0:
        fig2 = px.pie(emotion_dist, values='Count', names='Emotion',
                      color='Emotion',
                      color_discrete_map={
                          'Joy': '#FFD700',
                          'Neutral': '#808080',
                          'Sadness': '#4169E1',
                          'Anger': '#DC143C',
                          'Fear': '#9370DB'
                      })
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(255,255,255,0.1)',
            font_color='white',
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("📝 No emotion data yet. Start chatting to see your emotion distribution!")

st.markdown("---")

# ==================== ACHIEVEMENTS ====================
st.markdown("### 🏆 Achievements")
ach_col1, ach_col2, ach_col3 = st.columns(3)

with ach_col1:
    if streak_days >= 7:
        st.success(f"""
        **🔥 {streak_days}-Day Streak**  
        You maintained a streak for {streak_days} days!
        """)
    else:
        st.info(f"""
        **🔥 Current Streak: {streak_days} days**  
        Keep going to reach 7 days!
        """)

with ach_col2:
    total_convos = statistics.get('total_conversations', 0)
    if total_convos >= 100:
        st.success(f"""
        **💬 Active Conversationalist**  
        You've had {total_convos} conversations!
        """)
    elif total_convos >= 10:
        st.info(f"""
        **💬 Getting Started**  
        {total_convos} conversations so far!
        """)
    else:
        st.warning(f"""
        **💬 Just Beginning**  
        {total_convos} conversations. Keep chatting!
        """)

with ach_col3:
    mood_entries = len(data_storage.get_mood_entries())
    if mood_entries >= 20:
        st.success(f"""
        **📊 Accurate Tracker**  
        {mood_entries} mood entries logged!
        """)
    else:
        st.info(f"""
        **📊 Building History**  
        {mood_entries} mood entries so far!
        """)

# ==================== CRISIS ALERTS ====================
crisis_count = statistics.get('crisis_alerts', 0)
if crisis_count > 0:
    st.markdown("---")
    st.error(f"""
    ### 🚨 Crisis Alerts: {crisis_count}
    
    We detected {crisis_count} potential crisis situation(s) in your conversations.
    
    **Remember:**
    - 📞 Tunisia: **80 101 080**
    - 🌍 International: **116 123**
    
    These services are confidential and available 24/7.
    """)

# ==================== PERSONALIZED TIPS ====================
st.markdown("---")
st.markdown("### 💡 Personalized Tips for You")

# Generate personalized tips based on data
tips = []

if avg_mood >= 7:
    tips.append("🌟 You're doing great! Your mood has been consistently positive.")
elif avg_mood < 5:
    tips.append("💙 Your mood seems lower than usual. Consider reaching out for support.")

if dominant_emotion == "Joy":
    tips.append("😊 Joy is your dominant emotion! Keep doing what makes you happy.")
elif dominant_emotion == "Sadness":
    tips.append("🫂 Sadness has been prominent. It's okay to feel this way. Consider talking about it.")

if streak_days >= 7:
    tips.append(f"🔥 Amazing {streak_days}-day streak! Consistency is key to mental wellness.")
elif streak_days == 0:
    tips.append("📅 Try to check in daily for better mental health tracking.")

if mood_change > 10:
    tips.append("📈 Your mood improved significantly! Keep up the positive momentum.")
elif mood_change < -10:
    tips.append("📉 Your mood has declined recently. Let's work on improving it together.")

if not tips:
    tips.append("💭 Keep tracking your emotions to get personalized insights!")

for tip in tips:
    st.info(tip)

# ==================== RECENT CONVERSATIONS ====================
st.markdown("---")
st.markdown("### 💬 Recent Conversations")

recent_convos = data_storage.get_conversations(limit=5)

if recent_convos:
    for convo in reversed(recent_convos):
        timestamp = datetime.fromisoformat(convo['timestamp'])
        emotion = convo['detected_emotion'].capitalize()
        confidence = convo['emotion_confidence']
        
        with st.expander(f"🕒 {timestamp.strftime('%Y-%m-%d %H:%M')} - {emotion} ({confidence:.0%})"):
            st.markdown(f"**You:** {convo['user_message']}")
            st.markdown(f"**AI:** {convo['ai_response']}")
else:
    st.info("No conversations yet. Start chatting to see your history here!")