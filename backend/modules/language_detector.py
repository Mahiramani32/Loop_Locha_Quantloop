# -*- coding: utf-8 -*-
"""
Language Detection Module
Detects language of input text with confidence scoring
"""

from langdetect import detect, detect_langs, DetectorFactory, LangDetectException
import pycountry
from typing import Dict, List, Optional

# Set seed for consistent results
DetectorFactory.seed = 42

class LanguageDetector:
    """Advanced language detection for stories"""
    
    SUPPORTED_LANGUAGES = {
        'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
        'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'zh': 'Chinese',
        'ja': 'Japanese', 'ko': 'Korean', 'ar': 'Arabic', 'hi': 'Hindi',
        'bn': 'Bengali', 'tr': 'Turkish', 'nl': 'Dutch', 'pl': 'Polish',
        'sv': 'Swedish', 'da': 'Danish', 'fi': 'Finnish', 'el': 'Greek'
    }
    
    def __init__(self, confidence_threshold: float = 0.6):
        self.confidence_threshold = confidence_threshold
        
    def detect(self, text: str) -> Dict:
        """Detect language with detailed analysis"""
        try:
            text = self._preprocess_text(text)
            if not text:
                return self._get_error_response("Empty text provided")
            
            lang_probs = detect_langs(text)
            primary = lang_probs[0]
            lang_code = primary.lang
            confidence = primary.prob
            
            lang_name = self._get_language_name(lang_code)
            
            alternatives = [
                {
                    'language_code': l.lang,
                    'language_name': self._get_language_name(l.lang),
                    'confidence': round(l.prob, 3)
                }
                for l in lang_probs[1:4]
            ]
            
            return {
                'success': True,
                'language_code': lang_code,
                'language_name': lang_name,
                'confidence': round(confidence, 3),
                'is_supported': lang_code in self.SUPPORTED_LANGUAGES,
                'alternatives': alternatives,
                'needs_translation': confidence < self.confidence_threshold
            }
            
        except LangDetectException as e:
            return self._get_error_response(str(e))
    
    def _preprocess_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        text = ' '.join(text.split())
        return text if len(text) >= 10 else ""
    
    def _get_language_name(self, code: str) -> str:
        try:
            if code in self.SUPPORTED_LANGUAGES:
                return self.SUPPORTED_LANGUAGES[code]
            lang = pycountry.languages.get(alpha_2=code)
            return lang.name if lang else code
        except:
            return code
    
    def _get_error_response(self, error_msg: str) -> Dict:
        return {
            'success': False,
            'error': error_msg,
            'language_code': 'unknown',
            'language_name': 'Unknown',
            'confidence': 0.0,
            'is_supported': False,
            'alternatives': []
        }

# Create instance
language_detector = LanguageDetector()

if __name__ == "__main__":
    test_texts = [
        "Once upon a time, in a kingdom far away.",
        "Érase una vez, en un reino muy lejano.",
        "Il était une fois, dans un royaume lointain."
    ]
    
    print("?? Testing Language Detector")
    print("="*50)
    for text in test_texts:
        result = language_detector.detect(text)
        if result["success"]:
            print(f"Text: {text[:20]}... -> {result["language_name"]} ({result["confidence"]})")

