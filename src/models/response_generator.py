import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

class RealAdviceResponseGenerator:
    """
    Generate AUTHENTIC, HONEST responses that give REAL advice
    Not just validation - actual guidance like a true friend
    """
    
    def __init__(self):
        self.hf_token = os.getenv('HUGGINGFACE_TOKEN') or os.getenv('HUGGINGFACE_API_KEY')
        if not self.hf_token:
            print("⚠️ Warning: HUGGINGFACE_TOKEN not set")
        else:
            print("✅ HuggingFace API loaded")
        
        self.api_url = "https://router.huggingface.co/v1/chat/completions"
        
        # NEW SYSTEM PROMPT - AUTHENTIC & HONEST
        self.system_prompt = """You are MindSync, a genuinely caring AI companion who gives REAL advice.

Your Philosophy:
🎯 BE HONEST, NOT JUST NICE
- If someone is making bad choices, gently point it out
- Don't validate toxic behavior or unhealthy patterns
- Give advice you'd give your best friend
- Care enough to tell the truth, even when it's uncomfortable

🫂 AUTHENTIC EMPATHY
- Validate feelings, but challenge harmful thinking
- "I hear you're hurting, AND I'm worried about this pattern..."
- Be supportive but don't enable destructive behavior

💡 PRACTICAL WISDOM
- Give concrete, actionable advice
- Share healthy coping strategies
- Suggest professional help when needed
- Call out self-sabotage with compassion

🚨 DETECT RED FLAGS
- Toxic relationships → "This doesn't sound healthy..."
- Self-destructive patterns → "I'm concerned about..."
- Avoidance → "Running from this won't help..."
- Victim mentality → "What can YOU control here?"

Examples:
❌ BAD: "It's totally okay that you screamed at your mom. Your feelings are valid!"
✅ GOOD: "I hear you were frustrated, but yelling at your mom isn't okay. Let's find healthier ways to express anger."

❌ BAD: "Skipping classes is fine if you need mental health days!"
✅ GOOD: "Mental health matters, but avoiding responsibilities long-term will hurt you more. Let's create a sustainable plan."

Response Style:
- 2-4 sentences max
- Warm but honest
- End with actionable question or suggestion
- Use emojis naturally (💙 🤔 💪)

Crisis Detection:
If user mentions: suicide, self-harm, violence
→ Provide crisis hotlines immediately:
- Tunisia: 80 101 080
- International: 116 123

Remember: True care means honesty + support."""

    def generate(self, 
                 emotion: str,
                 intent: str,
                 user_input: str,
                 context: List[Dict],
                 user_memory: Optional[Dict] = None) -> str:
        """
        Generate REAL advice response with memory integration
        """
        
        # Crisis handling
        if intent == 'CRISIS':
            return self._crisis_response()
        
        # Build enriched context with memory
        conversation_history = self._build_context_with_memory(context, user_memory)
        
        # Detect unhealthy patterns
        pattern_context = self._detect_patterns(context, user_memory)
        
        if self.hf_token:
            try:
                return self._generate_chat_completion(
                    user_input, 
                    emotion, 
                    conversation_history,
                    pattern_context
                )
            except Exception as e:
                print(f"⚠️ API failed: {e}")
        
        return self._fallback_response(emotion, pattern_context)
    
    def _detect_patterns(self, context: List[Dict], user_memory: Optional[Dict]) -> str:
        """
        Detect unhealthy patterns from history
        """
        if not user_memory:
            return ""
        
        patterns = []
        
        # Check for repeated negative themes
        if user_memory.get('conversation_count', 0) > 3:
            emotion_history = user_memory.get('emotion_history', [])
            
            # Too much sadness?
            sadness_count = emotion_history.count('sadness')
            if sadness_count > len(emotion_history) * 0.6:
                patterns.append("PATTERN: Persistent sadness over multiple conversations")
            
            # Repeated anger?
            anger_count = emotion_history.count('anger')
            if anger_count > len(emotion_history) * 0.5:
                patterns.append("PATTERN: Frequent anger - possible unresolved issues")
            
            # Check for avoidance
            recent_topics = user_memory.get('topics_discussed', [])
            if any('avoid' in topic.lower() or 'skip' in topic.lower() for topic in recent_topics[-3:]):
                patterns.append("PATTERN: Possible avoidance behavior")
        
        if patterns:
            return "DETECTED PATTERNS:\n" + "\n".join(patterns) + "\n\n"
        return ""
    
    def _build_context_with_memory(self, context: List[Dict], user_memory: Optional[Dict]) -> str:
        """
        Build rich context including user memory
        """
        context_parts = []
        
        # User background from memory
        if user_memory:
            context_parts.append("=== USER BACKGROUND ===")
            if user_memory.get('name'):
                context_parts.append(f"Name: {user_memory['name']}")
            if user_memory.get('age'):
                context_parts.append(f"Age: {user_memory['age']}")
            if user_memory.get('concerns'):
                context_parts.append(f"Main concerns: {', '.join(user_memory['concerns'])}")
            if user_memory.get('goals'):
                context_parts.append(f"Goals: {', '.join(user_memory['goals'])}")
            context_parts.append("")
        
        # Recent conversation
        if context:
            context_parts.append("=== RECENT CONVERSATION ===")
            recent = context[-3:] if len(context) > 3 else context
            for msg in recent:
                role = "User" if msg['role'] == 'user' else "MindSync"
                content = msg['content'][:150]
                context_parts.append(f"{role}: {content}")
            context_parts.append("")
        
        return "\n".join(context_parts) if context_parts else "First conversation"
    
    def _generate_chat_completion(self, user_input: str, emotion: str, 
                                  context: str, pattern_context: str) -> str:
        """
        Call HuggingFace API with enhanced prompt
        """
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": f"""{context}

{pattern_context}

Current emotion: {emotion}
User message: "{user_input}"

Respond as MindSync with honest, caring advice (2-4 sentences):"""
            }
        ]
        
        payload = {
            "model": "meta-llama/Llama-3.1-8B-Instruct",
            "messages": messages,
            "max_tokens": 300,
            "temperature": 0.9,
            "top_p": 0.95,
            "stream": False
        }
        
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if not response.ok:
            raise Exception(f"API error {response.status_code}")
        
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0]["message"]["content"]
            return self._clean_response(message)
        
        raise Exception("Invalid response format")
    
    def _clean_response(self, text: str) -> str:
        """Clean up model output"""
        text = text.strip()
        
        # Remove role prefixes
        for prefix in ["MindSync:", "Assistant:", "AI:"]:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
        
        # Limit to 4 sentences
        sentences = [s.strip() for s in text.split('. ') if s.strip()]
        if len(sentences) > 4:
            sentences = sentences[:4]
        
        result = '. '.join(sentences)
        if not result.endswith(('.', '?', '!')):
            result += '.'
        
        return result
    
    def _crisis_response(self) -> str:
        """Crisis response"""
        return """🚨 I'm really worried about what you're sharing. Your life matters, and you deserve help.

**PLEASE call right now:**
- 🇹🇳 Tunisia: **80 101 080** (SOS Help)
- 🌍 International: **116 123** (Samaritans)

These people care and are trained to help. Will you call one of these numbers? I'll stay here with you, but professional help is crucial right now. 💙"""
    
    def _fallback_response(self, emotion: str, pattern_context: str) -> str:
        """Fallback responses with pattern awareness"""
        
        if pattern_context:
            return f"I've noticed a pattern: you've been feeling {emotion} quite often. This might be worth exploring deeper - maybe with a counselor? What do you think is at the root of this? 💙"
        
        responses = {
            'joy': "That's wonderful! 😊 Let's celebrate this moment. What made this happen, and how can you create more of these experiences?",
            
            'sadness': "I hear your sadness, and that's valid. 💙 But let's not just sit with it - what's one small thing you could do today to care for yourself? Even tiny steps matter.",
            
            'anger': "I can feel your frustration. 😤 Anger often tells us something's wrong. Instead of just venting, let's figure out what you can actually change here. What's in your control?",
            
            'fear': "Fear is real, but it doesn't define you. 💪 Let's break this down: what's the worst case scenario, and what's more likely? What's one brave step you could take?",
            
            'neutral': "I'm here for you. 💙 Sometimes the hardest part is just starting to talk. What's really on your mind today?"
        }
        
        return responses.get(emotion, 
            "I'm listening. 💙 Tell me what's really going on - the good, the bad, all of it. I can handle it.")