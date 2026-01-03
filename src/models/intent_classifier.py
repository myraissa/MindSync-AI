import re
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class IntentClassifier:
    """
    Classify user intent from text (Rule-based - no model required)
    Much more reliable than trying to load custom trained models
    """
    
    # Define intents
    INTENTS = [
        'VENT',              # User wants to talk
        'SEEK_ADVICE',       # Asking for advice
        'REPORT_SYMPTOM',    # Reporting mental health symptoms
        'CRISIS',            # Emergency/crisis situation
        'CHECK_IN',          # Daily check-in
        'SHARE_ACHIEVEMENT', # Sharing good news
        'GRATITUDE',         # Expressing thanks
        'SMALL_TALK',        # Casual conversation
        'GENERAL'            # Default
    ]
    
    def __init__(self, model_path=None):
        """
        Initialize intent classifier
        No model loading needed - uses rule-based matching
        """
        print("✅ Intent classifier loaded (rule-based)")
        
        # Crisis keywords (CRITICAL - multiple languages)
        self.crisis_keywords = [
            # English - Suicide
            'suicide', 'kill myself', 'end my life', 'want to die',
            'better off dead', 'no reason to live', 'ending it all',
            'take my own life', 'can\'t go on', 'don\'t want to be here',
            
            # English - Self-harm
            'self-harm', 'hurt myself', 'cut myself', 'cutting myself',
            'harm myself', 'self harm', 'selfharm',
            
            # French
            'suicide', 'me suicider', 'me tuer', 'mourir', 'fin de ma vie',
            'plus envie de vivre', 'me faire du mal',
            
            # Tunisian Arabic (transliterated)
            'n7eb nmout', 'besh nmout', 'nkhamem fel mawt',
        ]
        
        # Advice-seeking patterns
        self.advice_patterns = [
            r'what should i',
            r'how can i',
            r'how do i',
            r'can you help me',
            r'i need advice',
            r'what would you',
            r'what do you think',
            r'should i',
            r'chnou n3amel',  # Tunisian: what should I do
            r'kifeh',  # Tunisian: how
        ]
        
        # Symptom reporting patterns
        self.symptom_patterns = [
            r'i feel',
            r'i\'m feeling',
            r'i have been',
            r'i\'ve been',
            r'having trouble',
            r'can\'t sleep',
            r'losing interest',
            r'no energy',
            r'n7es bi',  # Tunisian: I feel
            r'3andi',  # Tunisian: I have
        ]
        
        # Achievement patterns
        self.achievement_patterns = [
            r'i did it',
            r'i finally',
            r'i managed to',
            r'i accomplished',
            r'i succeeded',
            r'i\'m proud',
            r'good news',
            r'great news',
            r'3malt',  # Tunisian: I did
            r'njem',  # Tunisian: succeeded
        ]
        
        # Gratitude patterns
        self.gratitude_patterns = [
            r'thank you',
            r'thanks',
            r'grateful',
            r'appreciate',
            r'merci',
            r'yesalmek',  # Tunisian
        ]
    
    def predict(self, text: str) -> Dict:
        """
        Predict user intent from text
        
        Returns:
        {
            'intent': 'CRISIS',
            'confidence': 0.95,
            'is_urgent': True
        }
        """
        text_lower = text.lower()
        
        # 1. CRISIS DETECTION (highest priority)
        if self._detect_crisis(text_lower):
            return {
                'intent': 'CRISIS',
                'confidence': 0.95,
                'is_urgent': True
            }
        
        # 2. GRATITUDE
        if self._matches_patterns(text_lower, self.gratitude_patterns):
            return {
                'intent': 'GRATITUDE',
                'confidence': 0.85,
                'is_urgent': False
            }
        
        # 3. ACHIEVEMENT SHARING
        if self._matches_patterns(text_lower, self.achievement_patterns):
            return {
                'intent': 'SHARE_ACHIEVEMENT',
                'confidence': 0.80,
                'is_urgent': False
            }
        
        # 4. ADVICE SEEKING
        if self._matches_patterns(text_lower, self.advice_patterns):
            return {
                'intent': 'SEEK_ADVICE',
                'confidence': 0.75,
                'is_urgent': False
            }
        
        # 5. SYMPTOM REPORTING
        if self._matches_patterns(text_lower, self.symptom_patterns):
            return {
                'intent': 'REPORT_SYMPTOM',
                'confidence': 0.70,
                'is_urgent': False
            }
        
        # 6. CHECK-IN (greetings)
        if self._is_greeting(text_lower):
            return {
                'intent': 'CHECK_IN',
                'confidence': 0.80,
                'is_urgent': False
            }
        
        # 7. SMALL TALK
        if self._is_small_talk(text_lower):
            return {
                'intent': 'SMALL_TALK',
                'confidence': 0.70,
                'is_urgent': False
            }
        
        # 8. VENTING (default for emotional expression)
        if len(text.split()) > 15:  # Longer messages often are venting
            return {
                'intent': 'VENT',
                'confidence': 0.65,
                'is_urgent': False
            }
        
        # 9. GENERAL (fallback)
        return {
            'intent': 'GENERAL',
            'confidence': 0.60,
            'is_urgent': False
        }
    
    def _detect_crisis(self, text: str) -> bool:
        """
        Detect crisis keywords (suicide, self-harm)
        """
        for keyword in self.crisis_keywords:
            if keyword in text:
                logger.warning(f"🚨 CRISIS KEYWORD DETECTED: {keyword}")
                return True
        return False
    
    def _matches_patterns(self, text: str, patterns: List[str]) -> bool:
        """
        Check if text matches any of the given regex patterns
        """
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _is_greeting(self, text: str) -> bool:
        """
        Detect greeting messages
        """
        greetings = [
            'hi', 'hello', 'hey', 'good morning', 'good afternoon',
            'good evening', 'bonjour', 'salut', 'coucou',
            'ahla', 'salam', 'labess', 'chbik'  # Tunisian
        ]
        
        # Check if text starts with greeting or is short greeting
        text_words = text.split()
        if len(text_words) <= 3:
            return any(greeting in text for greeting in greetings)
        
        return any(text.startswith(greeting) for greeting in greetings)
    
    def _is_small_talk(self, text: str) -> bool:
        """
        Detect small talk (weather, general questions)
        """
        small_talk_keywords = [
            'weather', 'how are you', 'what\'s up', 'whats up',
            'how\'s it going', 'comment ça va', 'ça va',
            'labess', 'chneya'  # Tunisian
        ]
        
        return any(keyword in text for keyword in small_talk_keywords)


# Test function
if __name__ == "__main__":
    print("🧪 Testing Intent Classifier\n")
    
    classifier = IntentClassifier()
    
    test_texts = [
        "I'm thinking about ending my life",
        "How can I deal with my anxiety?",
        "I feel really depressed lately",
        "I finally got the job!",
        "Thank you so much for your help",
        "Hi, how are you?",
        "What's the weather like?",
        "I just need to talk to someone"
    ]
    
    for text in test_texts:
        result = classifier.predict(text)
        urgency = "⚠️ URGENT" if result.get('is_urgent') else "✅ Normal"
        print(f"Text: '{text}'")
        print(f"Intent: {result['intent']} ({result['confidence']:.2%}) - {urgency}")
        print()