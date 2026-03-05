#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visualization Script for Emotion Analysis
Creates charts for hackathon presentation
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.modules.emotion_analyzer import emotion_analyzer
from backend.modules.story_decomposer import story_decomposer

def plot_emotion_timeline(text, save_path=None):
    """
    Plot emotion timeline for 90-second episode
    
    Args:
        text: Input story text
        save_path: Path to save the plot (optional)
    """
    # Get timeline data
    timeline = emotion_analyzer.get_emotion_timeline(text, time_blocks=5)
    
    # Prepare data for plotting
    time_blocks = [f"Block {t['time_block']}\n{t['time_range']}" for t in timeline]
    emotions = [t['dominant_emotion'] for t in timeline]
    sentiment_scores = [t['compound_score'] for t in timeline]
    
    # Create color map for emotions
    emotion_colors = {
        'joy': '#FFD700',
        'sadness': '#4169E1',
        'anger': '#FF4500',
        'fear': '#800080',
        'surprise': '#FF69B4',
        'trust': '#32CD32',
        'anticipation': '#FFA500',
        'disgust': '#8B4513'
    }
    
    colors = [emotion_colors.get(e, '#808080') for e in emotions]
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle('90-Second Episode Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Emotion distribution
    bars = ax1.bar(time_blocks, [1]*5, color=colors, alpha=0.7)
    ax1.set_ylabel('Emotion', fontsize=12)
    ax1.set_title('Dominant Emotion per Time Block', fontsize=14)
    ax1.set_ylim(0, 1.5)
    ax1.set_yticks([])
    
    # Add emotion labels on bars
    for i, (bar, emotion) in enumerate(zip(bars, emotions)):
        ax1.text(bar.get_x() + bar.get_width()/2, 0.5, emotion,
                ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Plot 2: Sentiment score
    ax2.plot(time_blocks, sentiment_scores, marker='o', linewidth=3, color='#2E86AB')
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax2.set_ylabel('Sentiment Score', fontsize=12)
    ax2.set_xlabel('Time Block', fontsize=12)
    ax2.set_title('Sentiment Progression', fontsize=14)
    ax2.set_ylim(-1.1, 1.1)
    ax2.grid(True, alpha=0.3)
    
    # Color positive/negative areas
    ax2.fill_between(range(len(time_blocks)), 0, sentiment_scores, 
                     where=np.array(sentiment_scores) > 0,
                     color='green', alpha=0.3, label='Positive')
    ax2.fill_between(range(len(time_blocks)), 0, sentiment_scores,
                     where=np.array(sentiment_scores) < 0,
                     color='red', alpha=0.3, label='Negative')
    ax2.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✅ Plot saved to {save_path}")
    
    plt.show()

def plot_cliffhanger_scores():
    """Compare cliffhanger scores for different story endings"""
    
    test_endings = [
        "The door slowly creaked open...",
        "And they lived happily ever after.",
        "Suddenly, a shadow appeared behind them!",
        "The mystery remained unsolved.",
        "Just then, everything went dark..."
    ]
    
    scores = []
    reasons = []
    
    for ending in test_endings:
        result = story_decomposer.decompose(ending)
        scores.append(result['cliffhanger']['score'])
        reasons.append(result['cliffhanger']['strength'])
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['#FF6B6B' if s > 50 else '#4ECDC4' for s in scores]
    bars = ax.bar(range(len(test_endings)), scores, color=colors, alpha=0.8)
    
    ax.set_xticks(range(len(test_endings)))
    ax.set_xticklabels([f"Ending {i+1}" for i in range(len(test_endings))])
    ax.set_ylabel('Cliffhanger Score (0-100)', fontsize=12)
    ax.set_title('Cliffhanger Strength Comparison', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.grid(True, axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, score, reason) in enumerate(zip(bars, scores, reasons)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{score}\n({reason})', ha='center', va='bottom', fontsize=9)
        
        # Add actual text preview
        ax.text(bar.get_x() + bar.get_width()/2., -8,
                test_endings[i][:20] + '...', ha='center', va='top', 
                fontsize=8, rotation=45)
    
    plt.tight_layout()
    plt.show()

def create_presentation_demo():
    """Create complete visualization for hackathon presentation"""
    
    print("📊 Creating presentation visuals...")
    
    # Test story
    story = """
    Chapter 1: The Adventure Begins
    
    John was excited about his journey. "This will be amazing!" he thought happily.
    
    Suddenly, dark clouds gathered. A storm was coming. He felt scared.
    
    But then he saw a light in the distance. Hope filled his heart.
    
    He ran toward the light, finding shelter just in time. He was relieved.
    
    The storm passed, and a beautiful rainbow appeared. John smiled with joy.
    """
    
    # Plot 1: Emotion timeline
    plot_emotion_timeline(story, save_path='emotion_timeline.png')
    
    # Plot 2: Cliffhanger comparison
    plot_cliffhanger_scores()
    
    print("\n✅ Visualizations created!")
    print("📁 Files saved: emotion_timeline.png")

if __name__ == "__main__":
    create_presentation_demo()
