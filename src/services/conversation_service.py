"""
Enhanced Conversation Service with Memory Integration
Combines emotion detection, intent classification, memory system, and real advice generation
"""

from pathlib import Path
import sys
from typing import Optional
# Add parent directory to path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.models.emotion_detector import EmotionDetector
from src.models.intent_classifier import IntentClassifier

# Import new components
try:
    from src.services.memory_system import UserMemorySystem
    MEMORY_AVAILABLE = True
except:
    MEMORY_AVAILABLE = False
    print("⚠️ Memory system not available")

try:
    from src.models.response_generator import RealAdviceResponseGenerator
    ENHANCED_GENERATOR_AVAILABLE = True
except:
    ENHANCED_GENERATOR_AVAILABLE = False
    print("⚠️ Enhanced response generator not available, using fallback")

# Fallback to original if enhanced not available
if not ENHANCED_GENERATOR_AVAILABLE:
    try:
        from src.models.response_generator import RealAdviceResponseGenerator as ResponseGenerator
    except:
        ResponseGenerator = None


class EnhancedConversationService:
    """
    Complete conversation service with memory and real advice
    """
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        
        print(f"🚀 Initializing Enhanced Conversation Service for user: {user_id}")
        
        # Core components
        try:
            self.emotion_detector = EmotionDetector()
            print("✅ Emotion detector loaded")
        except Exception as e:
            print(f"⚠️ Emotion detector failed: {e}")
            self.emotion_detector = None
        
        try:
            self.intent_classifier = IntentClassifier()
            print("✅ Intent classifier loaded")
        except Exception as e:
            print(f"⚠️ Intent classifier failed: {e}")
            self.intent_classifier = None
        
        # Memory system
        if MEMORY_AVAILABLE:
            try:
                self.memory_system = UserMemorySystem()
                print("✅ Memory system loaded")
            except Exception as e:
                print(f"⚠️ Memory system failed: {e}")
                self.memory_system = None
        else:
            self.memory_system = None
        
        # Response generator
        if ENHANCED_GENERATOR_AVAILABLE:
            try:
                self.response_generator = RealAdviceResponseGenerator()
                print("✅ Enhanced response generator loaded (REAL ADVICE MODE)")
            except Exception as e:
                print(f"⚠️ Enhanced generator failed: {e}")
                self.response_generator = None
        elif ResponseGenerator:
            try:
                self.response_generator = ResponseGenerator()
                print("✅ Standard response generator loaded")
            except Exception as e:
                print(f"⚠️ Standard generator failed: {e}")
                self.response_generator = None
        else:
            self.response_generator = None
        
        print("=" * 50)
        print("🧠 MindSync AI Ready!")
        print(f"   - Emotion Detection: {'✅' if self.emotion_detector else '❌'}")
        print(f"   - Intent Classification: {'✅' if self.intent_classifier else '❌'}")
        print(f"   - Memory System: {'✅' if self.memory_system else '❌'}")
        print(f"   - Real Advice: {'✅' if ENHANCED_GENERATOR_AVAILABLE else '❌'}")
        print("=" * 50)
    
    def process_text_message(self, user_input: str, conversation_history: Optional[list] = None) -> dict:
        """
        Process user message with full pipeline:
        1. Detect emotion
        2. Classify intent
        3. Load user memory
        4. Generate response with context
        5. Update memory
        
        Returns:
        {
            'response': str,
            'detected_emotion': str,
            'emotion_confidence': float,
            'intent': str,
            'intent_confidence': float,
            'crisis_detected': bool,
            'all_emotion_scores': dict,
            'memory_updated': bool
        }
        """
        
        if conversation_history is None:
            conversation_history = []
        
        # Step 1: Emotion Detection
        if self.emotion_detector:
            try:
                emotion_result = self.emotion_detector.predict(user_input)
                detected_emotion = emotion_result['emotion']
                emotion_confidence = emotion_result['confidence']
                all_emotion_scores = emotion_result.get('all_scores', {})
            except Exception as e:
                print(f"⚠️ Emotion detection failed: {e}")
                detected_emotion = 'neutral'
                emotion_confidence = 0.5
                all_emotion_scores = {}
        else:
            detected_emotion = 'neutral'
            emotion_confidence = 0.5
            all_emotion_scores = {}
        
        # Step 2: Intent Classification
        if self.intent_classifier:
            try:
                intent_result = self.intent_classifier.predict(user_input)
                detected_intent = intent_result['intent']
                intent_confidence = intent_result['confidence']
            except Exception as e:
                print(f"⚠️ Intent classification failed: {e}")
                detected_intent = 'GENERAL'
                intent_confidence = 0.5
        else:
            detected_intent = 'GENERAL'
            intent_confidence = 0.5
        
        # Step 3: Load User Memory
        user_memory = None
        if self.memory_system:
            try:
                user_memory = self.memory_system.get_user_memory(self.user_id)
            except Exception as e:
                print(f"⚠️ Memory load failed: {e}")
        
        # Step 4: Generate Response
        if self.response_generator:
            try:
                # Check if enhanced generator (has memory parameter)
                if ENHANCED_GENERATOR_AVAILABLE:
                    response_text = self.response_generator.generate(
                        emotion=detected_emotion,
                        intent=detected_intent,
                        user_input=user_input,
                        context=conversation_history,
                        user_memory=user_memory  # NEW: Pass memory
                    )
                else:
                    # Standard generator (no memory parameter)
                    response_text = self.response_generator.generate(
                        emotion=detected_emotion,
                        intent=detected_intent,
                        user_input=user_input,
                        context=conversation_history
                    )
            except Exception as e:
                print(f"⚠️ Response generation failed: {e}")
                response_text = self._fallback_response(detected_emotion)
        else:
            response_text = self._fallback_response(detected_emotion)
        
        # Step 5: Update Memory
        memory_updated = False
        if self.memory_system:
            try:
                # Extract information from conversation
                memory_updates = self.memory_system.extract_info_from_conversation(
                    user_input=user_input,
                    emotion=detected_emotion,
                    intent=detected_intent
                )
                
                # Increment conversation count
                current_memory = self.memory_system.get_user_memory(self.user_id)
                memory_updates['conversation_count'] = current_memory.get('conversation_count', 0) + 1
                
                # Update memory
                self.memory_system.update_memory(self.user_id, memory_updates)
                memory_updated = True
                
                print(f"💾 Memory updated for {self.user_id}")
                
            except Exception as e:
                print(f"⚠️ Memory update failed: {e}")
        
        # Return comprehensive result
        return {
            'response': response_text,
            'detected_emotion': detected_emotion,
            'emotion_confidence': emotion_confidence,
            'intent': detected_intent,
            'intent_confidence': intent_confidence,
            'crisis_detected': detected_intent == 'CRISIS',
            'all_emotion_scores': all_emotion_scores,
            'memory_updated': memory_updated
        }
    
    def _fallback_response(self, emotion: str) -> str:
        """
        Simple fallback responses if all else fails
        """
        responses = {
            'joy': "I'm so happy to hear that! 😊 Tell me more about what's making you feel good!",
            'sadness': "I hear you, and I'm here for you. 💙 Sometimes we just need someone to listen. Want to talk about it?",
            'anger': "I can sense your frustration. 😤 Let's work through this together. What's bothering you?",
            'fear': "It's okay to feel worried. 🤗 I'm here to help. What's on your mind?",
            'surprise': "That sounds unexpected! 😮 Tell me more!",
            'neutral': "I'm listening. 💭 How are you really feeling today?",
        }
        
        return responses.get(emotion, "I'm here for you. Tell me what's on your mind. 💙")
    
    def get_memory_summary(self) -> str:
        """
        Get a summary of user's memory
        """
        if self.memory_system:
            try:
                return self.memory_system.get_memory_summary(self.user_id)
            except Exception as e:
                print(f"⚠️ Memory summary failed: {e}")
        
        return "Memory not available"
    
    def analyze_user_patterns(self) -> dict:
        """
        Analyze user's emotional patterns
        """
        if self.memory_system:
            try:
                return self.memory_system.analyze_patterns(self.user_id)
            except Exception as e:
                print(f"⚠️ Pattern analysis failed: {e}")
        
        return {
            'most_common_emotion': None,
            'emotion_counts': {},
            'total_conversations': 0,
            'needs_professional_help': False
        }


# Test function
if __name__ == "__main__":
    print("🧪 Testing Enhanced Conversation Service...")
    
    service = EnhancedConversationService(user_id="test_user")
    
    # Test conversation
    test_messages = [
        "Hi, my name is Alex and I'm feeling really anxious about my exams",
        "I've been skipping classes because I'm too stressed",
        "Yeah, I know it's not helping but I just can't face going"
    ]
    
    conversation_history = []
    
    for msg in test_messages:
        print(f"\n{'='*50}")
        print(f"USER: {msg}")
        print(f"{'='*50}")
        
        result = service.process_text_message(msg, conversation_history)
        
        print(f"\n🤖 MINDSYNC: {result['response']}")
        print(f"\n📊 Analysis:")
        print(f"   Emotion: {result['detected_emotion']} ({result['emotion_confidence']:.2f})")
        print(f"   Intent: {result['intent']} ({result['intent_confidence']:.2f})")
        print(f"   Crisis: {'⚠️ YES' if result['crisis_detected'] else '✅ No'}")
        print(f"   Memory Updated: {'✅' if result['memory_updated'] else '❌'}")
        
        # Add to history
        conversation_history.append({'role': 'user', 'content': msg})
        conversation_history.append({'role': 'assistant', 'content': result['response']})
    
    # Show memory summary
    print(f"\n{'='*50}")
    print("📝 MEMORY SUMMARY")
    print(f"{'='*50}")
    print(service.get_memory_summary())
    
    # Show patterns
    print(f"\n{'='*50}")
    print("📊 PATTERN ANALYSIS")
    print(f"{'='*50}")
    patterns = service.analyze_user_patterns()
    for key, value in patterns.items():
        print(f"   {key}: {value}")