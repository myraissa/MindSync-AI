
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional, Union
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path
import pickle

class ContextMemoryService:
    """
    Advanced memory system with semantic search & personalization
    
    KEY FEATURES:
    1. Semantic similarity search (find related past conversations)
    2. User profile building (interests, triggers, coping mechanisms)
    3. Temporal pattern detection (mood cycles, weekly patterns)
    4. Personalized response adaptation
    """
    
    def __init__(self, user_id: str, storage_path: str = 'data/memory'):
        self.user_id = user_id
        self.storage_path = Path(storage_path) / user_id
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Load embedding model (multilingual!)
        print("🧠 Loading semantic memory model...")
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        print("✅ Memory system ready!")
        
        # Memory stores
        self.conversation_memory = []  # All conversations with embeddings
        self.user_profile = self._load_or_create_profile()
        self.emotional_timeline = []  # Track emotions over time
        
        # Load existing memories
        self._load_memories()
    
    def add_conversation(self, 
                        user_message: str,
                        bot_response: str,
                        emotion: str,
                        intent: str,
                        timestamp: Optional[datetime] = None):
        """
        Store conversation with semantic embedding
        
        This enables:
        - Finding similar past situations
        - Building user understanding over time
        - Detecting behavioral patterns
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Create semantic embedding
        embedding = self.embedding_model.encode(user_message)
        
        # Extract key entities and topics
        entities = self._extract_entities(user_message)
        topics = self._extract_topics(user_message)
        
        # Create memory entry
        memory_entry = {
            'timestamp': timestamp.isoformat(),
            'user_message': user_message,
            'bot_response': bot_response,
            'emotion': emotion,
            'intent': intent,
            'embedding': embedding.tolist(),  # Convert to list for JSON
            'entities': entities,
            'topics': topics,
            'day_of_week': timestamp.strftime('%A'),
            'hour': timestamp.hour
        }
        
        self.conversation_memory.append(memory_entry)
        
        # Update user profile
        self._update_profile(memory_entry)
        
        # Track emotional state
        self.emotional_timeline.append({
            'timestamp': timestamp.isoformat(),
            'emotion': emotion,
            'intensity': self._estimate_intensity(user_message)
        })
        
        # Save to disk
        self._save_memories()
    
    def find_similar_conversations(self, current_message: str, top_k: int = 3) -> List[Dict]:
        """
        Find semantically similar past conversations
        
        USE CASE:
        User: "I'm stressed about my exam tomorrow"
        
        System finds:
        1. (0.89 similarity) "I was nervous before my interview last month"
        2. (0.85 similarity) "Feeling anxious about presentation at work"
        
        → Reference successful coping strategies from past!
        """
        if not self.conversation_memory:
            return []
        
        # Encode current message
        current_embedding = np.asarray(
            self.embedding_model.encode(current_message)
        )

        # Calculate similarities with all past conversations
        similarities = []
        for memory in self.conversation_memory:
            past_embedding = np.asarray(memory["embedding"])
            similarity = self._cosine_similarity(current_embedding, past_embedding)
            
            similarities.append({
                'memory': memory,
                'similarity': float(similarity)
            })
        
        # Sort by similarity and return top K
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        return similarities[:top_k]
    
    def get_personalized_context(self, current_message: str) -> Dict:
        """
        Generate personalized context for response generation
        
        RETURNS:
        {
            'similar_situations': [...],  # Past similar conversations
            'known_triggers': [...],      # User's stress triggers
            'effective_coping': [...],    # What helped before
            'emotional_trend': 'improving' | 'stable' | 'deteriorating',
            'personality_traits': {...},
            'preferences': {...}
        }
        """
        # Find similar past situations
        similar = self.find_similar_conversations(current_message, top_k=2)
        
        # Analyze emotional trend
        trend = self._analyze_emotional_trend()
        
        # Get relevant triggers
        triggers = self._identify_current_triggers(current_message)
        
        # Find what coping mechanisms worked before
        effective_coping = self._get_effective_coping_mechanisms()
        
        return {
            'similar_situations': similar,
            'known_triggers': triggers,
            'effective_coping': effective_coping,
            'emotional_trend': trend,
            'personality_traits': self.user_profile['personality_traits'],
            'communication_preferences': self.user_profile['communication_preferences'],
            'interests': self.user_profile['interests'],
            'support_network': self.user_profile['support_network']
        }
    def _identify_current_triggers(self, text: str) -> List[str]:
        topics = self._extract_topics(text)
        known_triggers = self.user_profile.get("triggers", {})

        return [
            topic for topic in topics
            if topic in known_triggers
        ]
    def _get_effective_coping_mechanisms(self, top_k: int = 3) -> List[str]:
        coping = self.user_profile.get("coping_mechanisms", {})

        if not coping:
            return []

        sorted_coping = sorted(
            coping.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [c[0] for c in sorted_coping[:top_k]]
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        dot = float(np.dot(vec1, vec2))
        norm = np.linalg.norm(vec1) * np.linalg.norm(vec2)

        if norm == 0.0:
            return 0.0

        return float(dot / norm)

    def detect_patterns(self) -> Dict:
        """
        Detect behavioral and emotional patterns
        
        EXAMPLES OF PATTERNS:
        - "Every Monday, stress levels increase (work-related)"
        - "Anxiety peaks around 10 PM (sleep-related)"
        - "Mood improves after mentioning exercise"
        """
        if len(self.conversation_memory) < 5:
            return {'message': 'Not enough data yet'}
        
        patterns = {}
        
        # Weekly patterns
        patterns['weekly_pattern'] = self._detect_weekly_pattern()
        
        # Time-of-day patterns
        patterns['hourly_pattern'] = self._detect_hourly_pattern()
        
        # Topic-emotion correlations
        patterns['trigger_topics'] = self._detect_trigger_topics()
        
        # Improvement areas
        patterns['positive_activities'] = self._detect_positive_activities()
        
        return patterns
    
    def generate_insights(self) -> List[str]:
        """
        Generate actionable insights for user
        
        EXAMPLES:
        - "I've noticed you tend to feel more stressed on Mondays. 
           Would it help to do a calming exercise Sunday evening?"
        - "When you mention spending time with friends, your mood 
           improves by 40%. Maybe prioritize social connection?"
        """
        insights = []
        patterns = self.detect_patterns()
        
        # Weekly pattern insights
        if 'weekly_pattern' in patterns and patterns['weekly_pattern']:
            worst_day = max(patterns['weekly_pattern'].items(), 
                          key=lambda x: x[1]['negative_count'])
            insights.append(
                f"💡 I notice {worst_day[0]}s tend to be tougher for you. "
                f"Would you like to create a self-care plan for {worst_day[0]}?"
            )
        
        # Emotional trend insights
        if len(self.emotional_timeline) >= 7:
            recent_emotions = [e['emotion'] for e in self.emotional_timeline[-7:]]
            if recent_emotions.count('sadness') > 4:
                insights.append(
                    "💙 I've noticed you've been feeling down this week. "
                    "I'm here for you. Would you like to talk about what's been going on?"
                )
        
        # Positive reinforcement
        if 'positive_activities' in patterns:
            for activity in patterns['positive_activities'][:2]:
                insights.append(
                    f"✨ I've noticed {activity} tends to lift your mood. "
                    f"Have you been able to do that recently?"
                )
        
        return insights
    
    def _update_profile(self, memory_entry: Dict):
        """
        Update user profile based on new conversation
        """
        # Track mentioned topics
        for topic in memory_entry['topics']:
            if topic not in self.user_profile['interests']:
                self.user_profile['interests'][topic] = 0
            self.user_profile['interests'][topic] += 1
        
        # Track triggers (negative emotions + topics)
        if memory_entry['emotion'] in ['sadness', 'anger', 'fear']:
            for topic in memory_entry['topics']:
                if topic not in self.user_profile['triggers']:
                    self.user_profile['triggers'][topic] = 0
                self.user_profile['triggers'][topic] += 1
        
        # Track coping mechanisms (positive emotions + activities)
        if memory_entry['emotion'] in ['joy', 'trust']:
            activities = self._extract_activities(memory_entry['user_message'])
            for activity in activities:
                if activity not in self.user_profile['coping_mechanisms']:
                    self.user_profile['coping_mechanisms'][activity] = 0
                self.user_profile['coping_mechanisms'][activity] += 1
    
    def _analyze_emotional_trend(self, lookback_days: int = 7) -> str:
        """
        Analyze emotional trend over time
        """
        if len(self.emotional_timeline) < 3:
            return 'insufficient_data'
        
        cutoff_date = datetime.now() - timedelta(days=lookback_days)
        
        recent_emotions = [
            e for e in self.emotional_timeline
            if datetime.fromisoformat(e['timestamp']) > cutoff_date
        ]
        
        if not recent_emotions:
            return 'insufficient_data'
        
        # Simple scoring: positive emotions = +1, negative = -1
        emotion_scores = {
            'joy': 1, 'trust': 1, 'anticipation': 0.5, 'surprise': 0.5,
            'sadness': -1, 'anger': -1, 'fear': -1, 'disgust': -1
        }
        
        scores = [emotion_scores.get(e['emotion'], 0) for e in recent_emotions]
        avg_score = sum(scores) / len(scores)
        
        # Compare with previous period
        prev_cutoff = cutoff_date - timedelta(days=lookback_days)
        prev_emotions = [
            e for e in self.emotional_timeline
            if prev_cutoff < datetime.fromisoformat(e['timestamp']) <= cutoff_date
        ]
        
        if prev_emotions:
            prev_scores = [emotion_scores.get(e['emotion'], 0) for e in prev_emotions]
            prev_avg = sum(prev_scores) / len(prev_scores)
            
            if avg_score > prev_avg + 0.3:
                return 'improving'
            elif avg_score < prev_avg - 0.3:
                return 'deteriorating'
        
        return 'stable'
    
    def _detect_weekly_pattern(self) -> Dict:
        """
        Detect patterns by day of week
        """
        day_emotions = {}
        
        for memory in self.conversation_memory:
            day = memory['day_of_week']
            emotion = memory['emotion']
            
            if day not in day_emotions:
                day_emotions[day] = {'positive_count': 0, 'negative_count': 0}
            
            if emotion in ['joy', 'trust', 'anticipation']:
                day_emotions[day]['positive_count'] += 1
            elif emotion in ['sadness', 'anger', 'fear', 'disgust']:
                day_emotions[day]['negative_count'] += 1
        
        return day_emotions
    
    def _detect_hourly_pattern(self) -> Dict:
        """
        Detect patterns by time of day
        """
        hour_emotions = {}
        
        for memory in self.conversation_memory:
            hour = memory['hour']
            emotion = memory['emotion']
            
            if hour not in hour_emotions:
                hour_emotions[hour] = []
            
            hour_emotions[hour].append(emotion)
        
        return hour_emotions
    
    def _detect_trigger_topics(self) -> List[str]:
        """
        Find topics associated with negative emotions
        """
        triggers = self.user_profile['triggers']
        
        # Sort by frequency
        sorted_triggers = sorted(triggers.items(), key=lambda x: x[1], reverse=True)
        
        return [trigger[0] for trigger in sorted_triggers[:5]]
    
    def _detect_positive_activities(self) -> List[str]:
        """
        Find activities associated with positive emotions
        """
        coping = self.user_profile['coping_mechanisms']
        
        # Sort by frequency
        sorted_coping = sorted(coping.items(), key=lambda x: x[1], reverse=True)
        
        return [activity[0] for activity in sorted_coping[:5]]
    
    def _extract_entities(self, text: str) -> List[str]:
        """
        Extract key entities (people, places, events)
        Simple keyword-based for now
        """
        entities = []
        
        # Common keywords
        keywords = {
            'people': ['friend', 'family', 'mother', 'father', 'colleague', 
                      'ami', 'famille', 'mère', 'père'],
            'places': ['work', 'home', 'school', 'office', 'khdemti', 'dar'],
            'events': ['exam', 'interview', 'meeting', 'presentation', 'examen']
        }
        
        text_lower = text.lower()
        
        for category, words in keywords.items():
            for word in words:
                if word in text_lower:
                    entities.append(f"{category}:{word}")
        
        return entities
    
    def _extract_topics(self, text: str) -> List[str]:
        """
        Extract main topics from text
        """
        topics = []
        
        topic_keywords = {
            'work': ['work', 'job', 'career', 'khdemti', 'travail'],
            'relationships': ['friend', 'family', 'love', 'ami', 'famille'],
            'health': ['sleep', 'tired', 'sick', 'norkod', 'malade'],
            'education': ['exam', 'study', 'school', 'examen', 'étudier'],
            'stress': ['stress', 'anxiety', 'worried', 'nerveux', 'kha2ef']
        }
        
        text_lower = text.lower()
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _extract_activities(self, text: str) -> List[str]:
        """
        Extract activities mentioned in text
        """
        activities = []
        
        activity_keywords = [
            'exercise', 'sport', 'walk', 'music', 'meditation', 'prayer',
            'reading', 'friends', 'family', 'hobby', 'gaming',
            'exercice', 'marche', 'musique', 'prière', 'lecture'
        ]
        
        text_lower = text.lower()
        
        for activity in activity_keywords:
            if activity in text_lower:
                activities.append(activity)
        
        return activities
    
    def _estimate_intensity(self, text: str) -> str:
        """
        Estimate emotional intensity from text markers
        """
        text_lower = text.lower()
        
        # High intensity markers
        high_markers = ['very', 'extremely', 'really', 'so much', 'barcha', 
                       'zeer', 'trop', 'vraiment']
        
        # Low intensity markers
        low_markers = ['a bit', 'slightly', 'somewhat', 'chwaya', 'un peu']
        
        if any(marker in text_lower for marker in high_markers):
            return 'high'
        elif any(marker in text_lower for marker in low_markers):
            return 'low'
        else:
            return 'medium'
    
    
    def _load_or_create_profile(self) -> Dict:
        """
        Load existing user profile or create new one
        """
        profile_path = self.storage_path / 'profile.json'
        
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                return json.load(f)
        
        # Create new profile
        return {
            'user_id': self.user_id,
            'created_at': datetime.now().isoformat(),
            'interests': {},
            'triggers': {},
            'coping_mechanisms': {},
            'support_network': [],
            'personality_traits': {},
            'communication_preferences': {
                'language_mix': 'auto',  # Auto-detect FR/AR/EN mix
                'formality': 'casual'
            }
        }
    
    def _save_memories(self):
        """
        Save memories to disk
        """
        # Save conversation memory
        memory_path = self.storage_path / 'conversations.pkl'
        with open(memory_path, 'wb') as f:
            pickle.dump(self.conversation_memory, f)
        
        # Save emotional timeline
        timeline_path = self.storage_path / 'emotional_timeline.json'
        with open(timeline_path, 'w') as f:
            json.dump(self.emotional_timeline, f)
        
        # Save user profile
        profile_path = self.storage_path / 'profile.json'
        with open(profile_path, 'w') as f:
            json.dump(self.user_profile, f, indent=2)
    
    def _load_memories(self):
        """
        Load memories from disk
        """
        # Load conversation memory
        memory_path = self.storage_path / 'conversations.pkl'
        if memory_path.exists():
            with open(memory_path, 'rb') as f:
                self.conversation_memory = pickle.load(f)
        
        # Load emotional timeline
        timeline_path = self.storage_path / 'emotional_timeline.json'
        if timeline_path.exists():
            with open(timeline_path, 'r') as f:
                self.emotional_timeline = json.load(f)


# ============================================
# USAGE EXAMPLE
# ============================================

if __name__ == "__main__":
    # Initialize for user
    memory = ContextMemoryService(user_id="user_123")
    
    # Add conversation
    memory.add_conversation(
        user_message="I'm really stressed about my exam tomorrow",
        bot_response="I hear you. Exam stress is tough. What subject is it?",
        emotion="fear",
        intent="VENT"
    )
    
    # Later, user mentions similar situation
    similar = memory.find_similar_conversations(
        "I have a big presentation at work next week and I'm nervous"
    )
    
    print("Similar situations:", similar)
    
    # Generate insights
    insights = memory.generate_insights()
    print("Insights:", insights)