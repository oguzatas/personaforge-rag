"""
Automated Test Suite for PersonaForge
Tests multiple models and scenarios systematically
"""

import requests
import json
import time
import warnings
from typing import Dict, List, Tuple
from dataclasses import dataclass
from config.settings import LLM_ENDPOINT_URL
warnings.filterwarnings("ignore")

@dataclass
class TestScenario:
    """Test scenario configuration."""
    name: str
    prompt: str
    expected_traits: List[str]
    expected_context: List[str]
    difficulty: str  # "easy", "medium", "hard"

@dataclass
class ModelConfig:
    """Model configuration for testing."""
    name: str
    endpoint_url: str
    max_tokens: int = 150
    temperature: float = 0.7

class AutomatedTestSuite:
    def __init__(self):
        self.test_scenarios = self._create_test_scenarios()
        self.model_configs = self._create_model_configs()
        
    def _create_test_scenarios(self) -> List[TestScenario]:
        """Create comprehensive test scenarios."""
        return [
            # Basic Roleplay Scenarios
            TestScenario(
                name="Basic Greeting",
                prompt="""Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember.

User: Hello there!

Kael Vire:""",
                expected_traits=["wise", "elven", "mage", "formal"],
                expected_context=["fire magic", "mytherra", "ember"],
                difficulty="easy"
            ),
            
            TestScenario(
                name="Character Knowledge",
                prompt="""Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember.

User: Tell me about your magic.

Kael Vire:""",
                expected_traits=["wise", "elven", "mage", "formal"],
                expected_context=["fire magic", "mytherra", "ember"],
                difficulty="medium"
            ),
            
            # Conversation Flow Scenarios
            TestScenario(
                name="Conversation Continuity",
                prompt="""Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember.

Recent conversation:
User: Hello there!
Kael Vire: Greetings, traveler. I am Kael Vire, master of the arcane arts.
User: Nice to meet you!

User: How are you today?

Kael Vire:""",
                expected_traits=["wise", "elven", "mage", "formal"],
                expected_context=["fire magic", "mytherra", "ember"],
                difficulty="medium"
            ),
            
            # Emotional Response Scenarios
            TestScenario(
                name="Emotional Response - Offended",
                prompt="""Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a proud elven mage who gets offended easily.

User: Your magic is weak.

Kael Vire:""",
                expected_traits=["proud", "offended", "elven", "mage"],
                expected_context=["magic"],
                difficulty="hard"
            ),
            
            TestScenario(
                name="Emotional Response - Happy",
                prompt="""Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire loves when people show interest in his magical knowledge.

User: I'd love to learn about your magical studies!

Kael Vire:""",
                expected_traits=["wise", "elven", "mage", "enthusiastic"],
                expected_context=["magical", "studies"],
                difficulty="medium"
            ),
            
            # Edge Case Scenarios
            TestScenario(
                name="Out of Character Question",
                prompt="""Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember.

User: What's the weather like today?

Kael Vire:""",
                expected_traits=["wise", "elven", "mage", "formal"],
                expected_context=["mytherra", "forest"],
                difficulty="hard"
            ),
            
            TestScenario(
                name="Complex Question",
                prompt="""Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember.

User: Can you explain the relationship between fire magic and the natural elements, and how this affects your connection to the forest?

Kael Vire:""",
                expected_traits=["wise", "elven", "mage", "formal"],
                expected_context=["fire magic", "natural elements", "forest", "mytherra"],
                difficulty="hard"
            ),
            
            # Stress Test Scenarios
            TestScenario(
                name="Long Context",
                prompt="""Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember. The forest of Mytherra is home to ancient trees that have witnessed the rise and fall of countless civilizations. These trees hold memories of the first elves who discovered the art of magic, and their roots run deep into the earth where they draw power from the very essence of creation itself. Kael Vire has spent centuries studying these ancient texts and has become one of the most respected mages in the realm.

User: What makes Mytherra special?

Kael Vire:""",
                expected_traits=["wise", "elven", "mage", "formal"],
                expected_context=["mytherra", "ancient trees", "magic", "elves"],
                difficulty="medium"
            ),
            
            TestScenario(
                name="Multiple Characters",
                prompt="""Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember. He often works with other mages like Thalindra the water mage and Grimtooth the dwarf blacksmith.

User: Do you work with other mages?

Kael Vire:""",
                expected_traits=["wise", "elven", "mage", "formal"],
                expected_context=["fire magic", "mytherra", "other mages", "thalindra", "grimtooth"],
                difficulty="medium"
            )
        ]
    
    def _create_model_configs(self) -> List[ModelConfig]:
        """Create model configurations for testing."""
        return [
            ModelConfig(
                name="Nous-Hermes-2-Mistral-7B-DPO",
                endpoint_url=LLM_ENDPOINT_URL,
                max_tokens=150,
                temperature=0.7
            )
            # Add more models here when endpoints are available
            # ModelConfig(
            #     name="Phi-2",
            #     endpoint_url="http://localhost:8000/phi2",
            #     max_tokens=150,
            #     temperature=0.7
            # ),
            # ModelConfig(
            #     name="TinyLlama",
            #     endpoint_url="http://localhost:8000/tinyllama",
            #     max_tokens=150,
            #     temperature=0.7
            # )
        ]
    
    def test_model_scenario(self, model_config: ModelConfig, scenario: TestScenario) -> Dict:
        """Test a specific model with a specific scenario."""
        payload = {
            "prompt": scenario.prompt,
            "max_tokens": model_config.max_tokens,
            "temperature": model_config.temperature
        }
        
        start_time = time.time()
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = requests.post(model_config.endpoint_url, json=payload, headers=headers, timeout=60)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, dict) and "response" in result:
                    model_response = result["response"]
                elif isinstance(result, dict) and "text" in result:
                    model_response = result["text"]
                elif isinstance(result, dict) and "output" in result:
                    model_response = result["output"]
                else:
                    model_response = str(result)
            else:
                model_response = f"Error: {response.status_code}"
            
            response_time = end_time - start_time
            
            # Calculate scores
            scores = self._calculate_scores(model_response, scenario)
            
            return {
                "model_name": model_config.name,
                "scenario_name": scenario.name,
                "difficulty": scenario.difficulty,
                "prompt": scenario.prompt,
                "response": model_response,
                "response_time": response_time,
                "scores": scores,
                "success": response.status_code == 200
            }
            
        except Exception as e:
            return {
                "model_name": model_config.name,
                "scenario_name": scenario.name,
                "difficulty": scenario.difficulty,
                "prompt": scenario.prompt,
                "response": f"Exception: {str(e)}",
                "response_time": time.time() - start_time,
                "scores": {"overall": 0.0, "prompt_injection": 0.0, "roleplay": 0.0, "context": 0.0},
                "success": False
            }
    
    def _calculate_scores(self, response: str, scenario: TestScenario) -> Dict[str, float]:
        """Calculate various scores for the response."""
        # Prompt injection score
        injection_indicators = [
            "You are", "User says:", "Respond as your character:", 
            "Background:", "Recent conversation:"
        ]
        prompt_injection_score = 1.0
        for indicator in injection_indicators:
            if indicator in response:
                prompt_injection_score -= 0.2
        prompt_injection_score = max(0.0, prompt_injection_score)
        
        # Roleplay quality score
        roleplay_score = 0.5  # Base score
        for trait in scenario.expected_traits:
            if trait.lower() in response.lower():
                roleplay_score += 0.1
        
        # Penalty for generic responses
        generic_phrases = ["hello", "hi there", "how can i help", "i'm here to help"]
        for phrase in generic_phrases:
            if phrase.lower() in response.lower():
                roleplay_score -= 0.1
        
        roleplay_score = min(1.0, max(0.0, roleplay_score))
        
        # Context accuracy score
        context_score = 0.0
        found_context = 0
        for element in scenario.expected_context:
            if element.lower() in response.lower():
                found_context += 1
        
        if scenario.expected_context:
            context_score = found_context / len(scenario.expected_context)
        
        # Overall score (weighted average)
        overall_score = (
            prompt_injection_score * 0.4 +
            roleplay_score * 0.4 +
            context_score * 0.2
        )
        
        return {
            "overall": overall_score,
            "prompt_injection": prompt_injection_score,
            "roleplay": roleplay_score,
            "context": context_score
        }
    
    def run_full_test_suite(self) -> Dict:
        """Run the complete test suite for all models and scenarios."""
        print("Starting Automated Test Suite...")
        print(f"Testing {len(self.model_configs)} models with {len(self.test_scenarios)} scenarios")
        
        all_results = []
        
        for model_config in self.model_configs:
            print(f"\n=== Testing {model_config.name} ===")
            model_results = []
            
            for scenario in self.test_scenarios:
                print(f"  Running {scenario.name} ({scenario.difficulty})...")
                result = self.test_model_scenario(model_config, scenario)
                model_results.append(result)
                
                # Print quick score
                score = result["scores"]["overall"]
                print(f"    Score: {score:.2f}")
                
                # Add delay to avoid overwhelming the endpoint
                time.sleep(1)
            
            all_results.extend(model_results)
        
        return self._generate_test_report(all_results)
    
    def _generate_test_report(self, results: List[Dict]) -> Dict:
        """Generate comprehensive test report."""
        report = {
            "summary": {},
            "model_results": {},
            "scenario_results": {},
            "recommendations": []
        }
        
        # Group results by model
        model_groups = {}
        for result in results:
            model_name = result["model_name"]
            if model_name not in model_groups:
                model_groups[model_name] = []
            model_groups[model_name].append(result)
        
        # Calculate model summaries
        for model_name, model_results in model_groups.items():
            successful_tests = [r for r in model_results if r["success"]]
            
            if successful_tests:
                avg_overall = sum(r["scores"]["overall"] for r in successful_tests) / len(successful_tests)
                avg_injection = sum(r["scores"]["prompt_injection"] for r in successful_tests) / len(successful_tests)
                avg_roleplay = sum(r["scores"]["roleplay"] for r in successful_tests) / len(successful_tests)
                avg_context = sum(r["scores"]["context"] for r in successful_tests) / len(successful_tests)
                avg_time = sum(r["response_time"] for r in successful_tests) / len(successful_tests)
                
                report["model_results"][model_name] = {
                    "total_tests": len(model_results),
                    "successful_tests": len(successful_tests),
                    "success_rate": len(successful_tests) / len(model_results),
                    "avg_overall_score": avg_overall,
                    "avg_prompt_injection_score": avg_injection,
                    "avg_roleplay_score": avg_roleplay,
                    "avg_context_score": avg_context,
                    "avg_response_time": avg_time,
                    "results": model_results
                }
            else:
                report["model_results"][model_name] = {
                    "total_tests": len(model_results),
                    "successful_tests": 0,
                    "success_rate": 0.0,
                    "avg_overall_score": 0.0,
                    "avg_prompt_injection_score": 0.0,
                    "avg_roleplay_score": 0.0,
                    "avg_context_score": 0.0,
                    "avg_response_time": 0.0,
                    "results": model_results
                }
        
        # Generate recommendations
        for model_name, model_data in report["model_results"].items():
            if model_data["success_rate"] < 0.8:
                report["recommendations"].append(f"{model_name}: Check endpoint connectivity")
            
            if model_data["avg_prompt_injection_score"] < 0.8:
                report["recommendations"].append(f"{model_name}: Use natural conversation prompt format")
            
            if model_data["avg_roleplay_score"] < 0.6:
                report["recommendations"].append(f"{model_name}: Improve character trait integration")
            
            if model_data["avg_response_time"] > 10:
                report["recommendations"].append(f"{model_name}: Optimize model performance")
        
        return report
    
    def save_results(self, results: Dict, filename: str = "automated_test_results.json"):
        """Save test results to file."""
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {filename}")
    
    def print_report(self, report: Dict):
        """Print formatted test report."""
        print("\n" + "=" * 80)
        print("AUTOMATED TEST SUITE REPORT")
        print("=" * 80)
        
        for model_name, model_data in report["model_results"].items():
            print(f"\n🔹 {model_name.upper()}")
            print("-" * 50)
            print(f"Success Rate: {model_data['success_rate']:.1%}")
            print(f"Overall Score: {model_data['avg_overall_score']:.2f}/1.0")
            print(f"Prompt Injection: {model_data['avg_prompt_injection_score']:.2f}")
            print(f"Roleplay Quality: {model_data['avg_roleplay_score']:.2f}")
            print(f"Context Accuracy: {model_data['avg_context_score']:.2f}")
            print(f"Avg Response Time: {model_data['avg_response_time']:.2f}s")
            
            # Show scenario breakdown
            print("\nScenario Results:")
            for result in model_data["results"]:
                score = result["scores"]["overall"]
                status = "✅" if result["success"] else "❌"
                print(f"  {status} {result['scenario_name']}: {score:.2f}")
        
        if report["recommendations"]:
            print("\n📋 RECOMMENDATIONS:")
            for rec in report["recommendations"]:
                print(f"  • {rec}")

def main():
    """Run the automated test suite."""
    test_suite = AutomatedTestSuite()
    results = test_suite.run_full_test_suite()
    test_suite.print_report(results)
    test_suite.save_results(results)

if __name__ == "__main__":
    main() 