import pandas as pd
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
        Download GoEmotions dataset (FREE) via HuggingFace
        27+ emotions, 58k comments
        """
        print("📥 Downloading GoEmotions dataset...")
        
        try:
            from datasets import load_dataset
            
            print("  → Loading from HuggingFace...")
            dataset = load_dataset("google-research-datasets/go_emotions", "simplified")
            
            for split in ['train', 'validation', 'test']:
                if split in dataset:
                    data_dict = dataset[split].to_dict()
                    df = pd.DataFrame(data_dict)
                    filename = f'goemotions_{split}.csv'
                    df.to_csv(self.data_dir / filename, index=False)
                    print(f"  ✅ Saved {len(df)} examples to {filename}")
            
            return True
            
        except Exception as e:
            print(f" GoEmotions unavailable: {e}")
            print("  → Skipping this dataset")
            return False
    
    def download_counseling_dataset(self):
        """
        Download Counseling & Psychotherapy dataset (FREE)
        """
        print("\n📥 Downloading counseling conversations...")
        
        try:
            from datasets import load_dataset
            
            # Mental health conversations
            dataset = load_dataset("Amod/mental_health_counseling_conversations")
            
            # Convert to pandas properly
            train_data = dataset['train'].to_dict()
            df = pd.DataFrame(train_data)
            
            df.to_csv(self.data_dir / 'counseling.csv', index=False)    
            print(f"  ✅ Saved {len(df)} conversations")
            return True
            
        except Exception as e:
            print(f"  ⚠️ Counseling dataset unavailable: {e}")
            print("  → Skipping this dataset")
            return False
    
    def download_empathetic_dialogues(self):
        """
        Download Empathetic Dialogues (Facebook Research - FREE)
        25k conversations with emotions
        """
        print("\n📥 Downloading Empathetic Dialogues...")
        
        try:
            from datasets import load_dataset
            dataset = load_dataset("facebook/empathetic_dialogues", trust_remote_code=True)
            
            # Save train split
            train_data = dataset['train'].to_dict()
            train_df = pd.DataFrame(train_data)
            train_df.to_csv(self.data_dir / 'empathetic_train.csv', index=False)
            
            # Save validation split if available
            if 'validation' in dataset:
                val_data = dataset['validation'].to_dict()
                val_df = pd.DataFrame(val_data)
                val_df.to_csv(self.data_dir / 'empathetic_val.csv', index=False)
            
            print(f"  ✅ Saved {len(train_df)} dialogues")
            return True
            
        except Exception as e:
            print(f"  ⚠️ Empathetic Dialogues unavailable: {e}")
            print("  → Skipping this dataset")
            return False
    
    def download_daily_dialog(self):
        """
        Download DailyDialog dataset (FREE)
        13k multi-turn conversations with emotions
        """
        print("\n📥 Downloading DailyDialog dataset...")
        
        try:
            from datasets import load_dataset
            dataset = load_dataset("daily_dialog", trust_remote_code=True)
            
            train_data = dataset['train'].to_dict()
            train_df = pd.DataFrame(train_data)
            train_df.to_csv(self.data_dir / 'daily_dialog.csv', index=False)
            
            print(f"  ✅ Saved {len(train_df)} conversations")
            return True
            
        except Exception as e:
            print(f"  ⚠️ DailyDialog unavailable: {e}")
            print("  → Skipping this dataset")
            return False
    
    def collect_all(self):
        """
        Download all free datasets
        """
        print("🎯 Starting data collection (100% FREE)...\n")
        print("=" * 50)
        
        # Check if datasets library is installed
        try:
            import datasets
        except ImportError:
            print("❌ Error: 'datasets' library not installed")
            print("💡 Run: pip install datasets")
            return
        
        # Track successful downloads
        results = {
            'GoEmotions': self.download_emotion_dataset(),
            'Counseling': self.download_counseling_dataset(),
            'Empathetic Dialogues': self.download_empathetic_dialogues(),
            'DailyDialog': self.download_daily_dialog()
        }
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Collection Summary:")
        successful = sum(results.values())
        total = len(results)
        
        for name, success in results.items():
            status = "✅" if success else "❌"
            print(f"  {status} {name}")
        
        print(f"\n✨ Successfully downloaded {successful}/{total} datasets")
        print(f"📁 All data saved to: {self.data_dir.absolute()}")
        
        if successful == 0:
            print("\n⚠️ No datasets downloaded. Possible issues:")
            print("  1. Check internet connection")
            print("  2. Install datasets: pip install datasets")
            print("  3. HuggingFace may be temporarily down")
        elif successful < total:
            print("\n💡 Some datasets failed. This is OK - you can still proceed with available data!")

# Usage
if __name__ == "__main__":
    collector = DataCollector()
    collector.collect_all()