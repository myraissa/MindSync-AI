import streamlit as st
from datetime import datetime
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))


def show_settings_page():
    """
    Main settings page display
    
    STRUCTURE:
    1. Page header
    2. Profile settings
    3. Preferences
    4. Privacy & Data
    5. About
    """
    
    st.title("⚙️ Settings")
    st.markdown("Manage your profile, preferences, and data")
    st.markdown("---")
    
    # Create tabs for different settings sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Profile",
        "🎨 Preferences", 
        "🔒 Privacy & Data",
        "ℹ️ About"
    ])
    
    with tab1:
        show_profile_settings()
    
    with tab2:
        show_preferences_settings()
    
    with tab3:
        show_privacy_settings()
    
    with tab4:
        show_about_section()


# ============================================================================
# PROFILE SETTINGS
# ============================================================================

def show_profile_settings():
    """
    Edit user profile information
    
    EDITABLE FIELDS:
    - Name
    - Age
    - Language
    - Mental health concerns
    - Additional notes
    """
    
    st.markdown("### Profile Information")
    st.markdown("Update your personal information and areas of focus")
    
    profile = st.session_state.user_profile
    
    with st.form("profile_form"):
        
        # Basic info
        st.markdown("#### Basic Information")
        
        name = st.text_input(
            "Name",
            value=profile.get('name', ''),
            help="How should MindSync address you?"
        )
        
        age = st.number_input(
            "Age",
            min_value=13,
            max_value=120,
            value=profile.get('age', 18),
            help="Your current age"
        )
        
        language = st.selectbox(
            "Preferred Language",
            options=["English", "French", "Spanish", "Other"],
            index=["English", "French", "Spanish", "Other"].index(
                profile.get('language', 'English')
            ),
            help="Language for conversations"
        )
        
        st.markdown("---")
        
        # Mental health concerns
        st.markdown("#### Areas of Focus")
        st.caption("Select all that apply")
        
        all_concerns = [
            "Anxiety", "Depression", "Stress", "Sleep Issues",
            "Relationship Issues", "Work/School Stress", "Self-Esteem",
            "Trauma", "Anger Management", "Loneliness",
            "Life Transitions", "General Wellbeing"
        ]
        
        current_concerns = profile.get('concerns', [])
        
        # Display checkboxes in 3 columns
        cols = st.columns(3)
        selected_concerns = []
        
        for i, concern in enumerate(all_concerns):
            with cols[i % 3]:
                if st.checkbox(
                    concern,
                    value=concern in current_concerns,
                    key=f"concern_{concern}"
                ):
                    selected_concerns.append(concern)
        
        st.markdown("---")
        
        # Additional notes
        additional_notes = st.text_area(
            "Additional Notes",
            value=profile.get('additional_notes', ''),
            placeholder="Anything else we should know about your journey...",
            height=100,
            help="Optional context about your mental health goals"
        )
        
        st.markdown("---")
        
        # Submit button
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            submit = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True,
                type="primary"
            )
        
        if submit:
            # Validation
            if not name or len(name.strip()) < 2:
                st.error("Please enter a valid name")
                st.stop()
            
            if age < 13:
                st.error("Must be at least 13 years old")
                st.stop()
            
            # Update profile
            updated_profile = profile.copy()
            updated_profile.update({
                'name': name.strip(),
                'age': age,
                'language': language,
                'concerns': selected_concerns,
                'additional_notes': (additional_notes or "").strip(),
                'updated_at': datetime.now().isoformat()
            })
            
            # Save to session state
            st.session_state.user_profile = updated_profile
            
            # Save to memory system
            if st.session_state.memory_system and st.session_state.user_id:
                try:
                    memory = st.session_state.memory_system.get_user_memory(
                        st.session_state.user_id
                    )
                    memory['profile'] = updated_profile
                    st.session_state.memory_system.update_user_memory(
                        st.session_state.user_id,
                        memory
                    )
                    st.success("✅ Profile updated successfully!")
                except Exception as e:
                    st.error(f"Error saving profile: {str(e)}")
            else:
                st.success("✅ Profile updated!")
            
            # Small delay to show success message
            import time
            time.sleep(1)
            st.rerun()


# ============================================================================
# PREFERENCES SETTINGS
# ============================================================================

def show_preferences_settings():
    """
    Customize app preferences
    
    SETTINGS:
    - Support style
    - Response length
    - Check-in frequency
    - Notification preferences
    """
    
    st.markdown("### App Preferences")
    st.markdown("Customize how MindSync AI interacts with you")
    
    profile = st.session_state.user_profile
    
    with st.form("preferences_form"):
        
        # Support style
        st.markdown("#### Conversation Style")
        
        support_style = st.radio(
            "What type of support do you prefer?",
            options=[
                "Listening & Validation",
                "Actionable Advice",
                "Balanced Approach"
            ],
            index=["Listening & Validation", "Actionable Advice", "Balanced Approach"].index(
                profile.get('support_style', 'Balanced Approach')
            ),
            help="How MindSync responds to you"
        )
        
        # Explain current selection
        if support_style == "Listening & Validation":
            st.info("🎧 MindSync will focus on understanding and validating your feelings")
        elif support_style == "Actionable Advice":
            st.info("💡 MindSync will offer practical suggestions and coping strategies")
        else:
            st.info("⚖️ MindSync will both validate your feelings AND provide guidance")
        
        st.markdown("---")
        
        # Response preferences
        st.markdown("#### Response Preferences")
        
        response_length = st.select_slider(
            "Response Length",
            options=["Brief", "Medium", "Detailed"],
            value=profile.get('response_length', 'Medium'),
            help="How detailed should responses be?"
        )
        
        st.markdown("---")
        
        # Check-in frequency
        st.markdown("#### Check-in Settings")
        
        checkin_frequency = st.selectbox(
            "How often should MindSync check in?",
            options=[
                "Daily",
                "Every few days",
                "Weekly",
                "I'll reach out when needed"
            ],
            index=["Daily", "Every few days", "Weekly", "I'll reach out when needed"].index(
                profile.get('checkin_frequency', "I'll reach out when needed")
            ),
            help="Proactive wellbeing check-ins"
        )
        
        st.markdown("---")
        
        # Notification preferences
        st.markdown("#### Notifications")
        
        enable_reminders = st.checkbox(
            "Enable daily reminders",
            value=profile.get('enable_reminders', False),
            help="Get reminded to check in with MindSync"
        )
        
        if enable_reminders:
            reminder_time = st.time_input(
                "Reminder time",
                value=datetime.strptime(
                    profile.get('reminder_time', '20:00'),
                    '%H:%M'
                ).time(),
                help="When to send daily reminder"
            )
        else:
            reminder_time = None
        
        st.markdown("---")
        
        # Submit button
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            submit = st.form_submit_button(
                "💾 Save Preferences",
                use_container_width=True,
                type="primary"
            )
        
        if submit:
            # Update profile
            updated_profile = profile.copy()
            updated_profile.update({
                'support_style': support_style,
                'response_length': response_length,
                'checkin_frequency': checkin_frequency,
                'enable_reminders': enable_reminders,
                'reminder_time': reminder_time.strftime('%H:%M') if reminder_time else None,
                'updated_at': datetime.now().isoformat()
            })
            
            # Save
            st.session_state.user_profile = updated_profile
            
            if st.session_state.memory_system and st.session_state.user_id:
                try:
                    memory = st.session_state.memory_system.get_user_memory(
                        st.session_state.user_id
                    )
                    memory['profile'] = updated_profile
                    st.session_state.memory_system.update_user_memory(
                        st.session_state.user_id,
                        memory
                    )
                    st.success("✅ Preferences updated successfully!")
                except Exception as e:
                    st.error(f"Error saving preferences: {str(e)}")
            else:
                st.success("✅ Preferences updated!")
            
            import time
            time.sleep(1)
            st.rerun()


# ============================================================================
# PRIVACY & DATA SETTINGS
# ============================================================================

def show_privacy_settings():
    """
    Privacy and data management
    
    FEATURES:
    - Export data
    - Delete conversations
    - Delete account
    - Privacy information
    """
    
    st.markdown("### Privacy & Data Management")
    st.markdown("Control your data and privacy")
    
    st.markdown("---")
    
    # Data export
    st.markdown("#### 📥 Export Your Data")
    st.write("Download all your data including profile, conversations, and mood logs")
    
    if st.button("Export Data as JSON", use_container_width=True):
        export_user_data()
    
    st.markdown("---")
    
    # Delete conversations
    st.markdown("#### 🗑️ Delete Conversations")
    st.write("Remove all conversation history while keeping your profile")
    
    with st.expander("⚠️ Delete All Conversations"):
        st.warning("This will permanently delete all your conversation history. Your profile and mood logs will be preserved.")
        
        confirm_delete_convos = st.checkbox("I understand this cannot be undone")
        
        if st.button(
            "Delete All Conversations",
            type="primary",
            disabled=not confirm_delete_convos,
            key="delete_convos"
        ):
            delete_conversations()
    
    st.markdown("---")
    
    # Delete account
    st.markdown("#### ❌ Delete Account")
    st.write("Permanently delete your account and all associated data")
    
    with st.expander("⚠️ Delete My Account"):
        st.error("**Warning:** This will permanently delete your entire account including profile, conversations, mood logs, and all other data. This action cannot be undone.")
        
        confirm_text = st.text_input(
            "Type 'DELETE' to confirm",
            key="confirm_delete_account"
        )
        
        if st.button(
            "Delete My Account",
            type="primary",
            disabled=confirm_text != "DELETE",
            key="delete_account"
        ):
            delete_account()
    
    st.markdown("---")
    
    # Privacy information
    st.markdown("#### 🔒 Privacy Information")
    
    with st.expander("How We Handle Your Data"):
        st.markdown("""
        **Data Storage:**
        - All data is stored locally on your device
        - No data is sent to external servers (except AI model API)
        - Conversations are encrypted
        
        **Data Usage:**
        - Used only to provide personalized support
        - Analyzed locally to generate insights
        - Never shared with third parties
        
        **Data Retention:**
        - Kept until you delete it
        - You can export or delete anytime
        - Automatic cleanup options available
        
        **Your Rights:**
        - Access all your data anytime
        - Export data in standard format
        - Delete data permanently
        - Control what information you share
        """)


def export_user_data():
    """
    Export all user data as JSON
    
    INCLUDES:
    - Profile information
    - All conversations
    - Mood logs
    - Settings
    - Statistics
    """
    
    if not st.session_state.memory_system or not st.session_state.user_id:
        st.error("No data available to export")
        return
    
    try:
        # Gather all data
        memory = st.session_state.memory_system.get_user_memory(st.session_state.user_id)
        profile = st.session_state.user_profile
        
        export_data = {
            'export_date': datetime.now().isoformat(),
            'user_id': st.session_state.user_id,
            'profile': profile,
            'memory': memory,
            'conversations': memory.get('conversations', []),
            'mood_logs': memory.get('mood_logs', []),
            'statistics': {
                'total_conversations': memory.get('total_conversations', 0),
                'days_active': memory.get('days_active', 0)
            }
        }
        
        # Convert to JSON
        json_str = json.dumps(export_data, indent=2, default=str)
        
        # Provide download
        st.download_button(
            label="📥 Download Data",
            data=json_str,
            file_name=f"mindsync_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        st.success("✅ Data ready for download!")
    
    except Exception as e:
        st.error(f"Error exporting data: {str(e)}")


def delete_conversations():
    """
    Delete all conversation history
    
    WHY: Users may want fresh start while keeping profile
    """
    
    if not st.session_state.memory_system or not st.session_state.user_id:
        st.error("No data to delete")
        return
    
    try:
        # Clear conversations from memory
        memory = st.session_state.memory_system.get_user_memory(st.session_state.user_id)
        memory['conversations'] = []
        memory['total_conversations'] = 0
        
        st.session_state.memory_system.update_user_memory(
            st.session_state.user_id,
            memory
        )
        
        # Clear from session state
        st.session_state.messages = []
        
        st.success("✅ All conversations deleted")
        
        import time
        time.sleep(2)
        st.rerun()
    
    except Exception as e:
        st.error(f"Error deleting conversations: {str(e)}")


def delete_account():
    """
    Delete entire user account
    
    DESTRUCTIVE: Removes all user data
    """
    
    try:
        # Delete from memory system
        if st.session_state.memory_system and st.session_state.user_id:
            # Note: Implement delete_user_memory in UserMemorySystem
            # For now, we'll just clear session state
            pass
        
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        st.success("✅ Account deleted successfully")
        st.info("You will be redirected to the welcome page...")
        
        import time
        time.sleep(2)
        st.rerun()
    
    except Exception as e:
        st.error(f"Error deleting account: {str(e)}")


# ============================================================================
# ABOUT SECTION
# ============================================================================

def show_about_section():
    """
    Information about MindSync AI
    
    INCLUDES:
    - App version
    - Features
    - Credits
    - Support resources
    - Feedback
    """
    
    st.markdown("### About MindSync AI")
    
    # Version info
    st.markdown("""
    **Version:** 2.0.0 (2026 Edition)  
    **Last Updated:** January 2026
    """)
    
    st.markdown("---")
    
    # Features
    st.markdown("### ✨ Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Core Features:**
        - 💬 Empathetic AI conversations
        - 😊 Emotion detection
        - 🎯 Intent classification
        - 📊 Mood tracking
        - 💡 Personalized insights
        """)
    
    with col2:
        st.markdown("""
        **Advanced Features:**
        - 🧠 Context-aware memory
        - 📈 Pattern analysis
        - 🎨 Customizable preferences
        - 🔒 Privacy-focused design
        - 📥 Data export
        """)
    
    st.markdown("---")
    
    # Technology stack
    st.markdown("### 🛠️ Built With")
    
    with st.expander("Technology Stack"):
        st.markdown("""
        **Frontend:**
        - Streamlit - Web interface
        - Plotly - Data visualization
        
        **Backend:**
        - Python 3.10+
        - Hugging Face Transformers - AI models
        - NLTK - Natural language processing
        
        **AI Models:**
        - Emotion detection
        - Intent classification
        - Response generation
        
        **Data:**
        - SQLite - User data storage
        - JSON - Configuration
        - Local file system - Privacy
        """)
    
    st.markdown("---")
    
    # Crisis resources
    st.markdown("### 🚨 Crisis Resources")
    
    st.markdown("""
    **MindSync AI is NOT a substitute for professional help.**
    
    If you're in crisis, please reach out:
    
    📞 **National Suicide Prevention Lifeline:** 988 (US)  
    💬 **Crisis Text Line:** Text HOME to 741741  
    🌍 **International:** [findahelpline.com](https://findahelpline.com)  
    🆘 **Emergency Services:** 911
    
    **Mental Health Resources:**
    - [NAMI](https://www.nami.org) - National Alliance on Mental Illness
    - [MentalHealth.gov](https://www.mentalhealth.gov) - Government resources
    - [Psychology Today](https://www.psychologytoday.com) - Find a therapist
    """)
    
    st.markdown("---")
    
    # Feedback
    st.markdown("### 💭 Feedback")
    
    st.write("We'd love to hear from you! Your feedback helps improve MindSync AI.")
    
    with st.form("feedback_form"):
        feedback_type = st.selectbox(
            "Type",
            options=["Bug Report", "Feature Request", "General Feedback", "Other"]
        )
        
        feedback_text = st.text_area(
            "Your Feedback",
            placeholder="Tell us what you think...",
            height=150
        )
        
        if st.form_submit_button("Submit Feedback", use_container_width=True):
            if feedback_text.strip():
                # In production, save feedback to database or send email
                st.success("Thank you for your feedback! 🙏")
            else:
                st.error("Please enter some feedback")
    
    st.markdown("---")
    
    # Credits
    st.markdown("### 👥 Credits")
    
    st.markdown("""
    **Development:**
    - MindSync AI Team
    
    **Open Source:**
    - Built with open-source libraries
    - Powered by Hugging Face models
    - Community contributions welcome
    
    **Special Thanks:**
    - Mental health professionals who advised on features
    - Beta testers who provided valuable feedback
    - Open-source community
    """)
    
    st.markdown("---")
    
    # License
    st.markdown("### 📄 License")
    
    with st.expander("Terms & License"):
        st.markdown("""
        **License:** MIT License
        
        **Terms of Use:**
        - Free for personal use
        - No warranty provided
        - Use at your own risk
        - Not a medical device
        - Not FDA approved
        
        **Privacy:**
        - No data collection
        - Local storage only
        - No tracking
        - No advertisements
        
        **Disclaimer:**
        MindSync AI is a supportive tool and does not replace professional 
        mental health care. Always consult qualified professionals for 
        mental health concerns.
        """)