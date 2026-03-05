# Episodic Intelligence Engine - Person 2 (NLP Modules)

## 📋 Overview
This repository contains the NLP modules for the Episodic Intelligence Engine project. These modules handle language detection, story decomposition, and emotion analysis for story texts. Built with Python 3.13+ and production-ready for integration with the main API.

---

## 🎯 Modules Overview

| Module | File | Description |
|--------|------|-------------|
| **Language Detector** | `backend/modules/language_detector.py` | Detects 50+ languages with confidence scoring |
| **Story Decomposer** | `backend/modules/story_decomposer.py` | Extracts characters, scenes, and narrative structure |
| **Emotion Analyzer** | `backend/modules/emotion_analyzer.py` | Analyzes 8 emotions using VADER and TextBlob |
| **Emotion Model** | `backend/models/emotion_model.py` | ML model for emotion classification |
| **Utilities** | `backend/utils/helpers.py` | Text cleaning and preprocessing functions |
| **Validators** | `backend/utils/validators.py` | Input validation functions |

---

## 🔧 Detailed Module Documentation

### 1. Language Detector
**File:** `backend/modules/language_detector.py`

Detects the language of input text with confidence scoring.

```python
from modules.language_detector import language_detector

result = language_detector.detect("Once upon a time...")
print(result)
# Output: {
#   'success': True,
#   'language_code': 'en',
#   'language_name': 'English',
#   'confidence': 0.99,
#   'is_supported': True,
#   'alternatives': [...]
# }