# -*- coding: utf-8 -*-
"""
Emotion Analysis Module
Analyzes emotional content in stories using multiple methods
"""

import nltk
import re
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional
import logging

# Download VADER if needed
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

logger = logging.getLogger(__name__)

class EmotionAnalyzer:
    """Advanced emotion analysis for stories"""
    
    # Plutchik's wheel of emotions
    EMOTIONS = {
        'joy': {
            'keywords': ['happy', 'joy', 'delighted', 'excited', 'wonderful', 'great', 
                        'love', 'smile', 'laugh', 'celebration', 'pleased', 'glad',
                        'thrilled', 'ecstatic', 'bliss', 'euphoria'],
            'color': '#FFD700',  # Gold
            'intensity': 1.0
        },
        'sadness': {
            'keywords': ['sad', 'unhappy', 'depressed', 'grief', 'cry', 'tears', 
                        'heartbroken', 'mourn', 'pain', 'hurt', 'lonely', 'miserable',
                        'hopeless', 'despair', 'sorrow', 'anguish'],
            'color': '#4169E1',  # Royal Blue
            'intensity': 0.9
        },
        'anger': {
            'keywords': ['angry', 'furious', 'mad', 'hate', 'rage', 'annoyed', 
                        'frustrated', 'outrage', 'violent', 'fury', 'wrath', 'bitter',
                        'hostile', 'irritated', 'enraged'],
            'color': '#FF4500',  # Orange Red
            'intensity': 0.95
        },
        'fear': {
            'keywords': ['scared', 'afraid', 'terrified', 'horror', 'panic', 'dread', 
                        'fearful', 'anxious', 'worry', 'terror', 'frightened', 'nervous',
                        'alarmed', 'petrified', 'paranoid'],
            'color': '#800080',  # Purple
            'intensity': 0.9
        },
        'surprise': {
            'keywords': ['surprised', 'shocked', 'amazed', 'astonished', 'unexpected', 
                        'sudden', 'wow', 'gasp', 'stunned', 'startled', 'bewildered',
                        'speechless', 'astounded', 'dumbfounded'],
            'color': '#FF69B4',  # Hot Pink
            'intensity': 0.8
        },
        'trust': {
            'keywords': ['trust', 'believe', 'faith', 'loyal', 'confident', 'sure', 
                        'certain', 'honest', 'reliable', 'dependable', 'truthful',
                        'sincere', 'genuine', 'authentic'],
            'color': '#32CD32',  # Lime Green
            'intensity': 0.7
        },
        'anticipation': {
            'keywords': ['expect', 'anticipate', 'await', 'hope', 'look forward', 
                        'eager', 'prepare', 'ready', 'impatient', 'excited about',
                        'prospect', 'expectation'],
            'color': '#FFA500',  # Orange
            'intensity': 0.7
        },
        'disgust': {
            'keywords': ['disgusted', 'gross', 'awful', 'terrible', 'horrible', 
                        'repulsive', 'nasty', 'vile', 'revolting', 'appalling',
                        'abhorrent', 'loathsome'],
            'color': '#8B4513',  # Saddle Brown
            'intensity': 0.85
        }
    }
    
    def __init__(self):
        """Initialize emotion analyzer"""
        self.sia = SentimentIntensityAnalyzer()
        
        # Compile regex patterns for faster matching
        self.emotion_patterns = {
            emotion: re.compile(r'\b(' + '|'.join(re.escape(k) for k in data['keywords']) + r')\b', re.IGNORECASE)
            for emotion, data in self.EMOTIONS.items()
        }
    
    def analyze(self, text: str, detailed: bool = False) -> Dict[str, Any]:
        """
        Analyze emotions in text
        
        Args:
            text: Input text
            detailed: Return detailed analysis
            
        Returns:
            Emotion analysis results
        """
        # Get VADER sentiment
        vader_scores = self.sia.polarity_scores(text)
        
        # Get TextBlob sentiment
        blob = TextBlob(text)
        textblob_sentiment = {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
        
        # Calculate emotion scores
        emotion_scores = self._calculate_emotion_scores(text)
        
        # Determine dominant emotion
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        
        # Calculate emotional intensity
        intensity = self._calculate_intensity(emotion_scores)
        
        # Determine overall sentiment
        compound = vader_scores['compound']
        if compound >= 0.05:
            sentiment = 'positive'
        elif compound <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        result = {
            'success': True,
            'sentiment': {
                'overall': sentiment,
                'compound': round(compound, 3),
                'positive': round(vader_scores['pos'], 3),
                'negative': round(vader_scores['neg'], 3),
                'neutral': round(vader_scores['neu'], 3)
            },
            'textblob': textblob_sentiment,
            'emotions': emotion_scores,
            'dominant_emotion': {
                'name': dominant_emotion[0],
                'score': round(dominant_emotion[1], 3),
                'color': self.EMOTIONS[dominant_emotion[0]]['color']
            },
            'intensity': intensity,
            'emotion_count': len([e for e in emotion_scores.values() if e > 0.2])
        }
        
        if detailed:
            result['matches'] = self._get_emotion_matches(text)
            result['sentence_analysis'] = self.analyze_sentences(text)
            result['emotion_arc'] = self.get_emotion_arc(text)
        
        return result
    
    def _calculate_emotion_scores(self, text: str) -> Dict[str, float]:
        """Calculate scores for each emotion based on keyword frequency"""
        scores = {}
        for emotion, pattern in self.emotion_patterns.items():
            matches = pattern.findall(text)
            score = len(matches) * 0.15  # Each match contributes 0.15
            scores[emotion] = min(round(score, 2), 1.0)
        return scores
    
    def _calculate_intensity(self, emotion_scores: Dict[str, float]) -> str:
        """Calculate overall emotional intensity"""
        avg_score = sum(emotion_scores.values()) / len(emotion_scores)
        
        if avg_score > 0.5:
            return 'high'
        elif avg_score > 0.3:
            return 'medium'
        elif avg_score > 0.1:
            return 'low'
        else:
            return 'very_low'
    
    def _get_emotion_matches(self, text: str) -> Dict[str, List[str]]:
        """Get actual matched words for each emotion"""
        matches = {}
        for emotion, pattern in self.emotion_patterns.items():
            found = pattern.findall(text.lower())
            if found:
                matches[emotion] = list(set(found))[:5]  # Unique matches, limit to 5
        return matches
    
    def analyze_sentences(self, text: str) -> List[Dict]:
        """Analyze each sentence separately"""
        sentences = nltk.sent_tokenize(text)
        results = []
        
        for i, sentence in enumerate(sentences):
            if len(sentence.strip()) > 10:  # Skip very short sentences
                result = self.analyze(sentence)
                results.append({
                    'sentence_id': i + 1,
                    'text': sentence.strip(),
                    'sentiment': result['sentiment']['overall'],
                    'dominant_emotion': result['dominant_emotion']['name'],
                    'emotion_score': result['dominant_emotion']['score']
                })
        
        return results
    
    def get_emotion_arc(self, text: str, num_segments: int = None) -> List[Dict]:
        """
        Return data for plotting emotional progression
        
        Args:
            text: Input text
            num_segments: Number of segments to divide into (optional)
            
        Returns:
            List of emotion data points for visualization
        """
        sentences = self.analyze_sentences(text)
        
        if not sentences:
            return []
        
        # If num_segments specified, group sentences
        if num_segments and len(sentences) > num_segments:
            # Group sentences into segments
            segment_size = len(sentences) // num_segments
            grouped_data = []
            
            for i in range(0, len(sentences), segment_size):
                segment = sentences[i:i+segment_size]
                if segment:
                    # Find most common emotion in segment
                    emotions = [s['dominant_emotion'] for s in segment]
                    most_common = Counter(emotions).most_common(1)[0][0]
                    
                    # Average sentiment score
                    sentiment_scores = [1 if s['sentiment'] == 'positive' else -1 if s['sentiment'] == 'negative' else 0 for s in segment]
                    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
                    
                    grouped_data.append({
                        'position': i // segment_size,
                        'emotion': most_common,
                        'sentiment_score': avg_sentiment,
                        'segment_size': len(segment)
                    })
            return grouped_data
        else:
            # Return each sentence as a data point
            return [
                {
                    'position': i,
                    'emotion': s['dominant_emotion'],
                    'sentiment': s['sentiment'],
                    'sentence': s['text'][:50] + '...' if len(s['text']) > 50 else s['text']
                }
                for i, s in enumerate(sentences)
            ]
    
    def get_emotion_timeline(self, text: str, time_blocks: int = 5) -> List[Dict]:
        """
        Create emotion timeline for specific time blocks (for 90-second format)
        
        Args:
            text: Input text
            time_blocks: Number of time blocks (e.g., 5 for 90-second episodes)
            
        Returns:
            Emotion data for each time block
        """
        words = text.split()
        if not words:
            return []
        
        # Divide text into time blocks
        block_size = len(words) // time_blocks
        timeline = []
        
        for i in range(time_blocks):
            start = i * block_size
            end = start + block_size if i < time_blocks - 1 else len(words)
            block_text = ' '.join(words[start:end])
            
            # Analyze this block
            result = self.analyze(block_text)
            
            timeline.append({
                'time_block': i + 1,
                'time_range': f"{(i * 18)}-{(i + 1) * 18}s" if i < time_blocks - 1 else f"{i * 18}-90s",
                'dominant_emotion': result['dominant_emotion']['name'],
                'sentiment': result['sentiment']['overall'],
                'compound_score': result['sentiment']['compound']
            })
        
        return timeline

# Create singleton instance
emotion_analyzer = EmotionAnalyzer()

# Test the module
if __name__ == "__main__":
    test_texts = [
        "She was absolutely thrilled with the surprise party! Everyone was laughing and having a wonderful time.",
        "He sat alone in the dark room, tears streaming down his face. The pain was unbearable and he felt completely hopeless.",
        "Suddenly, the door burst open and a mysterious figure appeared! Everyone gasped in shock and amazement.",
        "The villain's evil plan was disgusting. The hero felt furious and determined to stop him at any cost.",
        "I trust you completely. You've always been honest and reliable."
    ]
    
    print("🔍 Testing Emotion Analyzer")
    print("="*70)
    
    for text in test_texts:
        print(f"\n📝 Text: {text[:80]}...")
        result = emotion_analyzer.analyze(text, detailed=True)
        
        print(f"   Sentiment: {result['sentiment']['overall'].upper()} (compound: {result['sentiment']['compound']})")
        print(f"   Dominant Emotion: {result['dominant_emotion']['name']} (score: {result['dominant_emotion']['score']})")
        print(f"   Intensity: {result['intensity']}")
        
        if 'matches' in result and result['matches']:
            print(f"   Emotion words found: {list(result['matches'].keys())}")
        
        print("-"*70)
    
    # Test sentence-by-sentence analysis
    print("\n📊 Sentence-by-Sentence Analysis:")
    story = "John was happy. Then he saw the monster and got scared. But his friends came to help and he felt relieved!"
    sentence_results = emotion_analyzer.analyze_sentences(story)
    for sent in sentence_results:
        print(f"   Sentence {sent['sentence_id']}: {sent['dominant_emotion']} ({sent['sentiment']})")
    
    # Test emotion arc
    print("\n📈 Emotion Arc:")
    arc = emotion_analyzer.get_emotion_arc(story)
    for point in arc:
        print(f"   Position {point['position']}: {point['emotion']} - {point['sentiment']}")
    
    # Test timeline for 90-second format
    print("\n⏱️ 90-Second Timeline:")
    long_story = " ".join([story] * 10)  # Make it longer
    timeline = emotion_analyzer.get_emotion_timeline(long_story, time_blocks=5)
    for block in timeline:
        print(f"   Block {block['time_block']} ({block['time_range']}): {block['dominant_emotion']} ({block['sentiment']})")
