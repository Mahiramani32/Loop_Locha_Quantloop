"""
Modules package - Contains all core functionality modules
"""

# Import key functions to make them available directly from modules package
from .twist_generator import generate_twists, TwistGenerator
from .suggestion_engine import generate_suggestions, SuggestionEngine

__all__ = [
    'generate_twists',
    'TwistGenerator',
    'generate_suggestions',
    'SuggestionEngine'
]