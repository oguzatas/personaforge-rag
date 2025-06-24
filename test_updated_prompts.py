import requests
import json
import time
import warnings
from config.settings import LLM_ENDPOINT_URL
warnings.filterwarnings("ignore")

def test_updated_prompt_format():
    """Test our updated prompt format to ensure it avoids prompt injection."""
    print("Testing Updated Prompt Format...")
    print(f"Using endpoint: {LLM_ENDPOINT_URL}")
    
    # Test 1: Basic prompt without conversation history
    prompt1 = """Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember.

User: How are you today?

Kael Vire:"""
    
    # Test 2: Prompt with conversation history
    prompt2 = """Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember.

Recent conversation:
User: Hello there!
Kael Vire: Greetings, traveler. I am Kael Vire, master of the arcane arts.
User: Nice to meet you!

User: How are you today?

Kael Vire:"""
    
    def test_endpoint(prompt, test_name):
        payload = {
            "prompt": prompt,
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        start_time = time.time()
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = requests.post(LLM_ENDPOINT_URL, json=payload, headers=headers)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, dict) and "response" in result:
                    return result["response"], end_time - start_time
                elif isinstance(result, dict) and "text" in result:
                    return result["text"], end_time - start_time
                elif isinstance(result, dict) and "output" in result:
                    return result["output"], end_time - start_time
                else:
                    return str(result), end_time - start_time
            else:
                return f"Error: {response.status_code}", end_time - start_time
        except Exception as e:
            return f"Exception: {str(e)}", time.time() - start_time
    
    # Test both prompts
    print("\n=== TEST 1: Basic Prompt ===")
    response1, time1 = test_endpoint(prompt1, "Basic")
    print(f"Prompt: {prompt1}")
    print(f"Response: {response1}")
    print(f"Time: {time1:.2f}s")
    print(f"Repeats 'You are': {'You are' in response1}")
    print(f"Repeats 'User says:': {'User says:' in response1}")
    print(f"Repeats 'Respond as': {'Respond as' in response1}")
    
    print("\n=== TEST 2: Prompt with Conversation History ===")
    response2, time2 = test_endpoint(prompt2, "With History")
    print(f"Prompt: {prompt2}")
    print(f"Response: {response2}")
    print(f"Time: {time2:.2f}s")
    print(f"Repeats 'You are': {'You are' in response2}")
    print(f"Repeats 'User says:': {'User says:' in response2}")
    print(f"Repeats 'Respond as': {'Respond as' in response2}")
    
    # Summary
    print("\n=== SUMMARY ===")
    print("Updated Prompt Format Results:")
    print(f"Test 1 - Prompt Injection Issues: {sum(['You are' in response1, 'User says:' in response1, 'Respond as' in response1])}/3")
    print(f"Test 2 - Prompt Injection Issues: {sum(['You are' in response2, 'User says:' in response2, 'Respond as' in response2])}/3")
    
    if 'You are' not in response1 and 'User says:' not in response1 and 'Respond as' not in response1:
        print("✅ SUCCESS: Updated prompt format avoids prompt injection!")
    else:
        print("❌ ISSUE: Prompt injection still occurs with updated format")

if __name__ == "__main__":
    test_updated_prompt_format() 