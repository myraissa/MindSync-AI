import streamlit as st
from datetime import datetime
import uuid


def show_onboarding_flow():
    """
    Enhanced onboarding controller with additional steps
    
    STEPS:
    0. Welcome
    1. Basic Information
    2. Current Feelings & Mental State (NEW - DETAILED)
    3. Mental Health Background (NEW)
    4. Support System & Coping Strategies (NEW)
    5. Concerns & Goals
    6. Support Style Preferences
    7. Completion
    """
    
    step = st.session_state.onboarding_step
    
    # Progress bar (8 steps total: 0-7)
    progress = step / 7
    st.progress(progress)
    st.markdown(f"### Step {step + 1} of 8")
    st.markdown("---")
    
    # Route to appropriate step
    if step == 0:
        show_welcome_step()
    elif step == 1:
        show_basic_info_step()
    elif step == 2:
        show_current_feelings_step()  # NEW
    elif step == 3:
        show_mental_health_background_step()  # NEW
    elif step == 4:
        show_support_system_step()  # NEW
    elif step == 5:
        show_concerns_goals_step()  # ENHANCED
    elif step == 6:
        show_support_style_step()
    elif step == 7:
        show_completion_step()


# ============================================================================
# STEP 0: WELCOME (Same as before)
# ============================================================================

def show_welcome_step():
    """Welcome screen"""
    
    st.title("Welcome to MindSync AI 🧠")
    
    st.markdown("""
    ### Your Personal Mental Health Companion
    
    MindSync AI is here to support your mental wellbeing through:
    
    ✨ **Empathetic Conversations** - A safe space to express yourself  
    📊 **Mood Tracking** - Understand your emotional patterns  
    💡 **Personalized Insights** - Tailored guidance for your journey  
    🎯 **Goal Setting** - Track progress toward wellbeing  
    
    ---
    
    ### Important Information
    
    ⚠️ **MindSync AI is NOT a replacement for professional therapy**
    
    This tool is designed for:
    - Emotional support and active listening
    - Mood tracking and self-reflection
    - Coping strategy suggestions
    - General mental wellness
    
    🚨 **In Crisis?**  
    If you're experiencing a mental health emergency:
    - **Tunisia**: 80 101 080
    - **US**: 988 (Suicide & Crisis Lifeline)
    - **International**: 116 123
    - **Emergency**: 911 / 112
    
    ---
    
    ### Privacy & Your Data
    
    🔒 Your conversations are private and confidential  
    🗑️ You can delete your data anytime  
    👤 We collect only what's needed for personalization  
    📊 No data is shared with third parties  
    
    ---
    
    ### This Setup Process
    
    We'll ask you some questions to personalize your experience. 
    
    **You can:**
    - Skip optional questions
    - Go back and change answers
    - Take breaks and return later
    
    **Time needed:** About 5-10 minutes
    
    ---
    
    Ready to begin your journey toward better mental health?
    """)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Let's Get Started 🚀", use_container_width=True, type="primary"):
            st.session_state.onboarding_step = 1
            st.rerun()


# ============================================================================
# STEP 1: BASIC INFORMATION (Same as before)
# ============================================================================

def show_basic_info_step():
    """Collect basic user information"""
    
    st.title("Let's Get Acquainted 👋")
    st.markdown("Tell us a bit about yourself to personalize your experience.")
    
    if 'temp_profile' not in st.session_state:
        st.session_state.temp_profile = {}
    
    with st.form("basic_info_form"):
        
        name = st.text_input(
            "What should we call you? *",
            value=st.session_state.temp_profile.get('name', ''),
            placeholder="Enter your name or nickname",
            help="This is how MindSync will address you"
        )
        
        age = st.number_input(
            "How old are you? *",
            min_value=13,
            max_value=120,
            value=st.session_state.temp_profile.get('age', 18),
            help="Must be 13 or older to use MindSync AI"
        )
        
        language = st.selectbox(
            "Preferred Language",
            options=["English", "French", "Arabic", "Spanish", "Other"],
            index=["English", "French", "Arabic", "Spanish", "Other"].index(
                st.session_state.temp_profile.get('language', 'English')
            ),
            help="The language you're most comfortable with"
        )
        
        st.markdown("---")
        st.caption("* Required fields")
        
        col1, col2 = st.columns(2)
        
        with col1:
            back = st.form_submit_button("← Back", use_container_width=True)
        
        with col2:
            submit = st.form_submit_button("Continue →", use_container_width=True, type="primary")
        
        if back:
            st.session_state.onboarding_step = 0
            st.rerun()
        
        if submit:
            if not name or len(name.strip()) < 2:
                st.error("Please enter a valid name (at least 2 characters)")
                st.stop()
            
            if age < 13:
                st.error("You must be at least 13 years old to use MindSync AI")
                st.stop()
            
            st.session_state.temp_profile['name'] = name.strip()
            st.session_state.temp_profile['age'] = age
            st.session_state.temp_profile['language'] = language
            st.session_state.temp_profile['created_at'] = datetime.now().isoformat()
            
            st.session_state.onboarding_step = 2
            st.rerun()


# ============================================================================
# STEP 2: CURRENT FEELINGS & MENTAL STATE (NEW - DETAILED)
# ============================================================================

def show_current_feelings_step():
    """
    Detailed assessment of current emotional and mental state
    
    WHY: Provides baseline for tracking progress and immediate context
    
    CAPTURES:
    - Current mood
    - Specific feelings/emotions
    - Physical sensations
    - Sleep quality
    - Energy level
    - Recent stressors
    """
    
    st.title("How Are You Feeling Right Now? 💭")
    st.markdown("""
    Understanding your current state helps us provide better support. 
    Be honest - there are no wrong answers here. This is a safe space.
    """)
    
    with st.form("current_feelings_form"):
        
        # Current mood rating
        st.markdown("### Overall Mood")
        current_mood = st.select_slider(
            "How would you rate your mood right now?",
            options=["Very Low", "Low", "Okay", "Good", "Very Good"],
            value=st.session_state.temp_profile.get('current_mood', 'Okay'),
            help="Your general emotional state at this moment"
        )
        
        # Specific emotions
        st.markdown("### Specific Feelings")
        st.markdown("Select all emotions you're experiencing: (Select multiple)")
        
        emotions = {
            '😊 Happy': st.checkbox('😊 Happy', value='Happy' in st.session_state.temp_profile.get('current_emotions', [])),
            '😔 Sad': st.checkbox('😔 Sad', value='Sad' in st.session_state.temp_profile.get('current_emotions', [])),
            '😰 Anxious': st.checkbox('😰 Anxious', value='Anxious' in st.session_state.temp_profile.get('current_emotions', [])),
            '😤 Angry/Irritated': st.checkbox('😤 Angry/Irritated', value='Angry/Irritated' in st.session_state.temp_profile.get('current_emotions', [])),
            '😨 Fearful': st.checkbox('😨 Fearful', value='Fearful' in st.session_state.temp_profile.get('current_emotions', [])),
            '😞 Hopeless': st.checkbox('😞 Hopeless', value='Hopeless' in st.session_state.temp_profile.get('current_emotions', [])),
            '🥺 Overwhelmed': st.checkbox('🥺 Overwhelmed', value='Overwhelmed' in st.session_state.temp_profile.get('current_emotions', [])),
            '😐 Numb/Empty': st.checkbox('😐 Numb/Empty', value='Numb/Empty' in st.session_state.temp_profile.get('current_emotions', [])),
            '😣 Stressed': st.checkbox('😣 Stressed', value='Stressed' in st.session_state.temp_profile.get('current_emotions', [])),
            '🏝️ Lonely': st.checkbox('🏝️ Lonely', value='Lonely' in st.session_state.temp_profile.get('current_emotions', [])),
            '😌 Calm': st.checkbox('😌 Calm', value='Calm' in st.session_state.temp_profile.get('current_emotions', [])),
            '🤔 Confused': st.checkbox('🤔 Confused', value='Confused' in st.session_state.temp_profile.get('current_emotions', [])),
        }
        
        selected_emotions = [emotion.split(' ', 1)[1] for emotion, checked in emotions.items() if checked]
        
        st.markdown("---")
        
        # Physical sensations
        st.markdown("### Physical Sensations")
        st.markdown("Are you experiencing any of these? (Select multiple)")
        
        physical = {
            'Headache': st.checkbox('🤕 Headache', value='Headache' in st.session_state.temp_profile.get('physical_sensations', [])),
            'Chest tightness': st.checkbox('🫀 Chest tightness or racing heart', value='Chest tightness' in st.session_state.temp_profile.get('physical_sensations', [])),
            'Fatigue': st.checkbox('😴 Fatigue or low energy', value='Fatigue' in st.session_state.temp_profile.get('physical_sensations', [])),
            'Muscle tension': st.checkbox('💪 Muscle tension or pain', value='Muscle tension' in st.session_state.temp_profile.get('physical_sensations', [])),
            'Stomach issues': st.checkbox('🤢 Stomach discomfort or nausea', value='Stomach issues' in st.session_state.temp_profile.get('physical_sensations', [])),
            'Changes in appetite': st.checkbox('🍽️ Changes in appetite', value='Changes in appetite' in st.session_state.temp_profile.get('physical_sensations', [])),
            'None': st.checkbox('✅ None of these', value='None' in st.session_state.temp_profile.get('physical_sensations', [])),
        }
        
        selected_physical = [symptom for symptom, checked in physical.items() if checked]
        
        st.markdown("---")
        
        # Sleep quality
        st.markdown("### Sleep & Energy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sleep_quality = st.select_slider(
                "How has your sleep been lately?",
                options=["Very Poor", "Poor", "Fair", "Good", "Very Good"],
                value=st.session_state.temp_profile.get('sleep_quality', 'Fair'),
                help="Over the past week"
            )
        
        with col2:
            energy_level = st.select_slider(
                "How is your energy level?",
                options=["Very Low", "Low", "Moderate", "High", "Very High"],
                value=st.session_state.temp_profile.get('energy_level', 'Moderate'),
                help="Right now or generally"
            )
        
        st.markdown("---")
        
        # Recent stressors
        st.markdown("### Recent Experiences")
        
        recent_events = st.text_area(
            "Have you experienced any significant stressors or changes recently? (Optional)",
            value=st.session_state.temp_profile.get('recent_events', ''),
            placeholder="Examples: Job loss, breakup, family issues, health concerns, major life changes...",
            height=100,
            help="This helps us understand your current context. You can skip this if you prefer."
        )
        
        # How long feeling this way
        duration = st.selectbox(
            "How long have you been feeling this way?",
            options=[
                "Just today",
                "A few days",
                "About a week",
                "A few weeks",
                "A month or more",
                "Several months",
                "A year or more",
                "As long as I can remember"
            ],
            index=["Just today", "A few days", "About a week", "A few weeks", "A month or more", 
                   "Several months", "A year or more", "As long as I can remember"].index(
                st.session_state.temp_profile.get('feelings_duration', 'A few days')
            ),
            help="Understanding the timeline helps provide appropriate support"
        )
        
        st.markdown("---")
        
        # Navigation
        col1, col2 = st.columns(2)
        
        with col1:
            back = st.form_submit_button("← Back", use_container_width=True)
        
        with col2:
            submit = st.form_submit_button("Continue →", use_container_width=True, type="primary")
        
        if back:
            st.session_state.onboarding_step = 1
            st.rerun()
        
        if submit:
            # Save data
            st.session_state.temp_profile.update({
                'current_mood': current_mood,
                'current_emotions': selected_emotions,
                'physical_sensations': selected_physical,
                'sleep_quality': sleep_quality,
                'energy_level': energy_level,
                'recent_events': (recent_events or "").strip(),
                'feelings_duration': duration
            })
            
            # Check for crisis indicators
            crisis_indicators = check_crisis_indicators(
                selected_emotions, 
                selected_physical, 
                current_mood, 
                duration
            )
            
            if crisis_indicators:
                st.warning("""
                ⚠️ **We notice you're going through a difficult time.**
                
                Please remember:
                - MindSync AI is here to support you, but we're not a crisis service
                - If you're in immediate danger, please call emergency services (911)
                - Crisis helplines are available 24/7:
                  - Tunisia: 80 101 080
                  - US: 988 (Suicide & Crisis Lifeline)
                  - International: 116 123
                
                You can still continue with MindSync AI for ongoing support.
                """)
                
                st.session_state.temp_profile['crisis_risk'] = True
            
            st.session_state.onboarding_step = 3
            st.rerun()


def check_crisis_indicators(emotions: list, physical: list, mood: str, duration: str) -> bool:
    """
    Check for potential crisis indicators
    
    INDICATORS:
    - Hopelessness + prolonged duration
    - Multiple severe symptoms
    - Very low mood + long duration
    
    RETURNS: True if concerning patterns detected
    """
    
    crisis_emotions = ['Hopeless', 'Numb/Empty']
    severe_mood = mood in ['Very Low']
    long_duration = duration in ['Several months', 'A year or more', 'As long as I can remember']
    
    has_crisis_emotion = any(e in crisis_emotions for e in emotions)
    multiple_symptoms = len(emotions) >= 4
    
    return (has_crisis_emotion and long_duration) or (severe_mood and long_duration) or (multiple_symptoms and severe_mood)


# ============================================================================
# STEP 3: MENTAL HEALTH BACKGROUND (NEW)
# ============================================================================

def show_mental_health_background_step():
    """
    Optional mental health history
    
    WHY: Understanding background helps provide contextual support
    
    CAPTURES:
    - Previous therapy/counseling
    - Diagnoses (self-reported)
    - Medication
    - Hospitalization history
    - Family history
    
    NOTE: All optional, clearly marked
    """
    
    st.title("Your Mental Health Background 📋")
    st.markdown("""
    This section is **completely optional**. Sharing helps us provide better support, 
    but you can skip any or all questions.
    
    🔒 **Privacy**: This information is confidential and stored securely.
    """)
    
    with st.form("mental_health_background_form"):
        
        # Previous professional help
        st.markdown("### Professional Support History")
        
        has_therapy = st.radio(
            "Have you ever worked with a mental health professional?",
            options=["Yes", "No", "Prefer not to say"],
            index=["Yes", "No", "Prefer not to say"].index(
                st.session_state.temp_profile.get('has_therapy', 'Prefer not to say')
            ),
            help="Therapist, counselor, psychologist, psychiatrist, etc."
        )
        
        if has_therapy == "Yes":
            therapy_current = st.radio(
                "Are you currently in therapy?",
                options=["Yes", "No"],
                index=["Yes", "No"].index(
                    st.session_state.temp_profile.get('therapy_current', 'No')
                )
            )
            
            therapy_helpful = st.select_slider(
                "How helpful was/is therapy for you?",
                options=["Not helpful", "Somewhat helpful", "Moderately helpful", "Very helpful", "Extremely helpful"],
                value=st.session_state.temp_profile.get('therapy_helpful', 'Moderately helpful')
            )
        else:
            therapy_current = None
            therapy_helpful = None
        
        st.markdown("---")
        
        # Diagnoses
        st.markdown("### Mental Health Conditions (Optional)")
        st.markdown("Have you been diagnosed with any of the following? (Select all that apply)")
        
        diagnoses = {
            'Depression': st.checkbox('Depression', value='Depression' in st.session_state.temp_profile.get('diagnoses', [])),
            'Anxiety Disorder': st.checkbox('Anxiety Disorder (GAD, Social Anxiety, etc.)', value='Anxiety Disorder' in st.session_state.temp_profile.get('diagnoses', [])),
            'PTSD': st.checkbox('PTSD (Post-Traumatic Stress Disorder)', value='PTSD' in st.session_state.temp_profile.get('diagnoses', [])),
            'Bipolar Disorder': st.checkbox('Bipolar Disorder', value='Bipolar Disorder' in st.session_state.temp_profile.get('diagnoses', [])),
            'OCD': st.checkbox('OCD (Obsessive-Compulsive Disorder)', value='OCD' in st.session_state.temp_profile.get('diagnoses', [])),
            'Eating Disorder': st.checkbox('Eating Disorder', value='Eating Disorder' in st.session_state.temp_profile.get('diagnoses', [])),
            'ADHD': st.checkbox('ADHD (Attention-Deficit/Hyperactivity Disorder)', value='ADHD' in st.session_state.temp_profile.get('diagnoses', [])),
            'Other': st.checkbox('Other (please specify below)', value='Other' in st.session_state.temp_profile.get('diagnoses', [])),
            'None': st.checkbox('None / Not diagnosed', value='None' in st.session_state.temp_profile.get('diagnoses', [])),
            'Prefer not to say': st.checkbox('Prefer not to say', value='Prefer not to say' in st.session_state.temp_profile.get('diagnoses', [])),
        }
        
        selected_diagnoses = [diagnosis for diagnosis, checked in diagnoses.items() if checked]
        
        if diagnoses['Other']:
            other_diagnosis = st.text_input(
                "Please specify:",
                value=st.session_state.temp_profile.get('other_diagnosis', ''),
                placeholder="Other diagnosis..."
            )
        else:
            other_diagnosis = ''
        
        st.markdown("---")
        
        # Medication
        st.markdown("### Medication (Optional)")
        
        on_medication = st.radio(
            "Are you currently taking medication for mental health?",
            options=["Yes", "No", "Prefer not to say"],
            index=["Yes", "No", "Prefer not to say"].index(
                st.session_state.temp_profile.get('on_medication', 'Prefer not to say')
            )
        )
        
        st.markdown("---")
        
        # Family history
        st.markdown("### Family History (Optional)")
        
        family_history = st.radio(
            "Is there a history of mental health conditions in your family?",
            options=["Yes", "No", "Not sure", "Prefer not to say"],
            index=["Yes", "No", "Not sure", "Prefer not to say"].index(
                st.session_state.temp_profile.get('family_history', 'Prefer not to say')
            ),
            help="This can help us understand potential genetic factors"
        )
        
        st.markdown("---")
        
        # Additional context
        anything_else = st.text_area(
            "Anything else about your mental health background you'd like to share? (Optional)",
            value=st.session_state.temp_profile.get('background_notes', ''),
            placeholder="Any other relevant information...",
            height=100
        )
        
        st.markdown("---")
        st.info("💡 **Remember**: You can skip this entire section if you prefer. Click 'Continue' to move forward.")
        
        # Navigation
        col1, col2 = st.columns(2)
        
        with col1:
            back = st.form_submit_button("← Back", use_container_width=True)
        
        with col2:
            submit = st.form_submit_button("Continue →", use_container_width=True, type="primary")
        
        if back:
            st.session_state.onboarding_step = 2
            st.rerun()
        
        if submit:
            # Save data
            st.session_state.temp_profile.update({
                'has_therapy': has_therapy,
                'therapy_current': therapy_current,
                'therapy_helpful': therapy_helpful,
                'diagnoses': selected_diagnoses,
                'other_diagnosis': other_diagnosis,
                'on_medication': on_medication,
                'family_history': family_history,
                'background_notes': (anything_else or "").strip()
            })
            
            st.session_state.onboarding_step = 4
            st.rerun()


# ============================================================================
# STEP 4: SUPPORT SYSTEM & COPING STRATEGIES (NEW)
# ============================================================================

def show_support_system_step():
    """
    Evaluate existing support system and coping strategies
    
    WHY: Understanding existing resources helps identify gaps and strengths
    
    CAPTURES:
    - Social support network
    - Current coping strategies
    - What helps/doesn't help
    - Barriers to support
    """
    
    st.title("Your Support System & Coping Tools 🤝")
    st.markdown("""
    Understanding what support and strategies you already have helps us complement them, not replace them.
    """)
    
    with st.form("support_system_form"):
        
        # Social support
        st.markdown("### Your Support Network")
        
        support_network = st.multiselect(
            "Who do you have in your support network? (Select all that apply)",
            options=[
                "Close family members",
                "Friends",
                "Romantic partner",
                "Therapist/Counselor",
                "Support group",
                "Religious/Spiritual community",
                "Coworkers/Colleagues",
                "Online communities",
                "Pets",
                "No one currently",
                "Prefer not to say"
            ],
            default=st.session_state.temp_profile.get('support_network', []),
            help="These are people/communities you can turn to"
        )
        
        support_satisfaction = st.select_slider(
            "How satisfied are you with your current support system?",
            options=["Very Dissatisfied", "Dissatisfied", "Neutral", "Satisfied", "Very Satisfied"],
            value=st.session_state.temp_profile.get('support_satisfaction', 'Neutral')
        )
        
        st.markdown("---")
        
        # Current coping strategies
        st.markdown("### What You Already Do to Cope")
        st.markdown("What strategies do you currently use when feeling stressed or down? (Select all that apply)")
        
        coping_strategies = {
            'Talk to someone': st.checkbox('💬 Talk to someone', value='Talk to someone' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Exercise': st.checkbox('🏃 Exercise or physical activity', value='Exercise' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Meditation/Mindfulness': st.checkbox('🧘 Meditation or mindfulness', value='Meditation/Mindfulness' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Journaling': st.checkbox('📝 Journaling or writing', value='Journaling' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Creative activities': st.checkbox('🎨 Creative activities (art, music, etc.)', value='Creative activities' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Time in nature': st.checkbox('🌳 Spend time in nature', value='Time in nature' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Reading': st.checkbox('📚 Reading', value='Reading' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Listening to music': st.checkbox('🎵 Listening to music', value='Listening to music' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Watching shows/movies': st.checkbox('📺 Watching shows or movies', value='Watching shows/movies' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Gaming': st.checkbox('🎮 Gaming', value='Gaming' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Sleeping': st.checkbox('😴 Sleeping or resting', value='Sleeping' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Eating': st.checkbox('🍔 Eating comfort food', value='Eating' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Isolation': st.checkbox('🚪 Isolating myself', value='Isolation' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Substance use': st.checkbox('🍺 Alcohol or substance use', value='Substance use' in st.session_state.temp_profile.get('coping_strategies', [])),
            'Nothing works': st.checkbox('❌ Nothing seems to help', value='Nothing works' in st.session_state.temp_profile.get('coping_strategies', [])),
        }
        
        selected_coping = [strategy for strategy, checked in coping_strategies.items() if checked]
        
        st.markdown("---")
        
        # What helps most
        what_helps = st.text_area(
            "What has been most helpful when you're struggling? (Optional)",
            value=st.session_state.temp_profile.get('what_helps', ''),
            placeholder="Specific activities, people, places, or strategies that help you feel better...",
            height=80
        )
        
        what_doesnt_help = st.text_area(
            "What hasn't been helpful or makes things worse? (Optional)",
            value=st.session_state.temp_profile.get('what_doesnt_help', ''),
            placeholder="Things to avoid or that haven't worked for you...",
            height=80
        )
        
        st.markdown("---")
        
        # Barriers
        st.markdown("### Barriers to Getting Support")
        
        barriers = st.multiselect(
            "What makes it difficult to get the support you need? (Select all that apply)",
            options=[
                "Cost/Financial concerns",
                "Don't know where to start",
                "Stigma or shame",
                "Lack of time",
                "No one to talk to",
                "Don't want to burden others",
                "Tried before and it didn't help",
                "Difficulty trusting others",
                "Cultural or language barriers",
                "Transportation issues",
                "No barriers - I have good access to support",
                "Other"
            ],
            default=st.session_state.temp_profile.get('barriers', [])
        )
        
        if "Other" in barriers:
            other_barrier = st.text_input(
                "Please specify:",
                value=st.session_state.temp_profile.get('other_barrier', ''),
                placeholder="Other barrier..."
            )
        else:
            other_barrier = ''
        
        st.markdown("---")
        
        # Navigation
        col1, col2 = st.columns(2)
        
        with col1:
            back = st.form_submit_button("← Back", use_container_width=True)
        
        with col2:
            submit = st.form_submit_button("Continue →", use_container_width=True, type="primary")
        
        if back:
            st.session_state.onboarding_step = 3
            st.rerun()
        
        if submit:
            # Save data
            st.session_state.temp_profile.update({
                'support_network': support_network,
                'support_satisfaction': support_satisfaction,
                'coping_strategies': selected_coping,
                'what_helps': (what_helps or "").strip(),
                'what_doesnt_help': (what_doesnt_help or "").strip(),
                'barriers': barriers,
                'other_barrier': other_barrier
            })
            
            st.session_state.onboarding_step = 5
            st.rerun()


# ============================================================================
# STEP 5: CONCERNS & GOALS (ENHANCED)
# ============================================================================

def show_concerns_goals_step():
    """
    Enhanced concerns and goals with specific, measurable objectives
    
    CAPTURES:
    - Primary concerns (as before)
    - Specific goals
    - Timeline expectations
    - Success metrics
    """
    
    st.title("What Do You Hope to Achieve? 🎯")
    st.markdown("Let's identify your concerns and set meaningful goals for your journey.")
    
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
    
    with st.form("concerns_goals_form"):
        
        st.markdown("### Areas Where You Want Support")
        
        selected_concerns = []
        
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
        
        st.markdown("---")
        
        # Specific goals
        st.markdown("### Your Goals")
        
        st.markdown("""
        What would you like to accomplish through MindSync AI?  
        *Be specific! For example: "Reduce anxiety attacks from 5/week to 1/week" or "Build a consistent sleep schedule"*
        """)
        
        goal_1 = st.text_input(
            "Primary Goal:",
            value=st.session_state.temp_profile.get('goal_1', ''),
            placeholder="Example: Learn to manage stress without feeling overwhelmed"
        )
        
        goal_2 = st.text_input(
            "Secondary Goal (Optional):",
            value=st.session_state.temp_profile.get('goal_2', ''),
            placeholder="Example: Improve my sleep quality"
        )
        
        goal_3 = st.text_input(
            "Another Goal (Optional):",
            value=st.session_state.temp_profile.get('goal_3', ''),
            placeholder="Example: Build confidence in social situations"
        )
        
        st.markdown("---")
        
        # Timeline
        timeline = st.selectbox(
            "What's your timeframe for seeing improvement?",
            options=[
                "Within a few weeks",
                "Within a few months",
                "Within 6 months",
                "Within a year",
                "I'm in this for the long haul",
                "Just taking it one day at a time"
            ],
            index=["Within a few weeks", "Within a few months", "Within 6 months", "Within a year", 
                   "I'm in this for the long haul", "Just taking it one day at a time"].index(
                st.session_state.temp_profile.get('timeline', 'Within a few months')
            ),
            help="Be realistic - mental health progress takes time"
        )
        
        st.markdown("---")
        
        # Additional context
        additional_notes = st.text_area(
            "Anything else you'd like us to know? (Optional)",
            value=st.session_state.temp_profile.get('additional_notes', ''),
            placeholder="Any other context about your situation, goals, or needs...",
            height=100
        )
        
        st.markdown("---")
        
        # Navigation
        col1, col2 = st.columns(2)
        
        with col1:
            back = st.form_submit_button("← Back", use_container_width=True)
        
        with col2:
            submit = st.form_submit_button("Continue →", use_container_width=True, type="primary")
        
        if back:
            st.session_state.onboarding_step = 4
            st.rerun()
        
        if submit:
            st.session_state.temp_profile.update({
                'concerns': selected_concerns,
                'goal_1': (goal_1 or "").strip(),
                'goal_2': (goal_2 or "").strip(),
                'goal_3': (goal_3 or "").strip(),
                'timeline': timeline,
                'additional_notes': (additional_notes or "").strip()
            })
            
            st.session_state.onboarding_step = 6
            st.rerun()


# ============================================================================
# STEP 6: SUPPORT STYLE (Same as before)
# ============================================================================

def show_support_style_step():
    """Determine user's preferred support style"""
    
    st.title("How Can We Best Support You? 🤝")
    st.markdown("Everyone has different preferences for support. Choose what works best for you.")
    
    with st.form("support_style_form"):
        
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
            label_visibility="collapsed"
        )
        
        if support_style == "Listening & Validation":
            st.info("🎧 **Listening Mode**: MindSync will focus on understanding and validating your feelings.")
        elif support_style == "Actionable Advice":
            st.info("💡 **Advice Mode**: MindSync will offer practical suggestions and coping strategies.")
        else:
            st.info("⚖️ **Balanced Mode**: MindSync will both validate feelings AND provide guidance.")
        
        st.markdown("---")
        
        st.markdown("### Additional Preferences")
        
        response_length = st.select_slider(
            "Response Length Preference",
            options=["Brief", "Medium", "Detailed"],
            value=st.session_state.temp_profile.get('response_length', 'Medium')
        )
        
        checkin_frequency = st.selectbox(
            "How often would you like check-ins?",
            options=["Daily", "Every few days", "Weekly", "I'll reach out when needed"],
            index=["Daily", "Every few days", "Weekly", "I'll reach out when needed"].index(
                st.session_state.temp_profile.get('checkin_frequency', "I'll reach out when needed")
            )
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            back = st.form_submit_button("← Back", use_container_width=True)
        
        with col2:
            submit = st.form_submit_button("Complete Setup →", use_container_width=True, type="primary")
        
        if back:
            st.session_state.onboarding_step = 5
            st.rerun()
        
        if submit:
            st.session_state.temp_profile['support_style'] = support_style
            st.session_state.temp_profile['response_length'] = response_length
            st.session_state.temp_profile['checkin_frequency'] = checkin_frequency
            
            st.session_state.onboarding_step = 7
            st.rerun()


# ============================================================================
# STEP 7: COMPLETION
# ============================================================================

def show_completion_step():
    """Final step - Review and create profile"""
    
    st.title("You're All Set! 🎉")
    st.markdown("Review your profile and start your mental health journey.")
    
    profile = st.session_state.temp_profile
    
    # Comprehensive summary
    with st.expander("📋 Your Complete Profile", expanded=True):
        
        st.markdown("### Basic Information")
        st.write(f"**Name:** {profile.get('name')}")
        st.write(f"**Age:** {profile.get('age')}")
        st.write(f"**Language:** {profile.get('language')}")
        
        st.markdown("### Current State")
        st.write(f"**Mood:** {profile.get('current_mood')}")
        if profile.get('current_emotions'):
            st.write(f"**Feelings:** {', '.join(profile.get('current_emotions'))}")
        st.write(f"**Duration:** {profile.get('feelings_duration')}")
        
        st.markdown("### Goals & Concerns")
        if profile.get('concerns'):
            st.write(f"**Focus Areas:** {', '.join(profile.get('concerns'))}")
        if profile.get('goal_1'):
            st.write(f"**Primary Goal:** {profile.get('goal_1')}")
        
        st.markdown("### Preferences")
        st.write(f"**Support Style:** {profile.get('support_style')}")
        st.write(f"**Check-in Frequency:** {profile.get('checkin_frequency')}")
    
    st.markdown("---")
    
    # Consent
    agree = st.checkbox(
        "I understand that MindSync AI is a support tool and not a replacement for professional therapy",
        value=False
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.onboarding_step = 6
            st.rerun()
    
    with col2:
        if st.button("Start My Journey 🚀", use_container_width=True, type="primary", disabled=not agree):
            create_user_profile()
            
            st.success("✅ Profile created successfully!")
            st.balloons()
            
            st.info(f"🎯 Welcome, {profile.get('name')}! Your personalized MindSync AI experience is ready.")
            
            st.session_state.onboarding_complete = True
            
            if 'temp_profile' in st.session_state:
                del st.session_state.temp_profile
            
            import time
            time.sleep(2)
            st.rerun()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_user_profile():
    """Create comprehensive user profile in database"""
    
    user_id = str(uuid.uuid4())
    profile = st.session_state.temp_profile.copy()
    profile['user_id'] = user_id
    profile['onboarding_version'] = 'enhanced_v2'
    
    try:
        st.session_state.user_id = user_id
        st.session_state.user_profile = profile
        
        # Initialize memory system
        from src.services.memory_system import UserMemorySystem
        st.session_state.memory_system = UserMemorySystem()
        
        # Save comprehensive profile
        st.session_state.memory_system.update_memory(user_id, {
            'profile': profile,
            'onboarding_completed': datetime.now().isoformat(),
            'total_conversations': 0,
            'days_active': 1,
            'last_milestone_shown': 0
        })
        
        return True
        
    except Exception as e:
        st.error(f"Error creating profile: {str(e)}")
        return False
    
    
# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Initialize session state variables
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 0
    
    if 'onboarding_complete' not in st.session_state:
        st.session_state.onboarding_complete = False
    
    if 'temp_profile' not in st.session_state:
        st.session_state.temp_profile = {}
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    
    if 'memory_system' not in st.session_state:
        st.session_state.memory_system = None
    
    # Set page config
    st.set_page_config(
        page_title="Welcome to MindSync AI",
        page_icon="🧠",
        layout="wide"
    )
    
    # Show the onboarding flow
    show_onboarding_flow()