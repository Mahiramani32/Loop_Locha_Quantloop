# -*- coding: utf-8 -*-
"""
Validation Module
Input validation functions for story processing
"""

import re
from typing import Tuple, Optional, List

def validate_story_text(text: str, min_length: int = 10, max_length: int = 100000) -> Tuple[bool, Optional[str]]:
    """
    Validate story text input
    
    Args:
        text: Input text to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        
    Returns:
        (is_valid, error_message)
    """
    if not text:
        return False, "Story text cannot be empty"
    
    if not isinstance(text, str):
        return False, "Story text must be a string"
    
    if len(text) < min_length:
        return False, f"Story text must be at least {min_length} characters"
    
    if len(text) > max_length:
        return False, f"Story text cannot exceed {max_length} characters"
    
    # Check for valid characters (allow basic punctuation and letters)
    if not re.match(r'^[\w\s\.\,\!\?\-\'\"]+$', text, re.UNICODE):
        return False, "Story text contains invalid characters"
    
    return True, None

def validate_language_code(code: str) -> bool:
    """
    Validate ISO language code
    
    Args:
        code: 2-letter language code
        
    Returns:
        True if valid
    """
    return bool(re.match(r'^[a-z]{2}$', code))

def validate_emotion_score(score: float) -> bool:
    """
    Validate emotion score (0-1)
    
    Args:
        score: Emotion score
        
    Returns:
        True if valid
    """
    return 0 <= score <= 1

def validate_positive_integer(value: int, min_val: int = 1, max_val: int = None) -> bool:
    """
    Validate positive integer within range
    
    Args:
        value: Value to validate
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        True if valid
    """
    if not isinstance(value, int):
        return False
    
    if value < min_val:
        return False
    
    if max_val and value > max_val:
        return False
    
    return True

def validate_email(email: str) -> bool:
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_url(url: str) -> bool:
    """Validate URL format"""
    pattern = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*$'
    return bool(re.match(pattern, url))

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing unsafe characters
    
    Args:
        filename: Original filename
        
    Returns:
        Safe filename
    """
    # Remove path separators and unsafe characters
    filename = re.sub(r'[\\/*?:"<>|]', '', filename)
    # Limit length
    return filename[:255]

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Validate file extension
    
    Args:
        filename: File name
        allowed_extensions: List of allowed extensions
        
    Returns:
        True if extension is allowed
    """
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    return ext in allowed_extensions

# Test the module
if __name__ == "__main__":
    print("🔍 Testing Validator Functions")
    print("="*50)
    
    # Test story validation
    valid, error = validate_story_text("This is a valid story text.")
    print(f"Valid story: {valid} - {error if error else 'OK'}")
    
    valid, error = validate_story_text("Short")
    print(f"Short story: {valid} - {error}")
    
    # Test language code
    print(f"Valid language code 'en': {validate_language_code('en')}")
    print(f"Invalid language code 'eng': {validate_language_code('eng')}")
    
    # Test emotion score
    print(f"Valid score 0.5: {validate_emotion_score(0.5)}")
    print(f"Invalid score 1.5: {validate_emotion_score(1.5)}")
    
    # Test email
    print(f"Valid email: {validate_email('test@example.com')}")
    print(f"Invalid email: {validate_email('test@.com')}")
