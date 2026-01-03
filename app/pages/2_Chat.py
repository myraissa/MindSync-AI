# app/pages/2_💬_Chat.py
import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.services.conversation_service import EnhancedConversationService
from datetime import datetime
from src.services.data_storage_service import DataStorageService

# ====================
# PAGE CONFIGURATION
# ====================
st.set_page_config(
    page_title="Chat - MindSync AI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================
# STYLING (Same CSS as original)
# ====================
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
    border-right: 2px solid rgba(255,255,255,0.1);
}

[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p {
    color: white !important;
}

.logo-container {
    text-align: center;
    margin-bottom: 30px;
    padding: 50px;
}

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

[data-testid="stChatInput"] {
    border-radius: 25px;
    border: 2px solid rgba(255,255,255,0.3);
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}

.main-title {
    font-size: 3em;
    font-weight: 800;
    margin: 10px 0;
    color: #4a5abf;
    text-align: center;
}

.subtitle {
    font-size: 1.5em;
    text-align: center;
    margin-bottom: 8px;
    opacity: 0.95;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.2);
}

.tagline {
    font-size: 1.2em;
    text-align: center;
    opacity: 0.85;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
}

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

if 'user_id' not in st.session_state:
    st.session_state.user_id = "demo_user"  # In production, get from authentication

if 'data_storage' not in st.session_state:
    st.session_state.data_storage = DataStorageService(user_id=st.session_state.user_id)

if 'conversation_service' not in st.session_state:
    with st.spinner("🤖 Initializing MindSync AI..."):
        try:
            st.session_state.conversation_service = EnhancedConversationService(
                user_id=st.session_state.user_id
            )
        except Exception as e:
            st.error(f"❌ **Failed to initialize AI service**")
            st.error(f"Details: {str(e)}")
            st.exception(e)
            st.session_state.conversation_service = None

# ====================
# SIDEBAR
# ====================
import os
with st.sidebar:
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
        st.image(logo_path)
    except Exception as e:
        st.markdown("<div class='logo-container'>MindSync AI</div>", unsafe_allow_html=True)
    
    st.markdown("""
    MindSync uses advanced AI to:
    - **Understand** your emotions
    - **Have** meaningful conversations  
    - **Detect** crisis situations
    - **Track** your mental well-being
    """)
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat cleared!")
        st.rerun()
    
    st.markdown("---")
    st.warning("⚠️ **Not a replacement for professional therapy**")
    
    st.markdown("---")
    st.error("""
    **🆘 Emergency Contacts:**
    - Tunisia: **80 101 080**
    - International: **116 123**
    """)

# ====================
# MAIN CONTENT
# ====================
st.markdown("<h1 class='main-title floating'>💬 MindSync Chat</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Deep conversations with AI</p>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>I'm here to listen, understand, and support you. 💙</p>", unsafe_allow_html=True)
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
    
    if st.session_state.conversation_service is None:
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
            response_data = {
                'response': "💭 I'm experiencing technical difficulties. Tell me more about how you're feeling.",
                'detected_emotion': 'neutral',
                'emotion_confidence': 0.5,
                'intent': 'GENERAL',
                'intent_confidence': 0.5,
                'crisis_detected': False,
                'all_emotion_scores': {}
            }

    # 🔥 SAVE TO DATABASE 🔥
    st.session_state.data_storage.add_conversation_entry(
        user_message=prompt,
        ai_response=response_data['response'],
        detected_emotion=response_data['detected_emotion'],
        emotion_confidence=response_data['emotion_confidence'],
        intent=response_data['intent'],
        crisis_detected=response_data['crisis_detected'],
        all_emotion_scores=response_data.get('all_emotion_scores', {})
    )

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
