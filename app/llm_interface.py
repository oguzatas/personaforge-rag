import requests
import json
from pathlib import Path
from config.settings import LLM_ENDPOINT_URL, LLM_MAX_TOKENS, LLM_TEMPERATURE

class Phi2Interface:
    def __init__(self, endpoint_url=None):
        self.endpoint_url = endpoint_url or LLM_ENDPOINT_URL
        
    def generate_response(self, prompt: str, max_length: int = None, temperature: float = None) -> str:
        """Generate response using remote Phi-2 endpoint."""
        # Use config defaults if not specified
        max_length = max_length or LLM_MAX_TOKENS
        temperature = temperature or LLM_TEMPERATURE
        
        try:
            # Prepare the request payload
            payload = {
                "prompt": prompt,
                "max_tokens": max_length,
                "temperature": temperature
            }
            
            # Make the request with headers
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = requests.post(self.endpoint_url, json=payload, headers=headers)
            
            # Check if request was successful
            if response.status_code == 200:
                result = response.json()
                # Try different possible response formats
                if isinstance(result, dict):
                    if "response" in result:
                        return result["response"]
                    elif "text" in result:
                        return result["text"]
                    elif "output" in result:
                        return result["output"]
                    else:
                        return str(result)
                else:
                    return str(result)
            else:
                raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

# Global instance
phi2_model = Phi2Interface()

def call_llm(prompt: str) -> str:
    """Main interface function for calling the LLM."""
    return phi2_model.generate_response(prompt)
