# src/models/emotion_detector.py

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from pathlib import Path
import traceback
from typing import List, Dict, Any, Optional, cast
class EmotionDetector:
    """
    Detect emotions from text using pre-trained models
    """
    
    def __init__(self, model_name='bhadresh-savani/distilbert-base-uncased-emotion'):
        """
        Initialize with a pre-trained emotion detection model
        
        Default: 'bhadresh-savani/distilbert-base-uncased-emotion'
        - Trained on GoEmotions dataset
        - Detects 6 emotions: sadness, joy, love, anger, fear, surprise
        
        Alternative models:
        - 'j-hartmann/emotion-english-distilroberta-base' (7 emotions)
        - 'SamLowe/roberta-base-go_emotions' (27 emotions)
        """
        self.model_name = model_name
        
        # Standard emotion labels (will be mapped from model output)
        self.emotions = ['joy', 'sadness', 'anger', 'fear', 
                        'surprise', 'love', 'neutral']
        
        try:
            print(f"🔄 Loading emotion detector: {model_name}")
            
            # Use transformers pipeline for easier inference
            self.classifier = pipeline(
                "text-classification", 
                model=model_name,
                top_k=None  # Return all scores
            )
            
            print(f"✅ Emotion detector loaded successfully")
            self.fallback_mode = False
            
        except Exception as e:
            print(f"⚠️ Error loading emotion detector: {e}")
            print(f"📝 Falling back to rule-based detection")
            self.classifier = None
            self.fallback_mode = True
    
    def predict(self, text: str) -> dict:
        """
        Predict emotion from text
        
        Returns:
        {
            'emotion': 'sadness',
            'confidence': 0.89,
            'all_scores': {'joy': 0.05, 'sadness': 0.89, ...}
        }
        """
        
        # Use fallback if model failed to load
        if self.fallback_mode or self.classifier is None:
            return self._fallback_predict(text)
        
        try:
            # Get predictions from model
            results = cast(List[Dict[str, Any]], self.classifier(text)[0])
            # Convert to our standard format
            all_scores = {}
            for item in results:
                
                emotion = item['label'].lower()
                score = item['score']
                
                # Map model labels to our standard emotions
                emotion = self._map_emotion(emotion)
                all_scores[emotion] = score
            
            # Ensure all our standard emotions have scores
            for emotion in self.emotions:
                if emotion not in all_scores:
                    all_scores[emotion] = 0.0
            
            # Get top emotion
            detected_emotion = max(all_scores.keys(), key=lambda k: all_scores[k])
            confidence = all_scores[detected_emotion]
            
            return {
                'emotion': detected_emotion,
                'confidence': float(confidence),
                'all_scores': all_scores
            }
            
        except Exception as e:
            print(f"⚠️ Prediction error: {e}")
            return self._fallback_predict(text)
    
    def _map_emotion(self, model_emotion: str) -> str:
        """
        Map model's emotion labels to our standard labels
        """
        emotion_mapping = {
            # Standard mappings
            'joy': 'joy',
            'sadness': 'sadness',
            'anger': 'anger',
            'fear': 'fear',
            'surprise': 'surprise',
            'love': 'love',
            'neutral': 'neutral',
            
            # Alternative mappings
            'happiness': 'joy',
            'happy': 'joy',
            'sad': 'sadness',
            'angry': 'anger',
            'scared': 'fear',
            'surprised': 'surprise',
            'disgust': 'anger',  # Map disgust to anger
            'trust': 'love',  # Map trust to love
            'anticipation': 'neutral',  # Map anticipation to neutral
        }
        
        return emotion_mapping.get(model_emotion.lower(), 'neutral')
    
    def _fallback_predict(self, text: str) -> dict:
        """
        Simple rule-based emotion detection (fallback)
        Works for English, French, and Arabic (Tunisian dialect)
        """
        text_lower = text.lower()
        
        # Enhanced keyword matching with multi-language support
        emotion_keywords = {
            'joy': [
                # English
                'happy', 'glad', 'excited', 'joy', 'great', 'wonderful', 
                'amazing', 'love', 'excellent', 'fantastic', 'good',
                # French
                'heureux', 'content', 'joyeux', 'super', 'génial',
                # Tunisian Arabic (transliterated)
                'fer7an', 'mabsout', 'fre7', 'behi'
            ],
            'sadness': [
                # English
                'sad', 'depressed', 'down', 'unhappy', 'crying', 'miserable',
                'lonely', 'hurt', 'disappointed', 'upset',
                # French
                'triste', 'déprimé', 'seul', 'malheureux', 'déçu',
                # Tunisian Arabic
                '7azin', 'mfajja3', 'wa7di', 'mahzouz'
            ],
            'anger': [
                # English
                'angry', 'mad', 'furious', 'annoyed', 'frustrated', 'hate',
                'irritated', 'pissed', 'outraged',
                # French
                'en colère', 'fâché', 'énervé', 'furieux',
                # Tunisian Arabic
                'mte3aseb', 'ghathban', 'za3foun'
            ],
            'fear': [
                # English
                'scared', 'afraid', 'worried', 'anxious', 'nervous', 'terrified',
                'panic', 'stressed', 'frightened',
                # French
                'peur', 'anxieux', 'inquiet', 'stressé', 'effrayé',
                # Tunisian Arabic
                'kha2ef', 'mkhawa', 'stress'
            ],
            'surprise': [
                # English
                'surprised', 'shocked', 'amazed', 'wow', 'unexpected',
                'astonished', 'stunned',
                # French
                'surpris', 'étonné', 'choqué',
                # Tunisian Arabic
                'metshajem', '3jib'
            ],
            'love': [
                # English
                'love', 'adore', 'cherish', 'care', 'affection',
                # French
                'amour', 'aimer', 'adorer',
                # Tunisian Arabic
                '7obbi', 'n7eb'
            ]
        }
        
        # Count keyword matches
        scores = {}
        for emotion, keywords in emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            scores[emotion] = count / len(keywords) if keywords else 0.0
        
        # Add neutral score
        scores['neutral'] = 0.3  # Base neutral score
        
        # Get best match
        if max(scores.values()) < 0.05:  # Very low confidence
            detected_emotion = 'neutral'
            confidence = 0.5
        else:
            detected_emotion = max(scores.keys(), key=lambda k: scores[k])
            # Normalize confidence
            raw_score = scores[detected_emotion]
            confidence = min(raw_score * 3 + 0.4, 0.95)  # Scale to 0.4-0.95
        
        return {
            'emotion': detected_emotion,
            'confidence': confidence,
            'all_scores': scores
        }


# Test function
if __name__ == "__main__":
    print("🧪 Testing Emotion Detector\n")
    
    detector = EmotionDetector()
    
    test_texts = [
        "I'm so happy today!",
        "I feel really sad and lonely",
        "This makes me so angry!",
        "I'm worried about my exam",
        "Wow, that's amazing!",
        "ana fer7an barsha" # Tunisian: I'm very happy
    ]
    
    for text in test_texts:
        result = detector.predict(text)
        print(f"Text: '{text}'")
        print(f"Emotion: {result['emotion']} ({result['confidence']:.2%})")
        print(f"Top 3 scores: {sorted(result['all_scores'].items(), key=lambda x: x[1], reverse=True)[:3]}")
        print()
