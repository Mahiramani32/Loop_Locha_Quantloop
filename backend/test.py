import sys
import copy
sys.path.append('.')
from flask import Flask
from app import app, cache

with app.test_request_context('/api/analyze', method='POST', json={'story': 'a girl lost her phone near eiffel tower and conrad fisher got it and gifted to belly.', 'episodes': 5}):
    from app import analyze_story
    response = analyze_story()
    data = response[0].get_json()
    print('EPISODES OUTPUT MAP:')
    for ep in data['data']['episodes']:
        print('Ep', ep['episode_number'], 'Cliff:', ep.get('cliffhanger_score'), 'Ret:', ep.get('retention_score'))
        print('   Summary:', repr(ep.get('summary', ''))[:50])
