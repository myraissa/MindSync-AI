import streamlit as st
from datetime import datetime, timedelta
import sys
from pathlib import Path
from collections import Counter
import pandas as pd
import random

# Plotting libraries
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not available. Install with: pip install plotly")

sys.path.append(str(Path(__file__).parent.parent.parent))
# ============================================================================
# MOTIVATIONAL CONTENT
# ============================================================================

MOTIVATIONAL_PROVERBS = [
    {
        'text': "The greatest glory in living lies not in never falling, but in rising every time we fall.",
        'author': "Nelson Mandela",
        'icon': "🌟"
    },
    {
        'text': "You are braver than you believe, stronger than you seem, and smarter than you think.",
        'author': "A.A. Milne",
        'icon': "💪"
    },
    {
        'text': "Mental health is not a destination, but a process. It's about how you drive, not where you're going.",
        'author': "Noam Shpancer",
        'icon': "🛤️"
    },
    {
        'text': "Healing takes time, and asking for help is a courageous step.",
        'author': "Mariska Hargitay",
        'icon': "🌱"
    },
    {
        'text': "You don't have to be positive all the time. It's perfectly okay to feel sad, angry, annoyed, frustrated, scared, or anxious. Having feelings doesn't make you a negative person. It makes you human.",
        'author': "Lori Deschene",
        'icon': "❤️"
    },
    {
        'text': "Your present circumstances don't determine where you can go; they merely determine where you start.",
        'author': "Nido Qubein",
        'icon': "🚀"
    },
    {
        'text': "The only way out is through.",
        'author': "Robert Frost",
        'icon': "🌈"
    },
    {
        'text': "What mental health needs is more sunlight, more candor, and more unashamed conversation.",
        'author': "Glenn Close",
        'icon': "☀️"
    },
    {
        'text': "You are not your illness. You have an individual story to tell. You have a name, a history, a personality. Staying yourself is part of the battle.",
        'author': "Julian Seifter",
        'icon': "🎭"
    },
    {
        'text': "Sometimes the bravest thing you can do is ask for help.",
        'author': "Anonymous",
        'icon': "🦸"
    },
    {
        'text': "Progress, not perfection.",
        'author': "Anonymous",
        'icon': "📈"
    },
    {
        'text': "You've survived 100% of your worst days. You're doing great.",
        'author': "Anonymous",
        'icon': "🎯"
    },
    {
        'text': "Small steps in the right direction can turn out to be the biggest step of your life.",
        'author': "Anonymous",
        'icon': "👣"
    },
    {
        'text': "Your mental health is a priority. Your happiness is essential. Your self-care is a necessity.",
        'author': "Anonymous",
        'icon': "🧘"
    },
    {
        'text': "It's okay to not be okay. But it's not okay to stay that way.",
        'author': "Anonymous",
        'icon': "🌸"
    }
]

ACHIEVEMENT_MILESTONES = {
    1: {"title": "First Step", "message": "You've taken the courageous first step! 🌱", "icon": "🌱"},
    3: {"title": "Building Momentum", "message": "Three conversations! You're building a healthy habit! 🔥", "icon": "🔥"},
    7: {"title": "One Week Strong", "message": "A week of self-care! You're amazing! ⭐", "icon": "⭐"},
    14: {"title": "Two Week Warrior", "message": "Two weeks of growth! Keep it up! 💪", "icon": "💪"},
    30: {"title": "Monthly Champion", "message": "30 days of dedication! You're inspiring! 🏆", "icon": "🏆"},
    50: {"title": "Halfway Hero", "message": "50 conversations! Your commitment is incredible! 🎖️", "icon": "🎖️"},
    100: {"title": "Century Milestone", "message": "100 conversations! You're a mental health champion! 👑", "icon": "👑"}
}

MOOD_IMPROVEMENT_MESSAGES = {
    'improving': [
        "🌈 Your mood is trending upward! Keep doing what you're doing!",
        "📈 We see positive progress! You're on the right path!",
        "✨ Things are looking brighter! Your efforts are paying off!",
        "🌅 The sun is breaking through the clouds! Keep going!",
        "🎉 Your resilience is showing! Celebrate these wins!"
    ],
    'stable': [
        "🧘 You're maintaining steady ground. Stability is strength!",
        "⚖️ Your emotional balance is admirable. Keep nurturing it!",
        "🌳 Like a strong tree, you're grounded. That's powerful!",
        "🎯 Consistency is key, and you're mastering it!",
        "💎 Steady progress is still progress. You're doing great!"
    ],
    'challenging': [
        "🤗 Tough times don't last, but tough people do. You've got this!",
        "🌧️ Every storm runs out of rain. Brighter days are coming!",
        "💪 You're stronger than you know. This too shall pass!",
        "🕯️ Even in darkness, you're still here. That's courage!",
        "🌱 Seeds grow in darkness before they bloom. Hang in there!"
    ]
}


def show_insights_page():
    """
    Main insights page display with enhanced motivation
    """
    
    # Header with motivational quote
    display_motivational_header()
    st.markdown("---")
    
    # Get user data
    user_data = get_user_data()
    
    if not user_data or user_data.get('total_conversations', 0) < 1:
        show_empty_state()
        return
    
    # Display achievement celebration
    display_achievement_banner(user_data)
    st.markdown("---")
    
    # Display insights sections
    display_quick_stats(user_data)
    st.markdown("---")
    
    display_mood_trends(user_data)
    st.markdown("---")
    
    display_emotion_analysis(user_data)
    st.markdown("---")
    
    display_activity_patterns(user_data)
    st.markdown("---")
    
    display_enhanced_recommendations(user_data)
    st.markdown("---")
    
    # Footer with encouragement
    display_encouragement_footer(user_data)


# ============================================================================
# MOTIVATIONAL DISPLAYS
# ============================================================================

def display_motivational_header():
    """Display rotating motivational quote at top of page"""
    
    # Get a consistent quote based on the day (changes daily)
    day_of_year = datetime.now().timetuple().tm_yday
    quote = MOTIVATIONAL_PROVERBS[day_of_year % len(MOTIVATIONAL_PROVERBS)]
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2)); 
                border-radius: 15px; padding: 25px; margin-bottom: 20px; border: 2px solid rgba(255,255,255,0.1);'>
        <h2 style='text-align: center; margin-bottom: 15px;'>{quote['icon']} Your Daily Inspiration</h2>
        <p style='text-align: center; font-size: 1.2em; font-style: italic; margin-bottom: 10px;'>
            "{quote['text']}"
        </p>
        <p style='text-align: center; opacity: 0.8;'>— {quote['author']}</p>
    </div>
    """, unsafe_allow_html=True)


def display_achievement_banner(data: dict):
    """Display achievement banners for milestones"""
    
    total_convos = data.get('total_conversations', 0)
    
    # Check for milestone achievements
    for milestone_count, milestone_data in ACHIEVEMENT_MILESTONES.items():
        if total_convos >= milestone_count:
            last_shown = data.get('last_milestone_shown', 0)
            
            # Show if this is a new milestone
            if milestone_count > last_shown:
                st.success(f"""
                ### {milestone_data['icon']} Achievement Unlocked: {milestone_data['title']}!
                
                {milestone_data['message']}
                """)
                
                st.balloons()
                
                # Update last shown milestone
                if st.session_state.memory_system:
                    st.session_state.memory_system.update_memory(
                        st.session_state.user_id,
                        {'last_milestone_shown': milestone_count}
                    )
                break


def display_encouragement_footer(data: dict):
    """Display personalized encouragement at bottom of page"""
    
    total_convos = data.get('total_conversations', 0)
    days_active = data.get('days_active', 0)
    
    encouragement_messages = [
        f"💙 You've shown up for yourself {total_convos} times. That's {total_convos} acts of self-care!",
        f"🌟 {days_active} days of prioritizing your mental health. You're building something beautiful!",
        "🎯 Remember: Progress isn't always linear. Every step forward counts, no matter how small.",
        "🌈 You're not alone on this journey. We're here with you every step of the way.",
        "💪 The fact that you're here, working on yourself, is already a victory. Celebrate that!",
        "🌱 Growth happens slowly, then all at once. Keep nurturing your wellbeing.",
        "✨ Your mental health journey is unique and valid. Honor your own pace.",
        "❤️ Self-care isn't selfish. You deserve the same compassion you give others."
    ]
    
    # Choose a message based on the day
    message_index = datetime.now().timetuple().tm_yday % len(encouragement_messages)
    
    st.info(encouragement_messages[message_index])
    
    # Add a "Share your progress" section
    with st.expander("📢 Celebrate Your Progress"):
        st.markdown("""
        ### You're doing amazing! 🎉
        
        Consider celebrating your progress by:
        - **Sharing with a friend**: Tell someone you trust about your mental health journey
        - **Journaling**: Write about what you've learned about yourself
        - **Reward yourself**: Treat yourself to something you enjoy
        - **Reflect**: Take a moment to acknowledge how far you've come
        
        **Remember**: Every conversation, every check-in, every moment of self-reflection is progress!
        """)


# ============================================================================
# DATA RETRIEVAL (Same as before)
# ============================================================================

def get_user_data() -> dict:
    """Retrieve user data from memory system"""
    
    if not st.session_state.memory_system or not st.session_state.user_id:
        return {}
    
    try:
        memory = st.session_state.memory_system.get_user_memory(st.session_state.user_id)
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
    """Display when user has no data yet"""
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2)); 
                border-radius: 15px; padding: 30px; text-align: center;'>
        <h2>🌱 Your Journey Begins Here</h2>
        <p style='font-size: 1.1em; margin: 20px 0;'>
            Every great journey starts with a single step. Yours starts with a conversation.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        ### What You'll Discover Here:
        
        📈 **Mood Trends** - Understand your emotional patterns  
        😊 **Emotion Insights** - See how you express yourself  
        🎯 **Progress Tracking** - Celebrate your growth  
        💡 **Personal Recommendations** - Get tailored support  
        🏆 **Achievements** - Unlock milestones as you go  
        
        ---
        
        ### Ready to Start?
        
        Your insights will appear as you chat with MindSync AI.  
        Every conversation brings new understanding.
        """)
        
        st.markdown("")
        
        if st.button("Start Your First Conversation 💬", use_container_width=True, type="primary"):
            st.switch_page("streamlit_app.py")


# ============================================================================
# QUICK STATS (Enhanced)
# ============================================================================

def display_quick_stats(data: dict):
    """Display key metrics with encouraging context"""
    
    st.markdown("### 📊 Your Wellbeing Dashboard")
    
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
            delta="+1 today" if total_convos > 0 else None,
            help="Every conversation is an act of self-care! 💙"
        )
        if total_convos >= 10:
            st.caption("🌟 Amazing dedication!")
    
    with col2:
        st.metric(
            label="Days Active",
            value=days_active,
            help="Days you've prioritized your mental health"
        )
        if days_active >= 7:
            st.caption("🔥 Building strong habits!")
    
    with col3:
        st.metric(
            label="Current Streak",
            value=f"{current_streak} days",
            delta="+1" if current_streak > 0 else None,
            help="Consecutive days of showing up for yourself"
        )
        if current_streak >= 3:
            st.caption("💪 Keep it going!")
    
    with col4:
        mood_emoji = get_mood_emoji(float(avg_mood))
        st.metric(
            label="Average Mood",
            value=f"{mood_emoji} {avg_mood:.1f}/5",
            help="Your overall emotional wellbeing"
        )
        if avg_mood >= 4.0:
            st.caption("✨ Thriving!")
        elif avg_mood >= 3.0:
            st.caption("🌱 Growing!")
        else:
            st.caption("🤗 We're here for you!")


def calculate_streak(data: dict) -> int:
    """Calculate consecutive days of activity"""
    
    conversations = data.get('conversations', [])
    if not conversations:
        return 0
    
    dates = []
    for convo in conversations:
        try:
            dt = datetime.fromisoformat(convo['timestamp'])
            dates.append(dt.date())
        except:
            continue
    
    if not dates:
        return 0
    
    unique_dates = sorted(set(dates), reverse=True)
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
    """Calculate average mood from mood logs"""
    
    mood_logs = data.get('mood_logs', [])
    
    if not mood_logs:
        return 3.0
    
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
    """Get emoji representation of mood score"""
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
# MOOD TRENDS (Enhanced with motivation)
# ============================================================================

def display_mood_trends(data: dict):
    """Display mood trends with encouraging insights"""
    
    st.markdown("### 📈 Your Mood Journey")
    
    mood_logs = data.get('mood_logs', [])
    
    if not mood_logs or len(mood_logs) < 2:
        st.info("💡 **Tip**: Log your mood regularly to discover patterns and track your progress! Use the mood check-in in the chat sidebar.")
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
    
    df = pd.DataFrame({
        'Date': timestamps,
        'Mood Score': scores
    })
    
    df = df.sort_values('Date')
    
    # Plot
    if PLOTLY_AVAILABLE:
        fig = px.line(
            df,
            x='Date',
            y='Mood Score',
            title='Your Emotional Landscape Over Time',
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
        
        fig.add_hline(y=3, line_dash="dash", line_color="gray", opacity=0.5, 
                     annotation_text="Baseline", annotation_position="right")
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(df.set_index('Date')['Mood Score'])
    
    # Enhanced insights
    display_enhanced_mood_insights(df)


def display_enhanced_mood_insights(df: pd.DataFrame):
    """Display encouraging insights from mood data"""
    
    with st.expander("💡 Your Mood Insights & Encouragement", expanded=True):
        
        # Trend analysis with encouragement
        if len(df) >= 3:
            recent_avg = df.tail(7)['Mood Score'].mean()
            older_avg = df.head(7)['Mood Score'].mean()
            
            if recent_avg > older_avg + 0.5:
                trend_type = 'improving'
                message = random.choice(MOOD_IMPROVEMENT_MESSAGES['improving'])
                st.success(f"**Positive Trend!** {message}")
            elif recent_avg < older_avg - 0.5:
                trend_type = 'challenging'
                message = random.choice(MOOD_IMPROVEMENT_MESSAGES['challenging'])
                st.info(f"**Challenging Period** {message}")
            else:
                trend_type = 'stable'
                message = random.choice(MOOD_IMPROVEMENT_MESSAGES['stable'])
                st.info(f"**Steady & Strong** {message}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            best_mood = df.loc[df['Mood Score'].idxmax()]
            best_score = float(best_mood['Mood Score'].item())
            st.markdown(f"""
            **🌟 Your Best Day**  
            {best_mood['Date'].strftime('%B %d, %Y')}  
            Mood: {get_mood_emoji(best_score)} {best_mood['Mood Score']:.0f}/5
            
            *You've felt this good before, and you can feel this way again!*
            """)
        
        with col2:
            worst_mood = df.loc[df['Mood Score'].idxmin()]
            worst_score = float(worst_mood['Mood Score'].item())
            st.markdown(f"""
            **💪 You Overcame This**  
            {worst_mood['Date'].strftime('%B %d, %Y')}  
            Mood: {get_mood_emoji(worst_score)} {worst_mood['Mood Score']:.0f}/5
            
            *You survived your hardest day. That's strength!*
            """)
        
        # Additional encouraging stats
        st.markdown("---")
        
        good_days = len(df[df['Mood Score'] >= 4])
        total_days = len(df)
        good_percentage = (good_days / total_days * 100) if total_days > 0 else 0
        
        st.markdown(f"""
        **📊 Mood Statistics**
        
        - 😊 **Good/Great Days**: {good_days} out of {total_days} ({good_percentage:.1f}%)
        - 📈 **Mood Range**: {df['Mood Score'].min():.0f} to {df['Mood Score'].max():.0f}
        - ⚖️ **Average Mood**: {df['Mood Score'].mean():.2f}/5
        
        *Every data point represents a moment you checked in with yourself. That's growth!*
        """)


# ============================================================================
# EMOTION ANALYSIS (Same structure, kept for completeness)
# ============================================================================

def display_emotion_analysis(data: dict):
    """Display emotion distribution from conversations"""
    
    st.markdown("### 😊 Your Emotional Spectrum")
    
    conversations = data.get('conversations', [])
    
    if not conversations:
        st.info("💭 Start chatting to discover your emotional patterns!")
        return
    
    emotions = [convo.get('emotion', 'neutral') for convo in conversations if convo.get('emotion')]
    
    if not emotions:
        st.info("No emotion data available yet.")
        return
    
    emotion_counts = Counter(emotions)
    
    df = pd.DataFrame({
        'Emotion': list(emotion_counts.keys()),
        'Count': list(emotion_counts.values())
    })
    
    df = df.sort_values('Count', ascending=False)
    
    emotion_emoji = {
        'joy': '😄', 'happiness': '😊', 'sadness': '😢', 'anger': '😠',
        'fear': '😰', 'anxiety': '😟', 'surprise': '😲', 'neutral': '😐',
        'trust': '🤗', 'anticipation': '🤔'
    }
    
    df['Emoji'] = df['Emotion'].map(emotion_emoji).fillna('😐')
    df['Label'] = df['Emoji'].str.cat(df['Emotion'].str.capitalize(), sep=' ')
    
    if PLOTLY_AVAILABLE:
        fig = px.bar(
            df,
            x='Label',
            y='Count',
            title='The Rich Tapestry of Your Emotions',
            color='Count',
            color_continuous_scale='Viridis'
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
    
    most_common = df.iloc[0]['Emotion']
    st.info(f"💭 **Insight**: You most often express **{most_common}**. All emotions are valid and part of being human! 🌈")


# ============================================================================
# ACTIVITY PATTERNS
# ============================================================================

def display_activity_patterns(data: dict):
    """Display when user is most active"""
    
    st.markdown("### 📅 Your Self-Care Patterns")
    
    conversations = data.get('conversations', [])
    
    if not conversations or len(conversations) < 5:
        st.info("🕐 Keep chatting to discover when you're most likely to reach out for support!")
        return
    
    timestamps = []
    for convo in conversations:
        try:
            dt = datetime.fromisoformat(convo['timestamp'])
            timestamps.append(dt)
        except:
            continue
    
    if not timestamps:
        return
    
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
    
    peak_hour = hour_df.loc[hour_df['Conversations'].idxmax(), 'Hour']
    peak_day = day_df.loc[day_df['Conversations'].idxmax(), 'Day']
    
    st.info(f"🕐 **Your Pattern**: You typically check in on **{peak_day}s** around **{peak_hour}:00**. Knowing when you need support is self-awareness! 🧠")


# ============================================================================
# ENHANCED RECOMMENDATIONS
# ============================================================================

def display_enhanced_recommendations(data: dict):
    """Display actionable, encouraging recommendations"""
    
    st.markdown("### 💡 Your Personalized Action Plan")
    
    recommendations = generate_enhanced_recommendations(data)
    
    if not recommendations:
        st.info("Keep engaging with MindSync to unlock personalized recommendations!")
        return
    
    for i, rec in enumerate(recommendations, 1):
        with st.expander(f"{rec['icon']} {rec['title']}", expanded=(i == 1)):
            st.markdown(rec['description'])
            
            if rec.get('action_tips'):
                st.markdown("**🎯 Action Steps:**")
                for tip in rec['action_tips']:
                    st.markdown(f"- {tip}")


def generate_enhanced_recommendations(data: dict) -> list:
    """Generate encouraging, actionable recommendations"""
    
    recommendations = []
    
    avg_mood = calculate_average_mood(data)
    conversations = data.get('conversations', [])
    
    # High mood - celebrate and maintain
    if avg_mood >= 4.0:
        recommendations.append({
            'icon': '🌟',
            'title': 'You\'re Thriving! Let\'s Keep This Momentum',
            'description': """
            Your mood has been consistently positive! This is wonderful, and it's important to maintain these good feelings.
            
            **Why this matters**: Understanding what works when you're feeling good helps you recreate these conditions.
            """,
            'action_tips': [
                "✍️ Journal about what's contributing to your positive mood",
                "🎯 Set a new personal growth goal while you have energy",
                "🤝 Reach out to someone and spread your positive energy",
                "🧘 Continue the practices that are working for you",
                "💙 Remember this feeling for tougher days ahead"
            ]
        })
    
    # Moderate mood - opportunities for growth
    elif avg_mood >= 2.5:
        recommendations.append({
            'icon': '🌱',
            'title': 'Building Resilience: Small Steps, Big Impact',
            'description': """
            You're navigating the ups and downs of life. This is the perfect time to build resilience and coping skills.
            
            **Why this matters**: Resilience is built during moderate times, preparing you for challenges ahead.
            """,
            'action_tips': [
                "📝 Start a daily gratitude practice (list 3 things)",
                "🚶 Add 10 minutes of movement to your day",
                "🧘 Try a 5-minute meditation or breathing exercise",
                "📞 Connect with one person who lifts you up",
                "🎨 Engage in a creative or enjoyable activity"
            ]
        })
    
    # Low mood - compassionate support
    else:
        recommendations.append({
            'icon': '🤗',
            'title': 'You\'re Going Through a Tough Time - And That\'s Okay',
            'description': """
            Things have been challenging lately. First, know that what you're feeling is valid, and you're not alone.
            
            **Why this matters**: Reaching out during difficult times is a sign of strength, not weakness. You deserve support.
            """,
            'action_tips': [
                "🆘 Consider talking to a mental health professional",
                "🤝 Reach out to a trusted friend or family member",
                "😴 Prioritize sleep and basic self-care",
                "🎯 Set one small, achievable goal for today",
                "📞 Keep crisis hotline numbers handy (988 in US)"
            ]
        })
    
    # Consistency recommendations
    if conversations:
        recent_count = sum(1 for c in conversations 
                          if datetime.fromisoformat(c['timestamp']) > datetime.now() - timedelta(days=7))
        
        if recent_count < 2:
            recommendations.append({
                'icon': '📅',
                'title': 'Build Your Self-Care Routine',
                'description': """
                Regular check-ins create powerful habits. Even 5 minutes a day can make a difference in tracking your wellbeing.
                
                **Why this matters**: Consistency helps you catch patterns, prevent crisis, and celebrate progress.
                """,
                'action_tips': [
                    "⏰ Set a daily reminder to check in with yourself",
                    "📱 Make MindSync AI part of your morning or evening routine",
                    "📊 Log your mood at the same time each day",
                    "🎯 Start with just 2-3 check-ins per week",
                    "🏆 Celebrate when you maintain your streak!"
                ]
            })
    
    # Emotion-based recommendations
    emotions = [c.get('emotion') for c in conversations if c.get('emotion')]
    if emotions:
        emotion_counts = Counter(emotions)
        top_emotion = emotion_counts.most_common(1)[0][0]
        
        if top_emotion in ['anxiety', 'fear']:
            recommendations.append({
                'icon': '🧘',
                'title': 'Calming Your Anxious Mind',
                'description': """
                You've been experiencing anxiety. These evidence-based techniques can help you find calm.
                
                **Why this matters**: Anxiety is manageable with the right tools and practice.
                """,
                'action_tips': [
                    "🫁 Practice 4-7-8 breathing (inhale 4, hold 7, exhale 8)",
                    "🏃 Move your body - even a short walk helps",
                    "📵 Take breaks from news and social media",
                    "✋ Try the 5-4-3-2-1 grounding technique",
                    "☕ Reduce caffeine and prioritize sleep"
                ]
            })
        
        elif top_emotion in ['sadness', 'depression']:
            recommendations.append({
                'icon': '🌤️',
                'title': 'Gentle Care for Your Low Mood',
                'description': """
                When you're feeling down, self-compassion is key. Start with small, manageable actions.
                
                **Why this matters**: Small positive actions compound over time. You don't have to fix everything at once.
                """,
                'action_tips': [
                    "☀️ Spend 10-15 minutes in natural light daily",
                    "🚶 Take a short walk, even just around the block",
                    "🤝 Reach out to one person - connection heals",
                    "🎵 Listen to music that comforts or uplifts you",
                    "💭 Practice self-compassion: talk to yourself like a friend"
                ]
            })
    
    # General wellness
    if len(recommendations) < 3:
        recommendations.append({
            'icon': '💪',
            'title': 'Strengthen Your Mental Fitness',
            'description': """
            Mental health is like physical fitness - it requires consistent practice and care.
            
            **Why this matters**: Proactive mental health care prevents crisis and builds lasting wellbeing.
            """,
            'action_tips': [
                "😴 Maintain a consistent sleep schedule (7-9 hours)",
                "🥗 Nourish your body with regular, balanced meals",
                "💧 Stay hydrated throughout the day",
                "🧘 Practice mindfulness or meditation (start with 5 min)",
                "📵 Set boundaries with technology and work",
                "🤝 Nurture your relationships regularly",
                "🎯 Set realistic goals and celebrate small wins"
            ]
        })
    
    return recommendations[:3]  # Return top 3 most relevant

if __name__ == "__main__":
    # Initialize session state if needed
    if 'memory_system' not in st.session_state:
        st.session_state.memory_system = None
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    
    # Set page config
    st.set_page_config(
        page_title="Insights - MindSync AI",
        layout="wide"
    )
    
    # Display the insights page
    show_insights_page()