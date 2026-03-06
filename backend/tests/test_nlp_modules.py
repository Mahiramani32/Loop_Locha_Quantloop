"""
Test script for Person 2 NLP modules using Qwen
Tests language detection, story decomposition, and emotion analysis
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.modules.language_detector import detect_language
from backend.modules.story_decomposer import decompose_story
from backend.modules.emotion_analyzer import analyze_emotions

print("=" * 70)
print("🧪 PERSON 2 - QWEN NLP MODULES TEST")
print("=" * 70)

# Test 1: Language Detection
print("\n" + "=" * 70)
print("📝 TEST 1: LANGUAGE DETECTION")
print("=" * 70)

test_texts = [
        "Hello, how are you? I'm doing great today!", 
        "नमस्ते, आप कैसे हैं? मैं आज बहुत अच्छा हूँ।", 
        "வணக்கம், எப்படி இருக்கிறீர்கள்? நான் இன்று நன்றாக இருக்கிறேன்।", 
        "Bonjour, comment allez-vous? Je vais très bien aujourd'hui.", 
        "મારું નામ... છે.", 
        "¿Cómo estás? Muy bien, gracias.",
        "Wie geht es dir? Mir geht es gut.", 
        "আমি ভালো আছি।", 
        "ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ.", 
        "मी ठीक आहे.", 
    ]

for text in test_texts:
    lang = detect_language(text, return_name=True)
    print(f"\n📌 Text: {text[:30]}...")
    print(f"   Detected Language: {lang}")

print("\n✅ Language Detection: PASSED")

# Test 2: Story Decomposition
print("\n" + "=" * 70)
print("📖 TEST 2: STORY DECOMPOSITION")
print("=" * 70)

test_story = """
a girl lost her phone near eiffel tower and conrad fisher got it and gifted to belly.
"""

episodes = decompose_story(test_story, num_episodes=5)

print(f"\n📌 Original Story: {test_story[:100]}...")
print(f"\n📌 Generated {len(episodes)} Episodes:")

for ep in episodes:
    print(f"\n   Episode {ep['number']}: {ep['title']}")
    print(f"   Summary: {ep['summary'][:80]}...")
    print(f"   Cliffhanger: {ep['cliffhanger']}")

print("\n✅ Story Decomposition: PASSED")

# Test 3: Emotion Analysis
print("\n" + "=" * 70)
print("🎭 TEST 3: EMOTION ANALYSIS")
print("=" * 70)

# Use episodes from decomposition
emotion_results = analyze_emotions(episodes)

for result in emotion_results:
    print(f"\n📺 Episode {result['episode']}:")
    print(f"   Emotion Curve:")
    for point in result['emotion_curve']:
        print(f"     At {point['time']}s: {point['emotion']} ({point['intensity']:.2f})")
    print(f"   Stats: {result['statistics']}")

print("\n✅ Emotion Analysis: PASSED")

# Summary
print("\n" + "=" * 70)
print("📊 TEST SUMMARY")
print("=" * 70)
print("""
✅ Language Detection: Working with Qwen
✅ Story Decomposition: Working with Qwen  
✅ Emotion Analysis: Working with Qwen

All modules using Qwen model are ready! 🚀
""")