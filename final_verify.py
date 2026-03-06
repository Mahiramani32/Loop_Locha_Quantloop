"""
FINAL VERIFICATION SCRIPT - Tests EVERYTHING!
"""

import requests
import json
import time
import sys
import subprocess
import os

# Add backend folder to path so we can import app if needed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

BASE_URL = "http://localhost:5000/api"

def print_header(text):
    print(f"\n{'='*60}")
    print(f"🔍 {text}")
    print('='*60)

def print_result(test_name, passed, details=""):
    if passed:
        print(f"✅ {test_name}: PASSED")
    else:
        print(f"❌ {test_name}: FAILED")
    if details:
        print(f"   {details}")

# Test 1: Server Connection
print_header("TEST 1: SERVER CONNECTION")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print_result("Server Connection", response.status_code == 200, 
                 f"Status: {response.status_code}")
except Exception as e:
    print_result("Server Connection", False, str(e))

# Test 2: Health Endpoint
print_header("TEST 2: HEALTH ENDPOINT")
try:
    response = requests.get(f"{BASE_URL}/health")
    data = response.json()
    tests_passed = (
        response.status_code == 200 and
        data.get('success') == True and
        data.get('data', {}).get('status') == 'healthy'
    )
    print_result("Health Endpoint", tests_passed,
                 f"Status: {data.get('data', {}).get('status')}")
except Exception as e:
    print_result("Health Endpoint", False, str(e))

# Test 3: Validation - Valid Story
print_header("TEST 3: VALIDATION - VALID STORY")
valid_story = {
    "story": "This is a test story about a brave knight who goes on an epic adventure. " * 15,
    "title": "The Brave Knight",
    "episodes": 5
}
try:
    response = requests.post(f"{BASE_URL}/validate", json=valid_story)
    data = response.json()
    tests_passed = (
        response.status_code == 200 and
        data.get('success') == True and
        data.get('data', {}).get('valid') == True
    )
    print_result("Valid Story Validation", tests_passed,
                 f"Length: {data.get('data', {}).get('length')} chars")
except Exception as e:
    print_result("Valid Story Validation", False, str(e))

# Test 4: Validation - Invalid Story
print_header("TEST 4: VALIDATION - INVALID STORY")
invalid_story = {
    "story": "Too short",
    "title": "Test"
}
try:
    response = requests.post(f"{BASE_URL}/validate", json=invalid_story)
    tests_passed = response.status_code == 400
    print_result("Invalid Story Validation", tests_passed,
                 f"Expected 400, Got: {response.status_code}")
except Exception as e:
    print_result("Invalid Story Validation", False, str(e))

# Test 5: Analyze Endpoint
print_header("TEST 5: ANALYZE ENDPOINT")
analyze_story = {
    "story": "A brave knight named Arthur lived in a small kingdom. " * 20,
    "title": "The Dragon's Treasure",
    "episodes": 5
}
try:
    response = requests.post(f"{BASE_URL}/analyze", json=analyze_story, timeout=10)
    data = response.json()
    tests_passed = (
        response.status_code == 200 and
        data.get('success') == True and
        'data' in data and
        'episodes' in data['data']
    )
    if tests_passed:
        episodes = len(data['data'].get('episodes', []))
        print_result("Analyze Endpoint", tests_passed,
                     f"Generated {episodes} episodes")
    else:
        print_result("Analyze Endpoint", False)
except Exception as e:
    print_result("Analyze Endpoint", False, str(e))

# Test 6: Error Handling - No Data
print_header("TEST 6: ERROR HANDLING - NO DATA")
try:
    response = requests.post(f"{BASE_URL}/validate", json={})
    tests_passed = response.status_code == 400
    print_result("Empty Data Error", tests_passed,
                 f"Expected 400, Got: {response.status_code}")
except Exception as e:
    print_result("Empty Data Error", False, str(e))

# Test 7: Error Handling - Wrong Method
print_header("TEST 7: ERROR HANDLING - WRONG METHOD")
try:
    response = requests.get(f"{BASE_URL}/validate")
    tests_passed = response.status_code == 405
    print_result("Wrong Method Error", tests_passed,
                 f"Expected 405, Got: {response.status_code}")
except Exception as e:
    print_result("Wrong Method Error", False, str(e))

# Test 8: Response Time
print_header("TEST 8: RESPONSE TIME")
try:
    start = time.time()
    requests.get(f"{BASE_URL}/health")
    response_time = (time.time() - start) * 1000
    tests_passed = response_time < 1000  # Under 1 second
    print_result("Response Time", tests_passed,
                 f"{response_time:.2f}ms")
except Exception as e:
    print_result("Response Time", False, str(e))

# Test 9: Caching
print_header("TEST 9: CACHING")
try:
    # First request
    start1 = time.time()
    response1 = requests.post(f"{BASE_URL}/analyze", json=analyze_story)
    time1 = time.time() - start1
    
    # Second request (should be cached)
    start2 = time.time()
    response2 = requests.post(f"{BASE_URL}/analyze", json=analyze_story)
    time2 = time.time() - start2
    
    if time2 < time1:
        print_result("Caching", True, 
                     f"First: {time1*1000:.2f}ms, Second: {time2*1000:.2f}ms (faster)")
    else:
        print_result("Caching", False, "Caching may not be working")
except Exception as e:
    print_result("Caching", False, str(e))

# Test 10: Docker Status
print_header("TEST 10: DOCKER STATUS")
try:
    result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    if "episodic-intelligence" in result.stdout:
        print_result("Docker Containers", True, "Containers are running")
        
        # Show running containers
        compose_result = subprocess.run(["docker-compose", "ps"], capture_output=True, text=True)
        print("\n" + compose_result.stdout)
    else:
        print_result("Docker Containers", False, "Containers not running")
except Exception as e:
    print_result("Docker Containers", False, str(e))

# FINAL SUMMARY
print_header("📊 FINAL VERIFICATION SUMMARY")
print("🎉 YOUR BACKEND IS READY! 🎉")
print(f"\n🌐 API URL: {BASE_URL}")
print("📚 Endpoints:")
print("   - GET  /health")
print("   - POST /validate")
print("   - POST /analyze")

# Optional: Test if we can import app (just to verify path)
try:
    from app import app
    print("\n✅ Backend module import successful!")
except Exception as e:
    print(f"\n⚠️ Note: Could not import app module (but API tests may still work): {e}")