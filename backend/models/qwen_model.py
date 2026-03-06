"""
Qwen Model Wrapper for OpenRouter
Handles all API calls to Qwen model
Author: Person 2
"""

import openai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

class QwenModel:
    """
    Wrapper for Qwen model on OpenRouter
    """
    
    def __init__(self):
        """Initialize the Qwen client"""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            print("⚠️ OPENROUTER_API_KEY not found in .env file! Using fallback mode.")
            self.api_key = "dummy-key"
        
        # OpenRouter base URL
        self.base_url = "https://openrouter.ai/api/v1"
        
        try:
            # Configure OpenAI client to use OpenRouter
            self.client = openai.OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
                default_headers={
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "Episodic Intelligence Engine",
                }
            )
            
            # Model to use
            self.model = "qwen/qwen-2.5-7b-instruct"
            print(f"✅ QwenModel initialized with model: {self.model}")
        except Exception as e:
            print(f"⚠️ Error initializing Qwen client: {e}")
            self.client = None
    
    def chat_completion(self, prompt, system_prompt=None, max_tokens=1000, temperature=0.7):
        """
        Send a chat completion request to Qwen
        
        Args:
            prompt (str): User prompt
            system_prompt (str): System instructions
            max_tokens (int): Max tokens in response
            temperature (float): Creativity (0-1)
        
        Returns:
            str: Model response
        """
        if not self.client or self.api_key == "dummy-key":
            print("⚠️ Qwen client not available, returning None")
            return None
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            print(f"❌ Error calling Qwen: {e}")
            return None
    
    def extract_json(self, text):
        """
        Extract JSON from model response
        
        Args:
            text (str): Model response
        
        Returns:
            dict/list: Parsed JSON or None
        """
        try:
            # Try to find JSON in the response
            json_match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return None
        except Exception as e:
            print(f"⚠️ JSON extraction error: {e}")
            return None


# Create singleton instance
_qwen_instance = None

def get_qwen_model():
    """Get or create Qwen model instance"""
    global _qwen_instance
    if _qwen_instance is None:
        _qwen_instance = QwenModel()
    return _qwen_instance