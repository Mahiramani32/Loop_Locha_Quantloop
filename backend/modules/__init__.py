"""
NLP Modules Package
Contains all core NLP functionality for story analysis
"""

from .language_detector import language_detector
from .story_decomposer import story_decomposer
from .emotion_analyzer import emotion_analyzer

__all__ = [
    'language_detector',
    'story_decomposer',
    'emotion_analyzer'
]