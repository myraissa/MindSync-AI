import streamlit as st
from datetime import datetime
import uuid


def show_onboarding_flow():
    """
    Main onboarding controller
    
    WHY: Routes to appropriate step based on progress
    """
    
    step = st.session_state.onboarding_step
    
    # Display progress bar at top
    progress = step / 4  # 5 steps total (0-4)
    st.progress(progress)
    st.markdown(f"### Step {step + 1} of 5")
    st.markdown("---")
    
    # Route to appropriate step
    if step == 0:
        show_welcome_step()
    elif step == 1:
        show_basic_info_step()
    elif step == 2:
        show_concerns_step()
    elif step == 3:
        show_support_style_step()
    elif step == 4:
        show_completion_step()


# ============================================================================
# STEP 0: WELCOME
# ============================================================================

def show_welcome_step():
    """
    Welcome screen - Introduce the app and set expectations
    
    WHY: Users need to understand what MindSync AI does
    """
    
    st.title("Welcome to MindSync AI 🧠")
    
    st.markdown("""
    ### Your Personal Mental Health Companion
    
    MindSync AI is here to support your mental wellbeing through:
    
    ✨ **Empathetic Conversations**  
    A safe space to express your thoughts and feelings
    
    📊 **Mood Tracking**  
    Understand patterns in your emotional wellbeing
    
    💡 **Personalized Insights**  
    Get tailored suggestions based on your unique journey
    
    🎯 **Goal Setting**  
    Track progress toward your mental health goals
    
    ---
    
    ### Important Information
    
    ⚠️ **MindSync AI is NOT a replacement for professional therapy**
    
    This tool is designed for:
    - Emotional support and active listening
    - Mood tracking and self-reflection
    - Coping strategy suggestions
    - General mental wellness
    
    🚨 **In Crisis?**  
    If you're experiencing a mental health emergency, please contact:
    - National Suicide Prevention Lifeline: 988 (US)
    - Crisis Text Line: Text HOME to 741741
    - Emergency Services: 911
    
    ---
    
    ### Privacy & Data
    
    🔒 Your conversations are private and stored locally  
    🗑️ You can delete your data anytime in Settings  
    👤 We collect minimal information for personalization  
    
    ---
    
    Ready to begin? Let's get to know you!
    """)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started 🚀", use_container_width=True):
            st.session_state.onboarding_step = 1
            st.rerun()


# ============================================================================
# STEP 1: BASIC INFORMATION
# ============================================================================

def show_basic_info_step():
    """
    Collect basic user information
    
    FIELDS:
    - Name (required)
    - Age (required, must be 13+)
    - Language preference (for UI and responses)
    
    WHY: Personalize greetings and ensure age-appropriate content
    """
    
    st.title("Let's Get Acquainted 👋")
    st.markdown("Tell us a bit about yourself to personalize your experience.")
    
    # Initialize temporary storage for form data
    if 'temp_profile' not in st.session_state:
        st.session_state.temp_profile = {}
    
    # Create form
    with st.form("basic_info_form"):
        
        # Name input
        name = st.text_input(
            "What should we call you? *",
            value=st.session_state.temp_profile.get('name', ''),
            placeholder="Enter your name or nickname",
            help="This is how MindSync will address you in conversations"
        )
        
        # Age input
        age = st.number_input(
            "How old are you? *",
            min_value=13,
            max_value=120,
            value=st.session_state.temp_profile.get('age', 18),
            help="We need to ensure age-appropriate support. Must be 13 or older."
        )
        
        # Language preference
        language = st.selectbox(
            "Preferred Language",
            options=["English", "French", "Spanish", "Other"],
            index=["English", "French", "Spanish", "Other"].index(
                st.session_state.temp_profile.get('language', 'English')
            ),
            help="The language you're most comfortable communicating in"
        )
        
        st.markdown("---")
        st.caption("* Required fields")
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        
        with col1:
            back = st.form_submit_button("← Back", use_container_width=True)
        
        with col2:
            submit = st.form_submit_button("Continue →", use_container_width=True, type="primary")
        
        # Handle form submission
        if back:
            st.session_state.onboarding_step = 0
            st.rerun()
        
        if submit:
            # Validation
            if not name or len(name.strip()) < 2:
                st.error("Please enter a valid name (at least 2 characters)")
                st.stop()
            
            if age < 13:
                st.error("You must be at least 13 years old to use MindSync AI")
                st.stop()
            
            # Save data
            st.session_state.temp_profile['name'] = name.strip()
            st.session_state.temp_profile['age'] = age
            st.session_state.temp_profile['language'] = language
            st.session_state.temp_profile['created_at'] = datetime.now().isoformat()
            
            # Move to next step
            st.session_state.onboarding_step = 2
            st.rerun()


# ============================================================================
# STEP 2: MENTAL HEALTH CONCERNS
# ============================================================================

def show_concerns_step():
    """
    Identify user's primary mental health concerns
    
    WHY: Allows AI to provide relevant support and resources
    
    CONCERNS:
    - Anxiety, Depression, Stress, etc.
    - Users can select multiple
    - Optional but recommended
    """
    
    st.title("What Brings You Here? 🌱")
    st.markdown("Select any areas where you'd like support. This helps us provide better guidance.")
    
    # Define concern categories
    concerns = {
        "Anxiety": "😰 Worry, nervousness, panic attacks",
        "Depression": "😔 Sadness, low mood, loss of interest",
        "Stress": "😓 Overwhelm, pressure, tension",
        "Sleep Issues": "😴 Insomnia, poor sleep quality",
        "Relationship Issues": "💔 Family, romantic, or friendship challenges",
        "Work/School Stress": "📚 Academic or career pressure",
        "Self-Esteem": "🪞 Confidence, self-worth concerns",
        "Trauma": "🌪️ Past difficult experiences",
        "Anger Management": "😤 Difficulty controlling emotions",
        "Loneliness": "🏝️ Social isolation, disconnection",
        "Life Transitions": "🔄 Major changes or adjustments",
        "General Wellbeing": "🌟 Overall mental health maintenance"
    }
    
    with st.form("concerns_form"):
        
        st.markdown("### Select all that apply:")
        
        # Create checkboxes for each concern
        selected_concerns = []
        
        # Display in 2 columns for better layout
        col1, col2 = st.columns(2)
        
        concern_items = list(concerns.items())
        mid = len(concern_items) // 2
        
        with col1:
            for concern, description in concern_items[:mid]:
                if st.checkbox(f"**{concern}**\n{description}", 
                             value=concern in st.session_state.temp_profile.get('concerns', [])):
                    selected_concerns.append(concern)
        
        with col2:
            for concern, description in concern_items[mid:]:
                if st.checkbox(f"**{concern}**\n{description}",
                             value=concern in st.session_state.temp_profile.get('concerns', [])):
                    selected_concerns.append(concern)
        
        # Additional notes
        st.markdown("---")
        additional_notes = st.text_area(
            "Anything else you'd like us to know? (Optional)",
            value=st.session_state.temp_profile.get('additional_notes', ''),
            placeholder="Feel free to share more context...",
            height=100
        )
        
        st.markdown("---")
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        
        with col1:
            back = st.form_submit_button("← Back", use_container_width=True)
        
        with col2:
            submit = st.form_submit_button("Continue →", use_container_width=True, type="primary")
        
        # Handle form submission
        if back:
            st.session_state.onboarding_step = 1
            st.rerun()
        
        if submit:
            # Save data
            st.session_state.temp_profile['concerns'] = selected_concerns
            st.session_state.temp_profile['additional_notes'] = (additional_notes or "").strip()
            
            # Move to next step
            st.session_state.onboarding_step = 3
            st.rerun()


# ============================================================================
# STEP 3: SUPPORT STYLE PREFERENCES
# ============================================================================

def show_support_style_step():
    """
    Determine user's preferred support style
    
    WHY: People want different types of support
    Some want advice, others just want to be heard
    
    STYLES:
    - Listening: Empathetic, validating
    - Advice: Actionable suggestions
    - Balanced: Mix of both
    """
    
    st.title("How Can We Best Support You? 🤝")
    st.markdown("Everyone has different preferences for support. Choose what works best for you.")
    
    with st.form("support_style_form"):
        
        # Support style preference
        st.markdown("### What kind of support do you prefer?")
        
        support_style = st.radio(
            "Support Style",
            options=[
                "Listening & Validation",
                "Actionable Advice",
                "Balanced Approach"
            ],
            index=["Listening & Validation", "Actionable Advice", "Balanced Approach"].index(
                st.session_state.temp_profile.get('support_style', 'Balanced Approach')
            ),
            help="This determines how MindSync responds to you",
            label_visibility="collapsed"
        )
        
        # Explain each style
        if support_style == "Listening & Validation":
            st.info("🎧 **Listening Mode**: MindSync will focus on understanding and validating your feelings, providing a safe space to express yourself.")
        elif support_style == "Actionable Advice":
            st.info("💡 **Advice Mode**: MindSync will offer practical suggestions, coping strategies, and actionable steps.")
        else:
            st.info("⚖️ **Balanced Mode**: MindSync will both validate your feelings AND provide practical guidance when appropriate.")
        
        st.markdown("---")
        
        # Communication preferences
        st.markdown("### Additional Preferences")
        
        # Response length
        response_length = st.select_slider(
            "Response Length Preference",
            options=["Brief", "Medium", "Detailed"],
            value=st.session_state.temp_profile.get('response_length', 'Medium'),
            help="How detailed should MindSync's responses be?"
        )
        
        # Check-in frequency
        checkin_frequency = st.selectbox(
            "How often would you like check-ins?",
            options=["Daily", "Every few days", "Weekly", "I'll reach out when needed"],
            index=["Daily", "Every few days", "Weekly", "I'll reach out when needed"].index(
                st.session_state.temp_profile.get('checkin_frequency', "I'll reach out when needed")
            ),
            help="MindSync can proactively check in on your wellbeing"
        )
        
        st.markdown("---")
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        
        with col1:
            back = st.form_submit_button("← Back", use_container_width=True)
        
        with col2:
            submit = st.form_submit_button("Complete Setup →", use_container_width=True, type="primary")
        
        # Handle form submission
        if back:
            st.session_state.onboarding_step = 2
            st.rerun()
        
        if submit:
            # Save data
            st.session_state.temp_profile['support_style'] = support_style
            st.session_state.temp_profile['response_length'] = response_length
            st.session_state.temp_profile['checkin_frequency'] = checkin_frequency
            
            # Move to completion step
            st.session_state.onboarding_step = 4
            st.rerun()


# ============================================================================
# STEP 4: COMPLETION
# ============================================================================

def show_completion_step():
    """
    Final step - Create user profile and initialize services
    
    WHY: 
    - Persist user data to database
    - Initialize memory system
    - Set up conversation service
    - Complete onboarding
    """
    
    st.title("All Set! 🎉")
    st.markdown("Your personalized MindSync AI experience is ready.")
    
    # Display summary of collected information
    st.markdown("### Your Profile Summary")
    
    profile = st.session_state.temp_profile
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Basic Information**")
        st.write(f"👤 Name: {profile.get('name')}")
        st.write(f"🎂 Age: {profile.get('age')}")
        st.write(f"🌍 Language: {profile.get('language')}")
    
    with col2:
        st.markdown("**Preferences**")
        st.write(f"💬 Support Style: {profile.get('support_style')}")
        st.write(f"📏 Response Length: {profile.get('response_length')}")
        st.write(f"📅 Check-ins: {profile.get('checkin_frequency')}")
    
    if profile.get('concerns'):
        st.markdown("**Areas of Focus**")
        st.write(", ".join(profile.get('concerns')))
    
    if profile.get('additional_notes'):
        st.markdown("**Additional Notes**")
        st.write(profile.get('additional_notes'))
    
    st.markdown("---")
    
    # Consent and agreement
    agree = st.checkbox(
        "I understand that MindSync AI is a support tool and not a replacement for professional therapy",
        value=False
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.onboarding_step = 3
            st.rerun()
    
    with col2:
        if st.button("Start My Journey 🚀", use_container_width=True, type="primary", disabled=not agree):
            # Create user profile
            create_user_profile()
            
            # Show success message
            st.success("Profile created successfully!")
            st.balloons()
            
            # Complete onboarding
            st.session_state.onboarding_complete = True
            
            # Clean up temporary data
            if 'temp_profile' in st.session_state:
                del st.session_state.temp_profile
            
            # Wait a moment then redirect
            import time
            time.sleep(2)
            st.rerun()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_user_profile():
    """
    Create user profile in database and initialize services
    
    STEPS:
    1. Generate unique user ID
    2. Save profile to database
    3. Initialize memory system
    4. Set session state variables
    
    WHY: Persist user data for future sessions
    """
    
    # Generate unique user ID
    user_id = str(uuid.uuid4())
    
    # Get profile data
    profile = st.session_state.temp_profile.copy()
    profile['user_id'] = user_id
    
    # Save to database via UserService
    try:
        # Note: You'll need to implement create_user in UserService
        # For now, we'll just set session state
        
        st.session_state.user_id = user_id
        st.session_state.user_profile = profile
        
        # Initialize memory system
        from src.services.memory_system import UserMemorySystem
        st.session_state.memory_system = UserMemorySystem()
        
        # Save initial profile to memory
        st.session_state.memory_system.update_memory(user_id, {
            'profile': profile,
            'onboarding_completed': datetime.now().isoformat(),
            'total_conversations': 0,
            'days_active': 1
        })
        
        return True
        
    except Exception as e:
        st.error(f"Error creating profile: {str(e)}")
        return False