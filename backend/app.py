"""
Main Flask application for the Episodic Intelligence Engine API.
"""

import os
import sys

# Add backend directory to path so imports work
sys.path.insert(0, os.path.dirname(__file__))

import logging
import time
import hashlib
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Configure logging NEXT
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info("🚀 Starting application...")

# Import your local modules - USE ABSOLUTE IMPORTS (no dots)
from config import current_config
from utils.validators import StoryValidator
from utils.helpers import (
    create_response,
    validate_story_length,
    read_json_file,
    generate_cache_key,
    write_json_file
)

# Person 4's modules
from modules.twist_generator import TwistGenerator
from modules.suggestion_engine import SuggestionEngine

# Person 3's modules
from modules.cliffhanger_scorer import CliffhangerScorer
from modules.retention_predictor import RetentionPredictor
from modules.graph_generator import GraphGenerator

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(current_config)

# Enable CORS for frontend
CORS(app, origins=app.config['CORS_ORIGINS'])

# Initialize Person 3's modules (NOW logger is defined)
logger.info("📊 Initializing Person 3's Analytics Modules...")
cliffhanger_scorer = CliffhangerScorer()
retention_predictor = RetentionPredictor()
graph_generator = GraphGenerator()
logger.info("✅ Person 3's analytics modules initialized")

# Initialize Person 4's modules
logger.info("🎨 Initializing Person 4's Creative Modules...")
twist_generator = TwistGenerator()
suggestion_engine = SuggestionEngine()
logger.info("✅ Person 4's creative modules initialized")

# Simple cache that works
# Simple cache that works - UPDATED VERSION
# Simple cache that works - ULTIMATE FIX
class SimpleCache:
    def __init__(self, timeout_seconds=300):
        self.cache = {}
        self.expiry = {}
        self.timeout = timeout_seconds
        self.hits = 0
        self.misses = 0
        logger.info(f"🗄️ Cache initialized with timeout {timeout_seconds}s")
    
    def get(self, key):
        if key in self.cache:
            # Check if expired
            if key in self.expiry and datetime.now() < self.expiry[key]:
                self.hits += 1
                logger.info(f"⚡ CACHE HIT: {key[:8]} (hits: {self.hits})")
                return self.cache[key]
            else:
                # Remove expired
                if key in self.cache:
                    del self.cache[key]
                if key in self.expiry:
                    del self.expiry[key]
                logger.info(f"⏰ CACHE EXPIRED: {key[:8]}")
        self.misses += 1
        logger.info(f"🔄 CACHE MISS: {key[:8]} (misses: {self.misses})")
        return None
    
    def set(self, key, value):
        self.cache[key] = value
        self.expiry[key] = datetime.now() + timedelta(seconds=self.timeout)
        logger.info(f"💾 Cached: {key[:8]} (expires in {self.timeout}s)")
        return True
    
    def clear(self):
        """Clear all cache (for testing)"""
        self.cache.clear()
        self.expiry.clear()
        self.hits = 0
        self.misses = 0
        logger.info("🧹 Cache cleared")
    
    def get_stats(self):
        """Get cache statistics"""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "size": len(self.cache),
            "hit_rate": round(self.hits / (self.hits + self.misses) * 100, 2) if (self.hits + self.misses) > 0 else 0
        }

# Initialize cache
cache = SimpleCache()

# Performance monitor decorator
def monitor_performance(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        duration = (end - start) * 1000
        logger.info(f"⏱️ {func.__name__} took {duration:.2f}ms")
        return result
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/api/health', methods=['GET'])
@monitor_performance
def health_check():
    """Health check endpoint"""
    logger.info("✅ Health check called")
    return jsonify(create_response(
        success=True,
        data={
            "status": "healthy",
            "version": app.config['API_VERSION'],
            "environment": app.config['FLASK_ENV']
        },
        message="API is running"
    )), 200

@app.route('/api/validate', methods=['POST'])
@monitor_performance
def validate_story():
    """Validate story input"""
    try:
        data = request.get_json()
        
        is_valid, error = StoryValidator.validate_story_input(data)
        
        if not is_valid:
            return jsonify(create_response(
                success=False,
                error=error,
                status_code=400
            )), 400
        
        story = data['story']
        
        return jsonify(create_response(
            success=True,
            data={
                "valid": True,
                "length": len(story),
                "word_count": len(story.split()),
                "estimated_episodes": max(3, min(8, len(story) // 500))
            },
            message="Story validation passed"
        )), 200
        
    except Exception as e:
        logger.error(f"Error in validate_story: {str(e)}")
        return jsonify(create_response(
            success=False,
            error="Internal server error",
            status_code=500
        )), 500


@app.route('/api/analyze', methods=['POST'])
@monitor_performance
def analyze_story():
    """
    Analyze story and generate episodes with emotions, cliffhangers, etc.
    Now integrated with Person 3's analytics modules!
    """
    try:
        # Get and validate input
        data = request.get_json()
        is_valid, error = StoryValidator.validate_story_input(data)
        
        if not is_valid:
            return jsonify(create_response(
                success=False,
                error=error,
                status_code=400
            )), 400
        
        story = data['story']
        title = data.get('title', 'Untitled Story')
        num_episodes = data.get('episodes', 5)
        
        # Generate cache key
        cache_key = hashlib.md5(f"{story}{num_episodes}".encode()).hexdigest()
        
        # CHECK CACHE FIRST - FAST PATH
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"⚡ CACHE HIT: {cache_key[:8]} - returning cached result")
            return jsonify(create_response(
                success=True,
                data=cached_result,
                message="Analysis complete (cached)"
            )), 200
        
        logger.info(f"🔄 CACHE MISS: {cache_key[:8]} - generating new result")
        
        # ===== PERSON 2's CODE WOULD GO HERE =====
        # For now, we're using mock episodes
        # When Person 2 is ready, replace this with:
        # episodes_data = story_decomposer.decompose(story, num_episodes)
        # for episode in episodes_data:
        #     emotions = emotion_analyzer.analyze(episode['content'])
        #     episode['emotional_arc'] = emotions
        
        # Generate mock episodes (temporary - remove when Person 2 is integrated)
        words = story.split()
        word_count = len(words)
        
        # Handle short stories
        if word_count < num_episodes * 10:
            words = words * ((num_episodes * 10) // word_count + 1)
            word_count = len(words)
        
        words_per_episode = max(1, word_count // num_episodes)
        
        # Generate episodes
        episodes = []
        
        for i in range(num_episodes):
            episode_num = i + 1
            
            # Mock emotional arc (temporary)
            emotional_arc = {
                "joy": round(0.3 + (i * 0.08), 2),
                "sadness": round(0.4 - (i * 0.04), 2),
                "anger": round(0.2 + (i * 0.01), 2),
                "fear": round(0.3 + (i * 0.02), 2),
                "surprise": round(0.5 + (i * 0.08), 2)
            }
            
            # Get episode content
            start_idx = i * words_per_episode
            end_idx = (i + 1) * words_per_episode if i < num_episodes - 1 else word_count
            episode_content = ' '.join(words[start_idx:end_idx])
            
            episodes.append({
                "episode_number": episode_num,
                "title": f"Episode {episode_num}: {title[:20]}",
                "content": episode_content[:200] + "..." if len(episode_content) > 200 else episode_content,
                "duration_seconds": 90,
                "emotional_arc": emotional_arc,
                # These will be overwritten by Person 3's modules
                "cliffhanger_score": 0.5,  # Placeholder
                "retention_score": 0.8      # Placeholder
            })
        
        # ===== PERSON 3's ANALYTICS MODULES =====
        logger.info("📊 Calling Person 3's Analytics Modules")
        
        # Calculate cliffhanger scores and retention for each episode
        retention_curve = []
        analyzed_episodes = []
        cliffhanger_details = []
        
        for i, episode in enumerate(episodes):
            # Score cliffhanger using Person 3's module - CORRECT METHOD
            cliffhanger_result = cliffhanger_scorer.analyze_story(episode.get('content', ''))
            episode['cliffhanger_score'] = cliffhanger_result['overall_score']
            episode['cliffhanger_moments'] = cliffhanger_result['cliffhanger_moments']
            episode['cliffhanger_count'] = cliffhanger_result['cliffhanger_count']
            
            # Store for later use
            cliffhanger_details.append(cliffhanger_result)
            
            # Predict retention using Person 3's module - CORRECT METHOD
            story_data = {
                'cliffhanger_score': episode['cliffhanger_score'],
                'cliffhanger_count': episode['cliffhanger_count']
            }
            retention_result = retention_predictor.predict_retention(story_data)
            
            episode['retention_score'] = retention_result['predicted_retention']
            episode['retention_curve'] = retention_result['retention_curve'][:5]  # First 5 episodes
            episode['retention_recommendations'] = retention_result['recommendations']
            
            retention_curve.append(episode['retention_score'])
            analyzed_episodes.append(episode)
        
        # Calculate overall scores using Person 3's data
        overall_scores = {
            "emotional_depth": round(sum(e['emotional_arc']['joy'] + e['emotional_arc']['fear'] 
                                        for e in analyzed_episodes) / (num_episodes * 2), 2),
            "cliffhanger_quality": round(sum(e['cliffhanger_score'] for e in analyzed_episodes) / num_episodes, 2),
            "retention_prediction": round(sum(e['retention_score'] for e in analyzed_episodes) / num_episodes, 2),
            "coherence": 0.75
        }
        
        # Generate graph data using Person 3's module
        graph_data = {
            "cliffhanger_gauges": [],
            "retention_chart": None
        }
        
        # Add cliffhanger gauges for each episode
        for i, episode in enumerate(analyzed_episodes):
            gauge = graph_generator.generate_cliffhanger_gauge(episode['cliffhanger_score'])
            graph_data["cliffhanger_gauges"].append({
                "episode": i + 1,
                "gauge": gauge
            })
        
        # Generate retention chart using the curve from retention_predictor
        retention_data = {"retention_curve": retention_curve}
        graph_data["retention_chart"] = graph_generator.generate_retention_chart(retention_data)
        
        # ===== PERSON 4's CREATIVE MODULES =====
        logger.info("🎨 Calling Person 4's Creative Modules")
        
        # Generate twists using Person 4's module
        twists = twist_generator.generate_twists(
            story=story,
            episodes=analyzed_episodes,
            language="en",
            twists_per_episode=2
        )
        
        # Generate suggestions using Person 4's module
        suggestions = suggestion_engine.generate_suggestions(
            episodes=analyzed_episodes,
            cliffhanger_scores=[e['cliffhanger_score'] for e in analyzed_episodes],
            retention_curve=retention_curve,
            twists=twists
        )
        
        # ===== COMPILE FINAL RESULT =====
        result = {
            "story_id": cache_key[:8],
            "title": title,
            "total_episodes": num_episodes,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            
            # Person 3's analytics data
            "overall_scores": overall_scores,
            "graph_data": graph_data,
            "retention_curve": retention_curve,
            "cliffhanger_details": cliffhanger_details,
            
            # Person 2's episode data (with Person 3's scores added)
            "episodes": analyzed_episodes,
            
            # Person 4's creative data
            "twists": twists,
            "suggestions": suggestions,
            
            # Additional data
            "emotional_progression": {
                "start": analyzed_episodes[0]['emotional_arc'] if analyzed_episodes else {},
                "middle": analyzed_episodes[num_episodes//2]['emotional_arc'] if analyzed_episodes else {},
                "end": analyzed_episodes[-1]['emotional_arc'] if analyzed_episodes else {}
            }
        }
        
        # Cache the result
        cache.set(cache_key, result)
        logger.info(f"💾 Cached result for key: {cache_key[:8]}")
        
        return jsonify(create_response(
            success=True,
            data=result,
            message="Analysis complete"
        )), 200
        
    except Exception as e:
        logger.error(f"Error in analyze_story: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify(create_response(
            success=False,
            error=f"Internal server error: {str(e)}",
            status_code=500
        )), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify(create_response(
        success=False,
        error="Endpoint not found",
        status_code=404
    )), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(create_response(
        success=False,
        error="Method not allowed",
        status_code=405
    )), 405

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify(create_response(
        success=False,
        error="Internal server error",
        status_code=500
    )), 500

def initialize_data_files():
    """Create initial data files"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    sample_path = os.path.join(data_dir, 'sample_stories.json')
    cache_dir = os.path.join(data_dir, 'cache')
    
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(cache_dir, exist_ok=True)
    
    if not os.path.exists(sample_path):
        sample_stories = {
            "stories": [
                {
                    "id": "story1",
                    "title": "The Lost Key",
                    "content": "In a small town, Emma finds an old key that leads to a mysterious door. She must solve puzzles and face her fears to discover what lies behind it.",
                    "genre": "mystery"
                },
                {
                    "id": "story2",
                    "title": "Last Chance",
                    "content": "A struggling musician gets one final opportunity to make her dream come true. But the price might be higher than she imagined.",
                    "genre": "drama"
                }
            ]
        }
        write_json_file(sample_path, sample_stories)
        logger.info(f"📁 Created sample stories file")

if __name__ == '__main__':
    initialize_data_files()
    logger.info(f"🚀 Starting server on {current_config.HOST}:{current_config.PORT}")
    app.run(
        host='0.0.0.0',  # Force 0.0.0.0 for Docker
        port=current_config.PORT,
        debug=current_config.DEBUG
    )