# -*- coding: utf-8 -*-
"""
Story Decomposer Module
Breaks stories into structural components for analysis
"""

import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from collections import Counter, defaultdict
from typing import Dict, List, Any, Optional
import logging
import string

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')

logger = logging.getLogger(__name__)

class StoryDecomposer:
    """Advanced story decomposition with structural analysis"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
        # Scene transition indicators
        self.scene_markers = [
            r'\n\s*\n', r'---', r'\*\*\*', r'Chapter \d+',
            r'Scene \d+', r'Act \d+', r'\[DAY \d+\]', r'\[NIGHT\]',
            r'Meanwhile,', r'Suddenly,', r'Later,', r'The next day,'
        ]
        
        # Dialogue indicators
        self.dialogue_patterns = [
            r'"[^"]*"',  # Double quotes
            r"'[^']*'",   # Single quotes
            r'Â«[^Â»]*Â»',   # French quotes
            r'"[^"]*"'    # Curly quotes
        ]
        
        # Cliffhanger indicators with weights
        self.cliffhanger_indicators = {
            'suddenly': 20,
            'without warning': 25,
            'to be continued': 30,
            'what happened next': 25,
            'just then': 15,
            'all of a sudden': 20,
            'out of nowhere': 25,
            '??': 10,
            '!?': 15,
            '...': 20,
            'but then': 15,
            'however': 10,
            'unexpectedly': 20,
            'knock on the door': 25,
            'a loud noise': 20,
            'the door opened': 15,
            'figure appeared': 25,
            'mysterious stranger': 30
        }
    
    def decompose(self, text: str, detailed: bool = False) -> Dict[str, Any]:
        """
        Decompose story into analyzable components
        
        Args:
            text: Full story text
            detailed: Return detailed analysis
            
        Returns:
            Structured story data
        """
        # Clean text
        text = self._clean_text(text)
        
        # Basic tokenization
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        paragraphs = self._extract_paragraphs(text)
        
        # Core analysis
        stats = self._get_basic_stats(text, sentences, words)
        elements = self._extract_story_elements(text, words)
        structure = self._identify_structure(paragraphs, sentences)
        scenes = self._extract_scenes(text)
        cliffhanger_score = self.score_cliffhanger(sentences)
        
        result = {
            'success': True,
            'statistics': stats,
            'elements': elements,
            'structure': structure,
            'cliffhanger': cliffhanger_score,
            'scenes': scenes[:10] if scenes else [],  # Limit scenes
        }
        
        if detailed:
            result['detailed'] = {
                'sentences': sentences[:20],
                'paragraphs': paragraphs[:10],
                'pos_distribution': self._get_pos_distribution(words),
                'vocabulary_richness': self._vocabulary_richness(words),
                'dialogue_analysis': self._analyze_dialogue(text)
            }
        
        return result
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common punctuation issues
        text = re.sub(r'\.\.+', '...', text)
        text = re.sub(r'!!+', '!', text)
        text = re.sub(r'\?\?+', '?', text)
        
        return text.strip()
    
    def _extract_paragraphs(self, text: str) -> List[str]:
        """Extract paragraphs from text"""
        # Split by double newlines or multiple newlines
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _get_basic_stats(self, text: str, sentences: List[str], words: List[str]) -> Dict:
        """Calculate basic text statistics"""
        # Filter out punctuation for word count
        clean_words = [w.lower() for w in words if w.isalnum()]
        
        return {
            'char_count': len(text),
            'word_count': len(clean_words),
            'sentence_count': len(sentences),
            'paragraph_count': len(self._extract_paragraphs(text)),
            'avg_word_length': sum(len(w) for w in clean_words) / len(clean_words) if clean_words else 0,
            'avg_sentence_length': len(clean_words) / len(sentences) if sentences else 0,
            'unique_words': len(set(clean_words)),
            'lexical_diversity': len(set(clean_words)) / len(clean_words) if clean_words else 0
        }
    
    def _extract_story_elements(self, text: str, words: List[str]) -> Dict:
        """Extract key story elements"""
        # Get part-of-speech tags
        pos_tags = pos_tag(words)
        
        # Extract named entities (simplified)
        named_entities = defaultdict(list)
        current_entity = []
        current_type = None
        
        for word, pos in pos_tags:
            # Simple NER using POS tags
            if pos == 'NNP' or pos == 'NNPS':
                current_entity.append(word)
                if pos == 'NNP':
                    current_type = 'PERSON'  # Simplification
                else:
                    current_type = 'ORGANIZATION'
            else:
                if current_entity:
                    named_entities[current_type].append(' '.join(current_entity))
                    current_entity = []
                    current_type = None
        
        if current_entity:
            named_entities[current_type].append(' '.join(current_entity))
        
        # Count frequencies
        character_freq = Counter(named_entities.get('PERSON', []))
        org_freq = Counter(named_entities.get('ORGANIZATION', []))
        
        # Detect setting (locations)
        locations = []
        for word, pos in pos_tags:
            if pos == 'NNP' and word.lower() in ['forest', 'castle', 'city', 'village', 'mountain', 'river']:
                locations.append(word)
        
        return {
            'characters': [
                {'name': name, 'mentions': count}
                for name, count in character_freq.most_common(10)
            ],
            'organizations': [
                {'name': name, 'mentions': count}
                for name, count in org_freq.most_common(5)
            ],
            'locations': list(set(locations))[:10],
            'has_protagonist': len(character_freq) > 0,
            'character_count': len(character_freq)
        }
    
    def _identify_structure(self, paragraphs: List[str], sentences: List[str]) -> Dict:
        """Identify narrative structure"""
        total_paragraphs = len(paragraphs)
        
        if total_paragraphs == 0:
            return {}
        
        # Rough 3-act structure based on paragraph position
        setup_end = max(1, int(total_paragraphs * 0.25))
        conflict_end = max(setup_end + 1, int(total_paragraphs * 0.6))
        
        # Detect story type based on structure
        story_type = 'unknown'
        if len(sentences) > 100:
            story_type = 'long_form'
        elif len(sentences) > 20:
            story_type = 'short_story'
        else:
            story_type = 'micro_fiction'
        
        return {
            'acts': {
                'setup': total_paragraphs > 0,
                'conflict': total_paragraphs > setup_end,
                'resolution': total_paragraphs > conflict_end
            },
            'paragraph_distribution': {
                'setup': setup_end,
                'conflict': conflict_end - setup_end,
                'resolution': total_paragraphs - conflict_end
            },
            'story_type': story_type,
            'has_cliffhanger': self._detect_cliffhanger(sentences)
        }
    
    def _detect_cliffhanger(self, sentences: List[str]) -> bool:
        """Detect if story ends with cliffhanger (simple boolean)"""
        if not sentences:
            return False
        
        last_sentence = sentences[-1].lower()
        
        # Cliffhanger indicators
        indicators = [
            'suddenly', 'without warning', 'to be continued',
            'what happened next', 'just then', 'all of a sudden',
            'out of nowhere', '??', '!?', '...',
            'but then', 'however', 'unexpectedly'
        ]
        
        # Check last sentence for cliffhanger patterns
        for indicator in indicators:
            if indicator in last_sentence:
                return True
        
        # Check if sentence ends with incomplete punctuation
        if last_sentence and not last_sentence[-1] in ['.', '!', '?']:
            return True
        
        # Check if last sentence is very short (dramatic effect)
        if len(last_sentence.split()) <= 3 and last_sentence:
            return True
        
        return False
    
    def score_cliffhanger(self, sentences: List[str]) -> Dict[str, Any]:
        """
        Return a detailed cliffhanger score 0-100 with explanation
        
        Args:
            sentences: List of sentences in the story
            
        Returns:
            Dictionary with score, strength, and reasons
        """
        if not sentences:
            return {'score': 0, 'strength': 'none', 'reasons': ['No sentences to analyze']}
        
        last_sentence = sentences[-1].lower()
        last_paragraph = ' '.join(sentences[-3:]).lower()  # Last few sentences
        
        score = 0
        reasons = []
        
        # Check last sentence for cliffhanger indicators
        for indicator, weight in self.cliffhanger_indicators.items():
            if indicator in last_sentence:
                score += weight
                reasons.append(f"Contains '{indicator}' in last sentence")
        
        # Check last paragraph for multiple indicators
        indicator_count = 0
        for indicator in self.cliffhanger_indicators.keys():
            if indicator in last_paragraph:
                indicator_count += 1
        
        if indicator_count >= 2:
            score += 15
            reasons.append(f"Multiple cliffhanger indicators ({indicator_count}) in closing")
        
        # Check for incomplete punctuation
        if last_sentence and last_sentence[-1] not in ['.', '!', '?']:
            score += 20
            reasons.append("Sentence ends with incomplete punctuation")
        
        # Check for very short sentence (dramatic effect)
        word_count = len(last_sentence.split())
        if word_count <= 3 and word_count > 0:
            score += 15
            reasons.append(f"Very short final sentence ({word_count} words) for dramatic effect")
        
        # Check for questions (creates anticipation)
        if '?' in last_sentence:
            score += 10
            reasons.append("Ends with a question, creating anticipation")
        
        # Check for exclamations (heightened emotion)
        if '!' in last_sentence:
            score += 10
            reasons.append("Ends with exclamation, emotional peak")
        
        # Check for ellipsis (trailing off)
        if '...' in last_sentence:
            score += 25
            reasons.append("Uses ellipsis to create suspense")
        
        # Normalize score to max 100
        score = min(score, 100)
        
        # Determine strength
        if score >= 70:
            strength = 'very_high'
        elif score >= 50:
            strength = 'high'
        elif score >= 30:
            strength = 'medium'
        elif score >= 10:
            strength = 'low'
        else:
            strength = 'none'
        
        return {
            'score': score,
            'strength': strength,
            'reasons': reasons[:5],  # Limit to top 5 reasons
            'has_cliffhanger': score > 20
        }
    
    def _extract_scenes(self, text: str) -> List[Dict]:
        """Extract scenes from text"""
        # Split by scene markers
        scene_pattern = '|'.join(self.scene_markers)
        potential_scenes = re.split(scene_pattern, text)
        
        scenes = []
        for i, scene_text in enumerate(potential_scenes):
            if len(scene_text.strip()) > 100:  # Minimum scene length
                scene_sentences = sent_tokenize(scene_text)
                scenes.append({
                    'scene_id': i + 1,
                    'text_preview': scene_text[:200] + '...' if len(scene_text) > 200 else scene_text,
                    'sentence_count': len(scene_sentences),
                    'word_count': len(scene_text.split()),
                    'has_dialogue': self._has_dialogue(scene_text)
                })
        
        return scenes
    
    def _has_dialogue(self, text: str) -> bool:
        """Check if text contains dialogue"""
        for pattern in self.dialogue_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def _get_pos_distribution(self, words: List[str]) -> Dict:
        """Get distribution of parts of speech"""
        pos_tags = pos_tag(words)
        pos_counts = Counter(tag for word, tag in pos_tags)
        
        total = len(pos_tags)
        return {
            tag: {
                'count': count,
                'percentage': round(count / total * 100, 2)
            }
            for tag, count in pos_counts.most_common(10)
        }
    
    def _vocabulary_richness(self, words: List[str]) -> float:
        """Calculate vocabulary richness (type-token ratio)"""
        clean_words = [w.lower() for w in words if w.isalnum()]
        if not clean_words:
            return 0
        return len(set(clean_words)) / len(clean_words)
    
    def _analyze_dialogue(self, text: str) -> Dict:
        """Analyze dialogue patterns"""
        dialogue_count = 0
        dialogue_lines = []
        
        for pattern in self.dialogue_patterns:
            matches = re.findall(pattern, text)
            dialogue_count += len(matches)
            dialogue_lines.extend(matches[:5])  # Store first 5
        
        return {
            'dialogue_count': dialogue_count,
            'has_dialogue': dialogue_count > 0,
            'dialogue_density': dialogue_count / len(sent_tokenize(text)) if text else 0,
            'sample_dialogues': dialogue_lines[:3]
        }

# Create singleton
story_decomposer = StoryDecomposer()

# Test code
if __name__ == "__main__":
    test_story = """
    Chapter 1: The Beginning
    
    Once upon a time, John and Mary lived in a small cottage near the forest.
    
    "I love this place," said Mary, looking at the sunset. "It's so peaceful here."
    
    John smiled and nodded. "Yes, but I wonder what lies beyond those mountains."
    
    The next day, a mysterious stranger arrived at their door. He wore dark robes 
    and carried an ancient map. "I need your help," he whispered urgently.
    
    Suddenly, the ground began to shake. A bright light appeared in the sky...
    """
    
    print("🔍 Testing Story Decomposer with Cliffhanger Scoring")
    print("="*70)
    
    result = story_decomposer.decompose(test_story, detailed=True)
    
    print(f"Statistics: {result['statistics']}")
    print(f"\nCharacters: {result['elements']['characters']}")
    print(f"\nStructure: {result['structure']}")
    print(f"\nCliffhanger Score: {result['cliffhanger']['score']} - {result['cliffhanger']['strength']}")
    print(f"Cliffhanger Reasons:")
    for reason in result['cliffhanger']['reasons']:
        print(f"  • {reason}")
    print(f"\nScenes: {len(result['scenes'])}")
