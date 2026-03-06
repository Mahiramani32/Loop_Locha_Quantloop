"""
Modules package - Contains all core functionality modules
"""

# Import key functions to make them available directly from modules package
from .twist_generator import generate_twists, TwistGenerator
from .suggestion_engine import generate_suggestions, SuggestionEngine
from .language_detector import detect_language, LanguageDetector
from .story_decomposer import decompose_story, StoryDecomposer
from .emotion_analyzer import analyze_emotions, EmotionAnalyzer

__all__ = [
    'generate_twists',
    'TwistGenerator',
    'generate_suggestions',
    'SuggestionEngine',
      'detect_language',
    'LanguageDetector',
    'decompose_story',
    'StoryDecomposer',
    'analyze_emotions',
    'EmotionAnalyzer'
]