"""
Input validation module for API requests.
"""

class StoryValidator:
    """Validator for story input data"""
    
    @staticmethod
    def validate_story_input(data):
        """
        Validate the main story analysis request.
        Returns: (is_valid, error_message)
        """
        # Check if data exists
        if not data:
            return False, "No data provided"
        
        # Check if story field exists
        if 'story' not in data:
            return False, "Missing 'story' field"
        
        story = data['story']
        
        # Validate story type
        if not isinstance(story, str):
            return False, "Story must be a string"
        
        # Validate story length
        story = story.strip()
        if len(story) < 50:
            return False, "Story too short (minimum 50 characters)"
        
        if len(story) > 10000:
            return False, "Story too long (maximum 10000 characters)"
        
        # Validate title if provided
        if 'title' in data and data['title']:
            if not isinstance(data['title'], str):
                return False, "Title must be a string"
            if len(data['title']) > 200:
                return False, "Title too long (maximum 200 characters)"
        
        # Validate episodes number if provided
        if 'episodes' in data:
            episodes = data['episodes']
            if not isinstance(episodes, int):
                return False, "Episodes must be a number"
            if episodes < 3 or episodes > 10:
                return False, "Episodes must be between 3 and 10"
        
        return True, None