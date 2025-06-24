import requests
import json
from config.settings import LLM_ENDPOINT_URL

def manual_test():
    print("=== MANUAL TESTING - REAL ASSESSMENT ===")
    
    tests = [
        {
            "name": "Simple Greeting",
            "prompt": "Hello, how are you?",
            "expected": "Simple, direct response"
        },
        {
            "name": "Roleplay Test",
            "prompt": """Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember.

User: Hello there!

Kael Vire:""",
            "expected": "Single response as Kael Vire"
        },
        {
            "name": "Factual Question",
            "prompt": "What is the capital of France?",
            "expected": "Direct answer: Paris"
        },
        {
            "name": "Emotional Response",
            "prompt": """You are a proud warrior who gets easily offended.

User: You're not very strong.

Warrior:""",
            "expected": "Single offended response"
        },
        {
            "name": "Complex Question",
            "prompt": "Can you explain the relationship between fire magic and the natural elements?",
            "expected": "Direct explanation"
        }
    ]
    
    results = []
    
    for i, test in enumerate(tests, 1):
        print(f"\n{i}. {test['name']}")
        print(f"Expected: {test['expected']}")
        print("Actual Response:")
        
        payload = {
            "prompt": test["prompt"],
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(LLM_ENDPOINT_URL, json=payload, headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                result = response.json()
                actual_response = result.get('response', 'No response')
                print(f"'{actual_response}'")
                
                # Manual assessment
                print("\nManual Assessment:")
                
                # Check for dialog continuation
                dialog_indicators = ["User:", "AI:", "BOT:", "SAM:", "Alex:", "Kael Vire:"]
                has_dialog_continuation = any(indicator in actual_response for indicator in dialog_indicators)
                
                if has_dialog_continuation:
                    print("❌ DIALOG CONTINUATION - Model continues conversation")
                    score = 0.2  # Very low score
                else:
                    print("✅ Single response - No dialog continuation")
                    score = 0.8  # Good base score
                
                # Check for prompt injection
                injection_indicators = ["You are", "Background:", "User says:"]
                has_injection = any(indicator in actual_response for indicator in injection_indicators)
                
                if has_injection:
                    print("❌ PROMPT INJECTION - Includes prompt instructions")
                    score -= 0.3
                else:
                    print("✅ No prompt injection")
                
                # Check response quality
                if len(actual_response.strip()) < 10:
                    print("❌ Too short response")
                    score -= 0.2
                elif len(actual_response) > 500:
                    print("❌ Too long response")
                    score -= 0.1
                else:
                    print("✅ Good response length")
                
                print(f"Final Score: {score:.1f}/1.0")
                results.append({"test": test["name"], "score": score, "response": actual_response})
                
            else:
                print(f"Error: {response.status_code}")
                results.append({"test": test["name"], "score": 0.0, "response": f"Error {response.status_code}"})
                
        except Exception as e:
            print(f"Exception: {e}")
            results.append({"test": test["name"], "score": 0.0, "response": f"Exception: {e}"})
    
    # Overall assessment
    print("\n" + "="*50)
    print("OVERALL ASSESSMENT")
    print("="*50)
    
    avg_score = sum(r["score"] for r in results) / len(results)
    print(f"Average Score: {avg_score:.2f}/1.0")
    
    dialog_issues = sum(1 for r in results if any(indicator in r["response"] for indicator in ["User:", "AI:", "BOT:", "SAM:", "Alex:", "Kael Vire:"]))
    print(f"Dialog Continuation Issues: {dialog_issues}/{len(results)}")
    
    if avg_score < 0.3:
        print("❌ POOR - Major issues with dialog continuation and response quality")
    elif avg_score < 0.6:
        print("⚠️ MODERATE - Some issues but usable with fixes")
    else:
        print("✅ GOOD - Generally acceptable performance")
    
    print(f"\nRealistic Assessment: This model has {'critical' if dialog_issues > 2 else 'moderate' if dialog_issues > 0 else 'no'} dialog continuation issues.")

if __name__ == "__main__":
    manual_test() 