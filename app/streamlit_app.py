# app/streamlit_app.py

import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.services.conversation_service import EnhancedConversationService
from datetime import datetime

# ====================
# PAGE CONFIGURATION
# ====================
st.set_page_config(
    page_title="MindSync AI - Mental Health Companion",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================
# ENHANCED STYLING WITH CUSTOM LOGO
# ====================
st.markdown("""
<style>
/* ============================================
   BACKGROUND OPTIONS - Choose one below
   ============================================ */

/* OPTION 1: Calming Teal to Blue (RECOMMENDED for mental health) */
/*[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}*/

/* OPTION 2: Peaceful Lavender to Peach */
/*
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 50%, #d4a5a5 100%);
    color: #2d2d2d;
}
*/

/* OPTION 3: Healing Green to Blue */
/*
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 50%, #89c9b8 100%);
    color: #2d2d2d;
}
*/

/* OPTION 4: Soft Purple Therapy Vibe */
/*
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
    color: #2d2d2d;
}
*/

/* OPTION 5: Warm Sunset Comfort */
/*
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 50%, #fab1a0 100%);
    color: #2d2d2d;
}
*/

/* OPTION 6: Subtle Pattern Overlay (Use with any gradient) */

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
}


/* Sidebar styling */
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

/* Custom Logo Container */
.logo-container {
    text-align: center;
    margin-bottom: 30px;
    padding: 20px;
}

.logo-container img {
    max-width: 50px;
    height: auto;
    border-radius: 5px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}

.logo-container img:hover {
    transform: scale(1.05);
}

/* Navigation buttons */
.stButton button {
    width: 100%;
    border-radius: 10px;
    padding: 12px;
    font-size: 16px;
    font-weight: 500;
    transition: all 0.3s ease;
    background-color: rgba(255,255,255,0.1);
    color: white;
    border: 1px solid rgba(255,255,255,0.2);
}

.stButton button:hover {
    background-color: rgba(255,255,255,0.2);
    border-color: rgba(255,255,255,0.4);
    transform: translateX(5px);
}

/* Chat messages - Glass morphism effect */
[data-testid="stChatMessage"][data-role="user"] {
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

[data-testid="stChatMessage"][data-role="assistant"] {
    background: rgba(0,0,0,0.2);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}

/* Emotion badge */
.emotion-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    margin-top: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.emotion-joy { background-color: #FFD700; color: #000; }
.emotion-sadness { background-color: #4169E1; color: #fff; }
.emotion-anger { background-color: #DC143C; color: #fff; }
.emotion-fear { background-color: #9370DB; color: #fff; }
.emotion-neutral { background-color: #808080; color: #fff; }

/* Crisis alert */
.crisis-alert {
    background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
    color: white;
    padding: 25px;
    border-radius: 20px;
    font-weight: bold;
    text-align: center;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(255,0,0,0.4);
    animation: pulse 2s infinite;
    border: 2px solid rgba(255,255,255,0.3);
}

@keyframes pulse {
    0%, 100% { transform: scale(1); box-shadow: 0 8px 25px rgba(255,0,0,0.4); }
    50% { transform: scale(1.02); box-shadow: 0 12px 35px rgba(255,0,0,0.6); }
}

/* Input box - Glass effect */
[data-testid="stChatInput"] {
    border-radius: 25px;
    border: 2px solid rgba(255,255,255,0.3);
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}

/* Title styling with logo */
.header-container {
    text-align: center;
    margin-bottom: 30px;
}

.main-title {
    font-size: 3em;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 10px;
    background: linear-gradient(135deg, #00d4ff 0%, #ffffff 50%, #00d4ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    /* Remove text-shadow when using gradient text */
}

.subtitle {
    font-size: 1.5em;
    margin-bottom: 8px;
    opacity: 0.95;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.2);
}

.tagline {
    font-size: 1.2em;
    opacity: 0.85;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
}

/* Floating animation for decorative elements */
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.floating {
    animation: float 3s ease-in-out infinite;
}
</style>
""", unsafe_allow_html=True)

# ====================
# SESSION STATE INIT
# ====================
# ====================
# SESSION STATE INIT
# ====================
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'conversation_service' not in st.session_state:
    with st.spinner("🤖 Initializing MindSync AI..."):
        try:
            st.session_state.conversation_service = EnhancedConversationService(user_id="demo_user")
        except ImportError as e:
            st.error(f"❌ **Import Error**: Cannot find the conversation service module.")
            st.error(f"Details: {str(e)}")
            st.info("💡 Make sure `src/services/conversation_service.py` exists and contains `EnhancedConversationService`")
            st.session_state.conversation_service = None
        except Exception as e:
            st.error(f"❌ **Failed to initialize AI service**")
            st.error(f"Error type: `{type(e).__name__}`")
            st.error(f"Details: {str(e)}")
            st.exception(e)  # Shows full traceback
            st.session_state.conversation_service = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Chat"

# ====================
# SIDEBAR WITH LOGO
# ====================
import os
with st.sidebar:
    # Display custom logo
    try:
        # Get the absolute path to the logo
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        st.image(logo_path, use_container_width=True)
    except Exception as e:
        # Fallback if logo not found - show error for debugging
        st.error(f"Logo not found: {e}")
        st.markdown("<div class='logo-container'>🧠 MindSync AI</div>", unsafe_allow_html=True)
    
    
    # About section
    st.markdown("""
    MindSync uses advanced AI to:
    - **Understand** your emotions
    - **Have** meaningful conversations  
    - **Detect** crisis situations
    - **Track** your mental well-being
    """)
    
    # Clear chat button
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.success("Chat cleared!")
        st.rerun()
    
    # Warning
    st.markdown("---")
    st.warning("⚠️ **Not a replacement for professional therapy**")
    
    # Emergency contacts
    st.markdown("---")
    st.error("""
    **🆘 Emergency Contacts:**
    - Tunisia: **80 101 080**
    - International: **116 123**
    """)

# ====================
# MAIN CONTENT WITH LOGO
# ====================
# Display logo in main area (optional - if you want it in both places)
# try:
#     col1, col2, col3 = st.columns([1,2,1])
#     with col2:
#         st.image("app/assets/logo.png", width=200)  # Adjust path and width
# except:
#     pass

st.markdown("<div class='header-container'>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title floating'>MindSync AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your Intelligent Mental Health Companion</p>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>I'm here to listen, understand, and support you. 💙</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")

# Display chat history
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show emotion badge for user messages
        if message["role"] == "user" and "emotion" in message:
            emotion = message['emotion'].lower()
            st.markdown(
                f"<span class='emotion-badge emotion-{emotion}'>"
                f"🎭 {message['emotion'].upper()} ({message['confidence']:.0%})"
                f"</span>", 
                unsafe_allow_html=True
            )

# Chat input
if prompt := st.chat_input("Type your message here... (I understand mixed languages!) 💬"):
    
    # Add user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().isoformat()
    })
    
    if "conversation_service" not in st.session_state:
        st.session_state.conversation_service = EnhancedConversationService()

    
    # Process with AI
    with st.spinner("🤔 Thinking..."):
        try:
            response_data = st.session_state.conversation_service.process_text_message(
                user_input=prompt,
                conversation_history=st.session_state.messages
            )
        except Exception as e:
            st.error(f"⚠️ Error processing message: {str(e)}")
            st.error(f"Error type: {type(e).__name__}")
            st.exception(e)
            
            # Fallback response
            response_data = {
                'response': "💭 I'm experiencing technical difficulties. Tell me more about how you're feeling.",
                'detected_emotion': 'neutral',
                'emotion_confidence': 0.5,
                'intent': 'GENERAL',
                'intent_confidence': 0.5,
                'crisis_detected': False,
                'all_emotion_scores': {}
            }

    # Check for crisis
    if response_data['crisis_detected']:
        st.markdown("""
        <div class="crisis-alert">
            🚨 CRISIS DETECTED 🚨<br><br>
            <strong>You're not alone. Please reach out for immediate help:</strong><br><br>
            📞 <strong>Tunisia: 80 101 080</strong><br>
            🌍 <strong>International: 116 123</strong><br><br>
            <em>These services are confidential and available 24/7</em>
        </div>
        """, unsafe_allow_html=True)
    
    # Add assistant response
    with st.chat_message("assistant"):
        st.markdown(response_data['response'])
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_data['response'],
        "timestamp": datetime.now().isoformat()
    })
    
    # Update last user message with emotion
    st.session_state.messages[-2].update({
        "emotion": response_data['detected_emotion'],
        "confidence": response_data['emotion_confidence'],
        "intent": response_data['intent']
    })
    
    st.rerun()

# Show message count
if st.session_state.messages:
    st.caption(f"💬 **{len(st.session_state.messages)} messages** in this conversation")
