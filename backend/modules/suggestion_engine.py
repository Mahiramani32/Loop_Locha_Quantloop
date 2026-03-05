"""
Suggestion Engine Module
Generates improvement suggestions based on story analysis
Author: Shreya (Person 4)
"""

import math

class SuggestionEngine:
    """
    Analyzes episode data and generates actionable improvement suggestions
    """
    
    def __init__(self):
        """Initialize the suggestion engine"""
        self.suggestion_templates = self._load_templates()
        print("✅ SuggestionEngine initialized")
    
    def _load_templates(self):
        """Load suggestion templates"""
        return {
            "cliffhanger": {
                "very_low": "Episode {ep_num}: Cliffhanger is very weak ({score}/10). Add a shocking revelation or unanswered question right at the end.",
                "low": "Episode {ep_num}: Cliffhanger could be stronger ({score}/10). Consider adding more suspense or a mystery.",
                "medium": "Episode {ep_num}: Cliffhanger is decent ({score}/10). To make it viral, add an unexpected element.",
                "good": "Episode {ep_num}: Strong cliffhanger ({score}/10)! This will keep viewers watching."
            },
            "emotion": {
                "flat": "Episode {ep_num}: Emotional range is limited. Add contrasting emotions like fear after joy, or surprise after calm.",
                "low_intensity": "Episode {ep_num}: Emotional intensity is low throughout. Add more dramatic moments and conflicts.",
                "good_range": "Episode {ep_num}: Good emotional variety! Viewers will stay engaged.",
                "monotone": "Episode {ep_num}: The emotion stays the same for too long. Break it up with a sudden change."
            },
            "retention": {
                "early_drop": "Episode {ep_num}: Viewers may drop off early ({time}s). Start with a stronger hook in the first 10 seconds.",
                "mid_drop": "Episode {ep_num}: High drop-off risk at {time}s. This scene might be too slow – add tension or cut it shorter.",
                "late_drop": "Episode {ep_num}: Viewers might leave before the climax ({time}s). Build anticipation earlier.",
                "multiple_drops": "Episode {ep_num}: Multiple risky points at {times}. Review pacing throughout the episode."
            },
            "pacing": {
                "too_slow": "Episode {ep_num}: Pacing is too slow. Aim for a scene change every 3-5 seconds in vertical videos.",
                "too_fast": "Episode {ep_num}: Pacing is too fast. Give viewers a moment to absorb key information.",
                "uneven": "Episode {ep_num}: Pacing is uneven. Balance slow and fast sections."
            },
            "structure": {
                "no_conflict": "Episode {ep_num}: No clear conflict. Every episode needs a problem to solve.",
                "weak_stakes": "Episode {ep_num}: Stakes aren't clear. Viewers need to know what the hero might lose.",
                "no_progress": "Episode {ep_num}: Story doesn't advance much. Reveal new information or raise the stakes."
            },
            "viral": {
                "hook_needed": "Episode {ep_num}: First 3 seconds need a stronger hook. Start with a question, mystery, or shocking moment.",
                "twist_opportunity": "Episode {ep_num}: Good place for a plot twist. Consider adding an unexpected revelation.",
                "emotional_hook": "Episode {ep_num}: Add an emotional moment here to connect with viewers."
            }
        }
    
    def generate_suggestions(self, episodes, language="en"):
        """
        Generate improvement suggestions based on episode analysis
        
        Args:
            episodes (list): List of episode dictionaries with analysis data
            language (str): Language code (default: "en")
        
        Returns:
            list: List of suggestion strings
        """
        print(f"\n💡 Generating suggestions for {len(episodes)} episodes...")
        
        all_suggestions = []
        total_episodes = len(episodes)  # ← FIX: Store total episodes count
        
        for episode in episodes:
            episode_suggestions = self._analyze_episode(episode, total_episodes)  # ← Pass total_episodes
            all_suggestions.extend(episode_suggestions)
        
        # Add general suggestions if we have very few
        if len(all_suggestions) < 3:
            general_tips = self._get_general_suggestions()
            all_suggestions.extend(general_tips[:3-len(all_suggestions)])
        
        # Remove duplicates (if same suggestion appears multiple times)
        unique_suggestions = []
        seen = set()
        for suggestion in all_suggestions:
            if suggestion not in seen:
                seen.add(suggestion)
                unique_suggestions.append(suggestion)
        
        print(f"✅ Generated {len(unique_suggestions)} unique suggestions")
        return unique_suggestions
    
    def _analyze_episode(self, episode, total_episodes):
        """
        Analyze a single episode and return suggestions
        
        Args:
            episode (dict): Episode data with analysis
            total_episodes (int): Total number of episodes in series
        
        Returns:
            list: Suggestions for this episode
        """
        suggestions = []
        ep_num = episode.get('number', episode.get('episode', 0))
        
        if not ep_num:
            ep_num = 1  # Default if not specified
        
        # 1. Analyze cliffhanger score
        cliffhanger_score = episode.get('cliffhanger_score', episode.get('cliffhangerScore', 5))
        if isinstance(cliffhanger_score, (int, float)):
            if cliffhanger_score < 4:
                suggestions.append(self.suggestion_templates["cliffhanger"]["very_low"].format(ep_num=ep_num, score=cliffhanger_score))
            elif cliffhanger_score < 6:
                suggestions.append(self.suggestion_templates["cliffhanger"]["low"].format(ep_num=ep_num, score=cliffhanger_score))
            elif cliffhanger_score < 8:
                suggestions.append(self.suggestion_templates["cliffhanger"]["medium"].format(ep_num=ep_num, score=cliffhanger_score))
        
        # 2. Analyze emotion curve
        emotion_curve = episode.get('emotion_curve', episode.get('emotions', []))
        if emotion_curve and len(emotion_curve) > 1:
            # Check emotion variety
            emotions = [e.get('emotion', '') for e in emotion_curve if e.get('emotion')]
            unique_emotions = set(emotions)
            
            if len(unique_emotions) < 2:
                suggestions.append(self.suggestion_templates["emotion"]["flat"].format(ep_num=ep_num))
            elif len(unique_emotions) < 3:
                # Check if intensity varies
                intensities = [e.get('intensity', 0) for e in emotion_curve]
                avg_intensity = sum(intensities) / len(intensities)
                if avg_intensity < 0.3:
                    suggestions.append(self.suggestion_templates["emotion"]["low_intensity"].format(ep_num=ep_num))
            
            # Check if same emotion persists
            if len(emotions) > 3 and len(set(emotions[-3:])) == 1:
                suggestions.append(self.suggestion_templates["emotion"]["monotone"].format(ep_num=ep_num))
        
        # 3. Analyze retention heatmap
        retention = episode.get('retention_heatmap', episode.get('retention', []))
        if retention:
            # Find high drop-off points (risk > 0.7)
            high_risk = [p for p in retention if p.get('dropoff_risk', p.get('risk', 0)) > 0.7]
            
            if len(high_risk) >= 3:
                times = ", ".join(str(p.get('time', p.get('second', 0))) for p in high_risk[:3])
                suggestions.append(self.suggestion_templates["retention"]["multiple_drops"].format(ep_num=ep_num, times=times))
            elif high_risk:
                # Categorize by time
                for risk_point in high_risk[:2]:  # Limit to first 2 high-risk points
                    time = risk_point.get('time', risk_point.get('second', 0))
                    if time < 15:
                        suggestions.append(self.suggestion_templates["retention"]["early_drop"].format(ep_num=ep_num, time=time))
                    elif time < 60:
                        suggestions.append(self.suggestion_templates["retention"]["mid_drop"].format(ep_num=ep_num, time=time))
                    else:
                        suggestions.append(self.suggestion_templates["retention"]["late_drop"].format(ep_num=ep_num, time=time))
        
        # 4. Check for conflict in summary
        summary = episode.get('summary', '')
        if summary:
            conflict_indicators = ['fight', 'battle', 'argue', 'conflict', 'problem', 'against', 'vs', 'versus', 'struggle', 'challenge']
            has_conflict = any(indicator in summary.lower() for indicator in conflict_indicators)
            
            if not has_conflict and len(summary) > 20:
                suggestions.append(self.suggestion_templates["structure"]["no_conflict"].format(ep_num=ep_num))
        
        # 5. Check for stakes
        stakes_indicators = ['must', 'need to', 'have to', 'otherwise', 'or else', 'if not', 'danger', 'risk', 'lose']
        has_stakes = any(indicator in summary.lower() for indicator in stakes_indicators) if summary else False
        
        if not has_stakes and summary:
            suggestions.append(self.suggestion_templates["structure"]["weak_stakes"].format(ep_num=ep_num))
        
        # 6. Episode-specific suggestions based on number
        if ep_num == 1:
            # First episode needs strong hook
            hook_indicators = ['mystery', 'sudden', 'unexpected', 'shock', 'strange', 'weird']
            has_hook = any(indicator in (summary + episode.get('cliffhanger', '')).lower() for indicator in hook_indicators) if summary else False
            
            if not has_hook:
                suggestions.append(self.suggestion_templates["viral"]["hook_needed"].format(ep_num=ep_num))
        
        elif ep_num == 3 and total_episodes >= 5:  # ← FIX: Use total_episodes parameter
            # Middle episode is good for twist
            suggestions.append(self.suggestion_templates["viral"]["twist_opportunity"].format(ep_num=ep_num))
        
        elif ep_num == total_episodes:  # ← FIX: Use total_episodes parameter
            # Final episode
            if cliffhanger_score and cliffhanger_score < 8:
                suggestions.append(f"Episode {ep_num}: Final episode cliffhanger should be the strongest. Raise stakes to maximum!")
        
        return suggestions
    
    def _get_general_suggestions(self):
        """Get general story improvement suggestions"""
        return [
            "💡 Add more emotional highs and lows throughout the series.",
            "💡 Each episode should end with a question viewers want answered.",
            "💡 In vertical videos, show close-ups of faces to connect emotionally.",
            "💡 Add text overlays for key moments to improve retention.",
            "💡 The first 3 seconds should make viewers ask 'what happens next?'",
            "💡 Use music to build tension before cliffhangers.",
            "💡 Reveal new information in each episode to keep viewers curious."
        ]
    
    def get_priority_suggestions(self, episodes, max_count=5):
        """
        Get top priority suggestions based on severity
        
        Args:
            episodes (list): List of episode dictionaries
            max_count (int): Maximum number of suggestions to return
        
        Returns:
            list: Top priority suggestions
        """
        all_suggestions = self.generate_suggestions(episodes)
        
        # In a real system, you'd rank by importance
        # For now, return first max_count
        return all_suggestions[:max_count]
    
    def format_suggestions_for_display(self, suggestions):
        """
        Format suggestions nicely for frontend display
        
        Args:
            suggestions (list): List of suggestion strings
        
        Returns:
            dict: Formatted suggestions by category
        """
        formatted = {
            "critical": [],
            "improvement": [],
            "tips": []
        }
        
        for suggestion in suggestions:
            if "very weak" in suggestion or "drop-off" in suggestion:
                formatted["critical"].append(suggestion)
            elif "could be stronger" in suggestion or "consider" in suggestion.lower():
                formatted["improvement"].append(suggestion)
            else:
                formatted["tips"].append(suggestion)
        
        return formatted


# Convenience function for easy import
def generate_suggestions(episodes, language="en"):
    """
    Easy-to-use function to generate suggestions
    
    Args:
        episodes (list): List of episodes with analysis data
        language (str): Language code
    
    Returns:
        list: Improvement suggestions
    """
    engine = SuggestionEngine()
    return engine.generate_suggestions(episodes, language)


# If this file is run directly, run a test
if __name__ == "__main__":
    print("=" * 60)
    print("SUGGESTION ENGINE - SELF TEST")
    print("=" * 60)
    
    # Create test episodes with analysis data
    test_episodes = [
        {
            "number": 1,
            "title": "The Mysterious Key",
            "summary": "Detective Raj finds an old key at a crime scene.",
            "cliffhanger": "The key glows in his hand.",
            "cliffhanger_score": 3.5,
            "emotion_curve": [
                {"time": 0, "emotion": "neutral", "intensity": 0.2},
                {"time": 30, "emotion": "curious", "intensity": 0.4},
                {"time": 60, "emotion": "curious", "intensity": 0.4},
                {"time": 90, "emotion": "curious", "intensity": 0.4}
            ],
            "retention_heatmap": [
                {"time": 5, "dropoff_risk": 0.3},
                {"time": 15, "dropoff_risk": 0.6},
                {"time": 45, "dropoff_risk": 0.8},
                {"time": 75, "dropoff_risk": 0.4}
            ]
        },
        {
            "number": 2,
            "title": "The Door",
            "summary": "Raj finds a door that appears at midnight.",
            "cliffhanger": "He opens it and sees his dead partner.",
            "cliffhanger_score": 8.5,
            "emotion_curve": [
                {"time": 0, "emotion": "suspense", "intensity": 0.7},
                {"time": 30, "emotion": "fear", "intensity": 0.8},
                {"time": 60, "emotion": "shock", "intensity": 0.9},
                {"time": 90, "emotion": "surprise", "intensity": 0.9}
            ],
            "retention_heatmap": [
                {"time": 10, "dropoff_risk": 0.1},
                {"time": 30, "dropoff_risk": 0.2},
                {"time": 60, "dropoff_risk": 0.2},
                {"time": 85, "dropoff_risk": 0.3}
            ]
        },
        {
            "number": 3,
            "title": "The Parallel World",
            "summary": "In the parallel world, his partner is alive.",
            "cliffhanger": "Someone follows him through.",
            "cliffhanger_score": 7.0,
            "emotion_curve": [
                {"time": 0, "emotion": "joy", "intensity": 0.8},
                {"time": 30, "emotion": "joy", "intensity": 0.7},
                {"time": 60, "emotion": "fear", "intensity": 0.6},
                {"time": 90, "emotion": "fear", "intensity": 0.8}
            ],
            "retention_heatmap": [
                {"time": 5, "dropoff_risk": 0.2},
                {"time": 25, "dropoff_risk": 0.3},
                {"time": 55, "dropoff_risk": 0.5},
                {"time": 80, "dropoff_risk": 0.4}
            ]
        }
    ]
    
    # Create engine instance
    engine = SuggestionEngine()
    
    # Generate suggestions
    print("\n💡 Generating suggestions...")
    suggestions = engine.generate_suggestions(test_episodes)
    
    # Print results
    print("\n" + "=" * 60)
    print("GENERATED SUGGESTIONS")
    print("=" * 60)
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
    
    # Test formatting
    print("\n" + "=" * 60)
    print("FORMATTED SUGGESTIONS (for frontend)")
    print("=" * 60)
    formatted = engine.format_suggestions_for_display(suggestions)
    
    if formatted["critical"]:
        print("\n🔴 CRITICAL:")
        for s in formatted["critical"]:
            print(f"   • {s}")
    
    if formatted["improvement"]:
        print("\n🟡 IMPROVEMENTS:")
        for s in formatted["improvement"]:
            print(f"   • {s}")
    
    if formatted["tips"]:
        print("\n🔵 TIPS:")
        for s in formatted["tips"]:
            print(f"   • {s}")
    
    print("\n✅ Test complete!")