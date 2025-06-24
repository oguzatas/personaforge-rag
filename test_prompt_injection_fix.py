import requests
import json
from config.settings import LLM_ENDPOINT_URL
from app.prompt_templates import format_prompt, clean_response

def test_prompt_injection_fix():
    print("=== TESTING PROMPT INJECTION FIX ===")
    
    # Test the new prompt format
    role_description = "Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language"
    context_chunks = ["Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember."]
    query = "Hello there!"
    
    # Test different prompt formats
    prompt_formats = [
        ("Original", f"""{role_description}

Background: {context_chunks[0]}

User: {query}

Kael Vire:"""),
        
        ("New Format", format_prompt(query, context_chunks, role_description)),
        
        ("Simple Format", f"""Kael Vire, {role_description}

{context_chunks[0]}

User: {query}

Kael Vire:""")
    ]
    
    for format_name, prompt in prompt_formats:
        print(f"\n{format_name} Prompt:")
        print(f"'{prompt}'")
        
        payload = {
            "prompt": prompt,
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(LLM_ENDPOINT_URL, json=payload, headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                result = response.json()
                raw_response = result.get('response', 'No response')
                
                print(f"\nRaw Response:")
                print(f"'{raw_response}'")
                
                # Test response cleaning
                cleaned_response = clean_response(raw_response)
                
                print(f"\nCleaned Response:")
                print(f"'{cleaned_response}'")
                
                # Check for prompt injection
                injection_indicators = ["You are", "Background:", "User says:", "Respond as your character:"]
                has_injection = any(indicator in raw_response for indicator in injection_indicators)
                
                # Check for dialog continuation
                dialog_indicators = ["User:", "AI:", "BOT:", "SAM:", "Alex:", "Kael Vire:"]
                has_dialog = any(indicator in raw_response for indicator in dialog_indicators)
                
                print(f"\nAssessment:")
                print(f"Prompt Injection: {'❌' if has_injection else '✅'}")
                print(f"Dialog Continuation: {'❌' if has_dialog else '✅'}")
                print(f"Response Length: {len(cleaned_response)} chars")
                
            else:
                print(f"Error: {response.status_code}")
                
        except Exception as e:
            print(f"Exception: {e}")
        
        print("\n" + "-"*50)

if __name__ == "__main__":
    test_prompt_injection_fix() 