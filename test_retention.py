from backend.modules.retention_predictor import RetentionPredictor

predictor = RetentionPredictor()

# Test cases
test_cases = [
    {
        "name": "Weak Story",
        "data": {
            'cliffhanger_score': 0.2,
            'cliffhanger_count': 0
        }
    },
    {
        "name": "Good Story", 
        "data": {
            'cliffhanger_score': 0.7,
            'cliffhanger_count': 3
        }
    },
    {
        "name": "Great Story",
        "data": {
            'cliffhanger_score': 0.9,
            'cliffhanger_count': 5
        }
    }
]

for test in test_cases:
    print(f"\n--- {test['name']} ---")
    result = predictor.predict_retention(test['data'])
    print(f"Retention: {result['predicted_retention']*100}%")
    print(f"First 3 episodes: {result['retention_curve'][:3]}")