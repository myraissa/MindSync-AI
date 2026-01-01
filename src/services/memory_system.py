import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import os

class UserMemorySystem:
    """
    Persistent memory system for personalized conversations
    Remembers user preferences, history, patterns
    """
    
    def __init__(self, memory_dir: str = "data/user_memories"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
    
    def get_user_memory(self, user_id: str) -> Dict:
        """
        Load user memory from file
        """
        memory_file = self.memory_dir / f"{user_id}.json"
        
        if memory_file.exists():
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading memory: {e}")
                return self._create_empty_memory(user_id)
        else:
            return self._create_empty_memory(user_id)
    
    def _create_empty_memory(self, user_id: str) -> Dict:
        """Create new user memory structure"""
        return {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'last_interaction': None,
            
            # Personal info (learned over time)
            'name': None,
            'age': None,
            'location': None,
            'timezone': None,
            
            # Mental health context
            'concerns': [],  # ['anxiety', 'relationships', 'work stress']
            'goals': [],  # ['better sleep', 'manage anger', 'social confidence']
            'triggers': [],  # Things that upset them
            'coping_strategies': [],  # What works for them
            
            # Conversation history
            'conversation_count': 0,
            'total_messages': 0,
            'emotion_history': [],  # Last 20 emotions
            'topics_discussed': [],  # Last 20 topics
            
            # Patterns & insights
            'frequent_emotions': {},  # {'sadness': 15, 'anger': 8}
            'best_times': [],  # When they feel best
            'worst_times': [],  # When they struggle
            
            # Important events
            'milestones': [],  # Achievements, breakthroughs
            'crisis_events': [],  # Times they needed help
            
            # Preferences
            'preferred_language': 'en',
            'communication_style': 'supportive',  # supportive, direct, gentle
            'boundaries': [],  # Topics they don't want to discuss
        }
    
    def update_memory(self, user_id: str, updates: Dict):
        """
        Update user memory with new information
        """
        memory = self.get_user_memory(user_id)
        
        # Update timestamp
        memory['last_interaction'] = datetime.now().isoformat()
        
        # Merge updates
        for key, value in updates.items():
            if key in memory:
                # Handle lists (append with limit)
                if isinstance(memory[key], list) and isinstance(value, (list, str)):
                    items = value if isinstance(value, list) else [value]
                    memory[key].extend(items)
                    # Keep last 20 items for history lists
                    if key in ['emotion_history', 'topics_discussed']:
                        memory[key] = memory[key][-20:]
                
                # Handle dictionaries (merge/update)
                elif isinstance(memory[key], dict) and isinstance(value, dict):
                    memory[key].update(value)
                
                # Simple values
                else:
                    memory[key] = value
        
        # Save
        self._save_memory(user_id, memory)
        return memory
    
    def extract_info_from_conversation(self, user_input: str, 
                                       emotion: str, intent: str) -> Dict:
        """
        Extract learnable information from conversation
        """
        updates = {}
        text_lower = user_input.lower()
        
        # Extract name
        if any(phrase in text_lower for phrase in ['my name is', "i'm ", 'call me']):
            # Simple name extraction (can be improved)
            words = user_input.split()
            for i, word in enumerate(words):
                if word.lower() in ['name', "i'm", 'call'] and i + 1 < len(words):
                    potential_name = words[i + 1].strip('.,!?')
                    if potential_name.isalpha() and len(potential_name) > 1:
                        updates['name'] = potential_name.capitalize()
        
        # Extract concerns/topics
        concern_keywords = {
            'anxiety': ['anxious', 'anxiety', 'worried', 'panic', 'nervous'],
            'depression': ['depressed', 'depression', 'sad', 'hopeless'],
            'relationships': ['boyfriend', 'girlfriend', 'partner', 'relationship', 'breakup'],
            'family': ['mom', 'dad', 'parents', 'family', 'siblings'],
            'work': ['work', 'job', 'boss', 'career', 'colleague'],
            'school': ['school', 'college', 'university', 'exam', 'grades'],
            'sleep': ['sleep', 'insomnia', 'tired', 'exhausted'],
            'self-esteem': ['worthless', 'ugly', 'failure', 'not good enough'],
        }
        
        detected_concerns = []
        for concern, keywords in concern_keywords.items():
            if any(kw in text_lower for kw in keywords):
                detected_concerns.append(concern)
        
        if detected_concerns:
            updates['concerns'] = detected_concerns
        
        # Track emotion
        updates['emotion_history'] = emotion
        
        # Increment counters
        updates['total_messages'] = 1  # Will be added to existing
        
        # Detect goals
        goal_phrases = ['i want to', 'i need to', 'i wish i could', 'my goal is']
        if any(phrase in text_lower for phrase in goal_phrases):
            updates['topics_discussed'] = f"Goal mentioned: {user_input[:100]}"
        
        return updates
    
    def _save_memory(self, user_id: str, memory: Dict):
        """Save memory to file"""
        memory_file = self.memory_dir / f"{user_id}.json"
        try:
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error saving memory: {e}")
    
    def get_memory_summary(self, user_id: str) -> str:
        """
        Get human-readable memory summary
        """
        memory = self.get_user_memory(user_id)
        
        parts = []
        
        if memory['name']:
            parts.append(f"Name: {memory['name']}")
        
        if memory['concerns']:
            parts.append(f"Main concerns: {', '.join(memory['concerns'][:3])}")
        
        if memory['goals']:
            parts.append(f"Goals: {', '.join(memory['goals'][:2])}")
        
        parts.append(f"Conversations: {memory['conversation_count']}")
        
        if memory['emotion_history']:
            recent_emotions = memory['emotion_history'][-5:]
            parts.append(f"Recent emotions: {', '.join(recent_emotions)}")
        
        return "\n".join(parts) if parts else "New user - no history yet"
    
    def analyze_patterns(self, user_id: str) -> Dict:
        """
        Analyze user patterns for insights
        """
        memory = self.get_user_memory(user_id)
        
        # Emotion frequency
        emotions = memory.get('emotion_history', [])
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Sort by frequency
        sorted_emotions = sorted(emotion_counts.items(), 
                                key=lambda x: x[1], reverse=True)
        
        return {
            'most_common_emotion': sorted_emotions[0][0] if sorted_emotions else None,
            'emotion_counts': dict(sorted_emotions[:3]),
            'total_conversations': memory['conversation_count'],
            'main_concerns': memory['concerns'][:3],
            'needs_professional_help': (
                memory['conversation_count'] > 5 and 
                emotion_counts.get('sadness', 0) > len(emotions) * 0.6
            )
        }