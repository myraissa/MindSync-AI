# src/data/data_loader.py

import pandas as pd
import requests
from pathlib import Path

class DataCollector:
    """
    Collect free mental health & conversation datasets
    """
    
    def __init__(self):
        self.data_dir = Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def download_emotion_dataset(self):
        """
        Download GoEmotions dataset (FREE from Google)
        27+ emotions, 58k comments
        """
        print("📥 Downloading GoEmotions dataset...")
        
        urls = {
            'train': 'https://storage.googleapis.com/gresearch/goemotions/data/train.tsv',
            'val': 'https://storage.googleapis.com/gresearch/goemotions/data/dev.tsv',
            'test': 'https://storage.googleapis.com/gresearch/goemotions/data/test.tsv'
        }
        
        for split, url in urls.items():
            print(f"  → Downloading {split} set...")
            df = pd.read_csv(url, sep='\t')
            df.to_csv(self.data_dir / f'goemotions_{split}.csv', index=False)
            print(f"  ✅ Saved {len(df)} examples")
    
    def download_counseling_dataset(self):
        """
        Download Counseling & Psychotherapy dataset (FREE)
        From: https://huggingface.co/datasets/
        """
        print("📥 Downloading counseling conversations...")
        
        # Using HuggingFace datasets (FREE!)
        from datasets import load_dataset
        
        # Mental health conversations
        dataset = load_dataset("Amod/mental_health_counseling_conversations")
        
        # Convert to pandas
        df = pd.DataFrame(dataset['train'])
        df.to_csv(self.data_dir / 'counseling.csv', index=False)
        
        print(f"  ✅ Saved {len(df)} conversations")
    
    def download_empathetic_dialogues(self):
        """
        Download Empathetic Dialogues (Facebook Research - FREE)
        25k conversations with emotions
        """
        print("📥 Downloading Empathetic Dialogues...")
        
        from datasets import load_dataset
        dataset = load_dataset("empathetic_dialogues")
        
        train_df = pd.DataFrame(dataset['train'])
        train_df.to_csv(self.data_dir / 'empathetic_train.csv', index=False)
        
        print(f"  ✅ Saved {len(train_df)} dialogues")
    
    def collect_all(self):
        """
        Download all free datasets
        """
        print("🎯 Starting data collection (100% FREE)...\n")
        
        try:
            self.download_emotion_dataset()
            self.download_counseling_dataset()
            self.download_empathetic_dialogues()
            
            print("\n✨ Data collection complete!")
            print(f"📁 All data saved to: {self.data_dir}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Check your internet connection")

# Usage
if __name__ == "__main__":
    collector = DataCollector()
    collector.collect_all()
