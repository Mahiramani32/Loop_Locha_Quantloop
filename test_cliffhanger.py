from backend.modules.cliffhanger_scorer import CliffhangerScorer

scorer = CliffhangerScorer()

# Test with different stories
test_stories = [
    {
        "name": "Boring Story",
        "text": "The cat sat on the mat. It was a sunny day. The end."
    },
    {
        "name": "Good Cliffhanger",
        "text": "Suddenly, the door burst open! She couldn't believe her eyes... To be continued!"
    },
    {
        "name": "Great Cliffhanger",
        "text": "Just then, she heard a strange noise. Little did she know, her life was about to change forever. What happened next would shock everyone... To be continued!"
    }
]

for story in test_stories:
    print(f"\n{'='*50}")
    print(f"Testing: {story['name']}")
    print('='*50)
    
    result = scorer.analyze_story(story['text'])
    print(f"Text: {story['text'][:50]}...")
    print(f"Cliffhanger Score: {result['overall_score']}")
    print(f"Number of Cliffhangers: {result['cliffhanger_count']}")
    if result['cliffhanger_moments']:
        print("Cliffhanger positions:", [m['position'] for m in result['cliffhanger_moments']])
    print("Recommendations:", result['recommendations'][0])