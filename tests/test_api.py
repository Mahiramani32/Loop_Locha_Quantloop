"""
Unit tests for the API endpoints.
"""

import pytest
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['data']['status'] == 'healthy'

def test_validate_story_valid(client):
    """Test story validation with valid input"""
    test_story = {
        "story": "This is a test story that is long enough to pass validation. " * 10,
        "title": "Test Story",
        "episodes": 5
    }
    response = client.post('/api/validate', json=test_story)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['data']['valid'] == True

def test_validate_story_too_short(client):
    """Test story validation with too short input"""
    test_story = {
        "story": "Too short",
        "title": "Test"
    }
    response = client.post('/api/validate', json=test_story)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] == False
    assert 'error' in data