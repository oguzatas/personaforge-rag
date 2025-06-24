import requests
import json
from config.settings import LLM_ENDPOINT_URL

def debug_test():
    print("=== DEBUG TEST - ACTUAL RESPONSES ===")
    
    # Test 1: Simple prompt
    prompt1 = "Hello, how are you?"
    
    payload1 = {
        "prompt": prompt1,
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    print(f"\n1. Simple prompt: '{prompt1}'")
    print("Response:")
    
    try:
        response1 = requests.post(LLM_ENDPOINT_URL, json=payload1, headers={'Content-Type': 'application/json'})
        if response1.status_code == 200:
            result1 = response1.json()
            print(f"Raw response: {result1.get('response', 'No response')}")
        else:
            print(f"Error: {response1.status_code}")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test 2: Roleplay prompt
    prompt2 = """Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember.

User: Hello there!

Kael Vire:"""
    
    payload2 = {
        "prompt": prompt2,
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    print(f"\n2. Roleplay prompt:")
    print("Response:")
    
    try:
        response2 = requests.post(LLM_ENDPOINT_URL, json=payload2, headers={'Content-Type': 'application/json'})
        if response2.status_code == 200:
            result2 = response2.json()
            print(f"Raw response: {result2.get('response', 'No response')}")
        else:
            print(f"Error: {response2.status_code}")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test 3: Check for dialog continuation
    prompt3 = "What is the capital of France?"
    
    payload3 = {
        "prompt": prompt3,
        "max_tokens": 30,
        "temperature": 0.7
    }
    
    print(f"\n3. Factual question: '{prompt3}'")
    print("Response:")
    
    try:
        response3 = requests.post(LLM_ENDPOINT_URL, json=payload3, headers={'Content-Type': 'application/json'})
        if response3.status_code == 200:
            result3 = response3.json()
            print(f"Raw response: {result3.get('response', 'No response')}")
        else:
            print(f"Error: {response3.status_code}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    debug_test() 