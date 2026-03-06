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
            'but then', 'however', 'everything changed', 'in an instant'
        ]
        
        self.cliffhanger_punctuation = [
            '...', '?!', '!?', '!!!', '??', '...!', '!...'
        ]
        
        self.weights = {
            'keyword': 0.4,
            'punctuation': 0.3,
            'position': 0.2,
            'ending': 0.1
        }
    
    def analyze_story(self, text: str) -> Dict[str, Any]:
        """Complete analysis of a story for cliffhangers"""
        sentences = self._split_sentences(text)
        
        if not sentences:
            return self._empty_result()
        
        sentence_scores = []
        cliffhanger_moments = []
        
        for i, sentence in enumerate(sentences):
            score = self._score_sentence(sentence, i, len(sentences))
            sentence_scores.append(score)
            
            if score > 0.3:
                cliffhanger_moments.append({
                    'position': i,
                    'sentence': sentence[:100] + '...' if len(sentence) > 100 else sentence,
                    'score': round(score, 2),
                    'intensity': self._get_intensity_label(score)
                })
        
        overall_score = self._calculate_overall_score(sentence_scores, cliffhanger_moments)
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
        
        # Check keywords
        keyword_score = 0
        for keyword in self.cliffhanger_keywords:
            if keyword in sentence_lower:
                keyword_score += 0.1
        keyword_score = min(keyword_score, 0.8)
        score += keyword_score * self.weights['keyword']
        
        # Check punctuation
        punct_score = 0
        for punct in self.cliffhanger_punctuation:
            if punct in sentence:
                punct_score += 0.15
        punct_score = min(punct_score, 0.6)
        score += punct_score * self.weights['punctuation']
        
        # Position bonus
        position_score = 0
        if position > total_sentences * 0.8:
            position_score = 0.3
        elif position > total_sentences * 0.6:
            position_score = 0.15
        score += position_score * self.weights['position']
        
        return min(score, 1.0)
    
    def _calculate_overall_score(self, sentence_scores: List[float], cliffhanger_moments: List[Dict]) -> float:
        """Calculate overall cliffhanger score"""
        if not sentence_scores:
            return 0.0
        
        base_score = max(sentence_scores) if sentence_scores else 0.0
        count_bonus = min(len(cliffhanger_moments) * 0.05, 0.2)
        
        return min(base_score + count_bonus, 1.0)
    
    def _has_final_cliffhanger(self, sentences: List[str], cliffhanger_moments: List[Dict]) -> bool:
        """Check if story ends with cliffhanger"""
        if not cliffhanger_moments or not sentences:
            return False
        last_pos = cliffhanger_moments[-1]['position']
        return last_pos > len(sentences) * 0.8
    
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
            recommendations.append("Add more cliffhanger moments throughout your story")
            recommendations.append("Use suspenseful keywords like 'suddenly' or 'unexpectedly'")
            recommendations.append("End scenes with questions or revelations")
        elif overall_score < 0.6:
            recommendations.append("Good start! Consider adding a stronger cliffhanger at the end")
            if len(cliffhanger_moments) < 3:
                recommendations.append("Add 1-2 more cliffhanger moments for better engagement")
            if not has_final:
                recommendations.append("Make sure your story ends with a cliffhanger to keep readers wanting more")
        else:
            recommendations.append("Excellent cliffhanger usage!")
            if not has_final:
                recommendations.append("Your story has good cliffhangers, but consider a stronger ending")
            else:
                recommendations.append("Perfect! Your story will keep readers hooked")
        
        return recommendations
    
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty result"""
        return {
            'overall_score': 0,
            'cliffhanger_count': 0,
            'cliffhanger_moments': [],
            'average_intensity': 0,
            'has_final_cliffhanger': False,
            'recommendations': ["Add some text to analyze"]
        }


# Test the module
if __name__ == "__main__":
    scorer = CliffhangerScorer()
    test_story = "Suddenly, everything changed. She found... an empty chair. To be continued..."
    result = scorer.analyze_story(test_story)
    print("Cliffhanger Score:", result['overall_score'])
    print("Has Final Cliffhanger:", result['has_final_cliffhanger'])
    print("Recommendations:", result['recommendations'][0])