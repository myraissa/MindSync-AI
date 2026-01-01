# src/models/intent_classifier.py

import joblib
from pathlib import Path
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class IntentClassifier:
    """
    Classify user intent from text
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
        'SMALL_TALK'         # Casual conversation
    ]
    
    # Crisis keywords (CRITICAL!)
    CRISIS_KEYWORDS = [
        # English
        'suicide', 'kill myself', 'end my life', 'want to die',
        'self-harm', 'hurt myself', 'cut myself',
        'no reason to live', 'better off dead',
        
        # French
        'suicide', 'me tuer', 'mourir', 'mort',
        'plus vivre', 'finir ma vie',
        
        # Arabic/Tunisian
        'نحب نموت', 'suicide', 'ma3adch 7abba el 7ayét',
        '7abbeit nموت', 'نقتل روحي'
    ]
    
    def __init__(self, model_path='models/intent_classifier/intent_model.pkl'):
        """
        Initialize intent classifier
        
        Args:
            model_path: Path to trained model file
        """
        self.model_path = Path(model_path)
        
        try:
            if self.model_path.exists():
                self.model = joblib.load(self.model_path)
                logger.info(f"✅ Intent classifier loaded from {self.model_path}")
            else:
                logger.warning(f"⚠️ Intent model not found at {self.model_path}")
                logger.info("Using rule-based classification")
                self.model = None
                
        except Exception as e:
            logger.error(f"Error loading intent model: {e}")
            self.model = None
    
    def predict(self, text: str) -> Dict:
        """
        Predict intent from text
        
        Args:
            text: Input text
            
        Returns:
            dict with keys:
                - intent: predicted intent
                - confidence: confidence score
                - crisis_detected: boolean flag
        """
        # ALWAYS check for crisis first!
        text_lower = text.lower()
        crisis_detected = self._detect_crisis(text_lower)
        
        if crisis_detected:
            return {
                'intent': 'CRISIS',
                'confidence': 1.0,
                'crisis_detected': True
            }
        
        # Use model if available
        if self.model is not None:
            try:
                intent = self.model.predict([text])[0]
                
                # Get confidence if available
                try:
                    proba = self.model.predict_proba([text])[0]
                    confidence = float(max(proba))
                except:
                    confidence = 0.75
                
                return {
                    'intent': intent,
                    'confidence': confidence,
                    'crisis_detected': False
                }
            
            except Exception as e:
                logger.error(f"Error predicting with model: {e}")
        
        # Fallback to rule-based
        return self._rule_based_prediction(text)
    
    def _detect_crisis(self, text_lower: str) -> bool:
        """
        Detect crisis keywords
        
        Args:
            text_lower: Lowercased text
            
        Returns:
            True if crisis detected
        """
        return any(keyword in text_lower for keyword in self.CRISIS_KEYWORDS)
    
    def _rule_based_prediction(self, text: str) -> Dict:
        """
        Simple rule-based intent classification
        
        Args:
            text: Input text
            
        Returns:
            Prediction dict
        """
        text_lower = text.lower()
        
        # Question words → seeking advice
        if any(word in text_lower for word in ['how', 'what', 'why', 'chnouwa', 'kifech', 'comment']):
            if any(word in text_lower for word in ['help', 'advice', 'tips', 'should', 'suggest']):
                return {'intent': 'SEEK_ADVICE', 'confidence': 0.7, 'crisis_detected': False}
        
        # Symptom reporting
        if any(word in text_lower for word in ['cant sleep', 'insomnia', 'anxiety', 'depression', 'panic', 'ma najmitch']):
            return {'intent': 'REPORT_SYMPTOM', 'confidence': 0.75, 'crisis_detected': False}
        
        # Achievements
        if any(word in text_lower for word in ['achieved', 'succeeded', 'happy', 'proud', 'mabrouk', 'fer7an']):
            return {'intent': 'SHARE_ACHIEVEMENT', 'confidence': 0.7, 'crisis_detected': False}
        
        # Gratitude
        if any(word in text_lower for word in ['thank', 'thanks', 'grateful', 'merci', 'yaatik']):
            return {'intent': 'GRATITUDE', 'confidence': 0.8, 'crisis_detected': False}
        
        # Default: venting
        return {'intent': 'VENT', 'confidence': 0.6, 'crisis_detected': False}
