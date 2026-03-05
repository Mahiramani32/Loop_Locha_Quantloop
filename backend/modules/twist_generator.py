"""
Twist Generator Module
Generates creative plot twists for episodes using twist_bank.json
Author: Shreya (Person 4)
"""

import json
import random
import os
from pathlib import Path

class TwistGenerator:
    """
    A class that generates plot twists for story episodes
    """
    
    def __init__(self):
        """Initialize the twist generator and load twist bank"""
        self.twist_bank = self._load_twist_bank()
        print("✅ TwistGenerator initialized with", sum(len(v) for v in self.twist_bank.values()), "twists")
        
    def _load_twist_bank(self):
        """
        Load twist templates from JSON file
        Returns a dictionary of twist categories and lists
        """
        # Find the twist_bank.json file
        # Get the directory where this file is located
        current_file = Path(__file__)  # backend/modules/twist_generator.py
        modules_dir = current_file.parent  # backend/modules/
        backend_dir = modules_dir.parent  # backend/
        models_path = backend_dir / 'models' / 'twist_bank.json'
        
        print(f"Looking for twist bank at: {models_path}")
        
        try:
            with open(models_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                print(f"✅ Loaded {len(data)} twist categories")
                return data
        except FileNotFoundError:
            print(f"❌ Twist bank file not found at {models_path}")
            print("Using default twists instead")
            # Return default twists if file not found
            return {
                "betrayal": ["Someone betrays the hero."],
                "revelation": ["A shocking truth is revealed."],
                "suspense": ["Something is not what it seems."]
            }
        except json.JSONDecodeError:
            print(f"❌ Error parsing JSON file")
            return self._get_default_twists()
    
    def _get_default_twists(self):
        """Return default twists if file loading fails"""
        return {
            "betrayal": ["A trusted friend reveals their true colors."],
            "revelation": ["The hero discovers a hidden truth about their past."],
            "suspense": ["Danger lurks where they least expect it."]
        }
    
    def generate_twists(self, story, episodes, language="en", twists_per_episode=1):
        """
        Generate twists for each episode
        
        Args:
            story (str): Original story text
            episodes (list): List of episode dictionaries
            language (str): Language code (default: "en")
            twists_per_episode (int): Number of twists per episode (default: 1)
        
        Returns:
            list: List of twists per episode
        """
        print(f"\n🎭 Generating {twists_per_episode} twist(s) per episode...")
        
        result = []
        
        for episode_index, episode in enumerate(episodes, 1):
            # Get episode details
            episode_title = episode.get('title', f'Episode {episode_index}')
            episode_summary = episode.get('summary', '')
            episode_cliffhanger = episode.get('cliffhanger', '')
            
            print(f"  Processing Episode {episode_index}: {episode_title}")
            
            # Generate twists for this episode
            episode_twists = []
            
            for twist_num in range(twists_per_episode):
                # Generate a twist based on episode context
                twist = self._generate_contextual_twist(
                    episode_index, 
                    episode_summary, 
                    episode_cliffhanger
                )
                episode_twists.append(twist)
            
            result.append({
                "episode": episode_index,
                "title": episode_title,
                "twists": episode_twists
            })
        
        print(f"✅ Generated twists for {len(result)} episodes")
        return result
    
    def _generate_contextual_twist(self, episode_num, summary, cliffhanger):
        """
        Generate a twist considering episode context
        
        Args:
            episode_num (int): Episode number
            summary (str): Episode summary
            cliffhanger (str): Episode cliffhanger
        
        Returns:
            str: A generated twist
        """
        # Choose random category based on episode number
        if episode_num == 1:
            # First episode: setup twists
            categories = ["revelation", "mystery"]
        elif episode_num == 3:
            # Middle episode: major twists
            categories = ["betrayal", "identity", "time"]
        elif episode_num >= 5:
            # Final episodes: big reveals
            categories = ["revelation", "identity", "moral_dilemma"]
        else:
            # Other episodes: any category
            categories = list(self.twist_bank.keys())
        
        # Pick a random category from available ones
        available_categories = [c for c in categories if c in self.twist_bank]
        if not available_categories:
            available_categories = list(self.twist_bank.keys())
        
        category = random.choice(available_categories)
        
        # Pick a random twist from that category
        twists_in_category = self.twist_bank[category]
        twist_template = random.choice(twists_in_category)
        
        # Add some context from the episode if available
        if summary and len(summary) > 10:
            # Take first few words of summary to personalize
            words = summary.split()[:3]
            context = " ".join(words)
            twist = f"About {context}... {twist_template}"
        else:
            twist = twist_template
        
        # Add prefix based on episode position
        if episode_num == 1:
            prefix = "🔮 Opening twist: "
        elif episode_num == len(episodes) if 'episodes' in locals() else False:
            prefix = "🎬 Finale shocker: "
        elif episode_num == 3:
            prefix = "⚡ Mid-point surprise: "
        else:
            prefix = "✨ Twist: "
        
        return prefix + twist
    
    def add_twist_category(self, category_name, twist_list):
        """
        Add a new twist category to the bank
        
        Args:
            category_name (str): Name of the category
            twist_list (list): List of twist strings
        
        Returns:
            bool: True if added successfully
        """
        if category_name not in self.twist_bank:
            self.twist_bank[category_name] = twist_list
            self._save_twist_bank()
            print(f"✅ Added new category: {category_name}")
            return True
        else:
            print(f"❌ Category '{category_name}' already exists")
            return False
    
    def add_twist_to_category(self, category_name, twist):
        """
        Add a single twist to an existing category
        
        Args:
            category_name (str): Name of the category
            twist (str): Twist to add
        
        Returns:
            bool: True if added successfully
        """
        if category_name in self.twist_bank:
            self.twist_bank[category_name].append(twist)
            self._save_twist_bank()
            print(f"✅ Added twist to {category_name}")
            return True
        else:
            print(f"❌ Category '{category_name}' not found")
            return False
    
    def _save_twist_bank(self):
        """Save the current twist bank back to the JSON file"""
        try:
            current_file = Path(__file__)
            modules_dir = current_file.parent
            backend_dir = modules_dir.parent
            models_path = backend_dir / 'models' / 'twist_bank.json'
            
            with open(models_path, 'w', encoding='utf-8') as file:
                json.dump(self.twist_bank, file, indent=2, ensure_ascii=False)
            print("✅ Twist bank saved successfully")
        except Exception as e:
            print(f"❌ Error saving twist bank: {e}")
    
    def get_statistics(self):
        """Get statistics about the twist bank"""
        stats = {
            "total_categories": len(self.twist_bank),
            "total_twists": sum(len(v) for v in self.twist_bank.values()),
            "categories": {}
        }
        
        for category, twists in self.twist_bank.items():
            stats["categories"][category] = len(twists)
        
        return stats


# Convenience function for easy import
def generate_twists(story, episodes, language="en", count=1):
    """
    Easy-to-use function to generate twists
    
    Args:
        story (str): Original story
        episodes (list): List of episodes
        language (str): Language code
        count (int): Number of twists per episode
    
    Returns:
        list: Generated twists
    """
    generator = TwistGenerator()
    return generator.generate_twists(story, episodes, language, count)


# If this file is run directly, run a test
if __name__ == "__main__":
    print("=" * 60)
    print("TWIST GENERATOR - SELF TEST")
    print("=" * 60)
    
    # Create test data
    test_story = "A detective finds a mysterious key that opens a door to a parallel world"
    
    test_episodes = [
        {
            "title": "The Discovery",
            "summary": "Detective Raj finds an old key at a crime scene that glows in the dark.",
            "cliffhanger": "As he touches the key, everything goes dark and he hears a whisper."
        },
        {
            "title": "The Door",
            "summary": "Raj discovers a door that only appears at midnight. The key fits perfectly.",
            "cliffhanger": "He opens the door and sees his dead partner standing there, alive."
        },
        {
            "title": "The Choice",
            "summary": "In the parallel world, Raj's partner is alive but doesn't recognize him.",
            "cliffhanger": "Someone from his world follows him through the door with a gun."
        }
    ]
    
    # Create generator instance
    generator = TwistGenerator()
    
    # Show stats
    stats = generator.get_statistics()
    print(f"\n📊 Twist Bank Statistics:")
    print(f"   - {stats['total_categories']} categories")
    print(f"   - {stats['total_twists']} total twists")
    for cat, count in stats['categories'].items():
        print(f"     • {cat}: {count} twists")
    
    # Generate twists
    print("\n🎭 Generating twists...")
    results = generator.generate_twists(test_story, test_episodes, count=2)
    
    # Print results
    print("\n" + "=" * 60)
    print("GENERATED TWISTS")
    print("=" * 60)
    
    for episode_result in results:
        print(f"\n📺 Episode {episode_result['episode']}: {episode_result['title']}")
        for i, twist in enumerate(episode_result['twists'], 1):
            print(f"   {i}. {twist}")
    
    print("\n✅ Test complete!")