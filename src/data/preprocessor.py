# src/data/preprocessor.py

import pandas as pd
import numpy as np
import re
import ast
from pathlib import Path
from typing import List, Dict, Tuple, Union
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data (first time only)
nltk.download('punkt')
nltk.download('stopwords')

class TextPreprocessor:
    """
    IMPROVED: Less aggressive preprocessing to preserve emotion signals
    """
    
    def __init__(self, languages=['english', 'french']):
        # Don't remove ALL stop words - keep emotional ones!
        self.stop_words = set()
        for lang in languages:
            self.stop_words.update(stopwords.words(lang))
        
        # REMOVE emotional stop words from removal list
        emotional_words = {
            'not', 'no', 'never', 'nothing', 'nobody', 'neither', 'nor',
            'very', 'so', 'too', 'really', 'absolutely', 'completely',
            'more', 'most', 'much', 'many', 'few', 'less',
            'always', 'never', 'sometimes', 'often'
        }
        self.stop_words -= emotional_words
    
    def clean_text(self, text: str) -> str:
        """
        IMPROVED: Preserve emotion signals while cleaning
        """
        if not isinstance(text, str):
            return ""
        
        # DON'T lowercase - capitalization can signal emotion (I AM ANGRY!)
        # But do normalize excessive caps
        text = self.normalize_caps(text)
        
        # Remove URLs (but keep the context)
        text = re.sub(r'http\S+|www\S+|https\S+', ' [LINK] ', text)
        
        # Remove emails
        text = re.sub(r'\S+@\S+', ' [EMAIL] ', text)
        
        # KEEP emojis - they're critical for emotion! 😊😢😠
        # Just normalize repeated emojis
        text = re.sub(r'(😊|😢|😠|😱|😮|🤢|🙏|🤔){3,}', r'\1\1', text)
        
        # KEEP some punctuation emphasis (!!! and ???)
        # Normalize to max 3 repetitions
        text = re.sub(r'([!?]){4,}', r'\1\1\1', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def normalize_caps(self, text: str) -> str:
        """
        Normalize excessive capitalization but preserve emotion signals
        """
        # If more than 70% is caps, convert to title case
        if sum(1 for c in text if c.isupper()) > len(text) * 0.7:
            return text.capitalize()
        return text
    
    def extract_emotion_features(self, text: str) -> dict:
        """
        ✨ NEW: Extract emotion-related features
        """
        features = {
            'has_emoji': bool(re.search(r'[\U0001F600-\U0001F64F]', text)),
            'has_caps': any(c.isupper() for c in text),
            'has_exclamation': '!' in text,
            'has_question': '?' in text,
            'has_ellipsis': '...' in text or '…' in text,
            'negation_count': len(re.findall(r'\b(not|no|never|n\'t)\b', text.lower()))
        }
        return features
    
    def preprocess_dataset(self, df: pd.DataFrame, 
                          text_column: str = 'text',
                          label_column: str = 'emotion') -> pd.DataFrame:
        """
        IMPROVED: Preprocess with feature extraction
        """
        print(f"🔄 Preprocessing {len(df)} examples...")
        
        # Clean text (less aggressive now)
        df['cleaned_text'] = df[text_column].apply(self.clean_text)
        
        # Remove only truly empty texts (keep short emotional exclamations!)
        df = df[df['cleaned_text'].str.len() > 5].copy()  # Changed from 10
        
        # Add text statistics
        df['text_length'] = df['cleaned_text'].str.len()
        df['word_count'] = df['cleaned_text'].apply(lambda x: len(x.split()))
        
        # ✨ NEW: Extract emotion features
        emotion_features = df['cleaned_text'].apply(self.extract_emotion_features)
        for key in ['has_emoji', 'has_caps', 'has_exclamation', 'has_question', 
                    'has_ellipsis', 'negation_count']:
            df[key] = emotion_features.apply(lambda x: x[key])
        
        print(f"✅ Preprocessed {len(df)} valid examples")
        
        return df


# src/data/preprocessor.py - IMPROVED VERSION

class EmotionDataProcessor:
    """
    Process emotion datasets with IMPROVED emotion mapping
    """
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        
        # GoEmotions labels (28 + neutral)
        self.goemotions_labels = {
            0: 'admiration', 1: 'amusement', 2: 'anger', 3: 'annoyance',
            4: 'approval', 5: 'caring', 6: 'confusion', 7: 'curiosity',
            8: 'desire', 9: 'disappointment', 10: 'disapproval', 11: 'disgust',
            12: 'embarrassment', 13: 'excitement', 14: 'fear', 15: 'gratitude',
            16: 'grief', 17: 'joy', 18: 'love', 19: 'nervousness',
            20: 'optimism', 21: 'pride', 22: 'realization', 23: 'relief',
            24: 'remorse', 25: 'sadness', 26: 'surprise', 27: 'neutral'
        }
        
        # ✨ IMPROVED MAPPING - More nuanced emotion grouping
        self.emotion_mapping = {
            # JOY cluster (positive high arousal)
            'joy': 'joy',
            'amusement': 'joy',
            'excitement': 'joy',
            'love': 'joy',
            
            # TRUST cluster (positive low arousal, affiliation)
            'admiration': 'trust',
            'approval': 'trust',
            'caring': 'trust',
            'gratitude': 'trust',
            'pride': 'trust',
            'relief': 'trust',
            
            # ANTICIPATION cluster (forward-looking, expectation)
            'desire': 'anticipation',
            'optimism': 'anticipation',
            'curiosity': 'anticipation',      # CHANGED: curiosity is forward-looking
            'realization': 'anticipation',     # CHANGED: "aha moment" is anticipatory
            
            # ANGER cluster (negative high arousal, confrontational)
            'anger': 'anger',
            'annoyance': 'anger',
            'disapproval': 'anger',
            
            # SADNESS cluster (negative low arousal, withdrawal)
            'sadness': 'sadness',
            'disappointment': 'sadness',
            'grief': 'sadness',
            'remorse': 'sadness',
            'embarrassment': 'sadness',        # CHANGED: embarrassment is shame-based
            
            # FEAR cluster (negative high arousal, threat)
            'fear': 'fear',
            'nervousness': 'fear',
            
            # DISGUST cluster (negative, rejection/avoidance)
            'disgust': 'disgust',
            
            # SURPRISE cluster (neutral arousal, unexpected)
            'surprise': 'surprise',
            'confusion': 'surprise',           # confusion is mild surprise
            
            # NEUTRAL
            'neutral': 'neutral'
        }
        
        # ✨ ADD: Emotion keywords for boosting weak classes
        self.emotion_keywords = {
            'disgust': [
                'gross', 'disgusting', 'revolting', 'nauseating', 'repulsive',
                'vile', 'nasty', 'sickening', 'foul', 'yuck', 'eww', 'ugh'
            ],
            'anticipation': [
                'waiting', 'expecting', 'hoping', 'upcoming', 'soon', 'future',
                'looking forward', 'can\'t wait', 'excited for', 'will be',
                'planning', 'gonna', 'about to', 'preparing'
            ],
            'trust': [
                'believe', 'trust', 'reliable', 'dependable', 'honest', 'loyal',
                'faithful', 'confident in', 'count on', 'rely on', 'support'
            ],
            'fear': [
                'scared', 'afraid', 'terrified', 'frightened', 'anxious', 'worried',
                'nervous', 'panic', 'dread', 'terror', 'horror', 'phobia'
            ]
        }

    
    def process_goemotions(self, filepath: Union[str, Path]) -> pd.DataFrame:
        """
        Process GoEmotions dataset
        """
        print(f"📂 Processing {filepath}...")
        
        df = pd.read_csv(filepath)
        
        print(f"   Columns found: {df.columns.tolist()}")
        print(f"   Sample labels: {df['labels'].head(3).tolist()}")
        
        # Parse labels from string to list
        def parse_labels(label_str):
            try:
                if isinstance(label_str, str):
                    return ast.literal_eval(label_str)
                return label_str
            except:
                return []
        
        df['label_indices'] = df['labels'].apply(parse_labels)
        
        # Convert label indices to emotion names (take first emotion)
        def get_emotion_name(indices):
            if not indices or len(indices) == 0:
                return 'neutral'
            # Take the first emotion
            first_idx = indices[0]
            return self.goemotions_labels.get(first_idx, 'neutral')
        
        df['emotion'] = df['label_indices'].apply(get_emotion_name)
        
        # Clean text
        df = self.preprocessor.preprocess_dataset(df)
        
        # Map to 8 core emotions
        df['emotion_category'] = df['emotion'].map(
            lambda x: self.emotion_mapping.get(x, 'neutral')
        )
        
        # Show emotion distribution
        print(f"   Original emotions (top 10):")
        print(df['emotion'].value_counts().head(10))
        print(f"\n   Mapped to core emotions:")
        print(df['emotion_category'].value_counts())
        
        return df
    
    def create_train_val_test(self, data_dir: Union[str, Path] = 'data/raw') -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Create train/val/test splits with proper distribution
        """
        print("🎲 Creating train/val/test splits...")
        
        data_dir = Path(data_dir)
        processed_dir = Path('data/processed')
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Load all datasets
        dfs = []
        
        # GoEmotions
        for split in ['train', 'validation', 'test']:
            file_path = data_dir / f'goemotions_{split}.csv'
            if file_path.exists():
                df = self.process_goemotions(file_path)
                df['source'] = 'goemotions'
                df['split'] = split
                dfs.append(df)
            else:
                print(f"   ⚠️ File not found: {file_path}")
        
        if not dfs:
            raise ValueError("No dataset files found! Please check your data directory.")
        
        # Combine
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # Balance classes (important!)
        combined_df = self.balance_classes(combined_df)
        
        # Split and save
        train_df = combined_df[combined_df['split'] == 'train']
        val_df = combined_df[combined_df['split'] == 'validation']
        test_df = combined_df[combined_df['split'] == 'test']
        
        train_df.to_csv(processed_dir / 'train.csv', index=False)
        val_df.to_csv(processed_dir / 'validation.csv', index=False)
        test_df.to_csv(processed_dir / 'test.csv', index=False)
        
        print(f"\n✅ Train: {len(train_df)} examples")
        print(f"✅ Validation: {len(val_df)} examples")
        print(f"✅ Test: {len(test_df)} examples")
        
        return train_df, val_df, test_df
    
    def balance_classes(self, df: pd.DataFrame, 
                       max_per_class: int = 5000) -> pd.DataFrame:
        """
        Balance emotion classes (avoid bias)
        """
        print("\n⚖️ Balancing emotion classes...")
        
        balanced_dfs = []
        
        for emotion in df['emotion_category'].unique():
            emotion_df = df[df['emotion_category'] == emotion]
            
            if len(emotion_df) > max_per_class:
                emotion_df = emotion_df.sample(n=max_per_class, random_state=42)
            
            balanced_dfs.append(emotion_df)
        
        balanced_df = pd.concat(balanced_dfs, ignore_index=True)
        
        print("✅ Classes balanced!")
        print(balanced_df['emotion_category'].value_counts())
        
        return balanced_df


# Usage
if __name__ == "__main__":
    processor = EmotionDataProcessor()
    train_df, val_df, test_df = processor.create_train_val_test()