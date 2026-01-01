# tests/test_models.py

import pytest
from src.models.emotion_detector import EmotionDetector
from src.models.intent_classifier import IntentClassifier

@pytest.fixture
def emotion_detector():
    return EmotionDetector()

@pytest.fixture
def intent_classifier():
    return IntentClassifier()

def test_emotion_detection_joy(emotion_detector):
    """
    Test joy emotion detection
    """
    text = "Ana fer7an barcha today! 😊"
    result = emotion_detector.predict(text)
    
    assert result['emotion'] == 'joy'
    assert result['confidence'] > 0.5

def test_emotion_detection_sadness(emotion_detector):
    """
    Test sadness detection
    """
    text = "Ma3andich 7atta espoir, je me sens seul"
    result = emotion_detector.predict(text)
    
    assert result['emotion'] in ['sadness', 'fear']
    assert result['confidence'] > 0.5

def test_crisis_detection(intent_classifier):
    """
    CRITICAL: Test crisis detection
    """
    crisis_texts = [
        "7abbeit nموت",
        "thinking about suicide",
        "ma3adch 7abba el 7ayét"
    ]
    
    for text in crisis_texts:
        result = intent_classifier.predict(text)
        
        assert result['crisis_detected'] == True
        assert result['intent'] == 'CRISIS'

def test_intent_classification(intent_classifier):
    """
    Test intent classification
    """
    texts_and_intents = [
        ("ana just 7abbeit na7ki", "VENT"),
        ("chnouwa naj3am bech...", "SEEK_ADVICE"),
        ("ma najmitch norkod", "REPORT_SYMPTOM")
    ]
    
    for text, expected_intent in texts_and_intents:
        result = intent_classifier.predict(text)
        assert result['intent'] == expected_intent
