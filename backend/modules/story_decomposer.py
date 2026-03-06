"""
Story Decomposer Module using Qwen
Splits story into 5-8 episodes with titles and cliffhangers
Author: Person 2
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.qwen_model import get_qwen_model
import json

class StoryDecomposer:
    """
    Decomposes story into episodes using Qwen
    """
    
    def __init__(self):
        """Initialize with Qwen"""
        self.qwen = get_qwen_model()
        print("✅ StoryDecomposer initialized with Qwen")
    
    def decompose(self, story, num_episodes=5, language="en"):
        """
        Split story into episodes using Qwen
        
        Args:
            story (str): Full story text
            num_episodes (int): Number of episodes (5-8)
            language (str): Language code
        
        Returns:
            list: List of episode dictionaries
        """
        print(f"\n📖 Decomposing story into {num_episodes} episodes...")
        
        # System prompt for Qwen
        system_prompt = """You are a professional scriptwriter who creates engaging episodic content for vertical videos (90 seconds each episode)."""
        
        # User prompt
        prompt = f"""Task: Split this story into {num_episodes} episodes for a vertical video series.

Story: {story}

Requirements:
- Each episode must be ~90 seconds when filmed
- End each episode with a cliffhanger to make viewers want the next episode
- Give each episode a catchy title
- Maintain story continuity across episodes
- Return as JSON array

Format:
[
  {{
    "number": 1,
    "title": "The Discovery",
    "summary": "What happens in this episode...",
    "cliffhanger": "Suddenly, something shocking happens..."
  }},
  ...
]

Return ONLY the JSON array, no other text."""

        try:
            # Get response from Qwen
            response = self.qwen.chat_completion(
                system_prompt=system_prompt,
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )
            
            if response:
                # Extract JSON from response
                episodes = self.qwen.extract_json(response)
                
                if episodes and isinstance(episodes, list):
                    print(f"✅ Created {len(episodes)} episodes")
                    return episodes
            
        except Exception as e:
            print(f"⚠️ Story decomposition error: {e}")
        
        # Fallback to simple decomposition
        print("⚠️ Using fallback decomposition")
        return self._fallback_decompose(story, num_episodes)
    
    def _fallback_decompose(self, story, num_episodes):
        """Simple fallback if Qwen fails"""
        # Split into sentences
        sentences = story.split('.')
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        episodes = []
        sentences_per_episode = max(1, len(sentences) // num_episodes)
        
        for i in range(num_episodes):
            start = i * sentences_per_episode
            end = start + sentences_per_episode if i < num_episodes - 1 else len(sentences)
            
            episode_text = '. '.join(sentences[start:end])
            
            episodes.append({
                "number": i + 1,
                "title": f"Episode {i+1}",
                "summary": episode_text,
                "cliffhanger": "To be continued..." if i < num_episodes - 1 else "The end... or is it?"
            })
        
        return episodes


# Convenience function
def decompose_story(story, num_episodes=5, language="en"):
    decomposer = StoryDecomposer()
    return decomposer.decompose(story, num_episodes, language)


if __name__ == "__main__":
    # Self-test
    print("=" * 50)
    print("STORY DECOMPOSER - TEST")
    print("=" * 50)
    
    decomposer = StoryDecomposer()
    
    test_story = """
    A detective named Priya finds a mysterious key at a crime scene. 
    The key glows in her hand and she hears whispers. She discovers 
    a hidden door that appears only at midnight. When she opens it, 
    she sees her dead partner alive in a parallel world. She must 
    choose between staying in this perfect world or returning home. 
    But something evil follows her through the door.
    """
    
    episodes = decomposer.decompose(test_story, num_episodes=5)
    
    for ep in episodes:
        print(f"\n📺 Episode {ep['number']}: {ep['title']}")
        print(f"   Summary: {ep['summary'][:80]}...")
        print(f"   Cliffhanger: {ep['cliffhanger']}")