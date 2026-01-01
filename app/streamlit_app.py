# # app/streamlit_app.py

# import streamlit as st
# from pathlib import Path
# import sys

# sys.path.append(str(Path(__file__).parent.parent))

# from src.services.conversation_service import EnhancedConversationService
# from datetime import datetime

# st.set_page_config(
#     page_title="MindSync AI - Intelligent Mental Health Companion",
#     page_icon="🧠",
#     layout="wide"
# )
# st.markdown("""
# <style>
# /* Page background */
# [data-testid="stAppViewContainer"] {
#     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#     color: white;
# }

# /* User messages */
# [data-testid="stChatMessage"][data-role="user"] .stMarkdown p {
#     color: black;
#     background-color: rgba(255,255,255,0.9);
#     border-radius: 15px;
#     padding: 10px;
# }

# /* Assistant messages */
# [data-testid="stChatMessage"][data-role="assistant"] .stMarkdown p {
#     color: white;
#     background-color: rgba(0,0,0,0.5);
#     border-radius: 15px;
#     padding: 10px;
# }

# /* Crisis alert */
# .crisis-alert {
#     background-color: #ff4444;
#     color: white;
#     padding: 20px;
#     border-radius: 10px;
#     font-weight: bold;
#     text-align: center;
#     margin: 20px 0;
# }

# /* Sidebar */
# [data-testid="stSidebar"] {
#     background-color: rgba(0,0,0,0.5);
#     color: white;
# }
# </style>
# """, unsafe_allow_html=True)

# # Initialize session state
# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# if 'conversation_service' not in st.session_state:
#     with st.spinner("🤖 Initializing MindSync AI..."):
#         st.session_state.conversation_service = EnhancedConversationService(user_id="demo_user")

# # Title
# st.title("🧠 MindSync AI")
# st.markdown("### Your Intelligent Mental Health Companion")
# st.markdown("**I'm here to listen, understand, and support you.** 💙")

# # Display chat history
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
        
#         # Show emotion badge for user messages
#         if message["role"] == "user" and "emotion" in message:
#             st.caption(f"Detected emotion: **{message['emotion'].upper()}** ({message['confidence']:.0%})")

# # Chat input
# if prompt := st.chat_input("Type your message here... (I understand mixed languages!)"):
    
#     # Add user message
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     st.session_state.messages.append({
#         "role": "user",
#         "content": prompt
#     })
    
#     # Process with AI
#     # app/streamlit_app.py (just the relevant part)

#     # Process with AI
#     with st.spinner("🤔 Thinking..."):
#         try:
#             response_data = st.session_state.conversation_service.process_text_message(
#                 user_input=prompt,
#                 conversation_history=st.session_state.messages
#             )
#         except KeyError as e:
#             st.error(f"⚠️ Model error: {e}")
#             st.info("Using fallback response...")
            
#             # Fallback response
#             response_data = {
#                 'response': "💭 I'm here to listen. Tell me more about how you're feeling.",
#                 'detected_emotion': 'neutral',
#                 'emotion_confidence': 0.5,
#                 'intent': 'GENERAL',
#                 'intent_confidence': 0.5,
#                 'crisis_detected': False,
#                 'all_emotion_scores': {}
#             }

    
#     # Check for crisis
#     if response_data['crisis_detected']:
#         st.markdown("""
#         <div class="crisis-alert">
#             🚨 CRISIS DETECTED 🚨<br><br>
#             Please reach out for immediate professional help:<br>
#             <strong>Tunisia: 80 101 080</strong><br>
#             <strong>International: 116 123</strong>
#         </div>
#         """, unsafe_allow_html=True)
    
#     # Add assistant response
#     with st.chat_message("assistant"):
#         st.markdown(response_data['response'])
    
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": response_data['response']
#     })
    
#     # Update last user message with emotion
#     st.session_state.messages[-2].update({
#         "emotion": response_data['detected_emotion'],
#         "confidence": response_data['emotion_confidence']
#     })
    
#     st.rerun()

# # Sidebar
# with st.sidebar:
#     st.title("💡 About MindSync")
#     st.write("""
#     MindSync uses advanced AI to:
#     - 🎭 Understand your emotions
#     - 💬 Have meaningful conversations
#     - 🆘 Detect crisis situations
#     - 📊 Track your mental well-being
#     """)
    
#     if st.button("🗑️ Clear Chat"):
#         st.session_state.messages = []
#         st.rerun()
    
#     st.markdown("---")
#     st.caption("⚠️ Not a replacement for professional therapy")








import streamlit as st
from pathlib import Path
import sys

# Add src directory to Python path so we can import our modules
# Add project root (parent of app/) to PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.services.user_service import UserService
from src.services.memory_system import UserMemorySystem

# Configure the page - MUST be first Streamlit command
st.set_page_config(
    page_title="MindSync AI - Mental Health Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# INITIALIZATION FUNCTIONS
# ============================================================================

def initialize_session_state():
    """
    Initialize all session state variables
    
    WHY: Session state persists data between page reruns and navigation
    Without this, data would reset every time user interacts with the app
    
    BEGINNER TIP: Always use 'if key not in st.session_state' pattern
    to avoid resetting values on page refresh
    """
    
    # User authentication state
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    
    if 'onboarding_complete' not in st.session_state:
        st.session_state.onboarding_complete = False
    
    # Onboarding flow state (tracks which step user is on)
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 0
    
    # Chat history (list of messages)
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Services (initialized once and reused)
    if 'user_service' not in st.session_state:
        st.session_state.user_service = UserService()
    
    if 'memory_system' not in st.session_state:
        st.session_state.memory_system = None  # Will be set after login
    
    # UI state
    if 'show_sidebar' not in st.session_state:
        st.session_state.show_sidebar = True
    
    # Crisis mode flag
    if 'crisis_mode' not in st.session_state:
        st.session_state.crisis_mode = False


def load_custom_css():
    """
    Load custom CSS for beautiful, modern UI
    
    WHY: Default Streamlit styling is basic. Custom CSS makes app professional
    
    CSS EXPLANATION:
    - Gradients: Modern, calming background
    - Border radius: Rounded corners for friendly feel
    - Shadows: Depth and hierarchy
    - Transitions: Smooth animations
    """
    st.markdown("""
    <style>
    /* ===== GLOBAL STYLES ===== */
    
    /* Main app background - gradient for calming effect */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* ===== CHAT MESSAGE STYLES ===== */
    
    /* User messages - white background, dark text */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        color: #333;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* AI messages - translucent dark background */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background-color: rgba(0, 0, 0, 0.4);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    /* ===== BUTTON STYLES ===== */
    
    /* Primary buttons */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* ===== FORM STYLES ===== */
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    /* ===== CARD STYLES ===== */
    
    .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    /* ===== CRISIS ALERT ===== */
    
    .crisis-alert {
        background-color: #ff4444;
        color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #cc0000;
        margin: 20px 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* ===== PROGRESS BAR ===== */
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* ===== METRICS ===== */
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    /* ===== EXPANDER ===== */
    
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* ===== SUCCESS/ERROR/WARNING MESSAGES ===== */
    
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 15px;
    }
    
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN APPLICATION LOGIC
# ============================================================================

def main():
    """
    Main application logic
    
    FLOW:
    1. Initialize session state
    2. Load custom CSS
    3. Check if user completed onboarding
    4. Show onboarding OR main app
    """
    
    # Initialize everything
    initialize_session_state()
    load_custom_css()
    
    # Check onboarding status
    if not st.session_state.onboarding_complete:
        # User hasn't completed onboarding - show onboarding flow
        show_onboarding()
    else:
        # User is logged in - show main app with navigation
        show_main_app()


def show_onboarding():
    """
    Display onboarding flow
    
    WHY: Collect user information for personalization
    
    STEPS:
    0. Welcome screen
    1. Basic info (name, age, language)
    2. Mental health concerns
    3. Support style preferences
    4. Completion and profile creation
    """
    from pages.onboarding import show_onboarding_flow
    show_onboarding_flow()


def show_main_app():
    """
    Display main app with navigation
    
    WHY: After onboarding, users access different features
    
    STRUCTURE:
    - Sidebar: Navigation menu
    - Main area: Selected page content
    """
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🧠 MindSync AI")
        st.markdown("---")
        
        # User info display
        if st.session_state.user_profile:
            st.markdown(f"### Welcome, {st.session_state.user_profile.get('name', 'User')}! 👋")
            st.markdown("---")
        
        # Navigation menu
        st.markdown("### Navigation")
        
        # Page selection
        page = st.radio(
            "Go to:",
            ["💬 Chat", "📊 Insights", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick stats (if available)
        if st.session_state.memory_system:
            memory = st.session_state.memory_system.get_user_memory(st.session_state.user_id)
            
            st.markdown("### Quick Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Conversations", memory.get('total_conversations', 0))
            with col2:
                st.metric("Days Active", memory.get('days_active', 0))
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Display selected page
    if page == "💬 Chat":
        from pages.Chat import show_chat_page
        show_chat_page()
    elif page == "📊 Insights":
        from pages.Insights import show_insights_page
        show_insights_page()
    elif page == "⚙️ Settings":
        from pages.Settings import show_settings_page
        show_settings_page()


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()