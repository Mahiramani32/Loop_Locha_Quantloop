"""
Helper utility functions for the backend.
Contains reusable functions for common operations.
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Any, Dict, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_json_file(file_path: str) -> Optional[Dict]:
    """
    Safely read and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return None

def write_json_file(file_path: str, data: Any) -> bool:
    """
    Safely write data to a JSON file.
    
    Args:
        file_path: Path to the JSON file
        data: Data to write
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error writing to {file_path}: {e}")
        return False

def generate_cache_key(text: str) -> str:
    """
    Generate a cache key from text input.
    
    Args:
        text: Input text to hash
        
    Returns:
        MD5 hash of the text
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def create_response(
    success: bool,
    data: Any = None,
    message: str = "",
    error: str = "",
    status_code: int = 200
) -> Dict:
    """
    Create a standardized API response.
    
    Args:
        success: Whether the request was successful
        data: Response data (for successful requests)
        message: Success message
        error: Error message (for failed requests)
        status_code: HTTP status code
        
    Returns:
        Standardized response dictionary
    """
    response = {
        "success": success,
        "timestamp": datetime.utcnow().isoformat(),
        "status_code": status_code
    }
    
    if success:
        response["data"] = data
        response["message"] = message
    else:
        response["error"] = error
        
    return response

def validate_story_length(story: str, min_length: int = 50, max_length: int = 5000) -> bool:
    """
    Validate that story length is within acceptable range.
    
    Args:
        story: Story text
        min_length: Minimum allowed characters
        max_length: Maximum allowed characters
        
    Returns:
        True if valid, False otherwise
    """
    if not story or not isinstance(story, str):
        return False
    
    length = len(story.strip())
    return min_length <= length <= max_length

def extract_keywords(text: str, max_keywords: int = 5) -> list:
    """
    Simple keyword extraction (basic version).
    More sophisticated version will be in NLP module.
    
    Args:
        text: Input text
        max_keywords: Maximum number of keywords to extract
        
    Returns:
        List of keywords
    """
    # Very basic implementation - just split and count
    words = text.lower().split()
    # Remove common words (stopwords) - simplified
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
    keywords = [w for w in words if w not in stopwords and len(w) > 3]
    
    # Get unique keywords
    unique_keywords = list(dict.fromkeys(keywords))
    return unique_keywords[:max_keywords]

def format_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.utcnow().isoformat()