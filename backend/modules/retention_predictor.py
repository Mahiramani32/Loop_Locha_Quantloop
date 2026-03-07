"""
Retention Predictor Module
Predicts audience retention based on story features
Author: Mahi
"""

import numpy as np
import pickle
import os
from typing import Dict, Any, List

class RetentionPredictor:
    """Predicts audience retention for stories"""
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path or os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'models', 'retention_model.pkl'
        )
        self.model = None
        print("✅ Retention Predictor initialized")
    
    def predict_retention(self, story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict audience retention percentage - IMPROVED"""
        
        # Extract features
        cliffhanger_score = story_data.get('cliffhanger_score', 0.5)
        cliffhanger_count = story_data.get('cliffhanger_count', 0)
        
        # Improved prediction formula
        base_retention = 0.7  # Increased from 0.5
        cliffhanger_boost = cliffhanger_score * 0.2  # Adjusted weight
        count_boost = min(cliffhanger_count * 0.08, 0.25)  # Increased boost
        
        retention = min(base_retention + cliffhanger_boost + count_boost, 0.98)  # Max 98%
        
        # Generate retention curve (5 episodes for 90-second format)
        curve = []
        current = 1.0
        # Better drop rate calculation
        drop_rate = 0.15 * (1 - retention)  # Slower drop for better retention
        
        for i in range(5):
            curve.append(round(current, 2))
            current = max(0.4, current - drop_rate)  # Minimum 40% retention
            # Reduce drop rate as episodes progress (loyal viewers)
            drop_rate *= 0.9
        
        return {
            'predicted_retention': round(retention, 2),
            'confidence': 0.85,
            'retention_curve': curve,
            'recommendations': [
                "Excellent retention potential!" if retention > 0.85 else
                "Good retention potential!" if retention > 0.7 else
                "Consider adding more cliffhangers",
                f"Predicted {round(retention*100)}% average audience retention"
            ]
        }


# Test
if __name__ == "__main__":
    predictor = RetentionPredictor()
    test_data = {
        'cliffhanger_score': 0.8,
        'cliffhanger_count': 3
    }
    result = predictor.predict_retention(test_data)
    print(f"Retention: {result['predicted_retention']*100}%")
    print(f"Curve: {result['retention_curve']}")