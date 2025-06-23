import requests
import json
from pathlib import Path
from config.settings import LLM_ENDPOINT_URL, LLM_MAX_TOKENS, LLM_TEMPERATURE

class Phi2Interface:
    def __init__(self, endpoint_url=None):
        self.endpoint_url = endpoint_url or LLM_ENDPOINT_URL
        
    def clean_response(self, response: str, prompt: str) -> str:
        """Clean the response to extract only the character's reply."""
        # Remove the prompt from the response if it's included
        if prompt in response:
            response = response.replace(prompt, "").strip()
        
        # Remove common prefixes that might be included
        prefixes_to_remove = [
            "You are",
            "Context:",
            "User:",
            "You:",
            "Character:",
            "Answer:"
        ]
        
        for prefix in prefixes_to_remove:
            if response.startswith(prefix):
                # Find the first newline after the prefix
                lines = response.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith(prefix):
                        # Remove this line and all previous lines
                        response = '\n'.join(lines[i+1:]).strip()
                        break
        
        # Clean up any remaining artifacts
        response = response.strip()
        
        # If response is empty or just whitespace, return a default
        if not response or response.isspace():
            return "I'm not sure how to respond to that."
            
        return response
        
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
                        raw_response = result["response"]
                    elif "text" in result:
                        raw_response = result["text"]
                    elif "output" in result:
                        raw_response = result["output"]
                    else:
                        raw_response = str(result)
                else:
                    raw_response = str(result)
                
                # Clean the response to extract only the character's reply
                cleaned_response = self.clean_response(raw_response, prompt)
                return cleaned_response
            else:
                raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

# Global instance
phi2_model = Phi2Interface()

def call_llm(prompt: str) -> str:
    """Main interface function for calling the LLM."""
    return phi2_model.generate_response(prompt)
