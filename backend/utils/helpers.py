# -*- coding: utf-8 -*-
"""
Helper Functions Module
Common utility functions for NLP processing
"""

import re
import hashlib
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\-\'\"]', '', text)
    
    return text.strip()

def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add when truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + suffix

def count_words(text: str) -> int:
    """Count words in text"""
    return len(text.split())

def count_sentences(text: str) -> int:
    """Count sentences in text (simple approximation)"""
    return len(re.findall(r'[.!?]+', text)) + 1

def generate_text_id(text: str) -> str:
    """Generate unique ID for text"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()[:16]

def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """
    Split text into chunks of approximately chunk_size characters
    
    Args:
        text: Input text
        chunk_size: Maximum chunk size
        
    Returns:
        List of text chunks
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        word_length = len(word) + 1  # +1 for space
        if current_length + word_length > chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def extract_emails(text: str) -> List[str]:
    """Extract email addresses from text"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)

def extract_urls(text: str) -> List[str]:
    """Extract URLs from text"""
    pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*'
    return re.findall(pattern, text)

def format_timestamp() -> str:
    """Get formatted current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely load JSON string"""
    try:
        return json.loads(json_str)
    except:
        return default

def safe_json_dumps(data: Any, default: str = '{}') -> str:
    """Safely dump JSON data"""
    try:
        return json.dumps(data, indent=2)
    except:
        return default

# Test the module
if __name__ == "__main__":
    print("🔍 Testing Helper Functions")
    print("="*50)
    
    test_text = "  This   is   a   test   with   extra   spaces.  "
    print(f"clean_text: '{clean_text(test_text)}'")
    
    long_text = "This is a very long text that needs to be truncated"
    print(f"truncate_text: {truncate_text(long_text, 20)}")
    
    print(f"count_words: {count_words('Hello world')}")
    print(f"count_sentences: {count_sentences('Hello. How are you? I am fine!')}")
    print(f"generate_text_id: {generate_text_id('test')}")
