"""
Emotion Analyzer Module using Qwen
Analyzes emotional progression in episodes
Author: Person 2
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.qwen_model import get_qwen_model
import json

class EmotionAnalyzer:
    """
    Analyzes emotions using Qwen model
    """
    
    def __init__(self):
        """Initialize with Qwen"""
        self.qwen = get_qwen_model()
        self.emotions = ['anger', 'fear', 'joy', 'sadness', 'surprise', 'disgust', 'neutral']
        print("✅ EmotionAnalyzer initialized with Qwen")
    
    def analyze_episode(self, episode_text, episode_number, num_segments=4):
        """
        Analyze emotions in an episode
        
        Args:
            episode_text (str): The episode text to analyze
            episode_number (int): Episode number
            num_segments (int): Number of time segments (for 90-second video)
        
        Returns:
            dict: Emotion analysis results
        """
        # Split text into segments for timeline
        words = episode_text.split()
        if len(words) < num_segments:
            # Text too short, use whole text
            segments = [episode_text] * num_segments
        else:
            # Split into segments
            segment_size = len(words) // num_segments
            segments = []
            for i in range(num_segments):
                start = i * segment_size
                end = start + segment_size if i < num_segments - 1 else len(words)
                segments.append(' '.join(words[start:end]))
        
        emotion_curve = []
        
        # Analyze each segment
        for i, segment in enumerate(segments):
            time = int((i / num_segments) * 90)  # Time in seconds
            
            # Get emotion for this segment
            emotion_data = self._get_emotion(segment)
            
            emotion_curve.append({
                "time": time,
                "emotion": emotion_data['dominant'],
                "intensity": emotion_data['intensity'],
                "all_emotions": emotion_data['scores']
            })
        
        # Calculate statistics
        stats = self._calculate_statistics(emotion_curve)
        
        return {
            "episode": episode_number,
            "emotion_curve": emotion_curve,
            "statistics": stats
        }
    
    def _get_emotion(self, text):
        """
        Get emotion from text using Qwen
        """
        prompt = f"""Task: Analyze the emotion in this text.

Text: "{text}"

Return a JSON object with scores (0-1) for these emotions:
- anger
- fear
- joy
- sadness
- surprise
- disgust
- neutral

Make sure scores sum to approximately 1.0.

Example: {{"anger": 0.1, "fear": 0.7, "joy": 0.0, "sadness": 0.1, "surprise": 0.05, "disgust": 0.0, "neutral": 0.05}}

Return ONLY the JSON object, no other text."""

        try:
            response = self.qwen.chat_completion(
                prompt=prompt,
                temperature=0.3,
                max_tokens=200
            )
            
            if response:
                emotions = self.qwen.extract_json(response)
                if emotions and isinstance(emotions, dict):
                    # Find dominant emotion
                    dominant = max(emotions.items(), key=lambda x: x[1])
                    return {
                        "dominant": dominant[0],
                        "intensity": dominant[1],
                        "scores": emotions
                    }
            
        except Exception as e:
            print(f"⚠️ Emotion analysis error: {e}")
        
        # Fallback
        return {
            "dominant": "neutral",
            "intensity": 0.5,
            "scores": {e: 0.14 for e in self.emotions}
        }
    
    def _calculate_statistics(self, emotion_curve):
        """Calculate emotion statistics"""
        if not emotion_curve:
            return {}
        
        # Count dominant emotions
        emotion_counts = {}
        for point in emotion_curve:
            emotion = point['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Calculate average intensity
        avg_intensity = sum(p['intensity'] for p in emotion_curve) / len(emotion_curve)
        
        return {
            "dominant_emotions": emotion_counts,
            "emotional_range": len(set(p['emotion'] for p in emotion_curve)),
            "average_intensity": avg_intensity,
            "total_segments": len(emotion_curve)
        }
    
    def analyze_episodes(self, episodes, language="en"):
        """
        Analyze emotions for all episodes
        
        Args:
            episodes (list): List of episode dicts with 'summary' and 'cliffhanger'
            language (str): Language code
        
        Returns:
            list: Emotion analysis for each episode
        """
        print(f"\n🎭 Analyzing emotions for {len(episodes)} episodes...")
        
        results = []
        
        for i, episode in enumerate(episodes, 1):
            # Combine summary and cliffhanger for analysis
            episode_text = episode.get('summary', '')
            cliffhanger = episode.get('cliffhanger', '')
            
            if cliffhanger:
                episode_text += " " + cliffhanger
            
            if not episode_text:
                print(f"⚠️ Episode {i} has no text, skipping")
                continue
            
            print(f"  Processing Episode {i}...")
            
            result = self.analyze_episode(episode_text, i)
            results.append(result)
        
        print(f"✅ Analyzed {len(results)} episodes")
        return results


# Convenience function
def analyze_emotions(episodes, language="en"):
    analyzer = EmotionAnalyzer()
    return analyzer.analyze_episodes(episodes, language)


if __name__ == "__main__":
    # Self-test
    print("=" * 50)
    print("EMOTION ANALYZER - TEST")
    print("=" * 50)
    
    analyzer = EmotionAnalyzer()
    
    test_episodes = [
        {
            "summary": "A detective finds a mysterious key at a crime scene. It glows in his hand.",
            "cliffhanger": "He hears a whisper: 'Find the door...'"
        },
        {
            "summary": "He discovers a door that appears at midnight. The key fits perfectly.",
            "cliffhanger": "He opens it and sees his dead partner alive!"
        }
    ]
    
    results = analyzer.analyze_episodes(test_episodes)
    
    for result in results:
        print(f"\n📺 Episode {result['episode']}:")
        for point in result['emotion_curve']:
            print(f"   At {point['time']}s: {point['emotion']} ({point['intensity']:.2f})")