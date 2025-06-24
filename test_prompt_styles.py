import requests
import json
import time
import warnings
from config.settings import LLM_ENDPOINT_URL
warnings.filterwarnings("ignore")

class PromptStyleTester:
    def __init__(self, endpoint_url=None):
        self.endpoint_url = endpoint_url or LLM_ENDPOINT_URL
        self.test_results = {}
        
    def test_endpoint(self, prompt, max_tokens=100, temperature=0.7):
        """Test the endpoint and return response with timing."""
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        start_time = time.time()
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = requests.post(self.endpoint_url, json=payload, headers=headers)
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
    
    def test_current_style(self):
        """Test our current prompt style (instruction-heavy)."""
        print("\n=== CURRENT STYLE TEST (Instruction-Heavy) ===")
        
        prompt = """You are Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

User says: How are you today?

Respond as Kael Vire:"""
        
        response, time_taken = self.test_endpoint(prompt)
        print(f"Current Style Response:")
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        print(f"Time: {time_taken:.2f}s")
        print(f"Repeats 'You are': {'You are' in response}")
        print(f"Repeats 'User says:': {'User says:' in response}")
        print(f"Repeats 'Respond as': {'Respond as' in response}")
        
        self.test_results['current_style'] = {
            'response': response,
            'time': time_taken,
            'repeats_instruction': 'You are' in response,
            'repeats_user_says': 'User says:' in response,
            'repeats_respond_as': 'Respond as' in response
        }
    
    def test_natural_style(self):
        """Test a more natural, conversational style."""
        print("\n=== NATURAL STYLE TEST (Conversational) ===")
        
        prompt = """Kael Vire is a wise elven mage who speaks with ancient wisdom and uses formal language.

Kael Vire: Greetings, traveler. I am Kael Vire, master of the arcane arts.

User: How are you today?

Kael Vire:"""
        
        response, time_taken = self.test_endpoint(prompt)
        print(f"Natural Style Response:")
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        print(f"Time: {time_taken:.2f}s")
        print(f"Repeats 'You are': {'You are' in response}")
        print(f"Repeats 'User says:': {'User says:' in response}")
        print(f"Repeats 'Respond as': {'Respond as' in response}")
        
        self.test_results['natural_style'] = {
            'response': response,
            'time': time_taken,
            'repeats_instruction': 'You are' in response,
            'repeats_user_says': 'User says:' in response,
            'repeats_respond_as': 'Respond as' in response
        }
    
    def test_minimal_style(self):
        """Test a minimal, direct style."""
        print("\n=== MINIMAL STYLE TEST (Direct) ===")
        
        prompt = """Kael Vire, a wise elven mage, speaks with ancient wisdom and formal language.

User: How are you today?

Kael Vire:"""
        
        response, time_taken = self.test_endpoint(prompt)
        print(f"Minimal Style Response:")
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        print(f"Time: {time_taken:.2f}s")
        print(f"Repeats 'You are': {'You are' in response}")
        print(f"Repeats 'User says:': {'User says:' in response}")
        print(f"Repeats 'Respond as': {'Respond as' in response}")
        
        self.test_results['minimal_style'] = {
            'response': response,
            'time': time_taken,
            'repeats_instruction': 'You are' in response,
            'repeats_user_says': 'User says:' in response,
            'repeats_respond_as': 'Respond as' in response
        }
    
    def test_roleplay_style(self):
        """Test a roleplay-focused style."""
        print("\n=== ROLEPLAY STYLE TEST (Character-Focused) ===")
        
        prompt = """*Kael Vire, a wise elven mage with ancient wisdom, stands before you*

User: How are you today?

*Kael Vire responds:*"""
        
        response, time_taken = self.test_endpoint(prompt)
        print(f"Roleplay Style Response:")
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        print(f"Time: {time_taken:.2f}s")
        print(f"Repeats 'You are': {'You are' in response}")
        print(f"Repeats 'User says:': {'User says:' in response}")
        print(f"Repeats 'Respond as': {'Respond as' in response}")
        
        self.test_results['roleplay_style'] = {
            'response': response,
            'time': time_taken,
            'repeats_instruction': 'You are' in response,
            'repeats_user_says': 'User says:' in response,
            'repeats_respond_as': 'Respond as' in response
        }
    
    def test_system_style(self):
        """Test a system message style."""
        print("\n=== SYSTEM STYLE TEST (System Message) ===")
        
        prompt = """<|system|>
You are roleplaying as Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.
</|system|>

<|user|>
How are you today?
</|user|>

<|assistant|>"""
        
        response, time_taken = self.test_endpoint(prompt)
        print(f"System Style Response:")
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        print(f"Time: {time_taken:.2f}s")
        print(f"Repeats 'You are': {'You are' in response}")
        print(f"Repeats 'User says:': {'User says:' in response}")
        print(f"Repeats 'Respond as': {'Respond as' in response}")
        
        self.test_results['system_style'] = {
            'response': response,
            'time': time_taken,
            'repeats_instruction': 'You are' in response,
            'repeats_user_says': 'User says:' in response,
            'repeats_respond_as': 'Respond as' in response
        }
    
    def test_conversation_style(self):
        """Test a conversation history style."""
        print("\n=== CONVERSATION STYLE TEST (Chat History) ===")
        
        prompt = """Kael Vire: Greetings, traveler. I am Kael Vire, master of the arcane arts.

User: Hello! Nice to meet you.

Kael Vire: The pleasure is mine, young one. What brings you to my tower?

User: How are you today?

Kael Vire:"""
        
        response, time_taken = self.test_endpoint(prompt)
        print(f"Conversation Style Response:")
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        print(f"Time: {time_taken:.2f}s")
        print(f"Repeats 'You are': {'You are' in response}")
        print(f"Repeats 'User says:': {'User says:' in response}")
        print(f"Repeats 'Respond as': {'Respond as' in response}")
        
        self.test_results['conversation_style'] = {
            'response': response,
            'time': time_taken,
            'repeats_instruction': 'You are' in response,
            'repeats_user_says': 'User says:' in response,
            'repeats_respond_as': 'Respond as' in response
        }
    
    def generate_report(self):
        """Generate a comparison report of all prompt styles."""
        print("\n" + "="*80)
        print("PROMPT STYLE COMPARISON REPORT")
        print("="*80)
        
        styles = [
            ('Current Style', 'current_style'),
            ('Natural Style', 'natural_style'),
            ('Minimal Style', 'minimal_style'),
            ('Roleplay Style', 'roleplay_style'),
            ('System Style', 'system_style'),
            ('Conversation Style', 'conversation_style')
        ]
        
        print("\n🔹 PROMPT INJECTION COMPARISON")
        print("-" * 50)
        
        for style_name, style_key in styles:
            if style_key in self.test_results:
                result = self.test_results[style_key]
                repeats_instruction = result.get('repeats_instruction', False)
                repeats_user_says = result.get('repeats_user_says', False)
                repeats_respond_as = result.get('repeats_respond_as', False)
                
                total_issues = sum([repeats_instruction, repeats_user_says, repeats_respond_as])
                
                print(f"{style_name}:")
                print(f"  Repeats 'You are': {'❌' if repeats_instruction else '✅'}")
                print(f"  Repeats 'User says:': {'❌' if repeats_user_says else '✅'}")
                print(f"  Repeats 'Respond as': {'❌' if repeats_respond_as else '✅'}")
                print(f"  Total Issues: {total_issues}/3")
                print(f"  Response Time: {result.get('time', 0):.2f}s")
                print()
        
        # Find the best style
        best_style = None
        best_score = 0
        
        for style_name, style_key in styles:
            if style_key in self.test_results:
                result = self.test_results[style_key]
                issues = sum([
                    result.get('repeats_instruction', False),
                    result.get('repeats_user_says', False),
                    result.get('repeats_respond_as', False)
                ])
                score = 3 - issues  # Higher score = fewer issues
                
                if score > best_score:
                    best_score = score
                    best_style = style_name
        
        print("\n🔹 RECOMMENDATION")
        print("-" * 50)
        if best_style:
            print(f"Best Style: {best_style} (Score: {best_score}/3)")
            print(f"Recommendation: Use {best_style} for production")
        else:
            print("All styles have issues - prompt injection may be model-specific")
        
        print("\n" + "="*80)

def main():
    print("Starting Prompt Style Comparison Test...")
    print(f"Using endpoint: {LLM_ENDPOINT_URL}")
    
    tester = PromptStyleTester()
    
    # Test all prompt styles
    tester.test_current_style()
    tester.test_natural_style()
    tester.test_minimal_style()
    tester.test_roleplay_style()
    tester.test_system_style()
    tester.test_conversation_style()
    
    # Generate comparison report
    tester.generate_report()

if __name__ == "__main__":
    main() 