"""
Suggestion Engine Module - ENHANCED VERSION
Generates weighted, prioritized improvement suggestions with:
- Importance weighting (critical vs improvement vs tip)
- Sophisticated multi-factor rules
- Genre-specific suggestions
- Priority scoring
- Smart suggestion merging
Author: Shreya (Person 4)
"""

import math
from collections import defaultdict
import re

class SuggestionEngine:
    """
    Enhanced suggestion engine with weighted importance and sophisticated rules
    """
    
    def __init__(self):
        """Initialize the suggestion engine"""
        self.weights = self._initialize_weights()
        self.thresholds = self._initialize_thresholds()
        self.suggestion_templates = self._load_templates()
        self.suggestion_history = defaultdict(list)  # Track suggestions by episode
        print("✅ Enhanced SuggestionEngine initialized")
    
    def _initialize_weights(self):
        """Initialize importance weights for different factors"""
        return {
            "cliffhanger": {
                "very_low": 10,  # Critical
                "low": 7,        # Important
                "medium": 4,      # Moderate
                "good": 1         # Minor
            },
            "emotion": {
                "flat": 9,
                "low_intensity": 7,
                "monotone": 8,
                "limited_range": 6,
                "good_range": 1
            },
            "retention": {
                "early_drop": 10,
                "mid_drop": 8,
                "late_drop": 7,
                "multiple_drops": 10,
                "high_risk_zone": 9
            },
            "structure": {
                "no_conflict": 10,
                "weak_stakes": 8,
                "no_progress": 8,
                "weak_opening": 9,
                "weak_closing": 8
            },
            "pacing": {
                "too_slow": 7,
                "too_fast": 6,
                "uneven": 7,
                "no_rhythm": 8
            },
            "viral": {
                "hook_needed": 9,
                "twist_opportunity": 7,
                "emotional_hook": 7,
                "shareable_moment": 6
            }
        }
    
    def _initialize_thresholds(self):
        """Initialize thresholds for different metrics"""
        return {
            "cliffhanger": {
                "critical": 4,
                "warning": 6,
                "good": 8
            },
            "emotion_variance": {
                "critical": 2,   # Less than 2 emotions
                "warning": 3,     # 2-3 emotions
                "good": 4         # 4+ emotions
            },
            "emotion_intensity": {
                "critical": 0.3,
                "warning": 0.5,
                "good": 0.7
            },
            "retention_risk": {
                "critical": 0.8,
                "warning": 0.6,
                "good": 0.4
            },
            "pacing_score": {
                "critical": 4,
                "warning": 6,
                "good": 8
            }
        }
    
    def _load_templates(self):
        """Load suggestion templates with categories"""
        return {
            "cliffhanger": {
                "very_low": {
                    "template": "Episode {ep_num}: ⚠️ Cliffhanger is critically weak ({score}/10). Add a shocking revelation or unanswered question immediately to keep viewers watching.",
                    "category": "critical",
                    "tags": ["cliffhanger", "pacing"]
                },
                "low": {
                    "template": "Episode {ep_num}: Cliffhanger needs improvement ({score}/10). Consider adding more suspense, a mystery, or an unexpected reveal.",
                    "category": "improvement",
                    "tags": ["cliffhanger"]
                },
                "medium": {
                    "template": "Episode {ep_num}: Cliffhanger is decent ({score}/10). To make it viral, add an element of surprise or raise the stakes.",
                    "category": "tip",
                    "tags": ["cliffhanger", "viral"]
                },
                "good": {
                    "template": "Episode {ep_num}: Strong cliffhanger ({score}/10)! This tension will keep viewers engaged for the next episode.",
                    "category": "tip",
                    "tags": ["cliffhanger", "positive"]
                }
            },
            "emotion": {
                "flat": {
                    "template": "Episode {ep_num}: 📉 Emotional range is very flat. Add contrasting emotions - joy after sadness, fear after calm - to keep viewers engaged.",
                    "category": "critical",
                    "tags": ["emotion", "engagement"]
                },
                "low_intensity": {
                    "template": "Episode {ep_num}: Emotional intensity is low throughout. Create more dramatic moments, conflicts, or high-stakes situations.",
                    "category": "improvement",
                    "tags": ["emotion", "drama"]
                },
                "monotone": {
                    "template": "Episode {ep_num}: Same emotion ({emotion}) persists too long. Break the pattern with a sudden change or plot twist.",
                    "category": "improvement",
                    "tags": ["emotion", "variety"]
                },
                "limited_range": {
                    "template": "Episode {ep_num}: Only {count} emotions detected. Add variety - try including surprise, fear, or joy for contrast.",
                    "category": "improvement",
                    "tags": ["emotion", "variety"]
                },
                "good_range": {
                    "template": "Episode {ep_num}: Good emotional variety! Viewers will stay engaged throughout.",
                    "category": "tip",
                    "tags": ["emotion", "positive"]
                }
            },
            "retention": {
                "early_drop": {
                    "template": "Episode {ep_num}: 🔴 CRITICAL - Viewers drop off early (at {time}s). Your first 10 seconds need a much stronger hook. Start with action, mystery, or shock.",
                    "category": "critical",
                    "tags": ["retention", "hook"]
                },
                "mid_drop": {
                    "template": "Episode {ep_num}: High drop-off risk at {time}s. This scene may be too slow - add tension, cut dialogue, or introduce a surprise here.",
                    "category": "improvement",
                    "tags": ["retention", "pacing"]
                },
                "late_drop": {
                    "template": "Episode {ep_num}: Viewers leave before climax (at {time}s). Build anticipation earlier and make the payoff worth waiting for.",
                    "category": "improvement",
                    "tags": ["retention", "climax"]
                },
                "multiple_drops": {
                    "template": "Episode {ep_num}: 🔴 MULTIPLE risky drop-off points at {times}. Review entire episode pacing - consider faster cuts and more engaging content throughout.",
                    "category": "critical",
                    "tags": ["retention", "pacing", "critical"]
                },
                "high_risk_zone": {
                    "template": "Episode {ep_num}: Section between {start}s-{end}s has high drop-off risk. Add a visual hook, text overlay, or plot development here.",
                    "category": "improvement",
                    "tags": ["retention", "zone"]
                }
            },
            "structure": {
                "no_conflict": {
                    "template": "Episode {ep_num}: ⚠️ No clear conflict detected. Every episode needs a problem to solve, an obstacle to overcome, or a mystery to unravel.",
                    "category": "critical",
                    "tags": ["structure", "conflict"]
                },
                "weak_stakes": {
                    "template": "Episode {ep_num}: Stakes are unclear. Viewers need to know what the hero might lose - a loved one, their life, their identity, or their future.",
                    "category": "improvement",
                    "tags": ["structure", "stakes"]
                },
                "no_progress": {
                    "template": "Episode {ep_num}: Story doesn't advance much. Reveal new information, raise the stakes, or introduce a complication.",
                    "category": "improvement",
                    "tags": ["structure", "progress"]
                },
                "weak_opening": {
                    "template": "Episode {ep_num}: Opening is weak. Start with a question, mystery, action, or emotional moment to hook viewers immediately.",
                    "category": "critical",
                    "tags": ["structure", "hook"]
                },
                "weak_closing": {
                    "template": "Episode {ep_num}: Ending lacks punch. Close with a cliffhanger, revelation, or emotional beat that makes viewers want the next episode.",
                    "category": "improvement",
                    "tags": ["structure", "closing"]
                }
            },
            "viral": {
                "hook_needed": {
                    "template": "Episode {ep_num}: 🚀 First 3 seconds need a viral hook. Start with: a shocking statement, a question, a mystery, or a visually striking moment.",
                    "category": "critical",
                    "tags": ["viral", "hook"]
                },
                "twist_opportunity": {
                    "template": "Episode {ep_num}: Perfect spot for a plot twist. Add an unexpected revelation, betrayal, or identity reveal here.",
                    "category": "improvement",
                    "tags": ["viral", "twist"]
                },
                "emotional_hook": {
                    "template": "Episode {ep_num}: Add an emotional moment here - a touching confession, a heartbreaking loss, or a joyful reunion to connect with viewers.",
                    "category": "tip",
                    "tags": ["viral", "emotion"]
                },
                "shareable_moment": {
                    "template": "Episode {ep_num}: Create a shareable moment - something viewers will want to send to friends. A shocking reveal, a funny line, or a heartwarming scene.",
                    "category": "tip",
                    "tags": ["viral", "share"]
                }
            },
            "genre_specific": {
                "horror": {
                    "template": "Episode {ep_num}: For horror, add jump scares every 30-40 seconds, use sound design to build dread, and show just enough - let imagination do the rest.",
                    "category": "tip",
                    "tags": ["genre", "horror"]
                },
                "romance": {
                    "template": "Episode {ep_num}: For romance, focus on emotional close-ups, meaningful glances, and small gestures. The tension is in what's unsaid.",
                    "category": "tip",
                    "tags": ["genre", "romance"]
                },
                "comedy": {
                    "template": "Episode {ep_num}: For comedy, punch up the dialogue, add visual gags, and use timing - pause before the punchline, then cut quickly.",
                    "category": "tip",
                    "tags": ["genre", "comedy"]
                },
                "thriller": {
                    "template": "Episode {ep_num}: For thriller, increase tension with quick cuts, suspenseful music, and the feeling that danger is always nearby.",
                    "category": "tip",
                    "tags": ["genre", "thriller"]
                },
                "scifi": {
                    "template": "Episode {ep_num}: For sci-fi, ground the futuristic elements in human emotion. The technology should serve the story, not overwhelm it.",
                    "category": "tip",
                    "tags": ["genre", "scifi"]
                },
                "fantasy": {
                    "template": "Episode {ep_num}: For fantasy, make the magical elements feel real through consistent rules and relatable character reactions.",
                    "category": "tip",
                    "tags": ["genre", "fantasy"]
                }
            },
            "pacing": {
                "too_slow": {
                    "template": "Episode {ep_num}: Pacing is too slow. For vertical videos, aim for a scene change every 3-5 seconds and new information every 10-15 seconds.",
                    "category": "improvement",
                    "tags": ["pacing"]
                },
                "too_fast": {
                    "template": "Episode {ep_num}: Pacing is too fast. Give viewers a moment to absorb key information and emotional beats.",
                    "category": "tip",
                    "tags": ["pacing"]
                },
                "uneven": {
                    "template": "Episode {ep_num}: Pacing is uneven. Balance slow, emotional moments with fast, action-packed sequences.",
                    "category": "improvement",
                    "tags": ["pacing"]
                },
                "no_rhythm": {
                    "template": "Episode {ep_num}: Lacks rhythmic flow. Create a pattern - build tension, release, then build again.",
                    "category": "improvement",
                    "tags": ["pacing"]
                }
            }
        }
    
    def _detect_genre_from_episodes(self, episodes):
        """Detect overall genre from episodes"""
        genre_count = defaultdict(int)
        
        for episode in episodes:
            # Check if genre is directly provided
            genre = episode.get('genre', '')
            if genre and genre != 'general':
                genre_count[genre] += 1
                continue
            
            # Try to detect from summary
            summary = episode.get('summary', '')
            if summary:
                summary_lower = summary.lower()
                genre_keywords = {
                    "horror": ['horror', 'ghost', 'scary', 'haunted', 'demon', 'creepy'],
                    "romance": ['love', 'romance', 'heart', 'kiss', 'relationship'],
                    "comedy": ['funny', 'comedy', 'joke', 'laugh', 'hilarious'],
                    "scifi": ['sci-fi', 'future', 'robot', 'alien', 'space'],
                    "fantasy": ['magic', 'fantasy', 'wizard', 'dragon', 'spell'],
                    "thriller": ['thriller', 'suspense', 'mystery', 'chase']
                }
                
                for genre, keywords in genre_keywords.items():
                    if any(keyword in summary_lower for keyword in keywords):
                        genre_count[genre] += 1
                        break
        
        # Return most common genre
        if genre_count:
            return max(genre_count.items(), key=lambda x: x[1])[0]
        return "general"
    
    def generate_suggestions(self, episodes, language="en", max_suggestions=10):
        """
        Generate weighted, prioritized improvement suggestions
        
        Args:
            episodes: List of episode dictionaries with analysis data
            language: Language code
            max_suggestions: Maximum number of suggestions to return
        
        Returns:
            dict: Suggestions organized by priority with scores
        """
        print(f"\n💡 Generating weighted suggestions for {len(episodes)} episodes...")
        
        all_suggestions = []
        overall_genre = self._detect_genre_from_episodes(episodes)
        total_episodes = len(episodes)  # Store total episodes count
        
        # Analyze each episode
        for episode in episodes:
            episode_suggestions = self._analyze_episode(episode, overall_genre, total_episodes)
            all_suggestions.extend(episode_suggestions)
        
        # Add overall series suggestions
        series_suggestions = self._analyze_series(episodes, overall_genre)
        all_suggestions.extend(series_suggestions)
        
        # Remove duplicates and merge similar suggestions
        merged_suggestions = self._merge_suggestions(all_suggestions)
        
        # Sort by importance score (higher = more important)
        merged_suggestions.sort(key=lambda x: x['importance'], reverse=True)
        
        # Limit to max_suggestions
        merged_suggestions = merged_suggestions[:max_suggestions]
        
        # Organize by category
        organized = {
            "critical": [s for s in merged_suggestions if s['category'] == 'critical'],
            "improvement": [s for s in merged_suggestions if s['category'] == 'improvement'],
            "tips": [s for s in merged_suggestions if s['category'] == 'tip']
        }
        
        print(f"✅ Generated {len(merged_suggestions)} unique suggestions")
        print(f"   - Critical: {len(organized['critical'])}")
        print(f"   - Improvements: {len(organized['improvement'])}")
        print(f"   - Tips: {len(organized['tips'])}")
        
        return organized
    
    def _analyze_episode(self, episode, overall_genre, total_episodes):
        """Analyze a single episode and return weighted suggestions"""
        suggestions = []
        ep_num = episode.get('number', episode.get('episode', 1))
        ep_genre = episode.get('genre', overall_genre)
        
        # Helper to add suggestion with score
        def add_suggestion(suggestion_type, key, **kwargs):
            if suggestion_type in self.suggestion_templates and key in self.suggestion_templates[suggestion_type]:
                template_data = self.suggestion_templates[suggestion_type][key]
                importance = self.weights.get(suggestion_type, {}).get(key, 5)
                
                # Format template with kwargs
                text = template_data['template'].format(ep_num=ep_num, **kwargs)
                
                suggestions.append({
                    'text': text,
                    'importance': importance,
                    'category': template_data['category'],
                    'tags': template_data.get('tags', []),
                    'episode': ep_num,
                    'type': suggestion_type
                })
        
        # 1. CLIFFHANGER ANALYSIS
        cliffhanger_score = episode.get('cliffhanger_score', episode.get('cliffhangerScore', 5))
        if isinstance(cliffhanger_score, (int, float)):
            if cliffhanger_score < self.thresholds['cliffhanger']['critical']:
                add_suggestion('cliffhanger', 'very_low', score=cliffhanger_score)
            elif cliffhanger_score < self.thresholds['cliffhanger']['warning']:
                add_suggestion('cliffhanger', 'low', score=cliffhanger_score)
            elif cliffhanger_score < self.thresholds['cliffhanger']['good']:
                add_suggestion('cliffhanger', 'medium', score=cliffhanger_score)
            else:
                add_suggestion('cliffhanger', 'good', score=cliffhanger_score)
        
        # 2. EMOTION ANALYSIS
        emotion_curve = episode.get('emotion_curve', episode.get('emotions', []))
        if emotion_curve and len(emotion_curve) > 1:
            # Check emotion variety
            emotions = [e.get('emotion', '') for e in emotion_curve if e.get('emotion')]
            unique_emotions = set(emotions)
            
            if len(unique_emotions) < self.thresholds['emotion_variance']['critical']:
                add_suggestion('emotion', 'flat')
            elif len(unique_emotions) < self.thresholds['emotion_variance']['warning']:
                add_suggestion('emotion', 'limited_range', count=len(unique_emotions))
            
            # Check intensity
            intensities = [e.get('intensity', 0) for e in emotion_curve]
            if intensities:
                avg_intensity = sum(intensities) / len(intensities)
                if avg_intensity < self.thresholds['emotion_intensity']['critical']:
                    add_suggestion('emotion', 'low_intensity')
            
            # Check if same emotion persists
            if len(emotions) > 3:
                last_emotions = emotions[-3:]
                if len(set(last_emotions)) == 1:
                    add_suggestion('emotion', 'monotone', emotion=last_emotions[0])
        
        # 3. RETENTION ANALYSIS
        retention = episode.get('retention_heatmap', episode.get('retention', []))
        if retention:
            # Find high drop-off points (risk > 0.7)
            high_risk = []
            for p in retention:
                risk = p.get('dropoff_risk', p.get('risk', 0))
                time = p.get('time', p.get('second', 0))
                if risk > self.thresholds['retention_risk']['critical']:
                    high_risk.append({'time': time, 'risk': risk})
            
            if len(high_risk) >= 3:
                times = ", ".join(str(p['time']) for p in high_risk[:3])
                add_suggestion('retention', 'multiple_drops', times=times)
            elif high_risk:
                for risk_point in high_risk[:2]:
                    time = risk_point['time']
                    if time < 15:
                        add_suggestion('retention', 'early_drop', time=time)
                    elif time < 60:
                        add_suggestion('retention', 'mid_drop', time=time)
                    else:
                        add_suggestion('retention', 'late_drop', time=time)
            
            # Check for high-risk zones (consecutive high risk)
            if len(retention) > 3:
                for i in range(len(retention) - 2):
                    risk1 = retention[i].get('dropoff_risk', retention[i].get('risk', 0))
                    risk2 = retention[i+1].get('dropoff_risk', retention[i+1].get('risk', 0))
                    risk3 = retention[i+2].get('dropoff_risk', retention[i+2].get('risk', 0))
                    
                    if risk1 > 0.6 and risk2 > 0.6 and risk3 > 0.6:
                        start = retention[i].get('time', retention[i].get('second', 0))
                        end = retention[i+2].get('time', retention[i+2].get('second', 0))
                        add_suggestion('retention', 'high_risk_zone', start=start, end=end)
                        break
        
        # 4. STRUCTURE ANALYSIS
        summary = episode.get('summary', '')
        if summary:
            # Check for conflict
            conflict_indicators = ['fight', 'battle', 'argue', 'conflict', 'problem', 'against', 'vs', 'versus', 'struggle', 'challenge', 'obstacle', 'enemy', 'danger']
            has_conflict = any(indicator in summary.lower() for indicator in conflict_indicators)
            
            if not has_conflict and len(summary) > 20:
                add_suggestion('structure', 'no_conflict')
            
            # Check for stakes
            stakes_indicators = ['must', 'need to', 'have to', 'otherwise', 'or else', 'if not', 'danger', 'risk', 'lose', 'save', 'protect', 'survive']
            has_stakes = any(indicator in summary.lower() for indicator in stakes_indicators)
            
            if not has_stakes:
                add_suggestion('structure', 'weak_stakes')
        
        # 5. EPISODE POSITION SPECIFIC - FIXED: using total_episodes parameter
        if ep_num == 1:
            # First episode - check for hook
            hook_indicators = ['mystery', 'sudden', 'unexpected', 'shock', 'strange', 'weird', 'discover', 'find', 'secret']
            has_hook = any(indicator in (summary + episode.get('cliffhanger', '')).lower() for indicator in hook_indicators) if summary else False
            
            if not has_hook:
                add_suggestion('viral', 'hook_needed')
            else:
                add_suggestion('structure', 'weak_opening')
        
        elif ep_num == total_episodes:  # Last episode - using total_episodes parameter
            # Last episode
            if cliffhanger_score and cliffhanger_score < 7:
                add_suggestion('structure', 'weak_closing')
        
        elif ep_num == 3 or ep_num == 4:  # Middle episodes
            add_suggestion('viral', 'twist_opportunity')
        
        # 6. GENRE-SPECIFIC SUGGESTIONS
        if ep_genre != 'general' and ep_genre in self.suggestion_templates['genre_specific']:
            add_suggestion('genre_specific', ep_genre)
        
        return suggestions
    
    def _analyze_series(self, episodes, overall_genre):
        """Analyze the entire series for overall suggestions"""
        series_suggestions = []
        
        if len(episodes) < 5:
            series_suggestions.append({
                'text': "📺 Your series has fewer than 5 episodes. For vertical storytelling, 5-8 episodes work best for audience retention.",
                'importance': 6,
                'category': 'improvement',
                'tags': ['series', 'structure'],
                'episode': 0,
                'type': 'series'
            })
        
        # Check if cliffhangers get stronger
        cliffhanger_scores = []
        for ep in episodes:
            score = ep.get('cliffhanger_score', ep.get('cliffhangerScore', 0))
            if score:
                cliffhanger_scores.append(score)
        
        if len(cliffhanger_scores) >= 3:
            if max(cliffhanger_scores) == cliffhanger_scores[0]:
                series_suggestions.append({
                    'text': "📊 Your strongest cliffhanger is in the first episode. Cliffhangers should build and peak in later episodes to keep viewers watching.",
                    'importance': 7,
                    'category': 'improvement',
                    'tags': ['series', 'cliffhanger'],
                    'episode': 0,
                    'type': 'series'
                })
        
        return series_suggestions
    
    def _merge_suggestions(self, suggestions):
        """Remove duplicates and merge similar suggestions"""
        seen_texts = set()
        merged = []
        
        for s in suggestions:
            # Create a simplified key for deduplication
            simple_key = s['text'].split('.')[0]  # First sentence
            
            if simple_key not in seen_texts:
                seen_texts.add(simple_key)
                merged.append(s)
        
        return merged
    
    def get_suggestions_summary(self, organized_suggestions):
        """Get a summary of suggestions"""
        summary = {
            "total": len(organized_suggestions['critical']) + len(organized_suggestions['improvement']) + len(organized_suggestions['tips']),
            "critical_count": len(organized_suggestions['critical']),
            "improvement_count": len(organized_suggestions['improvement']),
            "tips_count": len(organized_suggestions['tips']),
            "top_priority": organized_suggestions['critical'][:3] if organized_suggestions['critical'] else organized_suggestions['improvement'][:3]
        }
        return summary


# Convenience function
def generate_suggestions(episodes, language="en", max_suggestions=10):
    engine = SuggestionEngine()
    return engine.generate_suggestions(episodes, language, max_suggestions)


if __name__ == "__main__":
    # Self-test
    print("=" * 70)
    print("ENHANCED SUGGESTION ENGINE - SELF TEST")
    print("=" * 70)
    
    # Create test episodes with various data
    test_episodes = [
        {
            "number": 1,
            "title": "The Mysterious Key",
            "summary": "Detective Raj finds an old key at a crime scene.",
            "cliffhanger": "The key glows in his hand.",
            "cliffhanger_score": 3.2,
            "genre": "thriller",
            "emotion_curve": [
                {"time": 0, "emotion": "neutral", "intensity": 0.2},
                {"time": 30, "emotion": "curious", "intensity": 0.3},
                {"time": 60, "emotion": "curious", "intensity": 0.3},
                {"time": 90, "emotion": "curious", "intensity": 0.3}
            ],
            "retention_heatmap": [
                {"time": 5, "dropoff_risk": 0.3},
                {"time": 15, "dropoff_risk": 0.7},
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
            "genre": "thriller",
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
        }
    ]
    
    engine = SuggestionEngine()
    
    # Generate suggestions
    print("\n💡 Generating prioritized suggestions...")
    suggestions = engine.generate_suggestions(test_episodes, max_suggestions=15)
    
    # Print results
    print("\n" + "=" * 70)
    print("📊 PRIORITIZED SUGGESTIONS")
    print("=" * 70)
    
    if suggestions['critical']:
        print("\n🔴 CRITICAL (Must Fix):")
        for s in suggestions['critical']:
            print(f"   • [Importance: {s['importance']}/10] {s['text']}")
    
    if suggestions['improvement']:
        print("\n🟡 IMPORTANT IMPROVEMENTS:")
        for s in suggestions['improvement']:
            print(f"   • [Importance: {s['importance']}/10] {s['text']}")
    
    if suggestions['tips']:
        print("\n🔵 TIPS & SUGGESTIONS:")
        for s in suggestions['tips']:
            print(f"   • {s['text']}")