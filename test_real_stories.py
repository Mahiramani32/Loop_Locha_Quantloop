from backend.modules.cliffhanger_scorer import CliffhangerScorer

scorer = CliffhangerScorer()

# Real story examples that SHOULD get high scores
real_stories = [
    {
        "name": "Mystery Opening",
        "text": """The old mansion stood silent in the moonlight. Sarah hesitated at the door, 
        her hand trembling on the handle. Suddenly, a blood-curdling scream echoed from inside! 
        She pushed the door open and found... an empty room. But on the floor, a fresh trail of 
        blood led to a hidden passage. Little did she know, this was just the beginning of her nightmare."""
    },
    {
        "name": "Thriller Ending",
        "text": """Detective Brown examined the crime scene. Everything seemed normal, 
        but then he noticed something odd - the victim's watch was still ticking, 
        stopped at exactly 3:33 AM. Just then, his phone rang. A voice whispered, 
        'You're next.' The line went dead. To be continued..."""
    },
    {
        "name": "Romantic Cliffhanger",
        "text": """As they danced under the stars, Alex finally gathered the courage 
        to confess his feelings. But just as he was about to speak, a figure emerged 
        from the shadows - it was her ex, who was supposed to be thousands of miles away. 
        The look on her face said everything had just changed forever."""
    },
    {
        "name": "No Cliffhanger",
        "text": """The sun was shining. Birds were singing. It was a beautiful day. 
        They lived happily ever after. The end."""
    }
]

print("="*60)
print("TESTING CLIFFHANGER SCORER WITH REAL STORIES")
print("="*60)

for story in real_stories:
    print(f"\n📖 {story['name']}")
    print("-" * 40)
    result = scorer.analyze_story(story['text'])
    print(f"Cliffhanger Score: {result['overall_score']}")
    print(f"Cliffhangers Found: {result['cliffhanger_count']}")
    print(f"Average Intensity: {result['average_intensity']}")
    print(f"Has Final Cliffhanger: {result['has_final_cliffhanger']}")
    print("\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  • {rec}")
    
    # Show first cliffhanger if any
    if result['cliffhanger_moments']:
        print(f"\nFirst cliffhanger at position {result['cliffhanger_moments'][0]['position']}")
        print(f"Intensity: {result['cliffhanger_moments'][0]['intensity']}")