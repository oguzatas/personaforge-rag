import requests
import json
import time
import warnings
from config.settings import LLM_ENDPOINT_URL
warnings.filterwarnings("ignore")

# Use the actual endpoint from settings
GEMMA_ENDPOINT_URL = LLM_ENDPOINT_URL

class GemmaEvaluator:
    def __init__(self, endpoint_url=None):
        self.endpoint_url = endpoint_url or GEMMA_ENDPOINT_URL
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
    
    def test_instruction_tracking(self):
        """Test how well Gemma understands roleplaying and direct speech."""
        print("\n=== INSTRUCTION TRACKING TEST ===")
        
        # Test 1: Basic roleplay instruction
        prompt1 = """You are Kael Vire, a wise elven mage. Respond as this character.

User says: Hello there!

Respond as your character:"""
        
        response1, time1 = self.test_endpoint(prompt1)
        print(f"Test 1 - Basic Roleplay:")
        print(f"Prompt: {prompt1[:100]}...")
        print(f"Response: {response1}")
        print(f"Time: {time1:.2f}s")
        
        # Test 2: Direct speech instruction
        prompt2 = """You are Kael Vire. When the user speaks, respond naturally in character. Do not repeat what they say.

User says: What's the weather like?

Respond as Kael Vire:"""
        
        response2, time2 = self.test_endpoint(prompt2)
        print(f"\nTest 2 - Direct Speech:")
        print(f"Prompt: {prompt2[:100]}...")
        print(f"Response: {response2}")
        print(f"Time: {time2:.2f}s")
        
        # Test 3: Character switching
        prompt3 = """You are now a different character: Thorin, a gruff dwarf warrior. Act like Thorin.

User says: Tell me about yourself.

Respond as Thorin:"""
        
        response3, time3 = self.test_endpoint(prompt3)
        print(f"\nTest 3 - Character Switching:")
        print(f"Prompt: {prompt3[:100]}...")
        print(f"Response: {response3}")
        print(f"Time: {time3:.2f}s")
        
        self.test_results['instruction_tracking'] = {
            'basic_roleplay': {'response': response1, 'time': time1},
            'direct_speech': {'response': response2, 'time': time2},
            'character_switching': {'response': response3, 'time': time3}
        }
    
    def test_prompt_injection(self):
        """Test if Gemma copies and pastes the "You are..." part."""
        print("\n=== PROMPT INJECTION TEST ===")
        
        # Test 1: Check if it repeats the instruction
        prompt1 = """You are Kael Vire, a wise elven mage. Respond naturally as this character.

User says: Hello!

Respond as your character:"""
        
        response1, time1 = self.test_endpoint(prompt1)
        print(f"Test 1 - Instruction Repetition:")
        print(f"Response: {response1}")
        print(f"Repeats 'You are': {'You are' in response1}")
        print(f"Repeats 'Kael Vire': {'Kael Vire' in response1}")
        print(f"Time: {time1:.2f}s")
        
        # Test 2: Check if it includes prompt artifacts
        prompt2 = """You are a helpful assistant. The user will ask you questions.

User says: What is 2+2?

Answer:"""
        
        response2, time2 = self.test_endpoint(prompt2)
        print(f"\nTest 2 - Prompt Artifacts:")
        print(f"Response: {response2}")
        print(f"Contains 'Answer:': {'Answer:' in response2}")
        print(f"Contains 'User says:': {'User says:' in response2}")
        print(f"Time: {time2:.2f}s")
        
        self.test_results['prompt_injection'] = {
            'instruction_repetition': {'response': response1, 'time': time1},
            'prompt_artifacts': {'response': response2, 'time': time2}
        }
    
    def test_roleplay_naturalness(self):
        """Test if Gemma acts like the character or spews information."""
        print("\n=== ROLEPLAY NATURALNESS TEST ===")
        
        # Test 1: Character personality
        prompt1 = """You are Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

User says: How are you today?

Respond as Kael Vire:"""
        
        response1, time1 = self.test_endpoint(prompt1)
        print(f"Test 1 - Character Personality:")
        print(f"Response: {response1}")
        print(f"Time: {time1:.2f}s")
        
        # Test 2: Information vs. roleplay
        prompt2 = """You are Kael Vire, an elven mage. You know about magic and elven history.

User says: Tell me about elven magic.

Respond as Kael Vire:"""
        
        response2, time2 = self.test_endpoint(prompt2)
        print(f"\nTest 2 - Information vs Roleplay:")
        print(f"Response: {response2}")
        print(f"Time: {time2:.2f}s")
        
        # Test 3: Emotional response
        prompt3 = """You are Kael Vire, a proud elven mage who gets offended easily.

User says: Your magic is weak.

Respond as Kael Vire:"""
        
        response3, time3 = self.test_endpoint(prompt3)
        print(f"\nTest 3 - Emotional Response:")
        print(f"Response: {response3}")
        print(f"Time: {time3:.2f}s")
        
        self.test_results['roleplay_naturalness'] = {
            'character_personality': {'response': response1, 'time': time1},
            'information_vs_roleplay': {'response': response2, 'time': time2},
            'emotional_response': {'response': response3, 'time': time3}
        }
    
    def test_rag_compatibility(self):
        """Test if Gemma responds logically to external context."""
        print("\n=== RAG COMPATIBILITY TEST ===")
        
        # Test 1: Context integration
        prompt1 = """You are Kael Vire, an elven mage.

Your background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember.

User says: What's your pet's name?

Respond as Kael Vire:"""
        
        response1, time1 = self.test_endpoint(prompt1)
        print(f"Test 1 - Context Integration:")
        print(f"Response: {response1}")
        print(f"Mentions 'Ember': {'Ember' in response1}")
        print(f"Time: {time1:.2f}s")
        
        # Test 2: Multiple context chunks
        prompt2 = """You are Kael Vire, an elven mage.

Your background: 
- Kael Vire is a master of fire magic
- He lives in the ancient forest of Mytherra
- He has a pet phoenix named Ember
- He is 500 years old and very wise

User says: How old are you and where do you live?

Respond as Kael Vire:"""
        
        response2, time2 = self.test_endpoint(prompt2)
        print(f"\nTest 2 - Multiple Context Chunks:")
        print(f"Response: {response2}")
        print(f"Mentions age: {'500' in response2 or 'old' in response2.lower()}")
        print(f"Mentions location: {'Mytherra' in response2 or 'forest' in response2.lower()}")
        print(f"Time: {time2:.2f}s")
        
        # Test 3: Context vs. instruction conflict
        prompt3 = """You are Kael Vire, an elven mage.

Your background: Kael Vire is a master of ice magic.

User says: What type of magic do you use?

Respond as Kael Vire:"""
        
        response3, time3 = self.test_endpoint(prompt3)
        print(f"\nTest 3 - Context vs Instruction Conflict:")
        print(f"Response: {response3}")
        print(f"Mentions 'ice': {'ice' in response3.lower()}")
        print(f"Time: {time3:.2f}s")
        
        self.test_results['rag_compatibility'] = {
            'context_integration': {'response': response1, 'time': time1},
            'multiple_context': {'response': response2, 'time': time2},
            'context_conflict': {'response': response3, 'time': time3}
        }
    
    def test_response_time(self):
        """Test response time performance."""
        print("\n=== RESPONSE TIME TEST ===")
        
        times = []
        prompt = "Hello, how are you?"
        
        for i in range(5):
            response, time_taken = self.test_endpoint(prompt)
            times.append(time_taken)
            print(f"Test {i+1}: {time_taken:.2f}s - {response[:50]}...")
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\nResponse Time Summary:")
        print(f"Average: {avg_time:.2f}s")
        print(f"Min: {min_time:.2f}s")
        print(f"Max: {max_time:.2f}s")
        
        self.test_results['response_time'] = {
            'times': times,
            'average': avg_time,
            'min': min_time,
            'max': max_time
        }
    
    def test_dialog_continuation_issue(self):
        """Test the specific dialog continuation issue."""
        print("\n=== DIALOG CONTINUATION ISSUE TEST ===")
        
        # Test the specific case mentioned
        prompt1 = """You are Skywarden Kael Vire, a wise elven mage.

User says: I'm here to investigate the rumors about corruption in the High Wards.

Respond as your character:"""
        
        response1, time1 = self.test_endpoint(prompt1)
        print(f"Test 1 - Dialog Continuation Issue:")
        print(f"Response: {response1}")
        print(f"Contains 'User says:': {'User says:' in response1}")
        print(f"Contains 'Respond as your character:': {'Respond as your character:' in response1}")
        print(f"Continues dialog: {'That\'s interesting' in response1}")
        print(f"Time: {time1:.2f}s")
        
        # Test 2: Check if it fills in user responses
        prompt2 = """You are Kael Vire. The user asks you a question.

User says: What do you think about the weather?

Respond as Kael Vire:"""
        
        response2, time2 = self.test_endpoint(prompt2)
        print(f"\nTest 2 - User Response Filling:")
        print(f"Response: {response2}")
        print(f"Contains 'User says:': {'User says:' in response2}")
        print(f"Contains 'I think': {'I think' in response2.lower()}")
        print(f"Time: {time2:.2f}s")
        
        self.test_results['dialog_continuation'] = {
            'continuation_issue': {'response': response1, 'time': time1},
            'user_response_filling': {'response': response2, 'time': time2}
        }
    
    def generate_report(self):
        """Generate a comprehensive evaluation report."""
        print("\n" + "="*80)
        print("GEMMA 2B MODEL EVALUATION REPORT")
        print("="*80)
        
        # Instruction Tracking Analysis
        print("\n🔹 INSTRUCTION TRACKING")
        print("-" * 40)
        it_results = self.test_results.get('instruction_tracking', {})
        if it_results:
            basic = it_results.get('basic_roleplay', {})
            direct = it_results.get('direct_speech', {})
            switch = it_results.get('character_switching', {})
            
            print(f"Basic Roleplay Understanding: {'✅' if 'Hello' in basic.get('response', '') else '❌'}")
            print(f"Direct Speech Handling: {'✅' if not basic.get('response', '').startswith('User says:') else '❌'}")
            print(f"Character Switching: {'✅' if 'Thorin' in switch.get('response', '') or 'dwarf' in switch.get('response', '').lower() else '❌'}")
        
        # Prompt Injection Analysis
        print("\n🔹 PROMPT INJECTION")
        print("-" * 40)
        pi_results = self.test_results.get('prompt_injection', {})
        if pi_results:
            instr = pi_results.get('instruction_repetition', {})
            artifacts = pi_results.get('prompt_artifacts', {})
            
            repeats_instruction = 'You are' in instr.get('response', '') or 'Kael Vire' in instr.get('response', '')
            has_artifacts = 'Answer:' in artifacts.get('response', '') or 'User says:' in artifacts.get('response', '')
            
            print(f"Repeats Instructions: {'❌' if repeats_instruction else '✅'}")
            print(f"Contains Prompt Artifacts: {'❌' if has_artifacts else '✅'}")
        
        # Roleplay Naturalness Analysis
        print("\n🔹 ROLEPLAY NATURALNESS")
        print("-" * 40)
        rp_results = self.test_results.get('roleplay_naturalness', {})
        if rp_results:
            personality = rp_results.get('character_personality', {})
            info_vs_roleplay = rp_results.get('information_vs_roleplay', {})
            emotional = rp_results.get('emotional_response', {})
            
            print(f"Character Personality: {'✅' if 'wise' in personality.get('response', '').lower() or 'elven' in personality.get('response', '').lower() else '❌'}")
            print(f"Information vs Roleplay: {'✅' if not info_vs_roleplay.get('response', '').startswith('Elven magic') else '❌'}")
            print(f"Emotional Response: {'✅' if any(word in emotional.get('response', '').lower() for word in ['offended', 'proud', 'insult']) else '❌'}")
        
        # RAG Compatibility Analysis
        print("\n🔹 RAG COMPATIBILITY")
        print("-" * 40)
        rag_results = self.test_results.get('rag_compatibility', {})
        if rag_results:
            context = rag_results.get('context_integration', {})
            multiple = rag_results.get('multiple_context', {})
            conflict = rag_results.get('context_conflict', {})
            
            print(f"Context Integration: {'✅' if 'Ember' in context.get('response', '') else '❌'}")
            print(f"Multiple Context Chunks: {'✅' if 'Mytherra' in multiple.get('response', '') or 'forest' in multiple.get('response', '').lower() else '❌'}")
            print(f"Context Priority: {'✅' if 'ice' in conflict.get('response', '').lower() else '❌'}")
        
        # Dialog Continuation Analysis
        print("\n🔹 DIALOG CONTINUATION ISSUE")
        print("-" * 40)
        dc_results = self.test_results.get('dialog_continuation', {})
        if dc_results:
            continuation = dc_results.get('continuation_issue', {})
            user_filling = dc_results.get('user_response_filling', {})
            
            has_continuation = 'User says:' in continuation.get('response', '') or 'That\'s interesting' in continuation.get('response', '')
            fills_user_responses = 'User says:' in user_filling.get('response', '')
            
            print(f"Dialog Continuation Problem: {'❌' if has_continuation else '✅'}")
            print(f"Fills User Responses: {'❌' if fills_user_responses else '✅'}")
        
        # Response Time Analysis
        print("\n🔹 RESPONSE TIME")
        print("-" * 40)
        rt_results = self.test_results.get('response_time', {})
        if rt_results:
            avg_time = rt_results.get('average', 0)
            print(f"Average Response Time: {avg_time:.2f}s")
            print(f"Performance Rating: {'🟢 Fast' if avg_time < 2 else '🟡 Moderate' if avg_time < 5 else '🔴 Slow'}")
        
        # Overall Assessment
        print("\n🔹 OVERALL ASSESSMENT")
        print("-" * 40)
        
        # Calculate scores
        scores = []
        if it_results:
            scores.append(1 if 'Hello' in basic.get('response', '') else 0)
            scores.append(1 if not basic.get('response', '').startswith('User says:') else 0)
        
        if pi_results:
            scores.append(0 if repeats_instruction else 1)
            scores.append(0 if has_artifacts else 1)
        
        if rp_results:
            scores.append(1 if 'wise' in personality.get('response', '').lower() or 'elven' in personality.get('response', '').lower() else 0)
            scores.append(1 if not info_vs_roleplay.get('response', '').startswith('Elven magic') else 0)
        
        if rag_results:
            scores.append(1 if 'Ember' in context.get('response', '') else 0)
            scores.append(1 if 'Mytherra' in multiple.get('response', '') or 'forest' in multiple.get('response', '').lower() else 0)
        
        if dc_results:
            scores.append(0 if has_continuation else 1)
            scores.append(0 if fills_user_responses else 1)
        
        if scores:
            overall_score = sum(scores) / len(scores) * 100
            print(f"Overall Score: {overall_score:.1f}%")
            
            if overall_score >= 80:
                print("Recommendation: ✅ SUITABLE for roleplay")
            elif overall_score >= 60:
                print("Recommendation: ⚠️ MODERATELY SUITABLE")
            else:
                print("Recommendation: ❌ NOT SUITABLE for roleplay")
        
        print("\n" + "="*80)

def main():
    print("Starting Gemma 2B Model Evaluation...")
    print(f"Using endpoint: {GEMMA_ENDPOINT_URL}")
    
    # Use the configured endpoint
    evaluator = GemmaEvaluator()
    
    # Run all tests
    evaluator.test_instruction_tracking()
    evaluator.test_prompt_injection()
    evaluator.test_roleplay_naturalness()
    evaluator.test_rag_compatibility()
    evaluator.test_dialog_continuation_issue()
    evaluator.test_response_time()
    
    # Generate report
    evaluator.generate_report()

if __name__ == "__main__":
    main() 