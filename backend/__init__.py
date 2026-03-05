"""
Episodic Intelligence Engine - Backend Package
NLP modules for story analysis and emotion detection
"""

__version__ = "1.0.0"
__author__ = "Person 2 (NLP Team)"

# Export main modules for easy access
from backend.modules import (
    language_detector,
    story_decomposer,
    emotion_analyzer
)

__all__ = [
    'language_detector',
    'story_decomposer',
    'emotion_analyzer'
]