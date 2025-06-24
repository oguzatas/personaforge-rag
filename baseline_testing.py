"""
Baseline Testing Framework for PersonaForge
Compares models against standard benchmarks and other models
"""

import requests
import json
import time
import warnings
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from config.settings import LLM_ENDPOINT_URL
warnings.filterwarnings("ignore")

@dataclass
class BaselineTest:
    """Baseline test configuration."""
    name: str
    description: str
    prompt: str
    expected_response_patterns: List[str]
    category: str  # "roleplay", "conversation", "knowledge", "creativity"

@dataclass
class ModelBaseline:
    """Model baseline configuration."""
    name: str
    endpoint_url: str
    model_type: str  # "local", "remote", "api"
    expected_performance: Dict[str, float]  # Expected scores by category

class BaselineTestingFramework:
    def __init__(self):
        self.baseline_tests = self._create_baseline_tests()
        self.model_baselines = self._create_model_baselines()
        
    def _create_baseline_tests(self) -> List[BaselineTest]:
        """Create baseline tests for comparison."""
        return [
            # Roleplay Baseline Tests
            BaselineTest(
                name="Character Consistency",
                description="Test if model maintains character personality",
                prompt="""You are a wise elven mage named Kael Vire. You speak formally and are proud of your magical abilities.

User: Hello!
Kael Vire: Greetings, mortal. I am Kael Vire, master of the arcane arts.

User: How are you today?

Kael Vire:""",
                expected_response_patterns=["formal", "elven", "mage", "proud"],
                category="roleplay"
            ),
            
            BaselineTest(
                name="Emotional Response",
                description="Test emotional response capabilities",
                prompt="""You are a proud warrior who gets easily offended.

User: You're not very strong.

Warrior:""",
                expected_response_patterns=["offended", "proud", "defensive", "challenge"],
                category="roleplay"
            ),
            
            # Conversation Baseline Tests
            BaselineTest(
                name="Conversation Flow",
                description="Test natural conversation flow",
                prompt="""You are having a casual conversation with a friend.

Friend: Hey, how was your day?
You: It was pretty good! I went for a walk in the park.

Friend: That sounds nice. What did you see?

You:""",
                expected_response_patterns=["natural", "conversational", "engaging"],
                category="conversation"
            ),
            
            BaselineTest(
                name="Context Retention",
                description="Test ability to remember conversation context",
                prompt="""You are talking to someone about cooking.

Person: I love making pasta.
You: That's great! What's your favorite type of pasta?
Person: I really like fettuccine alfredo.

Person: Have you ever tried making it?

You:""",
                expected_response_patterns=["fettuccine", "alfredo", "pasta", "cooking"],
                category="conversation"
            ),
            
            # Knowledge Baseline Tests
            BaselineTest(
                name="Factual Knowledge",
                description="Test basic factual knowledge",
                prompt="""What is the capital of France?""",
                expected_response_patterns=["paris", "france"],
                category="knowledge"
            ),
            
            BaselineTest(
                name="Creative Writing",
                description="Test creative writing abilities",
                prompt="""Write a short story about a magical forest in exactly 3 sentences.""",
                expected_response_patterns=["magical", "forest", "story"],
                category="creativity"
            ),
            
            # Edge Case Tests
            BaselineTest(
                name="Instruction Following",
                description="Test ability to follow specific instructions",
                prompt="""Respond with exactly 5 words about the weather.""",
                expected_response_patterns=["weather", "5 words"],
                category="conversation"
            ),
            
            BaselineTest(
                name="Out of Character Handling",
                description="Test handling of out-of-character requests",
                prompt="""You are a medieval knight. 

User: What's the weather like today?

Knight:""",
                expected_response_patterns=["medieval", "knight", "weather"],
                category="roleplay"
            )
        ]
    
    def _create_model_baselines(self) -> List[ModelBaseline]:
        """Create model baseline configurations."""
        return [
            ModelBaseline(
                name="Nous-Hermes-2-Mistral-7B-DPO",
                endpoint_url=LLM_ENDPOINT_URL,
                model_type="remote",
                expected_performance={
                    "roleplay": 0.7,
                    "conversation": 0.8,
                    "knowledge": 0.6,
                    "creativity": 0.7
                }
            )
            # Add more models when available
        ]
    
    def test_model_baseline(self, model_baseline: ModelBaseline, baseline_test: BaselineTest) -> Dict:
        """Test a model against a baseline test."""
        payload = {
            "prompt": baseline_test.prompt,
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        start_time = time.time()
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = requests.post(model_baseline.endpoint_url, json=payload, headers=headers, timeout=60)
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
            
            # Calculate baseline score
            baseline_score = self._calculate_baseline_score(model_response, baseline_test)
            
            return {
                "model_name": model_baseline.name,
                "test_name": baseline_test.name,
                "category": baseline_test.category,
                "prompt": baseline_test.prompt,
                "response": model_response,
                "response_time": response_time,
                "baseline_score": baseline_score,
                "expected_patterns": baseline_test.expected_response_patterns,
                "found_patterns": self._find_patterns(model_response, baseline_test.expected_response_patterns),
                "success": response.status_code == 200
            }
            
        except Exception as e:
            return {
                "model_name": model_baseline.name,
                "test_name": baseline_test.name,
                "category": baseline_test.category,
                "prompt": baseline_test.prompt,
                "response": f"Exception: {str(e)}",
                "response_time": time.time() - start_time,
                "baseline_score": 0.0,
                "expected_patterns": baseline_test.expected_response_patterns,
                "found_patterns": [],
                "success": False
            }
    
    def _calculate_baseline_score(self, response: str, baseline_test: BaselineTest) -> float:
        """Calculate baseline score based on expected patterns."""
        found_patterns = self._find_patterns(response, baseline_test.expected_response_patterns)
        
        if not baseline_test.expected_response_patterns:
            return 0.5  # Neutral score if no patterns expected
        
        # Calculate pattern match ratio
        pattern_score = len(found_patterns) / len(baseline_test.expected_response_patterns)
        
        # Additional scoring based on category
        if baseline_test.category == "roleplay":
            # Check for roleplay indicators
            roleplay_indicators = ["i am", "my name", "character", "role"]
            roleplay_bonus = 0.1 if any(indicator in response.lower() for indicator in roleplay_indicators) else 0.0
            return min(1.0, pattern_score + roleplay_bonus)
        
        elif baseline_test.category == "conversation":
            # Check for conversational flow
            conversation_indicators = ["yes", "no", "well", "actually", "you know"]
            conversation_bonus = 0.1 if any(indicator in response.lower() for indicator in conversation_indicators) else 0.0
            return min(1.0, pattern_score + conversation_bonus)
        
        elif baseline_test.category == "knowledge":
            # Check for factual accuracy
            return pattern_score
        
        elif baseline_test.category == "creativity":
            # Check for creative elements
            creativity_indicators = ["imagine", "story", "tale", "adventure", "magical"]
            creativity_bonus = 0.1 if any(indicator in response.lower() for indicator in creativity_indicators) else 0.0
            return min(1.0, pattern_score + creativity_bonus)
        
        return pattern_score
    
    def _find_patterns(self, response: str, expected_patterns: List[str]) -> List[str]:
        """Find which expected patterns are present in the response."""
        found = []
        response_lower = response.lower()
        
        for pattern in expected_patterns:
            if pattern.lower() in response_lower:
                found.append(pattern)
        
        return found
    
    def run_baseline_comparison(self) -> Dict:
        """Run baseline comparison for all models."""
        print("Starting Baseline Testing Framework...")
        print(f"Testing {len(self.model_baselines)} models against {len(self.baseline_tests)} baseline tests")
        
        all_results = []
        
        for model_baseline in self.model_baselines:
            print(f"\n=== Testing {model_baseline.name} ===")
            model_results = []
            
            for baseline_test in self.baseline_tests:
                print(f"  Running {baseline_test.name} ({baseline_test.category})...")
                result = self.test_model_baseline(model_baseline, baseline_test)
                model_results.append(result)
                
                # Print quick score
                score = result["baseline_score"]
                print(f"    Score: {score:.2f}")
                
                # Add delay to avoid overwhelming the endpoint
                time.sleep(1)
            
            all_results.extend(model_results)
        
        return self._generate_baseline_report(all_results)
    
    def _generate_baseline_report(self, results: List[Dict]) -> Dict:
        """Generate baseline comparison report."""
        report = {
            "summary": {},
            "model_results": {},
            "category_results": {},
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
                # Overall performance
                avg_baseline = sum(r["baseline_score"] for r in successful_tests) / len(successful_tests)
                avg_time = sum(r["response_time"] for r in successful_tests) / len(successful_tests)
                
                # Category performance
                category_scores = {}
                for result in successful_tests:
                    category = result["category"]
                    if category not in category_scores:
                        category_scores[category] = []
                    category_scores[category].append(result["baseline_score"])
                
                avg_category_scores = {}
                for category, scores in category_scores.items():
                    avg_category_scores[category] = sum(scores) / len(scores)
                
                report["model_results"][model_name] = {
                    "total_tests": len(model_results),
                    "successful_tests": len(successful_tests),
                    "success_rate": len(successful_tests) / len(model_results),
                    "avg_baseline_score": avg_baseline,
                    "avg_response_time": avg_time,
                    "category_scores": avg_category_scores,
                    "results": model_results
                }
            else:
                report["model_results"][model_name] = {
                    "total_tests": len(model_results),
                    "successful_tests": 0,
                    "success_rate": 0.0,
                    "avg_baseline_score": 0.0,
                    "avg_response_time": 0.0,
                    "category_scores": {},
                    "results": model_results
                }
        
        # Generate recommendations
        for model_name, model_data in report["model_results"].items():
            if model_data["success_rate"] < 0.8:
                report["recommendations"].append(f"{model_name}: Check endpoint connectivity")
            
            if model_data["avg_baseline_score"] < 0.6:
                report["recommendations"].append(f"{model_name}: Improve overall baseline performance")
            
            # Category-specific recommendations
            for category, score in model_data.get("category_scores", {}).items():
                if score < 0.5:
                    report["recommendations"].append(f"{model_name}: Improve {category} performance")
        
        return report
    
    def save_baseline_results(self, results: Dict, filename: str = "baseline_test_results.json"):
        """Save baseline test results to file."""
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nBaseline results saved to {filename}")
    
    def print_baseline_report(self, report: Dict):
        """Print formatted baseline report."""
        print("\n" + "=" * 80)
        print("BASELINE TESTING REPORT")
        print("=" * 80)
        
        for model_name, model_data in report["model_results"].items():
            print(f"\n🔹 {model_name.upper()}")
            print("-" * 50)
            print(f"Success Rate: {model_data['success_rate']:.1%}")
            print(f"Overall Baseline Score: {model_data['avg_baseline_score']:.2f}/1.0")
            print(f"Avg Response Time: {model_data['avg_response_time']:.2f}s")
            
            # Category breakdown
            if model_data.get("category_scores"):
                print("\nCategory Performance:")
                for category, score in model_data["category_scores"].items():
                    print(f"  {category.capitalize()}: {score:.2f}")
            
            # Test breakdown
            print("\nTest Results:")
            for result in model_data["results"]:
                score = result["baseline_score"]
                status = "✅" if result["success"] else "❌"
                print(f"  {status} {result['test_name']}: {score:.2f}")
        
        if report["recommendations"]:
            print("\n📋 RECOMMENDATIONS:")
            for rec in report["recommendations"]:
                print(f"  • {rec}")

def main():
    """Run the baseline testing framework."""
    baseline_framework = BaselineTestingFramework()
    results = baseline_framework.run_baseline_comparison()
    baseline_framework.print_baseline_report(results)
    baseline_framework.save_baseline_results(results)

if __name__ == "__main__":
    main() 