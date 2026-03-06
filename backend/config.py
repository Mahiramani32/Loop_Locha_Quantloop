"""
Configuration module for the Episodic Intelligence Engine.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    
    # Get environment, default to development
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    
    # Server settings - IMPORTANT: Use 0.0.0.0 for Docker
    HOST = os.getenv('HOST', '0.0.0.0')  # Changed to 0.0.0.0 for Docker
    PORT = int(os.getenv('PORT', 5000))
    
    # API settings
    API_VERSION = os.getenv('API_VERSION', '1.0.0')
    
    # CORS - allow frontend
    CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000', 'http://127.0.0.1:5173', 'http://127.0.0.1:3000', 'http://localhost:5174', 'http://127.0.0.1:5174']
    
    # Secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-2024')
    
    # File paths
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    CACHE_DIR = os.path.join(DATA_DIR, 'cache')
    SAMPLE_STORIES_PATH = os.path.join(DATA_DIR, 'sample_stories.json')
    
    # Cache settings
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', 300))

# Simple config - use this directly
current_config = Config()