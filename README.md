# 🧠 MindSync AI - Your Real Mental Health Companion

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)](https://streamlit.io/)
[![HuggingFace](https://img.shields.io/badge/🤗-HuggingFace-yellow)](https://huggingface.co/)

> **Not just another chatbot** - An AI companion that gives honest advice, remembers your journey, and actually helps.

---

## 🌟 What Makes MindSync Different?

### ❌ What Most AI Do:
- Validate everything you say
- Never challenge unhealthy patterns  
- Forget everything when you close the tab
- Give generic responses

### ✅ What MindSync Does:
- **Gives REAL advice** - Honest, caring confrontation
- **Remembers EVERYTHING** - Your name, struggles, patterns
- **Detects PATTERNS** - Spots unhealthy behaviors
- **Multi-language** - English, French, Tunisian Arabic
- **Crisis detection** - Immediate help for emergencies
- **Beautiful UI** - Modern 2026 glassmorphism design

---

## ✨ Key Features

### 1. 💡 Real Advice System

**Not just validation:**
```
User: "I skipped class again, I'm just too tired"

Regular AI: "That's okay! Self-care is important! 💙"

MindSync: "I hear you're exhausted, but skipping classes 
repeatedly will hurt you long-term. Let's figure out what's 
really going on. What's making you avoid them? 💙"
```

### 2. 🧠 Advanced Memory System

- Remembers your name, concerns, goals
- Tracks emotional patterns over time
- Learns from every conversation
- Detects when you're stuck in cycles

### 3. 📱 Multi-Page Interface

1. **🏠 Dashboard** - Your mental wellness overview
2. **💬 Chat** - Deep conversations with AI
3. **📊 Mood Tracker** - Visualize your emotional journey

### 4. 🎨 Modern UI

- Glassmorphism effects
- Dark gradient backgrounds
- Interactive emotion charts
- Responsive design

### 5. 🌍 Multi-Language Support

- English
- French (Français)
- Tunisian Arabic (تونسي - Transliterated)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection (for model download)

### Installation

```bash
# 1. Clone or download the project
cd MindSync-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.template .env

# 4. Add your HuggingFace token (optional but recommended)
# Edit .env:
HUGGINGFACE_TOKEN=hf_your_token_here

# 5. Run the app
streamlit run app/streamlit_app.py
```

### First Run

The first time you run MindSync, it will:
1. Download the emotion detection model (~150MB)
2. Initialize the memory system
3. Open your browser automatically

**This takes 1-2 minutes on first run only.**

---

## 📁 Project Structure

```
MindSync/
│
├── 📱 app/
│   └── streamlit_app.py      # Main Streamlit app
│
├── 🧠 src/
│   ├── models/
│   │   ├── emotion_detector.py       # Emotion detection (HF model)
│   │   ├── intent_classifier.py      # Intent classification (rule-based)
│   │   └── enhanced_response_generator.py  # Real advice engine
│   │
│   └── services/
│       ├── enhanced_conversation_service.py  # Full pipeline
│       └── memory_system.py          # User memory & patterns
│
├── 📊 data/
│   └── user_memories/                # JSON storage (auto-created)
│
├── 📝 docs/
│   ├── README.md                     # This file
│   ├── SETUP_GUIDE.md               # Detailed installation
│   ├── TROUBLESHOOTING_MODELS.md    # Fix common issues
│   └── INSTALLATION_SUMMARY.md      # Quick reference
│
├── .env                              # Environment variables
├── .env.template                     # Template for .env
├── requirements.txt                  # Python dependencies
└── quick_start.sh                    # Automated setup script
```

---

## 💬 Usage Examples

### Example 1: First Conversation

```
You: "Hi, I'm Sarah and I'm feeling anxious"

MindSync: "Nice to meet you, Sarah! I'm here to listen. 
Tell me more about what's making you anxious. 💙"

[Memory saved: name=Sarah, concerns=[anxiety]]
```

### Example 2: Pattern Detection (After Multiple Conversations)

```
You: "I'm sad again today"

MindSync: "Hey Sarah, I've noticed you've been sad in 5 
of our last 6 conversations. This pattern concerns me. 
Have you considered talking to a therapist? This persistent 
sadness might need professional support. 💙"
```

### Example 3: Honest Advice

```
You: "I yelled at my mom, she deserved it"

MindSync: "I hear your frustration, but let's pause. Even 
when someone upsets us, yelling usually makes things worse. 
What were you really trying to communicate? 💭"
```

### Example 4: Crisis Detection

```
You: "I don't want to be here anymore"

🚨 CRISIS DETECTED 🚨

MindSync: "I'm really worried about what you're sharing. 
Your life matters. Please call:
- Tunisia: 80 101 080
- International: 116 123
These people are trained to help. Will you call? 💙"
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Required for better performance (optional)
HUGGINGFACE_TOKEN=hf_your_token_here

# Optional customizations
USER_ID=your_username
MEMORY_DIR=data/user_memories
```

Get HuggingFace token: https://huggingface.co/settings/tokens

### Customize AI Personality

Edit `src/models/response_generator.py`, line 23:

```python
# More direct & honest
self.system_prompt = """You're a no-BS advisor..."""

# More gentle & supportive
self.system_prompt = """You're extremely gentle..."""

# Coaching style
self.system_prompt = """You're an action-oriented coach..."""
```

### Change Emotion Detection Model

Edit `src/models/emotion_detector.py`, line 13:

```python
# Default (6 emotions, fast)
EmotionDetector('bhadresh-savani/distilbert-base-uncased-emotion')

# More detailed (27 emotions)
EmotionDetector('SamLowe/roberta-base-go_emotions')

# Better accuracy (7 emotions)
EmotionDetector('j-hartmann/emotion-english-distilroberta-base')
```

---

## 🧪 Testing

### Test Individual Components

```bash
# Test emotion detection
cd src/models
python emotion_detector.py

# Test intent classification
python intent_classifier.py

# Test conversation service
cd src/services
python enhanced_conversation_service.py
```

### Test Full Application

```bash
# Run the app
streamlit run app/streamlit_app.py

# Should see:
# ✅ Emotion detector loaded
# ✅ Intent classifier loaded
# ✅ Memory system loaded
# ✅ Enhanced response generator loaded
```

---

## 📊 Technical Details

### Emotion Detection

**Model:** `bhadresh-savani/distilbert-base-uncased-emotion`
- Trained on GoEmotions dataset
- Detects: joy, sadness, anger, fear, surprise, love
- Fallback: Rule-based keyword matching (multi-language)


### Memory System

**Storage:** JSON files in `data/user_memories/`

**Tracked Data:**
- Personal info (name, age, location)
- Concerns (anxiety, depression, relationships)
- Goals (what user is working towards)
- Emotion history (last 20 emotions)
- Conversation count
- Pattern analysis

### Response Generation

**Model:** `meta-llama/Llama-3.1-8B-Instruct` via HuggingFace API
- Real advice system prompt
- Memory integration
- Pattern-based interventions
- Crisis handling

---

## 🐛 Troubleshooting

### Common Issues

#### Issue 1: "Model not found" error

```bash
# Quick fix: Replace with fixed versions
cp fixed_emotion_detector.py src/models/emotion_detector.py
cp fixed_intent_classifier.py src/models/intent_classifier.py
```

#### Issue 2: Connection timeout on first run

**Cause:** Downloading emotion model

**Solution:** Wait 1-2 minutes for download to complete

#### Issue 3: Memory not saving

**Solution:**
```bash
mkdir -p data/user_memories
chmod 755 data/user_memories
```

#### Issue 4: API timeout errors

**Solution:** Check internet connection and HuggingFace API status
```bash
# Test connection
curl -I https://huggingface.co
```

#### Issue 5: Import errors

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or specific packages
pip install transformers torch sentencepiece streamlit
```


---

## 🔒 Privacy & Security

### Data Storage

- ✅ All data stored **locally** on your machine
- ✅ No external databases
- ✅ You control your data
- ✅ Easy to export/delete

### What's Stored

```json
{
  "user_id": "demo_user",
  "name": "Sarah",
  "concerns": ["anxiety", "work stress"],
  "emotion_history": ["sadness", "joy", "neutral"],
  "conversation_count": 8
}
```


---

## 🚀 Deployment

### Local Deployment

```bash
streamlit run app/streamlit_app.py --server.port 8501
```

### Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Add secrets (HuggingFace token)
5. Deploy!

### Docker (Coming Soon)

```dockerfile
# Dockerfile example
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD streamlit run app/streamlit_app.py
```

---

## 🤝 Contributing

Want to improve MindSync?

### Ways to Contribute

1. **Report bugs** - Open an issue
2. **Suggest features** - Share your ideas
3. **Improve documentation** - Fix typos, add examples
4. **Add languages** - Expand multi-language support
5. **Code contributions** - Submit pull requests

### Development Setup

```bash
# Fork the repository
git clone https://github.com/myraissa/MindSync-AI.git
cd MindSync-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dev dependencies
pip install -r requirements.txt

# Make changes and test
streamlit run app/streamlit_app.py
```

---



## ⚠️ Disclaimer

### Important Notice

**MindSync is NOT:**
- A replacement for professional therapy
- Medical advice
- A crisis intervention service
- Suitable for severe mental health emergencies

**If you're in crisis, please call:**
- 🇹🇳 Tunisia: **80 101 080** (SOS Psychological Help)
- 🇺🇸 USA: **988** (Suicide & Crisis Lifeline)
- 🇬🇧 UK: **116 123** (Samaritans)
- 🇫🇷 France: **3114** (National Suicide Prevention)
- 🌍 International: **116 123** (Samaritans)

### Limitations

- AI responses are not perfect
- Memory system stores data locally (backup important!)
- Requires internet for AI generation
- Response quality depends on API availability

---

## 💙 Acknowledgments

### Technologies

- **[Streamlit](https://streamlit.io/)** - Beautiful web apps
- **[HuggingFace](https://huggingface.co/)** - Pre-trained models & API
- **[Transformers](https://huggingface.co/docs/transformers/)** - NLP library
- **[PyTorch](https://pytorch.org/)** - Deep learning framework
- **[Plotly](https://plotly.com/)** - Interactive charts

### Models & Data

- **[GoEmotions Dataset](https://github.com/google-research/google-research/tree/master/goemotions)** - Google Research
- **[DistilBERT Emotion Model](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion)** - Bhadresh Savani
- **[Llama 3.1](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)** - Meta AI

### Inspiration

Built for everyone struggling with mental health. You're not alone. 💙

---

## 📞 Contact & Support

### Get Help

- 🐛 [Report a bug](https://github.com/myraissa/MindSync-AI.git/issues)
- 💡 [Request a feature](https://github.com/myraissa/MindSync-AI.git/issues)
- 📧 Email: myraissa36@gmail.com


---

## 🎯 Roadmap

### Current Version: 2.0.0

✅ Real advice system  
✅ Memory system  
✅ Multi-page UI  
✅ Pattern detection  
✅ Multi-language support  
✅ Crisis detection  

### Version 2.1.0 (Q1 2026)

- [ ] Voice input/output
- [ ] Daily check-in reminders
- [ ] Goal tracking dashboard
- [ ] Journaling feature
<!-- 
### Version 3.0.0 (Q2 2026)

- [ ] Mobile app (React Native)
- [ ] Therapist matching
- [ ] Community features
- [ ] Wearable device integration -->

---


**Made with 💙 for everyone on their mental health journey**

*"It's okay to not be okay. But you don't have to face it alone."* 🫂

---

*Last updated: January 2026*  
*Version: 2.0.0*  
*Maintained by: [Mariem Aissa]*