#!/usr/bin/env python3

import os
import requests
import json

ARLI_API_KEY = os.getenv("ARLI_API_KEY")

def test_content_generation():
    headers = {
        "Authorization": f"Bearer {ARLI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Test prompt
    system_prompt = "You are an expert music historian writing in German. Use clear, engaging language suitable for German readers."
    user_prompt = """
    Write about the Introduction section for the music genre Rock.
    The content should be at least 1000 characters long.
    Focus on providing a comprehensive overview of the genre.
    """
    
    data = {
        "model": "Llama-3.3-70B-Instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "repetition_penalty": 1.1,
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 2000,
        "stream": False
    }
    
    try:
        response = requests.post(
            "https://api.arliai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        print("Status Code:", response.status_code)
        print("\nResponse Headers:", json.dumps(dict(response.headers), indent=2))
        print("\nResponse Body:", json.dumps(response.json(), indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_content_generation()
