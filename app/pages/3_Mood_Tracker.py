# app/pages/3_📊_Mood_Tracker.py
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from src.services.data_storage_service import DataStorageService
from typing import cast

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Mood Tracker - MindSync AI",
    layout="wide"
)

# ==================== STYLING ====================
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

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d3561 0%, #1a1f3a 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.mood-card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px;
    padding: 20px;
    margin: 15px 0;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}

.mood-card:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}

.mood-emoji {
    font-size: 3em;
    margin: 10px 0;
}

.main-title {
    font-size: 3em;
    font-weight: 800;
    text-align: center;
    color: #4a5abf;
    margin: 20px 0;
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
    st.markdown("### Mood Tracker Settings")
    
    tracking_mode = st.radio(
        "Tracking Mode:",
        ["Log New Mood", "View History", "Analytics"]
    )
    
    st.markdown("---")
    st.info("💡 **Tip:** Log your mood daily to get better insights!")
    
    st.markdown("---")
    if st.button("Refresh Data"):
        st.rerun()

# ==================== TITLE ====================
st.markdown("<h1 class='main-title'>Mood Tracker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:1.3em;'>Visualize your emotional journey</p>", unsafe_allow_html=True)
st.markdown("---")

# ==================== MODE: LOG NEW MOOD ====================
if tracking_mode == "Log New Mood":
    st.markdown("### How are you feeling today?")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    moods = {
        '😊 Happy': col1,
        '😐 Neutral': col2,
        '😔 Sad': col3,
        '😡 Angry': col4,
        '😰 Anxious': col5
    }
    
    if 'selected_mood' not in st.session_state:
        st.session_state.selected_mood = None
    
    for mood, col in moods.items():
        with col:
            st.markdown(f"""
            <div class="mood-card">
                <div class="mood-emoji">{mood.split()[0]}</div>
                <div>{mood.split()[1]}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select", key=mood):
                st.session_state.selected_mood = mood
                st.rerun()
    
    if st.session_state.selected_mood:
        st.success(f"Selected mood: {st.session_state.selected_mood}")
        
        intensity = st.slider(
            "How intense is this feeling? (1-10)",
            min_value=1,
            max_value=10,
            value=5,
            key="intensity_slider"
        )
        
        note = st.text_area("Add a note (optional):", 
                           placeholder="What's on your mind?",
                           key="mood_note")
        
        if st.button("💾 Save Mood Entry"):
            # Save to database
            data_storage.add_mood_entry(
                mood=st.session_state.selected_mood,
                intensity=intensity,
                note=note if note else "No note"
            )
            
            st.success("✅ Mood logged successfully!")
            st.balloons()
            
            # Reset selection
            st.session_state.selected_mood = None
            st.rerun()

# ==================== MODE: VIEW HISTORY ====================
# ==================== MODE: VIEW HISTORY ====================
elif tracking_mode == "View History":
    st.markdown("### 📜 Your Mood History")
    
    # Get REAL mood entries
    mood_entries = data_storage.get_mood_entries()
    
    if mood_entries:
        # Convert to DataFrame
        df = pd.DataFrame(mood_entries)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp', ascending=False)
        
        # Filter by date range
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From:", 
                                    value=datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("To:", value=datetime.now())
        
        # Extract date for filtering
        df['date'] = pd.to_datetime(df['timestamp']).dt.date

        
        # Filter data
        filtered_data = df[
            (df['date'] >= start_date) &
            (df['date'] <= end_date)
        ]
        
        if not filtered_data.empty:
            # Display table
            display_df = filtered_data.copy()
            
            # Format timestamp as readable string
            display_df['Date'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')

            display_df = display_df[['Date', 'mood', 'intensity', 'note']]
            display_df.columns = ['Date', 'Mood', 'Intensity', 'Note']
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Export option
            st.markdown("---")
            if st.button("📥 Export to CSV"):
                csv = display_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"mood_history_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No mood entries found in the selected date range.")
    else:
        st.info("📝 No mood entries yet. Log your first mood to see your history!")

# ==================== MODE: ANALYTICS ====================
elif tracking_mode == "Analytics":
    st.markdown("### 📈 Mood Analytics")
    
    # Get REAL mood entries
    mood_entries = data_storage.get_mood_entries()
    
    if mood_entries:
        df = pd.DataFrame(mood_entries)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Mood distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Mood Distribution")
            mood_counts = df['mood'].value_counts()
            
            fig1 = px.pie(
                values=mood_counts.values,
                names=mood_counts.index,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(255,255,255,0.1)',
                font_color='white'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown("#### Average Intensity by Mood")
            avg_intensity = df.groupby('mood')['intensity'].mean()
            
            fig2 = px.bar(
                x=avg_intensity.index,
                y=avg_intensity.values,
                labels={'x': 'Mood', 'y': 'Average Intensity'},
                color=avg_intensity.values,
                color_continuous_scale='Viridis'
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(255,255,255,0.1)',
                font_color='white'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Timeline
        st.markdown("#### Mood Timeline")
        
        # Convert mood to numeric for plotting
        mood_to_num = {
            '😊 Happy': 5,
            '😐 Neutral': 3,
            '😔 Sad': 2,
            '😡 Angry': 1,
            '😰 Anxious': 2
        }
        
        timeline_data = df.copy()
        timeline_data['Mood_Numeric'] = timeline_data['mood'].map(mood_to_num)
        
        fig3 = px.scatter(
            timeline_data,
            x='timestamp',
            y='Mood_Numeric',
            size='intensity',
            color='mood',
            hover_data=['note'],
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(255,255,255,0.1)',
            font_color='white',
            xaxis_title='Date',
            yaxis_title='Mood',
            yaxis=dict(
                tickmode='array',
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['😡 Angry', '😔 Sad', '😐 Neutral', '', '😊 Happy']
            )
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Insights
        st.markdown("---")
        st.markdown("### 💡 Insights")
        
        most_common_mood = df['mood'].mode()[0]
        avg_intensity = df['intensity'].mean()
        total_entries = len(df)
        
        # Recent trend (last 7 days vs previous 7 days)
        recent_7 = df[df['timestamp'] >= (datetime.now() - timedelta(days=7))]
        previous_7 = df[(df['timestamp'] >= (datetime.now() - timedelta(days=14))) & 
                       (df['timestamp'] < (datetime.now() - timedelta(days=7)))]
        
        if len(recent_7) > 0 and len(previous_7) > 0:
            recent_avg = recent_7['intensity'].mean()
            previous_avg = previous_7['intensity'].mean()
            trend = "improving" if recent_avg > previous_avg else "declining"
            trend_emoji = "📈" if recent_avg > previous_avg else "📉"
        else:
            trend = "stable"
            trend_emoji = "➡️"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"""
            **Most Common Mood**  
            {most_common_mood}
            """)
        
        with col2:
            st.success(f"""
            **Average Intensity**  
            {avg_intensity:.1f}/10
            """)
        
        with col3:
            st.warning(f"""
            **Total Entries**  
            {total_entries} moods logged
            """)
        
        st.markdown("---")
        st.info(f"""
        **Weekly Trend:** {trend_emoji} Your mood is **{trend}** compared to last week.
        """)
        
    else:
        st.info("📝 No mood data yet. Start logging your moods to see analytics!")
        
        # Show message to encourage logging
        st.markdown("""
        ### 🎯 Get Started!
        
        Log your moods regularly to:
        - Track emotional patterns over time
        - Identify triggers and trends
        - Gain insights into your mental wellness
        - Export data for sharing with therapists
        
        Click "Log New Mood" in the sidebar to begin!
        """)