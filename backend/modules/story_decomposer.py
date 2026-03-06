"""
Story Decomposer Module using Qwen
Splits story into 5-8 episodes with titles and cliffhangers
Author: Person 2
"""

import sys
import os
import re
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
        
        # User prompt - UPDATED to include description field
        prompt = f"""Task: Split this story into {num_episodes} episodes for a vertical video series.

Story: {story}

Requirements:
- Each episode must be ~90 seconds when filmed
- End each episode with a cliffhanger to make viewers want the next episode
- Give each episode a catchy title
- Maintain story continuity across episodes
- The 'summary' should be a short 1-2 sentence logline.
- The 'description' MUST be a detailed 60-100 word narrative of exactly what happens, including scene changes, character actions, and dialogue hooks.
- Return as JSON array

Format:
[
  {{
    "number": 1,
    "title": "The Discovery",
    "summary": "Priya finds a mysterious key.",
    "description": "Detective Priya arrives at the crime scene in the pouring rain. While inspecting the victim's abandoned car, she notices a strange glowing key tucked beneath the floor mat. As she touches it, visions flash before her eyes. She hears a whisper: 'Find the door...'",
    "cliffhanger": "Suddenly, the key begins to glow brighter and a mysterious figure appears in the shadows."
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
                    # Ensure each episode has all required fields
                    validated_episodes = []
                    for i, ep in enumerate(episodes):
                        # Make sure we have a valid episode dict
                        if not isinstance(ep, dict):
                            ep = {}
                        
                        # Ensure number is correct
                        ep['number'] = i + 1
                        
                        # Ensure title exists - THIS IS CRITICAL!
                        if 'title' not in ep or not ep['title']:
                            ep['title'] = f"Episode {i+1}"
                        
                        # Ensure summary exists
                        if 'summary' not in ep or not ep['summary']:
                            ep['summary'] = f"Part {i+1} of the story continues."
                        
                        # Ensure description exists
                        if 'description' not in ep or not ep['description']:
                            ep['description'] = ep.get('summary', f"Episode {i+1} content")
                        
                        # Ensure cliffhanger exists
                        if 'cliffhanger' not in ep or not ep['cliffhanger']:
                            ep['cliffhanger'] = "To be continued..." if i < num_episodes - 1 else "The end... or is it?"
                        
                        validated_episodes.append(ep)
                    
                    print(f"✅ Created {len(validated_episodes)} episodes")
                    return validated_episodes
            
        except Exception as e:
            print(f"⚠️ Story decomposition error: {e}")
        
        # Fallback to simple decomposition with proper fields
        print("⚠️ Using enhanced fallback decomposition")
        return self._enhanced_fallback_decompose(story, num_episodes)
    
    def _enhanced_fallback_decompose(self, story, num_episodes):
        """Enhanced fallback with proper fields"""
        import re
        
        # Split into sentences
        sentences = [s.strip() + '.' for s in story.split('.') if len(s.strip()) > 10]
        
        if len(sentences) < num_episodes:
            # Not enough sentences, split by words
            words = story.split()
            words_per_episode = max(1, len(words) // num_episodes)
            episodes = []
            
            for i in range(num_episodes):
                start = i * words_per_episode
                end = start + words_per_episode if i < num_episodes - 1 else len(words)
                episode_text = ' '.join(words[start:end])
                
                # Create a proper title
                title = f"Episode {i+1}"
                if i == 0:
                    title = "The Beginning"
                elif i == num_episodes - 1:
                    title = "The Final Chapter"
                else:
                    title = f"Part {i+1}"
                
                # Create a proper description
                description = episode_text
                if len(description) < 100:
                    description += " This episode continues the story with exciting developments and character moments."
                
                episodes.append({
                    "number": i + 1,
                    "title": title,
                    "summary": episode_text[:80] + "..." if len(episode_text) > 80 else episode_text,
                    "description": description,
                    "cliffhanger": "To be continued..." if i < num_episodes - 1 else "The end... or is it?"
                })
            return episodes
        
        # Distribute sentences across episodes
        sentences_per_episode = max(1, len(sentences) // num_episodes)
        episodes = []
        
        # Titles for episodes
        titles = [
            "The Discovery", "The Mystery Deepens", "Hidden Truths",
            "Unexpected Turns", "The Revelation", "Final Confrontation",
            "The Aftermath", "New Beginning"
        ]
        
        for i in range(num_episodes):
            start = i * sentences_per_episode
            end = start + sentences_per_episode if i < num_episodes - 1 else len(sentences)
            
            # Combine sentences for this episode
            episode_sentences = sentences[start:end]
            summary = ' '.join(episode_sentences[:2])  # First 2 sentences as summary
            description = ' '.join(episode_sentences)  # All sentences as description
            
            # Add narrative flair if description is too short
            if len(description.split()) < 50:
                description += " The tension builds as the characters face new challenges and unexpected revelations unfold."
            
            # Get title from list or generate
            title = titles[i] if i < len(titles) else f"Episode {i+1}"
            
            episodes.append({
                "number": i + 1,
                "title": title,
                "summary": summary[:100] + "..." if len(summary) > 100 else summary,
                "description": description,
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
        print(f"   Description: {ep['description'][:100]}...")
        print(f"   Cliffhanger: {ep['cliffhanger']}")