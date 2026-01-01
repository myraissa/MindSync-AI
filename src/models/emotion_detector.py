# src/models/emotion_detector.py

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path
import traceback

class EmotionDetector:
    """
    Detect emotions from text
    """
    
    def __init__(self, model_path='models/emotion_classifier'):
        self.model_path = Path(model_path)
        
        try:
            # Load model & tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
            
            # Emotion labels
            self.emotions = ['joy', 'sadness', 'anger', 'fear', 
                            'surprise', 'disgust', 'trust', 'anticipation']
            
            self.id_to_emotion = {i: emotion for i, emotion in enumerate(self.emotions)}
            
            print(f"✅ Emotion detector loaded from {model_path}")
            
        except Exception as e:
            print(f"⚠️ Error loading emotion detector: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            # Fallback: use simple rule-based
            self.model = None
            self.tokenizer = None
    
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
        
        # If model failed to load, use simple fallback
        if self.model is None or self.tokenizer is None:
            return self._fallback_predict(text)
        
        try:
            # Tokenize
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=128,
                padding=True
            )
            
            # Predict
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get results
            predicted_id = int(torch.argmax(predictions, dim=-1).item())
            confidence = predictions[0][predicted_id].item()
            
            emotion = self.id_to_emotion[predicted_id]
            
            # All scores (FIXED KEY NAME!)
            all_scores = {
                self.id_to_emotion[i]: float(predictions[0][i].item())
                for i in range(len(self.emotions))
            }
            
            return {
                'emotion': emotion,
                'confidence': float(confidence),
                'all_scores': all_scores  # ✅ Consistent key name
            }
            
        except Exception as e:
            print(f"⚠️ Prediction error: {e}")
            return self._fallback_predict(text)
    
    def _fallback_predict(self, text: str) -> dict:
        """
        Simple rule-based emotion detection (fallback)
        """
        text_lower = text.lower()
        
        # Simple keyword matching
        emotion_keywords = {
            'joy': ['happy', 'glad', 'excited', 'joy', 'great', 'wonderful', 'amazing', 'fer7an', 'content'],
            'sadness': ['sad', 'depressed', 'down', 'unhappy', 'crying', '7azin', 'triste', 'seul'],
            'anger': ['angry', 'mad', 'furious', 'annoyed', 'frustrated', 'mte3aseb'],
            'fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous', 'kha2ef', 'peur'],
            'surprise': ['surprised', 'shocked', 'amazed', 'wow', 'unexpected'],
        }
        
        # Count matches
        scores = {}
        for emotion, keywords in emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            scores[emotion] = count / len(keywords)
        
        # Add missing emotions
        for emotion in self.emotions:
            if emotion not in scores:
                scores[emotion] = 0.0
        
        # Get best match
        if max(scores.values()) == 0:
            detected_emotion = 'neutral'
            confidence = 0.5
        else:
            detected_emotion = max(scores.keys(), key=lambda k: scores[k])
            confidence = min(scores[detected_emotion] + 0.5, 1.0)
        
        return {
            'emotion': detected_emotion,
            'confidence': confidence,
            'all_scores': scores
        }
