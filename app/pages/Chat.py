import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from src.services.conversation_service import EnhancedConversationService
    CONVERSATION_SERVICE_AVAILABLE = True
except ImportError:
    CONVERSATION_SERVICE_AVAILABLE = False
    st.warning("⚠️ ConversationService not available. Using demo mode.")


def show_chat_page():
    """
    Main chat page display
    
    STRUCTURE:
    1. Header with user greeting
    2. Crisis resources (if needed)
    3. Chat history display
    4. Input field
    5. Sidebar with conversation tools
    """
    
    # Initialize conversation service
    initialize_conversation_service()
    
    # Page header
    display_header()
    
    # Crisis resources banner (if in crisis mode)
    if st.session_state.get('crisis_mode', False):
        display_crisis_banner()
    
    # Main chat interface
    display_chat_interface()
    
    # Sidebar with chat tools
    display_chat_sidebar()


print(CONVERSATION_SERVICE_AVAILABLE)

# ============================================================================
# INITIALIZATION
# ============================================================================

def initialize_conversation_service():
    """
    Initialize or retrieve conversation service
    
    WHY: Conversation service handles:
    - Emotion detection
    - Intent classification  
    - Response generation
    - Memory integration
    
    PATTERN: Singleton pattern - create once, reuse
    """
    
    if 'conversation_service' not in st.session_state:
        if CONVERSATION_SERVICE_AVAILABLE:
            try:
                # Initialize with user ID
                user_id = st.session_state.get('user_id', 'demo_user')
                st.session_state.conversation_service = EnhancedConversationService(user_id)
                st.session_state.service_ready = True
            except Exception as e:
                st.error(f"Error initializing conversation service: {str(e)}")
                st.session_state.service_ready = False
        else:
            st.session_state.service_ready = False
    
    # Initialize messages if empty
    if not st.session_state.messages:
        # Add welcome message
        welcome_msg = generate_welcome_message()
        st.session_state.messages.append({
            "role": "assistant",
            "content": welcome_msg,
            "timestamp": datetime.now().isoformat(),
            "metadata": {"type": "welcome"}
        })


# ============================================================================
# HEADER & LAYOUT
# ============================================================================

def display_header():
    """
    Display page header with greeting
    
    PERSONALIZATION: Uses user's name and time of day
    """
    
    user_name = st.session_state.user_profile.get('name', 'there')
    
    # Get time-appropriate greeting
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    st.title(f"💬 {greeting}, {user_name}!")
    st.markdown("I'm here to listen and support you. What's on your mind today?")
    st.markdown("---")


def display_crisis_banner():
    """
    Display crisis resources banner
    
    WHY: If AI detects crisis keywords, provide immediate help
    
    CRISIS INDICATORS:
    - Suicide mentions
    - Self-harm
    - Emergency situations
    """
    
    st.markdown("""
    <div class="crisis-alert">
        <h3>🚨 Crisis Resources - You're Not Alone</h3>
        <p><strong>If you're in immediate danger, please call emergency services (911) now.</strong></p>
        
        <p><strong>Crisis Support Available 24/7:</strong></p>
        <ul>
            <li>📞 <strong>National Suicide Prevention Lifeline:</strong> 988 (US)</li>
            <li>💬 <strong>Crisis Text Line:</strong> Text HOME to 741741</li>
            <li>🌍 <strong>International:</strong> findahelpline.com</li>
        </ul>
        
        <p>MindSync AI cares about you, but trained crisis counselors can provide immediate specialized support.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Option to dismiss crisis mode
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("I'm Safe Now", use_container_width=True):
            st.session_state.crisis_mode = False
            st.rerun()
    
    st.markdown("---")


# ============================================================================
# CHAT INTERFACE
# ============================================================================

def display_chat_interface():
    """
    Main chat display with message history and input
    
    FLOW:
    1. Display all messages from history
    2. Show typing indicator (if generating response)
    3. Handle new user input
    4. Generate AI response
    """
    
    # Container for chat messages (allows scrolling)
    chat_container = st.container()
    
    with chat_container:
        # Display all messages from history
        for message in st.session_state.messages:
            display_message(message)
    
    # Input field at bottom
    handle_user_input()


def display_message(message: dict):
    """
    Display a single message with styling
    
    MESSAGE STRUCTURE:
    {
        "role": "user" or "assistant",
        "content": "message text",
        "timestamp": "ISO format",
        "metadata": {
            "emotion": "happy",
            "intent": "VENT",
            "confidence": 0.95
        }
    }
    
    WHY: Different styling for user vs AI messages
    """
    
    role = message["role"]
    content = message["content"]
    metadata = message.get("metadata", {})
    
    # Display message with appropriate avatar
    with st.chat_message(role, avatar="👤" if role == "user" else "🧠"):
        st.markdown(content)
        
        # Show metadata for user messages (emotion detection)
        if role == "user" and metadata.get("emotion"):
            emotion = metadata["emotion"]
            confidence = metadata.get("confidence", 0)
            
            # Emotion indicator
            st.caption(f"Detected emotion: {emotion} ({confidence:.0%} confidence)")
        
        # Timestamp (small, subtle)
        timestamp = message.get("timestamp", "")
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%I:%M %p")
                st.caption(f"🕐 {time_str}")
            except:
                pass


def handle_user_input():
    """
    Handle user input and generate response
    
    FLOW:
    1. Get user input from chat_input
    2. Add to message history
    3. Detect emotion/intent
    4. Generate AI response
    5. Add response to history
    6. Check for crisis indicators
    
    WHY: chat_input must be outside form for real-time feel
    """
    
    # Chat input field (fixed at bottom)
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to history
        user_message = {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat(),
            "metadata": {}
        }
        
        st.session_state.messages.append(user_message)
        
        # Display user message immediately
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        
        # Generate AI response
        with st.spinner("MindSync is thinking..."):
            response_data = generate_response(user_input)
        
        # Add AI response to history
        ai_message = {
            "role": "assistant",
            "content": response_data["response"],
            "timestamp": datetime.now().isoformat(),
            "metadata": response_data.get("metadata", {})
        }
        
        st.session_state.messages.append(ai_message)
        
        # Update user message with detected metadata
        user_message["metadata"] = {
            "emotion": response_data.get("emotion", "neutral"),
            "intent": response_data.get("intent", "UNKNOWN"),
            "confidence": response_data.get("emotion_confidence", 0)
        }
        
        # Check for crisis
        if response_data.get("crisis_detected", False):
            st.session_state.crisis_mode = True
        
        # Save conversation to memory
        save_conversation_to_memory(user_input, response_data)
        
        # Rerun to display new message
        st.rerun()


def generate_response(user_input: str) -> dict:
    """
    Generate AI response to user input
    
    PROCESS:
    1. Detect emotion from user message
    2. Classify intent
    3. Retrieve relevant memories
    4. Generate personalized response
    5. Return response with metadata
    
    RETURNS:
    {
        "response": "AI response text",
        "emotion": "happy",
        "emotion_confidence": 0.95,
        "intent": "VENT",
        "crisis_detected": False,
        "metadata": {...}
    }
    """
    
    if st.session_state.service_ready:
        try:
            # Use conversation service
            result = st.session_state.conversation_service.process_text_message(user_input)
            return result
        
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return get_fallback_response(user_input)
    else:
        # Fallback if service not available
        return get_fallback_response(user_input)


def get_fallback_response(user_input: str) -> dict:
    """
    Fallback response if AI service unavailable
    
    WHY: Always provide some response, even if service fails
    
    STRATEGY:
    - Acknowledge user's message
    - Provide empathetic response
    - Encourage expression
    """
    
    # Simple keyword-based responses
    user_lower = user_input.lower()
    
    if any(word in user_lower for word in ['sad', 'depressed', 'down', 'unhappy']):
        response = "I hear that you're feeling down. That sounds really difficult. Would you like to tell me more about what's been happening?"
        emotion = "sadness"
    
    elif any(word in user_lower for word in ['anxious', 'worried', 'nervous', 'scared']):
        response = "It sounds like you're feeling anxious. Those feelings can be really overwhelming. What's been on your mind?"
        emotion = "fear"
    
    elif any(word in user_lower for word in ['angry', 'frustrated', 'annoyed', 'mad']):
        response = "I can sense your frustration. It's okay to feel angry. Would you like to talk about what's bothering you?"
        emotion = "anger"
    
    elif any(word in user_lower for word in ['happy', 'excited', 'great', 'wonderful', 'good']):
        response = "That's wonderful to hear! I'm glad you're feeling good. What's been going well for you?"
        emotion = "joy"
    
    else:
        response = "I'm listening. Tell me more about what's on your mind."
        emotion = "neutral"
    
    return {
        "response": response,
        "emotion": emotion,
        "emotion_confidence": 0.5,
        "intent": "VENT",
        "crisis_detected": any(word in user_lower for word in ['suicide', 'kill myself', 'want to die']),
        "metadata": {}
    }


def generate_welcome_message() -> str:
    """
    Generate personalized welcome message
    
    PERSONALIZATION:
    - User's name
    - Time of day
    - User's concerns (from profile)
    """
    
    name = st.session_state.user_profile.get('name', 'there')
    concerns = st.session_state.user_profile.get('concerns', [])
    
    base_message = f"Hello {name}! Welcome to MindSync AI. 🌟\n\n"
    
    if concerns:
        concern_text = ", ".join(concerns[:2])  # Mention first 2 concerns
        base_message += f"I understand you're interested in support with {concern_text}. "
    
    base_message += "I'm here to listen without judgment and provide support.\n\n"
    base_message += "How are you feeling today? What would you like to talk about?"
    
    return base_message


def save_conversation_to_memory(user_input: str, response_data: dict):
    """
    Save conversation to memory system
    
    WHY: Enables long-term personalization
    - Remember user preferences
    - Track mood patterns
    - Reference past conversations
    """
    
    if st.session_state.memory_system and st.session_state.user_id:
        try:
            memory = st.session_state.memory_system.get_user_memory(st.session_state.user_id)
            
            # Update conversation count
            memory['total_conversations'] = memory.get('total_conversations', 0) + 1
            
            # Add to conversation history
            if 'conversations' not in memory:
                memory['conversations'] = []
            
            memory['conversations'].append({
                'timestamp': datetime.now().isoformat(),
                'user_message': user_input,
                'ai_response': response_data['response'],
                'emotion': response_data.get('emotion'),
                'intent': response_data.get('intent')
            })
            
            # Keep only last 100 conversations
            memory['conversations'] = memory['conversations'][-100:]
            
            # Update memory
            st.session_state.memory_system.update_user_memory(
                st.session_state.user_id,
                memory
            )
        
        except Exception as e:
            # Don't break chat if memory fails
            st.warning(f"Could not save to memory: {str(e)}")


# ============================================================================
# CHAT SIDEBAR TOOLS
# ============================================================================

def display_chat_sidebar():
    """
    Sidebar with chat utilities
    
    FEATURES:
    - Clear conversation
    - Export chat
    - Mood check-in
    - Quick actions
    """
    
    with st.sidebar:
        st.markdown("### Chat Tools")
        
        # Mood check-in
        with st.expander("😊 Quick Mood Check"):
            mood = st.select_slider(
                "How are you feeling right now?",
                options=["Very Bad", "Bad", "Okay", "Good", "Great"],
                value="Okay",
                label_visibility="collapsed"
            )
            
            if st.button("Log Mood", use_container_width=True):
                log_mood(mood)
                st.success("Mood logged!")
        
        # Conversation management
        st.markdown("---")
        st.markdown("### Conversation")
        
        # Message count
        msg_count = len([m for m in st.session_state.messages if m['role'] == 'user'])
        st.metric("Messages", msg_count)
        
        # Export conversation
        if st.button("📥 Export Chat", use_container_width=True):
            export_conversation()
        
        # Clear conversation
        if st.button("🗑️ Clear Chat", use_container_width=True):
            if st.session_state.messages:
                st.session_state.messages = []
                st.rerun()
        
        # Emergency resources
        st.markdown("---")
        st.markdown("### Need Immediate Help?")
        
        if st.button("🚨 Crisis Resources", use_container_width=True, type="primary"):
            st.session_state.crisis_mode = True
            st.rerun()


def log_mood(mood: str):
    """
    Log user's current mood
    
    WHY: Track mood over time for insights
    """
    
    if st.session_state.memory_system and st.session_state.user_id:
        try:
            memory = st.session_state.memory_system.get_user_memory(st.session_state.user_id)
            
            if 'mood_logs' not in memory:
                memory['mood_logs'] = []
            
            memory['mood_logs'].append({
                'timestamp': datetime.now().isoformat(),
                'mood': mood
            })
            
            # Keep only last 90 days
            memory['mood_logs'] = memory['mood_logs'][-90:]
            
            st.session_state.memory_system.update_user_memory(
                st.session_state.user_id,
                memory
            )
        
        except Exception as e:
            st.error(f"Could not log mood: {str(e)}")


def export_conversation():
    """
    Export chat history as text file
    
    WHY: Users may want to save conversations
    """
    
    if not st.session_state.messages:
        st.warning("No messages to export")
        return
    
    # Format conversation
    text = "MindSync AI Conversation Export\n"
    text += f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    text += "=" * 50 + "\n\n"
    
    for msg in st.session_state.messages:
        role = "You" if msg["role"] == "user" else "MindSync AI"
        timestamp = msg.get("timestamp", "")
        content = msg["content"]
        
        text += f"[{timestamp}] {role}:\n{content}\n\n"
    
    # Provide download button
    st.download_button(
        label="Download Conversation",
        data=text,
        file_name=f"mindsync_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )