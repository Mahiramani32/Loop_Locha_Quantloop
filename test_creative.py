"""
Tests for Person 4's creative modules
FINAL WORKING VERSION
"""

import unittest
import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Now import from modules (which is in backend/)
from modules.twist_generator import TwistGenerator
from modules.suggestion_engine import SuggestionEngine

class TestCreativeModules(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        print("\n" + "="*50)
        print("Setting up test for Person 4's modules")
        print("="*50)
        
        self.twist_gen = TwistGenerator()
        self.suggest_engine = SuggestionEngine()
        
        self.sample_episodes = [
            {
                "episode_number": 1,
                "content": "Episode 1 content",
                "emotional_arc": {"joy": 0.5, "fear": 0.3},
                "cliffhanger_score": 0.6,
                "retention_score": 0.95
            },
            {
                "episode_number": 2,
                "content": "Episode 2 content",
                "emotional_arc": {"joy": 0.6, "fear": 0.4},
                "cliffhanger_score": 0.7,
                "retention_score": 0.92
            }
        ]
    
    def test_twist_generator_imports(self):
        """Test that twist generator can be imported"""
        print("\n🧪 Testing TwistGenerator import...")
        self.assertIsNotNone(self.twist_gen)
        print("✅ TwistGenerator imported successfully")
    
    def test_suggestion_engine_imports(self):
        """Test that suggestion engine can be imported"""
        print("\n🧪 Testing SuggestionEngine import...")
        self.assertIsNotNone(self.suggest_engine)
        print("✅ SuggestionEngine imported successfully")
    
    def test_generate_twists(self):
        """Test twist generation"""
        print("\n🧪 Testing twist generation...")
        try:
            # Create a dummy story for testing
            dummy_story = "A test story about a brave knight."
            
            # Call with ALL required arguments
            twists = self.twist_gen.generate_twists(
                story=dummy_story,
                episodes=self.sample_episodes,
                language="en",
                twists_per_episode=2
            )
            self.assertIsNotNone(twists)
            print(f"✅ Generated twists successfully")
            if twists:
                print(f"   Number of episodes with twists: {len(twists)}")
        except Exception as e:
            print(f"❌ Error generating twists: {e}")
            raise
    
    def test_generate_suggestions(self):
        """Test suggestion generation"""
        print("\n🧪 Testing suggestion generation...")
        try:
            # First generate some twists
            dummy_story = "A test story about a brave knight."
            twists = self.twist_gen.generate_twists(
                story=dummy_story,
                episodes=self.sample_episodes,
                language="en",
                twists_per_episode=1
            )
            
            # Then generate suggestions
            suggestions = self.suggest_engine.generate_suggestions(
                episodes=self.sample_episodes,
                language="en",
                max_suggestions=5
            )
            self.assertIsNotNone(suggestions)
            print(f"✅ Generated suggestions successfully")
        except Exception as e:
            print(f"❌ Error generating suggestions: {e}")
            raise

if __name__ == '__main__':
    print("\n🎯 RUNNING PERSON 4'S CREATIVE MODULE TESTS")
    print("="*50)
    unittest.main(verbosity=2)