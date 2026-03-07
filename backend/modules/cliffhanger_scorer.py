"""
Cliffhanger Scorer Module
Analyzes story text to detect and score cliffhanger moments
Author: Mahi
"""

import re
import numpy as np
from typing import List, Dict, Any

class CliffhangerScorer:
    """Main class for cliffhanger detection and scoring"""
    
    def __init__(self):
        """Initialize the cliffhanger detector with patterns"""
        self.cliffhanger_keywords = [
            'suddenly', 'unexpected', 'without warning', 'out of nowhere',
            'just then', 'at that moment', 'little did they know',
            'to be continued', 'what happened next', 'never expected',
            'shock', 'surprise', 'revealed', 'discovered', 'realized',
            'but then', 'however', 'everything changed', 'in an instant',
            'couldn\'t believe', 'turned to see', 'gasped', 'froze',
            'heart pounded', 'shadow moved', 'door creaked', 'whispered',
            'mysterious', 'strange', 'odd', 'peculiar', 'unusual',
            'cliffhanger', 'stay tuned', 'next time', 'find out',
            'what happens next', 'will they survive', 'the truth'
        ]
        
        self.cliffhanger_punctuation = [
            '...', '?!', '!?', '!!!', '??', '...!', '!...', '?', '!'
        ]
        
        # Adjusted weights for better scoring
        self.weights = {
            'keyword': 0.5,
            'punctuation': 0.3,
            'position': 0.2,
            'ending': 0.1
        }
    
    def analyze_story(self, text: str) -> Dict[str, Any]:
        """Complete analysis of a story for cliffhangers"""
        if not text or len(text.strip()) < 20:
            return self._default_result()
        
        sentences = self._split_sentences(text)
        
        if not sentences:
            return self._default_result()
        
        sentence_scores = []
        cliffhanger_moments = []
        
        for i, sentence in enumerate(sentences):
            score = self._score_sentence(sentence, i, len(sentences))
            sentence_scores.append(score)
            
            if score > 0.15:  # Lower threshold to catch more cliffhangers
                cliffhanger_moments.append({
                    'position': i,
                    'sentence': sentence[:100] + '...' if len(sentence) > 100 else sentence,
                    'score': round(score, 2),
                    'intensity': self._get_intensity_label(score)
                })
        
        overall_score = self._calculate_overall_score(sentence_scores, cliffhanger_moments, text)
        has_final = self._has_final_cliffhanger(sentences, cliffhanger_moments)
        recommendations = self._generate_recommendations(overall_score, cliffhanger_moments, has_final)
        
        return {
            'overall_score': round(overall_score, 2),
            'cliffhanger_count': len(cliffhanger_moments),
            'cliffhanger_moments': cliffhanger_moments,
            'average_intensity': round(np.mean([c['score'] for c in cliffhanger_moments]), 2) if cliffhanger_moments else 0,
            'has_final_cliffhanger': has_final,
            'recommendations': recommendations
        }
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _score_sentence(self, sentence: str, position: int, total_sentences: int) -> float:
        """Score individual sentence for cliffhanger potential"""
        score = 0.0
        sentence_lower = sentence.lower()
        
        # Check keywords - increased weight
        keyword_score = 0
        for keyword in self.cliffhanger_keywords:
            if keyword in sentence_lower:
                keyword_score += 0.2  # Increased from 0.15
        keyword_score = min(keyword_score, 1.0)
        score += keyword_score * self.weights['keyword']
        
        # Check punctuation
        punct_score = 0
        for punct in self.cliffhanger_punctuation:
            if punct in sentence:
                punct_score += 0.25  # Increased from 0.2
        punct_score = min(punct_score, 0.9)
        score += punct_score * self.weights['punctuation']
        
        # Position bonus - last sentences get higher score
        if position >= total_sentences - 2:  # Last 2 sentences
            position_score = 0.8
        elif position > total_sentences * 0.7:
            position_score = 0.5
        elif position > total_sentences * 0.5:
            position_score = 0.3
        else:
            position_score = 0.1
            
        score += position_score * self.weights['position']
        
        return min(score, 1.0)
    
    def _calculate_overall_score(self, sentence_scores: List[float], cliffhanger_moments: List[Dict], text: str) -> float:
        """Calculate overall cliffhanger score - IMPROVED"""
        if not sentence_scores:
            return 0.3  # Base score
        
        # Give more weight to last sentences
        weighted_scores = []
        for i, score in enumerate(sentence_scores):
            weight = 1.0 + (i / len(sentence_scores))  # Later sentences weighted more
            weighted_scores.append(score * weight)
        
        # Use weighted average
        base_score = sum(weighted_scores) / len(weighted_scores)
        
        # Bonus for cliffhanger moments
        count_bonus = min(len(cliffhanger_moments) * 0.15, 0.4)
        
        # Check if text has cliffhanger indicators
        text_lower = text.lower()
        if 'to be continued' in text_lower or 'next episode' in text_lower:
            count_bonus += 0.2
        if '?' in text[-20:] or '!' in text[-20:]:
            count_bonus += 0.1
        
        return min(base_score + count_bonus, 1.0)
    
    def _has_final_cliffhanger(self, sentences: List[str], cliffhanger_moments: List[Dict]) -> bool:
        """Check if story ends with cliffhanger"""
        if not sentences:
            return False
        
        last_sentence = sentences[-1].lower()
        cliffhanger_indicators = ['?', '!', '...', 'suddenly', 'unexpected', 'surprise']
        
        # Check if last sentence has cliffhanger indicators
        has_indicator = any(ind in last_sentence for ind in cliffhanger_indicators)
        
        # Check if last sentence is a cliffhanger moment
        last_is_cliffhanger = False
        if cliffhanger_moments:
            last_pos = cliffhanger_moments[-1]['position']
            last_is_cliffhanger = last_pos >= len(sentences) - 2
        
        return has_indicator or last_is_cliffhanger
    
    def _get_intensity_label(self, score: float) -> str:
        """Convert score to label"""
        if score >= 0.7:
            return "High"
        elif score >= 0.4:
            return "Medium"
        else:
            return "Low"
    
    def _generate_recommendations(self, overall_score: float, cliffhanger_moments: List[Dict], has_final: bool) -> List[str]:
        """Generate recommendations"""
        recommendations = []
        
        if overall_score < 0.3:
            recommendations.append("⚠️ Your story needs stronger cliffhangers. Add unexpected twists or revelations.")
            recommendations.append("💡 End scenes with questions, mysteries, or shocking moments.")
            recommendations.append("📝 Use words like 'suddenly', 'unexpectedly', or 'to be continued'.")
        elif overall_score < 0.5:
            recommendations.append("👍 Good start! Add 1-2 more cliffhanger moments for better engagement.")
            if not has_final:
                recommendations.append("🎯 Make sure your final episode ends with a strong cliffhanger.")
            if len(cliffhanger_moments) < 3:
                recommendations.append("📈 Consider adding cliffhangers at the end of each episode.")
        elif overall_score < 0.7:
            recommendations.append("🌟 Great cliffhanger usage! Your story will keep viewers hooked.")
            if not has_final:
                recommendations.append("✨ Add a final twist to make viewers want the next season.")
        else:
            recommendations.append("🏆 Excellent cliffhanger scoring! Perfect for binge-watching.")
        
        return recommendations
    
    def _default_result(self) -> Dict[str, Any]:
        """Return default result"""
        return {
            'overall_score': 0.5,  # Default medium score
            'cliffhanger_count': 1,
            'cliffhanger_moments': [],
            'average_intensity': 0.5,
            'has_final_cliffhanger': False,
            'recommendations': ["Add more suspenseful moments to increase cliffhanger score"]
        }


# Test the module
if __name__ == "__main__":
    scorer = CliffhangerScorer()
    test_story = "Suddenly, everything changed. She found... an empty chair. To be continued..."
    result = scorer.analyze_story(test_story)
    print(f"Cliffhanger Score: {result['overall_score']}")
    print(f"Recommendations: {result['recommendations'][0]}")