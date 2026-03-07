"""
Story Decomposer Module using Qwen
Splits story into 5-8 episodes with titles and cliffhangers
Author: Person 2
"""

import sys
import os
import re
import random
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
- Give each episode a catchy title based on what happens in that episode
- Maintain story continuity across episodes
- The 'summary' should be a short 1-2 sentence logline.
- The 'description' MUST be a detailed 60-100 word narrative of exactly what happens, including scene changes, character actions, and dialogue hooks.
- Return as JSON array

Format:
[
  {{
    "number": 1,
    "title": "Title based on episode content",
    "summary": "Short summary...",
    "description": "Detailed description...",
    "cliffhanger": "Cliffhanger ending..."
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
                episodes = self.qwen.extract_json(response)
                
                if episodes and isinstance(episodes, list):
                    validated_episodes = []
                    for i, ep in enumerate(episodes):
                        if not isinstance(ep, dict):
                            ep = {}
                        
                        ep['number'] = i + 1
                        
                        if 'title' not in ep or not ep['title']:
                            ep['title'] = f"Episode {i+1}"
                        
                        if 'summary' not in ep or not ep['summary']:
                            ep['summary'] = f"Part {i+1} of the story continues."
                        
                        if 'description' not in ep or not ep['description']:
                            ep['description'] = ep.get('summary', f"Episode {i+1} content")
                        
                        if 'cliffhanger' not in ep or not ep['cliffhanger']:
                            ep['cliffhanger'] = "To be continued..." if i < num_episodes - 1 else "The end... or is it?"
                        
                        validated_episodes.append(ep)
                    
                    print(f"✅ Created {len(validated_episodes)} episodes")
                    return validated_episodes
            
        except Exception as e:
            print(f"⚠️ Story decomposition error: {e}")
        
        print("⚠️ Using enhanced fallback decomposition")
        return self._enhanced_fallback_decompose(story, num_episodes)
    
    def _enhanced_fallback_decompose(self, story, num_episodes):
        """Enhanced fallback that creates titles from the actual story content"""
        
        story = story.strip()
        
        # Split into sentences
        sentences = []
        raw_sentences = re.split(r'(?<=[.!?])\s+', story)
        for s in raw_sentences:
            if s.strip():
                sentences.append(s.strip())
        
        # Ensure we have enough segments
        if len(sentences) < num_episodes * 1.5:
            expanded = []
            for sent in sentences:
                if len(sent.split()) > 20:
                    parts = re.split(r'(?:,\s*|\s+and\s+|\s+but\s+)', sent)
                    expanded.extend([p.strip() + '.' for p in parts if len(p.strip()) > 10])
                else:
                    expanded.append(sent)
            sentences = expanded
        
        if len(sentences) < num_episodes:
            words = story.split()
            words_per_episode = max(1, len(words) // num_episodes)
            sentences = []
            for i in range(num_episodes):
                start = i * words_per_episode
                end = start + words_per_episode if i < num_episodes - 1 else len(words)
                sentences.append(' '.join(words[start:end]))
        
        episodes = []
        sentences_per_episode = max(1, len(sentences) // num_episodes)
        
        for i in range(num_episodes):
            start = i * sentences_per_episode
            end = start + sentences_per_episode if i < num_episodes - 1 else len(sentences)
            
            episode_sentences = sentences[start:end]
            base_content = ' '.join(episode_sentences)
            
            # ===== GENERATE TITLE FROM ACTUAL STORY CONTENT =====
            if episode_sentences:
                first_sentence = episode_sentences[0]
                words = first_sentence.split()
                if len(words) > 4:
                    # Take first 4-5 words for title
                    title_words = words[:min(5, len(words))]
                    title = ' '.join(title_words).rstrip('.,!?')
                    title = title[0].upper() + title[1:] if title else f"Part {i+1}"
                elif len(words) > 2:
                    title = ' '.join(words[:3]).rstrip('.,!?')
                else:
                    title = first_sentence.rstrip('.,!?')
            else:
                title = f"Episode {i+1}"
            
            # Create summary
            summary = episode_sentences[0] if episode_sentences else f"Episode {i+1}"
            if len(summary) > 80:
                summary = summary[:80] + "..."
            
            # Description is the actual content
            description = base_content
            
            # Cliffhanger based on next episode
            if i < num_episodes - 1 and end < len(sentences):
                next_hint = sentences[end][:50]
                cliffhanger = f"Little did they know, {next_hint.lower()} would change everything..."
            elif i < num_episodes - 1:
                cliffhanger = "But something unexpected was about to happen..."
            else:
                cliffhanger = "The story reaches its conclusion, but some mysteries remain..."
            
            episodes.append({
                "number": i + 1,
                "title": title,
                "summary": summary,
                "description": description,
                "cliffhanger": cliffhanger
            })
        
        return episodes


# Convenience function
def decompose_story(story, num_episodes=5, language="en"):
    decomposer = StoryDecomposer()
    return decomposer.decompose(story, num_episodes, language)