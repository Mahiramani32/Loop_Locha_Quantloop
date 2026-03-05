#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Demo Script for Person 2 NLP Modules
Showcases all features for hackathon presentation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.modules.language_detector import language_detector
from backend.modules.story_decomposer import story_decomposer
from backend.modules.emotion_analyzer import emotion_analyzer
from backend.models.emotion_model import EmotionModel, create_sample_data
import json

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"🔍 {text}")
    print("="*70)

def print_json(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2, default=str))

def demo_language_detector():
    """Demo language detection"""
    print_header("LANGUAGE DETECTOR")
    
    test_texts = [
        "Once upon a time in a faraway kingdom...",
        "Érase una vez en un reino lejano...",
        "Il était une fois dans un royaume lointain..."
    ]
    
    for text in test_texts:
        result = language_detector.detect(text)
        print(f"\n📝 Text: {text[:30]}...")
        print(f"   Language: {result['language_name']} ({result['language_code']})")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Supported: {result['is_supported']}")

def demo_story_decomposer():
    """Demo story decomposition with cliffhanger scoring"""
    print_header("STORY DECOMPOSER WITH CLIFFHANGER SCORING")
    
    test_story = """
    Chapter 1: The Mysterious Door
    
    John and Mary discovered an old mansion while walking in the woods.
    
    "Should we go inside?" Mary whispered nervously.
    
    John pushed open the creaky door. Suddenly, a cold wind swept past them.
    
    They heard footsteps from upstairs...
    """
    
    result = story_decomposer.decompose(test_story, detailed=True)
    
    print(f"\n📊 Statistics:")
    print(f"   Word count: {result['statistics']['word_count']}")
    print(f"   Sentences: {result['statistics']['sentence_count']}")
    print(f"   Characters: {[c['name'] for c in result['elements']['characters']]}")
    
    print(f"\n🎯 Cliffhanger Analysis:")
    print(f"   Score: {result['cliffhanger']['score']}/100")
    print(f"   Strength: {result['cliffhanger']['strength']}")
    print(f"   Reasons:")
    for reason in result['cliffhanger']['reasons']:
        print(f"     • {reason}")

def demo_emotion_analyzer():
    """Demo emotion analysis with 90-second timeline"""
    print_header("EMOTION ANALYZER & 90-SECOND TIMELINE")
    
    test_story = """
    John was absolutely thrilled about his birthday party! Everyone was laughing and having fun.
    Suddenly, a loud crash came from outside. Everyone froze in terror.
    But then Mary appeared with a cake, smiling warmly. Everyone cheered with joy!
    """
    
    # Basic analysis
    result = emotion_analyzer.analyze(test_story, detailed=True)
    print(f"\n📊 Overall Analysis:")
    print(f"   Sentiment: {result['sentiment']['overall']}")
    print(f"   Dominant Emotion: {result['dominant_emotion']['name']}")
    print(f"   Intensity: {result['intensity']}")
    
    # 90-second timeline (matches hackathon requirement)
    print(f"\n⏱️ 90-SECOND EPISODE TIMELINE:")
    timeline = emotion_analyzer.get_emotion_timeline(test_story, time_blocks=5)
    for block in timeline:
        print(f"   Block {block['time_block']} ({block['time_range']}): {block['dominant_emotion']} ({block['sentiment']})")
    
    # Sentence analysis
    print(f"\n📝 Sentence-by-Sentence:")
    sentences = emotion_analyzer.analyze_sentences(test_story)
    for sent in sentences:
        print(f"   {sent['sentence_id']}: {sent['dominant_emotion']} ({sent['sentiment']})")

def demo_emotion_model():
    """Demo ML emotion model"""
    print_header("ML EMOTION MODEL")
    
    # Create and train model
    model = EmotionModel()
    texts, emotions = create_sample_data()
    
    print("\n📊 Training model...")
    result = model.train(texts, emotions)
    print(f"   Trained on {result['samples']} samples")
    print(f"   Emotions: {result['emotions']}")
    
    # Test predictions
    test_texts = [
        "I am so happy and excited!",
        "This is so sad and depressing",
        "I'm furious about this!"
    ]
    
    print("\n🎯 Predictions:")
    for text in test_texts:
        pred = model.predict(text)
        print(f"   Text: {text[:20]}... → {pred['emotion']} (confidence: {pred['confidence']})")

def demo_integration():
    """Demo all modules working together"""
    print_header("COMPLETE INTEGRATION DEMO")
    
    story = """
    John was excited about his birthday party. "I can't wait!" he said happily.
    Suddenly, a loud crash scared everyone. They were terrified.
    But it was just Mary with a surprise gift! Everyone laughed with joy.
    """
    
    print(f"\n📖 Story: {story[:100]}...")
    
    # Language
    lang = language_detector.detect(story)
    print(f"\n🌐 Language: {lang['language_name']}")
    
    # Story decomposition
    story_result = story_decomposer.decompose(story)
    print(f"\n📊 Story Stats:")
    print(f"   Words: {story_result['statistics']['word_count']}")
    print(f"   Cliffhanger: {story_result['cliffhanger']['score']}/100")
    
    # Emotion timeline
    timeline = emotion_analyzer.get_emotion_timeline(story, time_blocks=5)
    print(f"\n⏱️ 90-Second Timeline:")
    for block in timeline:
        print(f"   {block['time_range']}: {block['dominant_emotion']}")

if __name__ == "__main__":
    print("\n" + "🌟"*35)
    print("🌟  PERSON 2 NLP MODULES - COMPLETE DEMO  🌟")
    print("🌟"*35)
    
    demo_language_detector()
    demo_story_decomposer()
    demo_emotion_analyzer()
    demo_emotion_model()
    demo_integration()
    
    print("\n" + "✅"*35)
    print("✅  DEMO COMPLETE - ALL MODULES WORKING  ✅")
    print("✅"*35)
