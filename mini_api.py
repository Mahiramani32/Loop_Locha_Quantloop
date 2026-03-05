#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple Flask API for Person 2 NLP Modules
Run with: python mini_api.py
Test with: curl or Postman
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.modules.language_detector import language_detector
from backend.modules.story_decomposer import story_decomposer
from backend.modules.emotion_analyzer import emotion_analyzer
from backend.models.emotion_model import EmotionModel, create_sample_data

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize and train emotion model on startup
print("📊 Training emotion model...")
emotion_model = EmotionModel()
texts, emotions = create_sample_data()
emotion_model.train(texts, emotions)
print("✅ Emotion model ready!")

@app.route('/', methods=['GET'])
def home():
    """API home with available endpoints"""
    return jsonify({
        'name': 'Episodic Intelligence Engine - NLP API',
        'version': '1.0.0',
        'endpoints': {
            '/': 'GET - This help',
            '/health': 'GET - Health check',
            '/detect-language': 'POST - Detect language of text',
            '/decompose-story': 'POST - Decompose story structure',
            '/analyze-emotions': 'POST - Analyze emotions',
            '/timeline-90s': 'POST - 90-second emotion timeline',
            '/predict-emotion': 'POST - ML emotion prediction',
            '/analyze-all': 'POST - Complete analysis (all modules)'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'modules': {
            'language_detector': 'ready',
            'story_decomposer': 'ready',
            'emotion_analyzer': 'ready',
            'emotion_model': 'ready'
        }
    })

@app.route('/detect-language', methods=['POST'])
def detect_language():
    """Detect language of input text"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400
    
    result = language_detector.detect(data['text'])
    return jsonify(result)

@app.route('/decompose-story', methods=['POST'])
def decompose_story():
    """Decompose story structure"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400
    
    detailed = data.get('detailed', False)
    result = story_decomposer.decompose(data['text'], detailed=detailed)
    return jsonify(result)

@app.route('/analyze-emotions', methods=['POST'])
def analyze_emotions():
    """Analyze emotions in text"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400
    
    detailed = data.get('detailed', False)
    result = emotion_analyzer.analyze(data['text'], detailed=detailed)
    return jsonify(result)

@app.route('/timeline-90s', methods=['POST'])
def timeline_90s():
    """
    90-second emotion timeline (directly matches hackathon requirement)
    Divides text into 5 time blocks (18s each) for 90-second episodes
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400
    
    time_blocks = data.get('time_blocks', 5)
    result = emotion_analyzer.get_emotion_timeline(data['text'], time_blocks=time_blocks)
    
    return jsonify({
        'success': True,
        'episode_length': '90 seconds',
        'time_blocks': time_blocks,
        'timeline': result
    })

@app.route('/predict-emotion', methods=['POST'])
def predict_emotion():
    """Predict emotion using ML model"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400
    
    result = emotion_model.predict(data['text'])
    return jsonify(result)

@app.route('/analyze-all', methods=['POST'])
def analyze_all():
    """Complete analysis using all modules"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400
    
    text = data['text']
    detailed = data.get('detailed', False)
    
    # Run all modules
    lang_result = language_detector.detect(text)
    story_result = story_decomposer.decompose(text, detailed=detailed)
    emotion_result = emotion_analyzer.analyze(text, detailed=detailed)
    timeline = emotion_analyzer.get_emotion_timeline(text, time_blocks=5)
    ml_prediction = emotion_model.predict(text)
    
    return jsonify({
        'success': True,
        'language': lang_result,
        'story': story_result,
        'emotion': emotion_result,
        'timeline_90s': timeline,
        'ml_prediction': ml_prediction
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting NLP API Server")
    print("="*60)
    print("📡 Endpoints:")
    print("   GET  /              - API info")
    print("   GET  /health        - Health check")
    print("   POST /detect-language - Language detection")
    print("   POST /decompose-story - Story decomposition")
    print("   POST /analyze-emotions - Emotion analysis")
    print("   POST /timeline-90s   - 90-second timeline")
    print("   POST /predict-emotion - ML emotion prediction")
    print("   POST /analyze-all    - Complete analysis")
    print("\n🌐 Server running at http://localhost:5000")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
