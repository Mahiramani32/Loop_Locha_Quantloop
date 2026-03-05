# -*- coding: utf-8 -*-
"""
Test Module for Person 2 NLP Components
Run with: pytest test_modules.py -v
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from modules.language_detector import language_detector
from modules.story_decomposer import story_decomposer
from modules.emotion_analyzer import emotion_analyzer

class TestLanguageDetector:
    """Test language detection functionality"""
    
    def test_english_detection(self):
        """Test English language detection"""
        text = "This is a test story in English."
        result = language_detector.detect(text)
        assert result['success'] == True
        assert result['language_code'] == 'en'
        assert result['language_name'] == 'English'
        assert result['confidence'] > 0.5
    
    def test_spanish_detection(self):
        """Test Spanish language detection"""
        text = "Esta es una historia de prueba en español."
        result = language_detector.detect(text)
        assert result['success'] == True
        assert result['language_code'] == 'es'
        assert result['language_name'] == 'Spanish'
    
    def test_french_detection(self):
        """Test French language detection"""
        text = "C'est une histoire de test en français."
        result = language_detector.detect(text)
        assert result['success'] == True
        assert result['language_code'] == 'fr'
    
    def test_empty_text(self):
        """Test empty text handling"""
        result = language_detector.detect("")
        assert result['success'] == False
        assert 'error' in result


class TestStoryDecomposer:
    """Test story decomposition functionality"""
    
    def test_basic_stats(self):
        """Test basic statistics extraction"""
        text = "This is a test. This is another sentence. And one more for good measure."
        result = story_decomposer.decompose(text)
        assert result['success'] == True
        assert result['statistics']['sentence_count'] >= 3
        assert result['statistics']['word_count'] > 0
    
    def test_character_extraction(self):
        """Test character extraction"""
        text = "John and Mary went to the park. John was happy. Mary smiled."
        result = story_decomposer.decompose(text)
        assert len(result['elements']['characters']) > 0
        assert 'John' in str(result['elements']['characters'])
    
    def test_cliffhanger_detection(self):
        """Test cliffhanger detection"""
        text = "Suddenly, the door opened and..."
        result = story_decomposer.decompose(text)
        assert result['structure']['has_cliffhanger'] == True
    
    def test_dialogue_detection(self):
        """Test dialogue detection"""
        text = '"Hello there," said John. "How are you?"'
        result = story_decomposer.decompose(text)
        assert result['elements']['has_dialogue'] == True
        assert result['elements']['dialogue_count'] > 0


class TestEmotionAnalyzer:
    """Test emotion analysis functionality"""
    
    def test_joy_detection(self):
        """Test joy emotion detection"""
        text = "I am so happy and excited! This is wonderful news!"
        result = emotion_analyzer.analyze(text)
        assert result['success'] == True
        assert result['dominant_emotion']['name'] == 'joy'
        assert result['sentiment']['overall'] == 'positive'
    
    def test_sadness_detection(self):
        """Test sadness emotion detection"""
        text = "I feel so sad and lonely. This is heartbreaking."
        result = emotion_analyzer.analyze(text)
        assert result['dominant_emotion']['name'] == 'sadness'
        assert result['sentiment']['overall'] == 'negative'
    
    def test_anger_detection(self):
        """Test anger emotion detection"""
        text = "I am so angry! This is frustrating and infuriating!"
        result = emotion_analyzer.analyze(text)
        assert result['dominant_emotion']['name'] == 'anger'
    
    def test_fear_detection(self):
        """Test fear emotion detection"""
        text = "I'm terrified! Something scary is happening!"
        result = emotion_analyzer.analyze(text)
        assert result['dominant_emotion']['name'] == 'fear'
    
    def test_sentence_analysis(self):
        """Test sentence-by-sentence analysis"""
        text = "John was happy. Then he got scared. But he felt relieved."
        result = emotion_analyzer.analyze_sentences(text)
        assert len(result) == 3
        assert result[0]['dominant_emotion'] == 'joy'
        assert result[1]['dominant_emotion'] == 'fear'


class TestIntegration:
    """Test integration of all modules"""
    
    def test_full_story_analysis(self):
        """Test complete story analysis with all modules"""
        story = """
        John was excited about his birthday party. "I can't wait!" he said.
        Suddenly, a loud noise scared everyone. But it was just a surprise!
        """
        
        # Test language
        lang_result = language_detector.detect(story)
        assert lang_result['success'] == True
        assert lang_result['language_code'] == 'en'
        
        # Test story decomposition
        story_result = story_decomposer.decompose(story)
        assert story_result['success'] == True
        assert story_result['statistics']['word_count'] > 0
        assert 'John' in str(story_result['elements']['characters'])
        
        # Test emotion analysis
        emotion_result = emotion_analyzer.analyze(story)
        assert emotion_result['success'] == True
        assert 'emotions' in emotion_result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
