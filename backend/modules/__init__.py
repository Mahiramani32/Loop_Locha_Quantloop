# Modules package
# Export key functions for easier imports

from .twist_generator import generate_twists, TwistGenerator
from .suggestion_engine import generate_suggestions, SuggestionEngine

__all__ = ['generate_twists', 'TwistGenerator', 'generate_suggestions', 'SuggestionEngine']