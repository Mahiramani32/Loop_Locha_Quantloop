"""
Language Detector Module using Qwen
Detects language of input text (supports 50+ languages)
Author: Person 2
"""

import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.qwen_model import get_qwen_model
import json

class LanguageDetector:
    """
    Detects language using Qwen model with improved fallback
    """
    
    def __init__(self):
        """Initialize with Qwen"""
        self.qwen = get_qwen_model()
        self.supported_languages = self._get_supported_languages()
        # Unicode ranges for Indian languages
        self.unicode_ranges = {
            'hi': (0x0900, 0x097F),  # Devanagari (Hindi, Marathi, Nepali)
            'bn': (0x0980, 0x09FF),  # Bengali
            'gu': (0x0A80, 0x0AFF),  # Gujarati
            'pa': (0x0A00, 0x0A7F),  # Punjabi (Gurmukhi)
            'ta': (0x0B80, 0x0BFF),  # Tamil
            'te': (0x0C00, 0x0C7F),  # Telugu
            'kn': (0x0C80, 0x0CFF),  # Kannada
            'ml': (0x0D00, 0x0D7F),  # Malayalam
            'or': (0x0B00, 0x0B7F),  # Oriya
            'ur': (0x0600, 0x06FF),  # Arabic/Urdu
        }
        print("✅ LanguageDetector initialized with Qwen")
    
    def _get_supported_languages(self):
        """Return list of supported languages"""
        return {
            'en': 'English', 'hi': 'Hindi', 'ta': 'Tamil',
            'te': 'Telugu', 'bn': 'Bengali', 'mr': 'Marathi',
            'gu': 'Gujarati', 'kn': 'Kannada', 'ml': 'Malayalam',
            'pa': 'Punjabi', 'ur': 'Urdu', 'es': 'Spanish',
            'fr': 'French', 'de': 'German', 'zh': 'Chinese',
            'ja': 'Japanese', 'ru': 'Russian', 'ar': 'Arabic'
        }
    
    def _detect_by_script(self, text):
        """
        Detect language based on Unicode script ranges
        Returns language code or None if not detected
        """
        if not text:
            return None
        
        # Check each language's Unicode range
        for lang_code, (start, end) in self.unicode_ranges.items():
            for char in text:
                if ord(char) >= start and ord(char) <= end:
                    return lang_code
        
        return None
    
    def detect_language(self, text, return_name=True):
        """
        Detect language using Qwen with improved fallback
        
        Args:
            text (str): Text to detect language from
            return_name (bool): Return language name instead of code
        
        Returns:
            str: Language code or name
        """
        if not text or len(text.strip()) < 5:
            print("⚠️ Text too short, defaulting to English")
            return 'English' if return_name else 'en'
        
        # First try script-based detection (fast and reliable for Indian languages)
        script_lang = self._detect_by_script(text)
        if script_lang:
            if return_name:
                return self.supported_languages.get(script_lang, script_lang)
            return script_lang
        
        # If script not detected, try Qwen
        prompt = f"""Task: Detect the language of the following text.
        
Text: "{text}"

Return ONLY the ISO language code (like 'en', 'hi', 'ta', 'es', 'fr', etc.) and nothing else.
Do not add any explanation, just the code."""

        try:
            # Get response from Qwen
            response = self.qwen.chat_completion(
                prompt=prompt,
                temperature=0,
                max_tokens=10
            )
            
            if response:
                lang_code = response.strip().lower()
                # Clean up response (remove quotes, periods)
                lang_code = lang_code.replace('"', '').replace("'", "").replace('.', '')
                
                if return_name:
                    return self.supported_languages.get(lang_code, f"Unknown ({lang_code})")
                return lang_code
            
        except Exception as e:
            print(f"⚠️ Language detection error: {e}")
        
        # Final fallback
        return 'English' if return_name else 'en'
    
    def detect_batch(self, texts):
        """Detect languages for multiple texts"""
        results = []
        for text in texts:
            results.append(self.detect_language(text))
        return results


# Convenience function
def detect_language(text, return_name=True):
    detector = LanguageDetector()
    return detector.detect_language(text, return_name)


if __name__ == "__main__":
    # Self-test
    print("=" * 70)
    print("🧪 LANGUAGE DETECTOR - COMPREHENSIVE TEST")
    print("=" * 70)
    
    detector = LanguageDetector()
    
    test_texts = [
        ("Hello, how are you? I'm doing great today!", "English"),
        ("नमस्ते, आप कैसे हैं? मैं आज बहुत अच्छा हूँ।", "Hindi"),
        ("வணக்கம், எப்படி இருக்கிறீர்கள்? நான் இன்று நன்றாக இருக்கிறேன்।", "Tamil"),
        ("Bonjour, comment allez-vous? Je vais très bien aujourd'hui.", "French"),
        ("હું મજામાં છું.", "Gujarati"),
        ("¿Cómo estás? Muy bien, gracias.", "Spanish"),
        ("Wie geht es dir? Mir geht es gut.", "German"),
        ("আমি ভালো আছি।", "Bengali"),
        ("ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ.", "Kannada"),
        ("मी ठीक आहे.", "Marathi"),
    ]
    
    print("\n📊 Testing multiple languages:")
    print("-" * 50)
    
    for i, (text, expected) in enumerate(test_texts, 1):
        print(f"\n{i}. Text: {text[:30]}...")
        
        # Test with return_name=True
        detected = detector.detect_language(text, return_name=True)
        
        print(f"   Detected: {detected}")
        print(f"   Expected: {expected}")
        
        if detected == expected:
            print(f"   ✅ CORRECT!")
        else:
            print(f"   ❌ WRONG - Got {detected}, expected {expected}")
    
    print("\n" + "=" * 70)
    print("✅ Test complete!")