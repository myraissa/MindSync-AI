# src/services/data_storage_service.py

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd

class DataStorageService:
    """
    Service to store and retrieve user conversation data
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.data_dir = Path("data/users")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.user_file = self.data_dir / f"{user_id}.json"
        
        # Initialize user file if it doesn't exist
        if not self.user_file.exists():
            self._initialize_user_data()
    
    def _initialize_user_data(self):
        """Create initial user data file"""
        initial_data = {
            "user_id": self.user_id,
            "created_at": datetime.now().isoformat(),
            "conversations": [],
            "mood_entries": [],
            "statistics": {
                "total_conversations": 0,
                "total_messages": 0,
                "crisis_alerts": 0,
                "emotions_detected": {}
            }
        }
        self._save_data(initial_data)
    
    def _load_data(self) -> Dict:
        """Load user data from file"""
        try:
            with open(self.user_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}
    
    def _save_data(self, data: Dict):
        """Save user data to file"""
        try:
            with open(self.user_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_conversation_entry(self, 
                              user_message: str,
                              ai_response: str,
                              detected_emotion: str,
                              emotion_confidence: float,
                              intent: str,
                              crisis_detected: bool,
                              all_emotion_scores: Dict):
        """
        Add a conversation entry with emotion analysis
        """
        data = self._load_data()
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "ai_response": ai_response,
            "detected_emotion": detected_emotion,
            "emotion_confidence": emotion_confidence,
            "intent": intent,
            "crisis_detected": crisis_detected,
            "all_emotion_scores": all_emotion_scores
        }
        
        data["conversations"].append(entry)
        
        # Update statistics
        data["statistics"]["total_conversations"] += 1
        data["statistics"]["total_messages"] += 2  # user + AI
        
        if crisis_detected:
            data["statistics"]["crisis_alerts"] += 1
        
        # Update emotion counts
        if detected_emotion not in data["statistics"]["emotions_detected"]:
            data["statistics"]["emotions_detected"][detected_emotion] = 0
        data["statistics"]["emotions_detected"][detected_emotion] += 1
        
        self._save_data(data)
    
    def add_mood_entry(self, mood: str, intensity: int, note: str = ""):
        """
        Add a manual mood entry (from Mood Tracker)
        """
        data = self._load_data()
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "mood": mood,
            "intensity": intensity,
            "note": note
        }
        
        data["mood_entries"].append(entry)
        self._save_data(data)
    
    def get_conversations(self, limit: Optional[int] = None) -> List[Dict]:
        """Get conversation history"""
        data = self._load_data()
        conversations = data.get("conversations", [])
        
        if limit:
            return conversations[-limit:]
        return conversations
    
    def get_mood_entries(self, limit: Optional[int] = None) -> List[Dict]:
        """Get mood entries"""
        data = self._load_data()
        mood_entries = data.get("mood_entries", [])
        
        if limit:
            return mood_entries[-limit:]
        return mood_entries
    
    def get_statistics(self) -> Dict:
        """Get user statistics"""
        data = self._load_data()
        return data.get("statistics", {})
    
    def get_emotion_timeline(self, days: int = 30) -> pd.DataFrame:
        """
        Get emotion data for the last N days as DataFrame
        """
        conversations = self.get_conversations()
        
        if not conversations:
            # Return empty DataFrame with expected columns
            return pd.DataFrame(columns=['Date', 'Joy', 'Sadness', 'Anger', 'Fear', 'Neutral'])
        
        # Convert to DataFrame
        df = pd.DataFrame(conversations)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        # Remove invalid timestamps
        df = df.dropna(subset=['timestamp'])
        
        if df.empty:
            return pd.DataFrame(columns=['Date', 'Joy', 'Sadness', 'Anger', 'Fear', 'Neutral'])
        
        # Filter last N days
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        df = df[df['timestamp'] >= cutoff_date]
        
        if df.empty:
            return pd.DataFrame(columns=['Date', 'Joy', 'Sadness', 'Anger', 'Fear', 'Neutral'])
        
        # Extract emotion scores
        emotion_data = []
        for _, row in df.iterrows():
            scores = row['all_emotion_scores']
            emotion_data.append({
                'Date': row['timestamp'].date(),  # Use .date() directly
                'Joy': scores.get('joy', 0) * 100,
                'Sadness': scores.get('sadness', 0) * 100,
                'Anger': scores.get('anger', 0) * 100,
                'Fear': scores.get('fear', 0) * 100,
                'Neutral': scores.get('neutral', 0) * 100
            })
        
        emotion_df = pd.DataFrame(emotion_data)
        
        # Group by date and calculate averages
        if not emotion_df.empty:
            emotion_df = emotion_df.groupby('Date').mean().reset_index()
        
        return emotion_df

    def get_emotion_distribution(self, days: int = 7) -> pd.DataFrame:
        """
        Get emotion distribution for the last N days
        """
        conversations = self.get_conversations()
        
        if not conversations:
            return pd.DataFrame({
                'Emotion': ['Joy', 'Neutral', 'Sadness', 'Anger', 'Fear'],
                'Count': [0, 0, 0, 0, 0]
            })
        
        df = pd.DataFrame(conversations)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Filter last N days
        cutoff_date = datetime.now() - pd.Timedelta(days=days)
        df = df[df['timestamp'] >= cutoff_date]
        
        # Count emotions
        emotion_counts = df['detected_emotion'].value_counts()
        
        # Ensure all emotions are present
        all_emotions = ['joy', 'neutral', 'sadness', 'anger', 'fear']
        emotion_data = []
        
        for emotion in all_emotions:
            count = emotion_counts.get(emotion, 0)
            emotion_data.append({
                'Emotion': emotion.capitalize(),
                'Count': count
            })
        
        return pd.DataFrame(emotion_data)
    
    def get_average_mood_score(self, days: int = 7) -> float:
        """
        Calculate average mood score (1-10 scale)
        Higher = better mood
        """
        conversations = self.get_conversations()
        
        if not conversations:
            return 5.0
        
        df = pd.DataFrame(conversations)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Filter last N days
        cutoff_date = datetime.now() - pd.Timedelta(days=days)
        df = df[df['timestamp'] >= cutoff_date]
        
        if df.empty:
            return 5.0
        
        # Emotion to score mapping
        emotion_scores = {
            'joy': 9,
            'neutral': 6,
            'sadness': 3,
            'anger': 2,
            'fear': 3
        }
        
        # Calculate weighted average
        total_score = 0
        total_weight = 0
        
        for _, row in df.iterrows():
            emotion = row['detected_emotion']
            confidence = row['emotion_confidence']
            score = emotion_scores.get(emotion, 5)
            
            total_score += score * confidence
            total_weight += confidence
        
        if total_weight == 0:
            return 5.0
        
        return round(total_score / total_weight, 1)
    
    def get_streak_days(self) -> int:
        """
        Calculate consecutive days with activity
        """
        conversations = self.get_conversations()
        
        if not conversations:
            return 0
        
        df = pd.DataFrame(conversations)
        
        # Convert timestamp to datetime explicitly
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        # Remove any invalid timestamps
        df = df.dropna(subset=['timestamp'])
        
        if df.empty:
            return 0
        
        # Extract date using .dt.date (proper method)
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        
        # Get unique dates sorted in descending order
        unique_dates = sorted(df['date'].unique(), reverse=True)
        
        if not unique_dates:
            return 0
        
        # Calculate streak
        streak = 0
        today = datetime.now().date()
        
        for i, date in enumerate(unique_dates):
            expected_date = today - pd.Timedelta(days=i).to_pytimedelta()
            if date == expected_date:
                streak += 1
            else:
                break
        
        return streak

    def get_dominant_emotion(self, days: int = 7) -> str:
        """Get the most common emotion in the last N days"""
        conversations = self.get_conversations()
        
        if not conversations:
            return "Neutral"
        
        df = pd.DataFrame(conversations)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Filter last N days
        cutoff_date = datetime.now() - pd.Timedelta(days=days)
        df = df[df['timestamp'] >= cutoff_date]
        
        if df.empty:
            return "Neutral"
        
        # Get most common emotion
        dominant = df['detected_emotion'].mode()
        
        if len(dominant) > 0:
            return dominant[0].capitalize()
        
        return "Neutral"
    
    def clear_all_data(self):
        """Clear all user data (for testing/reset)"""
        self._initialize_user_data()
