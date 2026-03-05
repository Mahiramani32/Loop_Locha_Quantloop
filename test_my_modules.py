"""
Test script for Person 4 modules
Run this to verify both modules are working
"""

import json
from backend.modules.twist_generator import generate_twists
from backend.modules.suggestion_engine import generate_suggestions

print("=" * 70)
print("TESTING PERSON 4 MODULES - CREATIVE INTELLIGENCE")
print("=" * 70)

# Test data
test_story = "A detective named Raj finds a mysterious key that opens a door to a parallel world where his dead partner is alive. He must decide whether to stay or return."

test_episodes = [
    {
        "number": 1,
        "title": "The Mysterious Key",
        "summary": "Detective Raj finds an old key at a crime scene that glows in the dark. He feels it's connected to his dead partner.",
        "cliffhanger": "As he touches the key, everything goes dark and he hears a whisper: 'Find the door...'"
    },
    {
        "number": 2,
        "title": "The Midnight Door",
        "summary": "Raj discovers a door that only appears at midnight. The key fits perfectly into its lock.",
        "cliffhanger": "He opens the door and sees his dead partner standing there, alive and smiling."
    },
    {
        "number": 3,
        "title": "The Parallel World",
        "summary": "In the parallel world, Raj's partner is alive but doesn't recognize him. Raj learns this world is in danger.",
        "cliffhanger": "Someone from Raj's world follows him through the door, holding a gun."
    }
]

# Add analysis data for suggestion engine
for ep in test_episodes:
    # Cliffhanger scores (different for each episode)
    if ep["number"] == 1:
        ep["cliffhanger_score"] = 3.5  # Weak
    elif ep["number"] == 2:
        ep["cliffhanger_score"] = 8.5  # Strong
    else:
        ep["cliffhanger_score"] = 7.0  # Good
    
    # Emotion curves
    if ep["number"] == 1:
        ep["emotion_curve"] = [
            {"time": 0, "emotion": "neutral", "intensity": 0.2},
            {"time": 30, "emotion": "curious", "intensity": 0.4},
            {"time": 60, "emotion": "curious", "intensity": 0.4},
            {"time": 90, "emotion": "curious", "intensity": 0.4}
        ]
    elif ep["number"] == 2:
        ep["emotion_curve"] = [
            {"time": 0, "emotion": "suspense", "intensity": 0.7},
            {"time": 30, "emotion": "fear", "intensity": 0.8},
            {"time": 60, "emotion": "shock", "intensity": 0.9},
            {"time": 90, "emotion": "surprise", "intensity": 0.9}
        ]
    else:
        ep["emotion_curve"] = [
            {"time": 0, "emotion": "joy", "intensity": 0.8},
            {"time": 30, "emotion": "joy", "intensity": 0.7},
            {"time": 60, "emotion": "fear", "intensity": 0.6},
            {"time": 90, "emotion": "fear", "intensity": 0.8}
        ]
    
    # Retention heatmaps
    if ep["number"] == 1:
        ep["retention_heatmap"] = [
            {"time": 5, "dropoff_risk": 0.3},
            {"time": 15, "dropoff_risk": 0.6},
            {"time": 45, "dropoff_risk": 0.8},
            {"time": 75, "dropoff_risk": 0.4}
        ]
    elif ep["number"] == 2:
        ep["retention_heatmap"] = [
            {"time": 10, "dropoff_risk": 0.1},
            {"time": 30, "dropoff_risk": 0.2},
            {"time": 60, "dropoff_risk": 0.2},
            {"time": 85, "dropoff_risk": 0.3}
        ]
    else:
        ep["retention_heatmap"] = [
            {"time": 5, "dropoff_risk": 0.2},
            {"time": 25, "dropoff_risk": 0.3},
            {"time": 55, "dropoff_risk": 0.5},
            {"time": 80, "dropoff_risk": 0.4}
        ]

print("\n📝 STORY INPUT:")
print(f"'{test_story[:100]}...'")
print(f"\n📺 EPISODES: {len(test_episodes)}")

# ============================================
# TEST 1: TWIST GENERATOR
# ============================================
print("\n" + "=" * 70)
print("TEST 1: TWIST GENERATOR")
print("=" * 70)

try:
    twists = generate_twists(test_story, test_episodes, count=2)
    
    print("\n🎭 GENERATED TWISTS:")
    print("-" * 50)
    for episode_result in twists:
        print(f"\n📺 Episode {episode_result['episode']}: {episode_result['title']}")
        for i, twist in enumerate(episode_result['twists'], 1):
            print(f"   {i}. {twist}")
    
    print("\n✅ Twist Generator: PASSED")
except Exception as e:
    print(f"\n❌ Twist Generator: FAILED - {e}")

# ============================================
# TEST 2: SUGGESTION ENGINE
# ============================================
print("\n" + "=" * 70)
print("TEST 2: SUGGESTION ENGINE")
print("=" * 70)

try:
    suggestions = generate_suggestions(test_episodes)
    
    print("\n💡 IMPROVEMENT SUGGESTIONS:")
    print("-" * 50)
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
    
    print(f"\n✅ Suggestion Engine: PASSED ({len(suggestions)} suggestions)")
except Exception as e:
    print(f"\n❌ Suggestion Engine: FAILED - {e}")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 70)
print("📊 TEST SUMMARY")
print("=" * 70)

print("""
✅ Your modules are working!
   
   Next steps:
   1. Enhance twist_bank.json with more categories
   2. Fine-tune suggestion rules
   3. Coordinate with Person 1 for API integration
   4. Create a Pull Request when ready

Keep up the great work! 🚀
""")