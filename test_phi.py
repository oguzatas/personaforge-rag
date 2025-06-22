import requests
import json
import warnings
from config.settings import LLM_ENDPOINT_URL
warnings.filterwarnings("ignore")

def test_phi():
    print("Testing remote Phi-2 endpoint...")
    
    # Use configured endpoint URL
    endpoint_url = LLM_ENDPOINT_URL
    
    # Test prompt
    prompt = "Hello, I am an AI assistant. How can I help you today?"
    
    try:
        # Prepare the request payload
        payload = {
            "prompt": prompt,
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        # Print request details for debugging
        print("\nRequest details:")
        print(f"URL: {endpoint_url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Make the request with headers
        print("\nSending request to endpoint...")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(endpoint_url, json=payload, headers=headers)
        
        # Print full response details for debugging
        print("\nResponse details:")
        print(f"Status code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Raw response: {response.text}")
        
        # Try to parse response as JSON
        try:
            result = response.json()
            print("\nParsed JSON response:", json.dumps(result, indent=2))
            
            # Try different possible response formats
            if isinstance(result, dict):
                if "response" in result:
                    print("\nModel Response:", result["response"])
                elif "text" in result:
                    print("\nModel Response:", result["text"])
                elif "output" in result:
                    print("\nModel Response:", result["output"])
                else:
                    print("\nResponse keys available:", list(result.keys()))
            else:
                print("\nModel Response:", result)
                
        except json.JSONDecodeError:
            print("\nResponse is not JSON. Raw response:", response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"\nNetwork error occurred: {str(e)}")
    except Exception as e:
        print(f"\nUnexpected error occurred: {str(e)}")

if __name__ == "__main__":
    test_phi() 