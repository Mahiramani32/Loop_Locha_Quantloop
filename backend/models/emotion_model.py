# -*- coding: utf-8 -*-
"""
Emotion Model Module
Machine Learning model for emotion classification
"""

import numpy as np
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from typing import Dict, List, Any, Optional

class EmotionModel:
    """Machine Learning model for emotion classification"""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize emotion model
        
        Args:
            model_path: Path to pre-trained model file
        """
        self.model = None
        self.vectorizer = None
        self.is_trained = False
        self.emotion_labels = ['joy', 'sadness', 'anger', 'fear', 'surprise']
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def train(self, texts: List[str], emotions: List[str]) -> Dict[str, Any]:
        """
        Train the emotion classification model
        
        Args:
            texts: List of text samples
            emotions: List of corresponding emotion labels
            
        Returns:
            Training results
        """
        # Create pipeline
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            stop_words='english'
        )
        
        self.model = Pipeline([
            ('vectorizer', self.vectorizer),
            ('classifier', RandomForestClassifier(
                n_estimators=100,
                random_state=42
            ))
        ])
        
        # Train model
        self.model.fit(texts, emotions)
        self.is_trained = True
        
        return {
            'success': True,
            'samples': len(texts),
            'emotions': list(set(emotions))
        }
    
    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predict emotion for text
        
        Args:
            text: Input text
            
        Returns:
            Prediction results
        """
        if not self.is_trained:
            return {
                'success': False,
                'error': 'Model not trained',
                'emotion': 'unknown',
                'confidence': 0.0
            }
        
        # Get prediction
        emotion = self.model.predict([text])[0]
        
        # Get probabilities
        proba = self.model.predict_proba([text])[0]
        confidence = max(proba)
        
        # Get all probabilities
        probabilities = {}
        for label, prob in zip(self.model.classes_, proba):
            probabilities[label] = round(prob, 3)
        
        return {
            'success': True,
            'emotion': emotion,
            'confidence': round(confidence, 3),
            'probabilities': probabilities
        }
    
    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Predict emotions for multiple texts"""
        return [self.predict(text) for text in texts]
    
    def save_model(self, filepath: str = 'emotion_model.pkl') -> bool:
        """Save trained model to file"""
        try:
            model_data = {
                'model': self.model,
                'vectorizer': self.vectorizer,
                'is_trained': self.is_trained,
                'emotion_labels': self.emotion_labels
            }
            joblib.dump(model_data, filepath)
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False
    
    def load_model(self, filepath: str) -> bool:
        """Load trained model from file"""
        try:
            model_data = joblib.load(filepath)
            self.model = model_data['model']
            self.vectorizer = model_data['vectorizer']
            self.is_trained = model_data['is_trained']
            self.emotion_labels = model_data.get('emotion_labels', self.emotion_labels)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

# Create sample training data
def create_sample_data():
    """Create sample training data for demonstration"""
    texts = [
        # Joy
        "I am so happy today!",
        "This is wonderful news!",
        "I love this beautiful day",
        "She was thrilled with the surprise",
        "We had a fantastic celebration",
        
        # Sadness
        "I feel so sad and lonely",
        "He was heartbroken after the loss",
        "Tears streamed down her face",
        "The pain was unbearable",
        "She cried all night long",
        
        # Anger
        "I am so angry right now",
        "This makes me furious",
        "He was enraged by the injustice",
        "The betrayal made her see red",
        "They were frustrated with the delay",
        
        # Fear
        "I'm terrified of the dark",
        "She was scared by the noise",
        "Panic spread through the crowd",
        "He felt anxious about the future",
        "The horror movie was frightening",
        
        # Surprise
        "Wow! I didn't expect that!",
        "She was amazed by the reveal",
        "The sudden news shocked everyone",
        "He was astonished by the view",
        "What a surprising twist!"
    ]
    
    emotions = [
        'joy', 'joy', 'joy', 'joy', 'joy',
        'sadness', 'sadness', 'sadness', 'sadness', 'sadness',
        'anger', 'anger', 'anger', 'anger', 'anger',
        'fear', 'fear', 'fear', 'fear', 'fear',
        'surprise', 'surprise', 'surprise', 'surprise', 'surprise'
    ]
    
    return texts, emotions

# Test the module
if __name__ == "__main__":
    print("🔍 Testing Emotion Model")
    print("="*50)
    
    # Create model
    model = EmotionModel()
    
    # Create training data
    texts, emotions = create_sample_data()
    
    # Train model
    print("\n📊 Training model...")
    result = model.train(texts, emotions)
    print(f"✅ Trained on {result['samples']} samples")
    print(f"✅ Emotions: {result['emotions']}")
    
    # Test predictions
    test_texts = [
        "I am absolutely thrilled and excited!",
        "This is so sad and depressing",
        "I'm furious about this injustice",
        "That was completely unexpected! Wow!",
        "I'm scared and anxious about what might happen"
    ]
    
    print("\n🎯 Testing predictions:")
    for text in test_texts:
        pred = model.predict(text)
        print(f"\nText: {text[:40]}...")
        print(f"Predicted: {pred['emotion']} (confidence: {pred['confidence']})")
    
    # Save model
    model.save_model('emotion_model.pkl')
    print("\n✅ Model saved to emotion_model.pkl")
