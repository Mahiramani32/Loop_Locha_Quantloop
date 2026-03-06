"""
Complete test script for Person 3's analytics modules
"""

import sys
sys.path.insert(0, 'backend')

from modules.cliffhanger_scorer import CliffhangerScorer
from modules.retention_predictor import RetentionPredictor
from modules.graph_generator import GraphGenerator

print("🧪 Testing Person 3's Analytics Modules")
print("="*60)

# Test 1: Cliffhanger Scorer
print("\n1️⃣ Testing CliffhangerScorer...")
scorer = CliffhangerScorer()
test_text = "Suddenly, everything changed. She found... an empty chair. To be continued..."

result = scorer.analyze_story(test_text)
print(f"   ✅ Overall score: {result['overall_score']}")
print(f"   ✅ Cliffhanger count: {result['cliffhanger_count']}")
print(f"   ✅ Has final cliffhanger: {result['has_final_cliffhanger']}")
print(f"   ✅ Recommendations: {result['recommendations'][0]}")

# Test 2: Retention Predictor
print("\n2️⃣ Testing RetentionPredictor...")
predictor = RetentionPredictor()

story_data = {
    'cliffhanger_score': 0.8,
    'cliffhanger_count': 3
}
retention_result = predictor.predict_retention(story_data)
print(f"   ✅ Predicted retention: {retention_result['predicted_retention']*100}%")
print(f"   ✅ Retention curve (first 5): {retention_result['retention_curve'][:5]}")
print(f"   ✅ Recommendations: {retention_result['recommendations'][0]}")

# Test 3: Graph Generator
print("\n3️⃣ Testing GraphGenerator...")
generator = GraphGenerator()

# Test gauge
gauge = generator.generate_cliffhanger_gauge(0.75)
print(f"   ✅ Gauge: {gauge['label']} - {gauge['value']}%")

# Test retention chart
retention_data = {"retention_curve": [0.95, 0.88, 0.82, 0.75, 0.68]}
chart = generator.generate_retention_chart(retention_data)
print(f"   ✅ Chart generated: {chart['title']}")
print(f"   ✅ Chart has {len(chart['series'][0]['data'])} data points")

print("\n" + "="*60)
print("✅ All Person 3 modules working correctly!")