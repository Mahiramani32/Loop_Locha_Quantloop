"""
Helper utility functions for the backend.
"""

import json
import os
import hashlib
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def read_json_file(file_path):
    """Safely read and parse a JSON file"""
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

def write_json_file(file_path, data):
    """Safely write data to a JSON file"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error writing to {file_path}: {e}")
        return False

def generate_cache_key(text):
    """Generate a cache key from text input"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def create_response(success, data=None, message="", error="", status_code=200):
    """Create a standardized API response"""
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

def validate_story_length(story, min_length=50, max_length=10000):
    """Validate that story length is within acceptable range"""
    if not story or not isinstance(story, str):
        return False
    length = len(story.strip())
    return min_length <= length <= max_length

def format_timestamp():
    """Get current timestamp in ISO format"""
    return datetime.utcnow().isoformat()