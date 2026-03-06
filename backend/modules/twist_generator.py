"""
Twist Generator Module - ENHANCED VERSION
Generates creative plot twists for episodes with:
- 15+ categories, 150+ twists
- Hindi language support
- Contextual twists using episode keywords
- Genre detection from summary
- Weighted importance scoring
Author: Shreya (Person 4)
"""

import json
import random
import re
from pathlib import Path
from collections import defaultdict

class TwistGenerator:
    """
    Enhanced twist generator with multi-language support and contextual generation
    """
    
    def __init__(self):
        """Initialize the twist generator and load twist bank"""
        self.twist_bank = self._load_twist_bank()
        self.supported_languages = ['en', 'hi']  # Add more as needed
        self.stats = self.get_statistics()
        print(f"✅ TwistGenerator initialized with:")
        print(f"   - {self.stats['total_categories']} categories")
        print(f"   - {self.stats['total_twists']} total twists")
        print(f"   - Languages: {', '.join(self.stats['languages'])}")
        
    def _load_twist_bank(self):
        """Load twist templates from JSON file"""
        current_file = Path(__file__)
        modules_dir = current_file.parent
        backend_dir = modules_dir.parent
        models_path = backend_dir / 'models' / 'twist_bank.json'
        
        try:
            with open(models_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"⚠️ Twist bank file not found. Using defaults.")
            return self._get_default_twists()
        except json.JSONDecodeError:
            print(f"⚠️ Error parsing JSON. Using defaults.")
            return self._get_default_twists()
    
    def _get_default_twists(self):
        """Return default twists if file loading fails"""
        return {
            "betrayal": {
                "en": ["Someone betrays the hero."],
                "hi": ["कोई हीरो को धोखा देता है।"]
            },
            "revelation": {
                "en": ["A shocking truth is revealed."],
                "hi": ["एक चौंकाने वाला सच सामने आता है।"]
            }
        }
    
    def _detect_genre_from_summary(self, summary):
        """Detect genre from episode summary using keywords"""
        if not summary:
            return "general"
            
        summary = summary.lower()
        
        genre_keywords = {
            "horror": ['horror', 'ghost', 'scary', 'haunted', 'demon', 'possessed', 'creepy', 'terrifying', 'fear', 'nightmare', 'blood', 'die', 'dead', 'kill', 'murder', 'corpse', 'scream', 'dark', 'shadow', 'monster'],
            "romance": ['love', 'romance', 'heart', 'kiss', 'relationship', 'couple', 'marry', 'wedding', 'feelings', 'emotion', 'care', 'together', 'romantic', 'date', 'crush', 'passion'],
            "comedy": ['funny', 'comedy', 'humor', 'joke', 'laugh', 'hilarious', 'silly', 'crazy', 'absurd', 'ridiculous', 'prank', 'comic', 'wit', 'humorous'],
            "scifi": ['sci-fi', 'future', 'robot', 'alien', 'space', 'technology', 'scientific', 'experiment', 'time travel', 'dimension', 'parallel universe', 'cyber', 'ai', 'android', 'spaceship', 'galaxy'],
            "fantasy": ['magic', 'fantasy', 'wizard', 'dragon', 'spell', 'curse', 'mythical', 'legend', 'sword', 'kingdom', 'prophecy', 'quest', 'sorcerer', 'elf', 'fairy', 'mythology'],
            "thriller": ['thriller', 'suspense', 'mystery', 'chase', 'escape', 'hunt', 'stalk', 'frame', 'conspiracy', 'secret', 'hide', 'danger', 'tense', 'edge', 'suspenseful']
        }
        
        for genre, keywords in genre_keywords.items():
            if any(keyword in summary for keyword in keywords):
                return genre
        
        return "general"
    
    def _extract_keywords(self, text, max_words=5):
        """Extract important keywords from text"""
        if not text:
            return []
        
        # Simple keyword extraction
        text = text.lower()
        # Remove common words
        common_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'was', 'are', 'were', 'has', 'have', 'had', 'this', 'that', 'these', 'those']
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text)  # Only words with 4+ letters
        keywords = [w for w in words if w not in common_words]
        
        # Return unique keywords, limited to max_words
        return list(set(keywords))[:max_words]
    
    def calculate_twist_importance(self, episode_num, genre, category):
        """Calculate importance score for a twist (1-10)"""
        importance = 7  # Base score
        
        # Episode position matters
        if episode_num == 1 or episode_num == 5:  # First or last episode
            importance += 2
        elif episode_num == 3:  # Middle episode
            importance += 1
        
        # Genre matters
        important_categories = {
            "horror": ["suspense", "revelation"],
            "thriller": ["betrayal", "identity"],
            "fantasy": ["revelation", "time"],
            "romance": ["betrayal", "unexpected_ally"],
            "scifi": ["time", "revelation"]
        }
        
        if genre in important_categories and category in important_categories[genre]:
            importance += 1
        
        return min(importance, 10)
    
    def generate_twists(self, story=None, episodes=None, language="en", twists_per_episode=2):

        if story is None:
           story = ""  # Default empty story
        if episodes is None:
           episodes = []  # Default empty list
        
        """
        Generate contextual twists for each episode
        
        Args:
            story: Original story text
            episodes: List of episode dictionaries
            language: Language code ('en' or 'hi')
            twists_per_episode: Number of twists per episode
        
        Returns:
            list: Twists per episode with context and importance scores
        """
        print(f"\n🎭 Generating {twists_per_episode} contextual twist(s) per episode...")
        
        if language not in self.supported_languages:
            print(f"⚠️ Language '{language}' not supported. Falling back to English.")
            language = 'en'
        
        result = []
        all_keywords = []
        total_episodes = len(episodes)
        
        # First pass: collect all keywords for context
        for episode in episodes:
            episode_summary = episode.get('summary', '')
            episode_cliffhanger = episode.get('cliffhanger', '')
            combined = episode_summary + " " + episode_cliffhanger
            all_keywords.extend(self._extract_keywords(combined, max_words=3))
        
        all_keywords = list(set(all_keywords))  # Remove duplicates
        
        # Second pass: generate twists
        for episode_index, episode in enumerate(episodes, 1):
            episode_title = episode.get('title', f'Episode {episode_index}')
            episode_summary = episode.get('summary', '')
            episode_cliffhanger = episode.get('cliffhanger', '')
            
            # Detect genre from summary
            genre = self._detect_genre_from_summary(episode_summary)
            
            # Extract keywords for this episode specifically
            episode_keywords = self._extract_keywords(episode_summary + " " + episode_cliffhanger)
            
            print(f"  Processing Episode {episode_index}: {episode_title}")
            print(f"    Genre detected: {genre}")
            print(f"    Keywords: {', '.join(episode_keywords) if episode_keywords else 'none'}")
            
            # Generate twists for this episode
            episode_twists = []
            
            for twist_num in range(twists_per_episode):
                twist_data = self._generate_contextual_twist(
                    episode_index,
                    total_episodes,
                    episode_summary,
                    episode_cliffhanger,
                    genre,
                    episode_keywords,
                    all_keywords,
                    language
                )
                episode_twists.append(twist_data)
            
            result.append({
                "episode": episode_index,
                "title": episode_title,
                "genre": genre,
                "twists": episode_twists
            })
        
        print(f"✅ Generated {len(result)} episodes with {twists_per_episode} twists each")
        return result
    
    def _generate_contextual_twist(self, episode_num, total_episodes, summary, cliffhanger, genre, episode_keywords, all_keywords, language):
        """Generate a twist considering all context"""
        
        # Determine which categories to use based on genre and episode position
        if genre != "general" and genre in self.twist_bank:
            # Use genre-specific categories first
            primary_categories = [genre]
            secondary_categories = ["revelation", "suspense", "betrayal"]
        else:
            # Default categories based on episode position
            if episode_num == 1:
                primary_categories = ["revelation", "suspense"]
                secondary_categories = ["identity", "time"]
            elif episode_num == total_episodes:
                primary_categories = ["revelation", "identity", "moral_dilemma"]
                secondary_categories = ["betrayal", "time"]
            elif total_episodes > 2 and episode_num == (total_episodes // 2) + 1:
                primary_categories = ["betrayal", "identity", "time"]
                secondary_categories = ["revelation", "suspense"]
            else:
                primary_categories = ["suspense", "revelation"]
                secondary_categories = ["unexpected_ally", "moral_dilemma"]
        
        # Build available categories list
        available_categories = []
        for cat in primary_categories:
            if cat in self.twist_bank and language in self.twist_bank[cat]:
                available_categories.append(cat)
        
        if not available_categories:
            for cat in secondary_categories:
                if cat in self.twist_bank and language in self.twist_bank[cat]:
                    available_categories.append(cat)
        
        # If still no categories, use any available
        if not available_categories:
            available_categories = [cat for cat in self.twist_bank.keys() 
                                   if language in self.twist_bank[cat]]
        
        if not available_categories:
            return {
                "text": "Something unexpected happens." if language == 'en' else "कुछ अप्रत्याशित होता है।",
                "category": "general",
                "importance": 5,
                "language": language
            }
        
        # Choose category and twist
        category = random.choice(available_categories)
        twists_in_category = self.twist_bank[category][language]
        twist_template = random.choice(twists_in_category)
        
        # Calculate importance score
        importance = self.calculate_twist_importance(episode_num, genre, category)
        
        # Personalize twist with keywords if available
        if episode_keywords and random.random() > 0.4:  # 60% chance to personalize
            keyword = random.choice(episode_keywords)
            if language == 'en':
                twist_text = f"When it comes to {keyword}... {twist_template}"
            else:
                twist_text = f"जब {keyword} की बात आती है... {twist_template}"
        elif all_keywords and random.random() > 0.6:  # 40% chance to use global keywords
            keyword = random.choice(all_keywords)
            if language == 'en':
                twist_text = f"About {keyword}... {twist_template}"
            else:
                twist_text = f"{keyword} के बारे में... {twist_template}"
        else:
            twist_text = twist_template
        
        # Add prefix based on episode position - FIXED
        if episode_num == 1:
            prefix = "🔮 Opening shock: " if language == 'en' else "🔮 शुरुआती झटका: "
        elif episode_num == total_episodes:
            prefix = "🎬 Finale bombshell: " if language == 'en' else "🎬 समापन धमाका: "
        elif total_episodes > 2 and episode_num == (total_episodes // 2) + 1:
            prefix = "⚡ Mid-point twist: " if language == 'en' else "⚡ मध्य मोड़: "
        else:
            prefix = "✨ Twist: " if language == 'en' else "✨ ट्विस्ट: "
        
        return {
            "text": prefix + twist_text,
            "category": category,
            "importance": importance,
            "language": language
        }
    
    def get_twists_by_category(self, category, language="en", count=5):
        """Get multiple twists from a specific category"""
        if category in self.twist_bank and language in self.twist_bank[category]:
            twists = self.twist_bank[category][language]
            selected = random.sample(twists, min(count, len(twists)))
            return [{"text": t, "category": category, "language": language} for t in selected]
        return []
    
    def get_statistics(self):
        """Get detailed statistics about the twist bank"""
        stats = {
            "total_categories": len(self.twist_bank),
            "total_twists": 0,
            "languages": set(),
            "categories": {}
        }
        
        for category, lang_data in self.twist_bank.items():
            stats["categories"][category] = {}
            for lang, twists in lang_data.items():
                stats["languages"].add(lang)
                stats["categories"][category][lang] = len(twists)
                stats["total_twists"] += len(twists)
        
        stats["languages"] = list(stats["languages"])
        return stats
    
    def add_twist(self, category, language, twist_text):
        """Add a new twist to the bank"""
        if category not in self.twist_bank:
            self.twist_bank[category] = {}
        if language not in self.twist_bank[category]:
            self.twist_bank[category][language] = []
        
        self.twist_bank[category][language].append(twist_text)
        self._save_twist_bank()
        return True
    
    def _save_twist_bank(self):
        """Save the current twist bank to file"""
        try:
            current_file = Path(__file__)
            modules_dir = current_file.parent
            backend_dir = modules_dir.parent
            models_path = backend_dir / 'models' / 'twist_bank.json'
            
            with open(models_path, 'w', encoding='utf-8') as file:
                json.dump(self.twist_bank, file, indent=2, ensure_ascii=False)
            print("✅ Twist bank saved successfully")
        except Exception as e:
            print(f"❌ Error saving twist bank: {e}")


# Convenience function
def generate_twists(story, episodes, language="en", count=2):
    generator = TwistGenerator()
    return generator.generate_twists(story, episodes, language, count)


if __name__ == "__main__":
    # Self-test
    print("=" * 70)
    print("ENHANCED TWIST GENERATOR - SELF TEST")
    print("=" * 70)
    
    test_story = "A detective finds a mysterious key that opens a door to a parallel world"
    test_episodes = [
        {
            "title": "The Discovery",
            "summary": "Detective Raj finds an old key at a haunted crime scene that glows in the dark. Strange things start happening.",
            "cliffhanger": "As he touches the key, everything goes dark and he hears a whisper: 'Find the door...'"
        },
        {
            "title": "The Door",
            "summary": "Raj discovers a magical door that only appears at midnight. The key fits perfectly and strange symbols glow.",
            "cliffhanger": "He opens the door and sees his dead partner standing there, alive and smiling."
        },
        {
            "title": "The Parallel World",
            "summary": "In the parallel world, Raj's partner is alive but doesn't recognize him. This world is darker and dangerous.",
            "cliffhanger": "Someone from Raj's world follows him through the door, holding a weapon."
        }
    ]
    
    generator = TwistGenerator()
    
    # Test English twists
    print("\n🇬🇧 ENGLISH TWISTS:")
    twists_en = generator.generate_twists(test_story, test_episodes, language="en", count=2)
    for ep in twists_en:
        print(f"\n📺 Episode {ep['episode']} - {ep['title']} (Genre: {ep['genre']})")
        for i, twist in enumerate(ep['twists'], 1):
            print(f"   {i}. [{twist['importance']}/10] {twist['text']}")