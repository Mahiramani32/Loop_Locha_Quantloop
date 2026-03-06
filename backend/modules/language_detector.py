"""
Language Detector Module using Qwen
Detects language of input text (supports 50+ languages)
Author: Person 2
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.qwen_model import get_qwen_model
import json

class LanguageDetector:
    """
    Detects language using Qwen model
    """
    
    def __init__(self):
        """Initialize with Qwen"""
        self.qwen = get_qwen_model()
        self.supported_languages = self._get_supported_languages()
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
    
    def detect_language(self, text, return_name=True):
        """
        Detect language using Qwen
        
        Args:
            text (str): Text to detect language from
            return_name (bool): Return language name instead of code
        
        Returns:
            str: Language code or name
        """
        if not text or len(text.strip()) < 5:
            print("⚠️ Text too short, defaulting to English")
            return 'English' if return_name else 'en'
        
        # Create prompt for Qwen
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
        
        # Fallback
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
    print("=" * 50)
    print("LANGUAGE DETECTOR - TEST")
    print("=" * 50)
    
    detector = LanguageDetector()
    
    test_texts = [
        "Hello, how are you? I'm doing great today!",
        "नमस्ते, आप कैसे हैं? मैं आज बहुत अच्छा हूँ।",
        "வணக்கம், எப்படி இருக்கிறீர்கள்? நான் இன்று நன்றாக இருக்கிறேன்।",
        "Bonjour, comment allez-vous? Je vais très bien aujourd'hui."
    ]
    
    for text in test_texts:
        lang = detector.detect_language(text, return_name=True)
        print(f"\n📝 Text: {text[:30]}...")
        print(f"   Language: {lang}")