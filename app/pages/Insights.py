# pages/insights.py
"""
Insights Page - Analytics & Patterns
=====================================

This page provides users with analytics about their mental health journey.

FEATURES:
- Mood tracking over time
- Emotion patterns
- Conversation statistics
- Progress toward goals
- Personalized recommendations

VISUALIZATIONS:
- Line charts (mood trends)
- Bar charts (emotion frequency)
- Heatmaps (activity patterns)
- Progress bars (goals)

BEGINNER NOTES:
- Uses Plotly for interactive charts
- Analyzes data from memory system
- Provides actionable insights
- Updates in real-time
"""

import streamlit as st
from datetime import datetime, timedelta
import sys
from pathlib import Path
from collections import Counter
import pandas as pd

# Plotting libraries
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not available. Install with: pip install plotly")


def show_insights_page():
    """
    Main insights page display
    
    STRUCTURE:
    1. Page header
    2. Quick stats overview
    3. Mood trends chart
    4. Emotion analysis
    5. Activity patterns
    6. Recommendations
    """
    
    # Header
    st.title("📊 Your Wellbeing Insights")
    st.markdown("Understanding patterns in your mental health journey")
    st.markdown("---")
    
    # Get user data
    user_data = get_user_data()
    
    if not user_data or user_data.get('total_conversations', 0) < 1:
        show_empty_state()
        return
    
    # Display insights sections
    display_quick_stats(user_data)
    st.markdown("---")
    
    display_mood_trends(user_data)
    st.markdown("---")
    
    display_emotion_analysis(user_data)
    st.markdown("---")
    
    display_activity_patterns(user_data)
    st.markdown("---")
    
    display_recommendations(user_data)


# ============================================================================
# DATA RETRIEVAL
# ============================================================================

def get_user_data() -> dict:
    """
    Retrieve user data from memory system
    
    RETURNS:
    {
        'total_conversations': 25,
        'days_active': 7,
        'mood_logs': [{timestamp, mood}, ...],
        'conversations': [{timestamp, emotion, intent}, ...],
        'concerns': ['anxiety', 'stress'],
        ...
    }
    """
    
    if not st.session_state.memory_system or not st.session_state.user_id:
        return {}
    
    try:
        memory = st.session_state.memory_system.get_user_memory(st.session_state.user_id)
        
        # Combine with profile data
        data = memory.copy()
        data.update(st.session_state.user_profile)
        
        return data
    
    except Exception as e:
        st.error(f"Error loading user data: {str(e)}")
        return {}


# ============================================================================
# EMPTY STATE
# ============================================================================

def show_empty_state():
    """
    Display when user has no data yet
    
    WHY: Encourage first conversation
    """
    
    st.info("### 🌱 Start Your Journey")
    
    st.markdown("""
    You haven't had any conversations yet! 
    
    Your insights will appear here as you chat with MindSync AI.
    
    **What you'll see:**
    - 📈 Mood trends over time
    - 😊 Emotion patterns
    - 🎯 Progress tracking
    - 💡 Personalized recommendations
    
    Ready to begin?
    """)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Start Chatting 💬", use_container_width=True, type="primary"):
            st.switch_page("pages/chat.py")


# ============================================================================
# QUICK STATS OVERVIEW
# ============================================================================

def display_quick_stats(data: dict):
    """
    Display key metrics at a glance
    
    METRICS:
    - Total conversations
    - Days active
    - Current streak
    - Mood average
    """
    
    st.markdown("### 📈 Quick Stats")
    
    # Calculate metrics
    total_convos = data.get('total_conversations', 0)
    days_active = data.get('days_active', 0)
    current_streak = calculate_streak(data)
    avg_mood = calculate_average_mood(data)
    
    # Display in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Conversations",
            value=total_convos,
            delta="+1" if total_convos > 0 else None,
            help="Total number of conversations with MindSync AI"
        )
    
    with col2:
        st.metric(
            label="Days Active",
            value=days_active,
            help="Number of days you've used MindSync AI"
        )
    
    with col3:
        st.metric(
            label="Current Streak",
            value=f"{current_streak} days",
            delta="+1" if current_streak > 0 else None,
            help="Consecutive days of activity"
        )
    
    with col4:
        mood_emoji = get_mood_emoji(float(avg_mood))
        st.metric(
            label="Average Mood",
            value=f"{mood_emoji} {avg_mood:.1f}/5",
            help="Your average mood rating"
        )


def calculate_streak(data: dict) -> int:
    """
    Calculate consecutive days of activity
    
    LOGIC:
    1. Get all conversation dates
    2. Sort chronologically
    3. Count consecutive days back from today
    
    RETURNS: Number of consecutive days
    """
    
    conversations = data.get('conversations', [])
    if not conversations:
        return 0
    
    # Extract dates
    dates = []
    for convo in conversations:
        try:
            dt = datetime.fromisoformat(convo['timestamp'])
            dates.append(dt.date())
        except:
            continue
    
    if not dates:
        return 0
    
    # Get unique dates and sort
    unique_dates = sorted(set(dates), reverse=True)
    
    # Count consecutive days from most recent
    streak = 0
    expected_date = datetime.now().date()
    
    for date in unique_dates:
        if date == expected_date:
            streak += 1
            expected_date = date - timedelta(days=1)
        else:
            break
    
    return streak


def calculate_average_mood(data: dict) -> float:
    """
    Calculate average mood from mood logs
    
    MOOD SCALE:
    Very Bad = 1
    Bad = 2
    Okay = 3
    Good = 4
    Great = 5
    
    RETURNS: Average mood score (1-5)
    """
    
    mood_logs = data.get('mood_logs', [])
    
    if not mood_logs:
        return 3.0  # Default to "Okay"
    
    mood_map = {
        "Very Bad": 1,
        "Bad": 2,
        "Okay": 3,
        "Good": 4,
        "Great": 5
    }
    
    scores = []
    for log in mood_logs:
        mood = log.get('mood')
        if mood in mood_map:
            scores.append(mood_map[mood])
    
    if not scores:
        return 3.0
    
    return sum(scores) / len(scores)


def get_mood_emoji(score: float) -> str:
    """
    Get emoji representation of mood score
    """
    if score >= 4.5:
        return "😄"
    elif score >= 3.5:
        return "🙂"
    elif score >= 2.5:
        return "😐"
    elif score >= 1.5:
        return "😔"
    else:
        return "😢"


# ============================================================================
# MOOD TRENDS CHART
# ============================================================================

def display_mood_trends(data: dict):
    """
    Display mood trends over time
    
    VISUALIZATION: Line chart showing mood changes
    
    WHY: Helps users see patterns and triggers
    """
    
    st.markdown("### 📈 Mood Trends")
    
    mood_logs = data.get('mood_logs', [])
    
    if not mood_logs or len(mood_logs) < 2:
        st.info("Log your mood more often to see trends! Use the mood check-in in the chat sidebar.")
        return
    
    # Prepare data
    mood_map = {"Very Bad": 1, "Bad": 2, "Okay": 3, "Good": 4, "Great": 5}
    
    timestamps = []
    scores = []
    
    for log in mood_logs:
        try:
            dt = datetime.fromisoformat(log['timestamp'])
            mood = log.get('mood')
            
            if mood in mood_map:
                timestamps.append(dt)
                scores.append(mood_map[mood])
        except:
            continue
    
    if not timestamps:
        st.warning("No valid mood data to display")
        return
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': timestamps,
        'Mood Score': scores
    })
    
    # Sort by date
    df = df.sort_values('Date')
    
    # Plot with Plotly (if available)
    if PLOTLY_AVAILABLE:
        fig = px.line(
            df,
            x='Date',
            y='Mood Score',
            title='Your Mood Over Time',
            markers=True
        )
        
        fig.update_layout(
            yaxis=dict(
                tickmode='array',
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['Very Bad', 'Bad', 'Okay', 'Good', 'Great'],
                range=[0.5, 5.5]
            ),
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        # Add horizontal line at "Okay" level
        fig.add_hline(y=3, line_dash="dash", line_color="gray", opacity=0.5)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Fallback to Streamlit line chart
        st.line_chart(df.set_index('Date')['Mood Score'])
    
    # Insights
    display_mood_insights(df)


def display_mood_insights(df: pd.DataFrame):
    """
    Display insights from mood data
    
    INSIGHTS:
    - Trend (improving/declining/stable)
    - Best and worst days
    - Volatility
    """
    
    with st.expander("📊 Mood Insights"):
        
        # Trend analysis
        if len(df) >= 3:
            recent_avg = df.tail(7)['Mood Score'].mean()
            older_avg = df.head(7)['Mood Score'].mean()
            
            if recent_avg > older_avg + 0.5:
                st.success("📈 **Trend:** Your mood has been improving recently! Keep it up!")
            elif recent_avg < older_avg - 0.5:
                st.warning("📉 **Trend:** Your mood has been declining. Consider reaching out to support.")
            else:
                st.info("➡️ **Trend:** Your mood has been relatively stable.")
        
        # Best and worst
        best_mood = df.loc[df['Mood Score'].idxmax()]
        worst_mood = df.loc[df['Mood Score'].idxmin()]
        
        col1, col2 = st.columns(2)
        
        with col1:
            best_score = float(best_mood['Mood Score'].item())
            st.markdown(f"**Best Day:** {best_mood['Date'].strftime('%b %d')}")
            st.markdown(f"Mood: {get_mood_emoji(best_score)} {best_mood['Mood Score']:.0f}/5")
        
        with col2:
            worst_score = float(worst_mood['Mood Score'].item())
            st.markdown(f"**Challenging Day:** {worst_mood['Date'].strftime('%b %d')}")
            st.markdown(f"Mood: {get_mood_emoji(worst_score)} {worst_mood['Mood Score']:.0f}/5")


# ============================================================================
# EMOTION ANALYSIS
# ============================================================================

def display_emotion_analysis(data: dict):
    """
    Display emotion distribution from conversations
    
    VISUALIZATION: Bar chart of emotion frequencies
    
    WHY: Shows what emotions user expresses most
    """
    
    st.markdown("### 😊 Emotion Patterns")
    
    conversations = data.get('conversations', [])
    
    if not conversations:
        st.info("Start chatting to see your emotion patterns!")
        return
    
    # Extract emotions
    emotions = [convo.get('emotion', 'neutral') for convo in conversations if convo.get('emotion')]
    
    if not emotions:
        st.info("No emotion data available yet.")
        return
    
    # Count emotions
    emotion_counts = Counter(emotions)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Emotion': list(emotion_counts.keys()),
        'Count': list(emotion_counts.values())
    })
    
    # Sort by count
    df = df.sort_values('Count', ascending=False)
    
    # Add emoji mapping
    emotion_emoji = {
        'joy': '😄',
        'happiness': '😊',
        'sadness': '😢',
        'anger': '😠',
        'fear': '😰',
        'anxiety': '😟',
        'surprise': '😲',
        'neutral': '😐',
        'trust': '🤗',
        'anticipation': '🤔'
    }
    
    df['Emoji'] = df['Emotion'].map(emotion_emoji).fillna('😐')
    df['Label'] = df['Emoji'].str.cat(df['Emotion'].str.capitalize(), sep=' ')

    
    # Plot
    if PLOTLY_AVAILABLE:
        fig = px.bar(
            df,
            x='Label',
            y='Count',
            title='Emotions Expressed in Conversations',
            color='Count',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            xaxis_title='Emotion',
            yaxis_title='Frequency',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(df.set_index('Label')['Count'])
    
    # Insights
    most_common = df.iloc[0]['Emotion']
    st.info(f"💭 You most often express **{most_common}** in your conversations.")


# ============================================================================
# ACTIVITY PATTERNS
# ============================================================================

def display_activity_patterns(data: dict):
    """
    Display when user is most active
    
    VISUALIZATIONS:
    - Activity by day of week
    - Activity by time of day
    
    WHY: Understand usage patterns
    """
    
    st.markdown("### 📅 Activity Patterns")
    
    conversations = data.get('conversations', [])
    
    if not conversations or len(conversations) < 5:
        st.info("More data needed to show activity patterns. Keep chatting!")
        return
    
    # Extract timestamps
    timestamps = []
    for convo in conversations:
        try:
            dt = datetime.fromisoformat(convo['timestamp'])
            timestamps.append(dt)
        except:
            continue
    
    if not timestamps:
        return
    
    # Activity by day of week
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = Counter([dt.weekday() for dt in timestamps])
    
    day_df = pd.DataFrame({
        'Day': [day_names[i] for i in range(7)],
        'Conversations': [day_counts.get(i, 0) for i in range(7)]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### By Day of Week")
        if PLOTLY_AVAILABLE:
            fig = px.bar(day_df, x='Day', y='Conversations', color='Conversations')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart(day_df.set_index('Day')['Conversations'])
    
    # Activity by hour
    hour_counts = Counter([dt.hour for dt in timestamps])
    hour_df = pd.DataFrame({
        'Hour': range(24),
        'Conversations': [hour_counts.get(i, 0) for i in range(24)]
    })
    
    with col2:
        st.markdown("#### By Time of Day")
        if PLOTLY_AVAILABLE:
            fig = px.bar(hour_df, x='Hour', y='Conversations', color='Conversations')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart(hour_df.set_index('Hour')['Conversations'])
    
    # Peak time insight
    peak_hour = hour_df.loc[hour_df['Conversations'].idxmax(), 'Hour']
    peak_day = day_df.loc[day_df['Conversations'].idxmax(), 'Day']
    
    st.info(f"🕐 You're most active on **{peak_day}s** around **{peak_hour}:00**")


# ============================================================================
# RECOMMENDATIONS
# ============================================================================

def display_recommendations(data: dict):
    """
    Display personalized recommendations
    
    BASED ON:
    - Mood patterns
    - Emotion trends
    - Activity patterns
    - User concerns
    
    RECOMMENDATIONS:
    - Coping strategies
    - Resources
    - Behavioral suggestions
    """
    
    st.markdown("### 💡 Personalized Recommendations")
    
    # Generate recommendations based on data
    recommendations = generate_recommendations(data)
    
    if not recommendations:
        st.info("Keep using MindSync AI to get personalized recommendations!")
        return
    
    # Display recommendations
    for i, rec in enumerate(recommendations, 1):
        with st.expander(f"{rec['icon']} {rec['title']}", expanded=(i == 1)):
            st.markdown(rec['description'])
            
            if rec.get('action'):
                if st.button(rec['action']['label'], key=f"rec_{i}"):
                    # Handle action
                    st.success(rec['action']['success_message'])


def generate_recommendations(data: dict) -> list:
    """
    Generate personalized recommendations
    
    LOGIC:
    1. Analyze mood trends
    2. Check emotion patterns
    3. Review activity
    4. Match with concern areas
    5. Generate relevant recommendations
    
    RETURNS: List of recommendation dicts
    """
    
    recommendations = []
    
    # Mood-based recommendations
    avg_mood = calculate_average_mood(data)
    
    if avg_mood < 2.5:
        recommendations.append({
            'icon': '🆘',
            'title': 'Reach Out for Support',
            'description': """
            Your mood has been lower than usual. This is a good time to reach out:
            
            - Talk to a trusted friend or family member
            - Consider speaking with a mental health professional
            - Use the crisis resources if you're in immediate distress
            
            Remember: Asking for help is a sign of strength, not weakness.
            """,
            'action': {
                'label': 'View Crisis Resources',
                'success_message': 'Remember, you\'re not alone. Help is available 24/7.'
            }
        })
    
    # Activity recommendations
    conversations = data.get('conversations', [])
    if conversations:
        timestamps = [datetime.fromisoformat(c['timestamp']) for c in conversations if 'timestamp' in c]
        if timestamps:
            recent_activity = sum(1 for dt in timestamps if dt > datetime.now() - timedelta(days=7))
            
            if recent_activity < 3:
                recommendations.append({
                    'icon': '🗓️',
                    'title': 'Build a Routine',
                    'description': """
                    Regular check-ins can help track your wellbeing more effectively.
                    
                    **Tips:**
                    - Set a daily reminder to chat with MindSync
                    - Log your mood each morning or evening
                    - Reflect on your day in a brief conversation
                    
                    Consistency helps identify patterns and track progress.
                    """,
                    'action': None
                })
    
    # Emotion-based recommendations
    emotions = [c.get('emotion') for c in conversations if c.get('emotion')]
    if emotions:
        emotion_counts = Counter(emotions)
        top_emotion = emotion_counts.most_common(1)[0][0]
        
        if top_emotion in ['sadness', 'depression']:
            recommendations.append({
                'icon': '🌤️',
                'title': 'Activities for Low Mood',
                'description': """
                When feeling down, small actions can help:
                
                - **Get moving:** Even a 10-minute walk can boost mood
                - **Connect:** Reach out to one person today
                - **Create:** Try journaling, drawing, or music
                - **Rest:** Ensure you're getting adequate sleep
                - **Sunlight:** Spend time outdoors if possible
                
                Start small - any positive action counts!
                """,
                'action': None
            })
        
        elif top_emotion in ['anxiety', 'fear']:
            recommendations.append({
                'icon': '🧘',
                'title': 'Anxiety Management Techniques',
                'description': """
                Try these evidence-based anxiety reduction strategies:
                
                - **Breathing:** 4-7-8 technique (inhale 4, hold 7, exhale 8)
                - **Grounding:** 5-4-3-2-1 sensory exercise
                - **Movement:** Physical activity reduces anxiety
                - **Limit caffeine:** Can worsen anxiety symptoms
                - **Sleep hygiene:** Prioritize consistent sleep schedule
                
                Practice regularly for best results.
                """,
                'action': None
            })
    
    # Concern-specific recommendations
    concerns = data.get('concerns', [])
    
    if 'Sleep Issues' in concerns:
        recommendations.append({
            'icon': '😴',
            'title': 'Improve Sleep Quality',
            'description': """
            Sleep is foundational to mental health. Try these strategies:
            
            - **Consistency:** Same bedtime and wake time daily
            - **Environment:** Dark, cool, quiet room
            - **Wind down:** 30-60 min screen-free before bed
            - **Limit naps:** If needed, keep under 30 minutes
            - **Avoid:** Caffeine after 2pm, alcohol before bed
            
            Give changes 1-2 weeks to take effect.
            """,
            'action': None
        })
    
    # If no specific recommendations, give general wellness tips
    if not recommendations:
        recommendations.append({
            'icon': '🌟',
            'title': 'Continue Your Wellness Journey',
            'description': """
            You're doing great! Here are ways to maintain and enhance your wellbeing:
            
            - **Regular check-ins:** Keep tracking your mood
            - **Social connection:** Maintain relationships
            - **Physical health:** Exercise, nutrition, sleep
            - **Stress management:** Practice relaxation techniques
            - **Growth mindset:** Celebrate small wins
            
            Keep up the excellent work on your mental health!
            """,
            'action': None
        })
    
    return recommendations[:3]