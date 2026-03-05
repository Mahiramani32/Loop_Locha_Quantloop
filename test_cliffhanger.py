from backend.modules.cliffhanger_scorer import CliffhangerScorer

scorer = CliffhangerScorer()

# Test with different stories
stories = [
    "The cat sat on the mat. It was a sunny day. The end.",
    "Suddenly, the door burst open! She couldn't believe her eyes... To be continued!",
    "Just then, she heard a noise. Little did she know, everything would change..."
]

for i, story in enumerate(stories):
    print(f"\n--- Story {i+1} ---")
    result = scorer.analyze_story(story)
    print(f"Score: {result['overall_score']}")
    print(f"Cliffhangers: {result['cliffhanger_count']}")
    print(f"Recommendation: {result['recommendations'][0]}")