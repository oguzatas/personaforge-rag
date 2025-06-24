"""
Comprehensive Testing Framework for PersonaForge Model Evaluation
Addresses limitations of current testing approach
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
class TestResult:
    """Structured test result with metrics."""
    model_name: str
    test_name: str
    prompt: str
    response: str
    response_time: float
    prompt_injection_score: float  # 0-1, where 1 is no injection
    roleplay_quality_score: float  # 0-1, where 1 is excellent roleplay
    context_accuracy_score: float  # 0-1, where 1 is perfect context use
    overall_score: float  # 0-1, weighted average
    issues: List[str]
    recommendations: List[str]

class ComprehensiveModelTester:
    def __init__(self, endpoint_url: str = None):
        self.endpoint_url = endpoint_url or LLM_ENDPOINT_URL
        self.test_results: List[TestResult] = []
        
    def test_endpoint(self, prompt: str, max_tokens: int = 150, temperature: float = 0.7) -> Tuple[str, float]:
        """Test endpoint with timing and error handling."""
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
            response = requests.post(self.endpoint_url, json=payload, headers=headers, timeout=60)
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
    
    def calculate_prompt_injection_score(self, response: str) -> float:
        """Calculate prompt injection score (0-1, where 1 is no injection)."""
        injection_indicators = [
            "You are",
            "User says:",
            "Respond as your character:",
            "Background:",
            "Recent conversation:"
        ]
        
        score = 1.0
        for indicator in injection_indicators:
            if indicator in response:
                score -= 0.2  # Penalty for each injection indicator
        
        return max(0.0, score)
    
    def calculate_roleplay_quality_score(self, response: str, character_traits: List[str]) -> float:
        """Calculate roleplay quality score based on character traits."""
        score = 0.5  # Base score
        
        # Check for character-specific language
        formal_indicators = ["greetings", "mortal", "ancient", "wisdom", "arcan", "magic"]
        for indicator in formal_indicators:
            if indicator.lower() in response.lower():
                score += 0.1
        
        # Check for character traits
        for trait in character_traits:
            if trait.lower() in response.lower():
                score += 0.1
        
        # Penalty for generic responses
        generic_phrases = ["hello", "hi there", "how can i help", "i'm here to help"]
        for phrase in generic_phrases:
            if phrase.lower() in response.lower():
                score -= 0.1
        
        return min(1.0, max(0.0, score))
    
    def calculate_context_accuracy_score(self, response: str, context_elements: List[str]) -> float:
        """Calculate how well the model uses provided context."""
        score = 0.0
        found_elements = 0
        
        for element in context_elements:
            if element.lower() in response.lower():
                found_elements += 1
        
        if context_elements:
            score = found_elements / len(context_elements)
        
        return score
    
    def test_basic_roleplay(self, model_name: str) -> TestResult:
        """Test basic roleplay capabilities."""
        prompt = """Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember.

User: How are you today?

Kael Vire:"""
        
        response, response_time = self.test_endpoint(prompt)
        
        # Calculate scores
        prompt_injection_score = self.calculate_prompt_injection_score(response)
        roleplay_quality_score = self.calculate_roleplay_quality_score(
            response, ["wise", "elven", "mage", "ancient", "formal"]
        )
        context_accuracy_score = self.calculate_context_accuracy_score(
            response, ["fire magic", "mytherra", "ember"]
        )
        
        # Overall score (weighted average)
        overall_score = (
            prompt_injection_score * 0.4 +
            roleplay_quality_score * 0.4 +
            context_accuracy_score * 0.2
        )
        
        # Identify issues
        issues = []
        if prompt_injection_score < 0.8:
            issues.append("Prompt injection detected")
        if roleplay_quality_score < 0.6:
            issues.append("Poor roleplay quality")
        if context_accuracy_score < 0.5:
            issues.append("Poor context usage")
        if response_time > 10:
            issues.append("Slow response time")
        
        # Generate recommendations
        recommendations = []
        if prompt_injection_score < 0.8:
            recommendations.append("Use natural conversation prompt format")
        if roleplay_quality_score < 0.6:
            recommendations.append("Improve character trait integration")
        if context_accuracy_score < 0.5:
            recommendations.append("Enhance context utilization")
        
        return TestResult(
            model_name=model_name,
            test_name="Basic Roleplay",
            prompt=prompt,
            response=response,
            response_time=response_time,
            prompt_injection_score=prompt_injection_score,
            roleplay_quality_score=roleplay_quality_score,
            context_accuracy_score=context_accuracy_score,
            overall_score=overall_score,
            issues=issues,
            recommendations=recommendations
        )
    
    def test_conversation_flow(self, model_name: str) -> TestResult:
        """Test conversation flow and continuity."""
        prompt = """Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a master of fire magic and lives in the ancient forest of Mytherra. He has a pet phoenix named Ember.

Recent conversation:
User: Hello there!
Kael Vire: Greetings, traveler. I am Kael Vire, master of the arcane arts.
User: Nice to meet you!

User: How are you today?

Kael Vire:"""
        
        response, response_time = self.test_endpoint(prompt)
        
        # Calculate scores
        prompt_injection_score = self.calculate_prompt_injection_score(response)
        roleplay_quality_score = self.calculate_roleplay_quality_score(
            response, ["wise", "elven", "mage", "ancient", "formal"]
        )
        context_accuracy_score = self.calculate_context_accuracy_score(
            response, ["fire magic", "mytherra", "ember"]
        )
        
        # Bonus for conversation continuity
        continuity_bonus = 0.1 if "greetings" in response.lower() or "traveler" in response.lower() else 0.0
        context_accuracy_score = min(1.0, context_accuracy_score + continuity_bonus)
        
        overall_score = (
            prompt_injection_score * 0.4 +
            roleplay_quality_score * 0.4 +
            context_accuracy_score * 0.2
        )
        
        issues = []
        if prompt_injection_score < 0.8:
            issues.append("Prompt injection in conversation")
        if roleplay_quality_score < 0.6:
            issues.append("Poor conversation roleplay")
        if context_accuracy_score < 0.5:
            issues.append("Poor conversation context usage")
        
        recommendations = []
        if prompt_injection_score < 0.8:
            recommendations.append("Use conversation-optimized prompts")
        if roleplay_quality_score < 0.6:
            recommendations.append("Improve conversation roleplay")
        
        return TestResult(
            model_name=model_name,
            test_name="Conversation Flow",
            prompt=prompt,
            response=response,
            response_time=response_time,
            prompt_injection_score=prompt_injection_score,
            roleplay_quality_score=roleplay_quality_score,
            context_accuracy_score=context_accuracy_score,
            overall_score=overall_score,
            issues=issues,
            recommendations=recommendations
        )
    
    def test_emotional_response(self, model_name: str) -> TestResult:
        """Test emotional response capabilities."""
        prompt = """Kael Vire, a wise elven mage who speaks with ancient wisdom and uses formal language.

Background: Kael Vire is a proud elven mage who gets offended easily.

User: Your magic is weak.

Kael Vire:"""
        
        response, response_time = self.test_endpoint(prompt)
        
        # Calculate scores
        prompt_injection_score = self.calculate_prompt_injection_score(response)
        roleplay_quality_score = self.calculate_roleplay_quality_score(
            response, ["proud", "offended", "insult", "dare", "question"]
        )
        context_accuracy_score = self.calculate_context_accuracy_score(
            response, ["proud", "offended", "magic"]
        )
        
        overall_score = (
            prompt_injection_score * 0.4 +
            roleplay_quality_score * 0.4 +
            context_accuracy_score * 0.2
        )
        
        issues = []
        if prompt_injection_score < 0.8:
            issues.append("Prompt injection in emotional response")
        if roleplay_quality_score < 0.6:
            issues.append("Poor emotional roleplay")
        
        recommendations = []
        if roleplay_quality_score < 0.6:
            recommendations.append("Improve emotional response generation")
        
        return TestResult(
            model_name=model_name,
            test_name="Emotional Response",
            prompt=prompt,
            response=response,
            response_time=response_time,
            prompt_injection_score=prompt_injection_score,
            roleplay_quality_score=roleplay_quality_score,
            context_accuracy_score=context_accuracy_score,
            overall_score=overall_score,
            issues=issues,
            recommendations=recommendations
        )
    
    def test_performance_benchmark(self, model_name: str) -> TestResult:
        """Test performance with multiple requests."""
        prompt = "Hello, how are you?"
        
        times = []
        responses = []
        
        for i in range(5):
            response, time_taken = self.test_endpoint(prompt)
            times.append(time_taken)
            responses.append(response)
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        # Performance scoring
        if avg_time < 2:
            performance_score = 1.0
        elif avg_time < 5:
            performance_score = 0.8
        elif avg_time < 10:
            performance_score = 0.6
        elif avg_time < 20:
            performance_score = 0.4
        else:
            performance_score = 0.2
        
        # Consistency scoring
        time_variance = max_time - min_time
        if time_variance < 1:
            consistency_score = 1.0
        elif time_variance < 3:
            consistency_score = 0.8
        elif time_variance < 5:
            consistency_score = 0.6
        else:
            consistency_score = 0.4
        
        overall_score = (performance_score + consistency_score) / 2
        
        issues = []
        if avg_time > 10:
            issues.append(f"Slow average response time: {avg_time:.2f}s")
        if time_variance > 5:
            issues.append(f"Inconsistent response times: {time_variance:.2f}s variance")
        
        recommendations = []
        if avg_time > 10:
            recommendations.append("Optimize model performance")
        if time_variance > 5:
            recommendations.append("Improve response time consistency")
        
        return TestResult(
            model_name=model_name,
            test_name="Performance Benchmark",
            prompt=f"5 requests: {prompt}",
            response=f"Average: {avg_time:.2f}s, Min: {min_time:.2f}s, Max: {max_time:.2f}s",
            response_time=avg_time,
            prompt_injection_score=1.0,  # Not applicable for performance test
            roleplay_quality_score=performance_score,
            context_accuracy_score=consistency_score,
            overall_score=overall_score,
            issues=issues,
            recommendations=recommendations
        )
    
    def run_comprehensive_test_suite(self, model_name: str) -> List[TestResult]:
        """Run all tests for a model."""
        print(f"\n=== COMPREHENSIVE TESTING: {model_name} ===")
        
        tests = [
            self.test_basic_roleplay,
            self.test_conversation_flow,
            self.test_emotional_response,
            self.test_performance_benchmark
        ]
        
        results = []
        for test_func in tests:
            print(f"\nRunning {test_func.__name__}...")
            result = test_func(model_name)
            results.append(result)
            print(f"Score: {result.overall_score:.2f}")
            if result.issues:
                print(f"Issues: {', '.join(result.issues)}")
        
        self.test_results.extend(results)
        return results
    
    def generate_comprehensive_report(self) -> str:
        """Generate a comprehensive test report."""
        if not self.test_results:
            return "No test results available."
        
        report = []
        report.append("=" * 80)
        report.append("COMPREHENSIVE MODEL TESTING REPORT")
        report.append("=" * 80)
        
        # Group results by model
        model_results = {}
        for result in self.test_results:
            if result.model_name not in model_results:
                model_results[result.model_name] = []
            model_results[result.model_name].append(result)
        
        for model_name, results in model_results.items():
            report.append(f"\n🔹 {model_name.upper()}")
            report.append("-" * 50)
            
            # Calculate overall model score
            overall_scores = [r.overall_score for r in results]
            avg_overall = sum(overall_scores) / len(overall_scores)
            
            report.append(f"Overall Model Score: {avg_overall:.2f}/1.0")
            
            # Individual test results
            for result in results:
                report.append(f"\n{result.test_name}:")
                report.append(f"  Score: {result.overall_score:.2f}/1.0")
                report.append(f"  Response Time: {result.response_time:.2f}s")
                report.append(f"  Prompt Injection: {result.prompt_injection_score:.2f}")
                report.append(f"  Roleplay Quality: {result.roleplay_quality_score:.2f}")
                report.append(f"  Context Accuracy: {result.context_accuracy_score:.2f}")
                
                if result.issues:
                    report.append(f"  Issues: {', '.join(result.issues)}")
                if result.recommendations:
                    report.append(f"  Recommendations: {', '.join(result.recommendations)}")
        
        # Summary and recommendations
        report.append("\n" + "=" * 80)
        report.append("SUMMARY AND RECOMMENDATIONS")
        report.append("=" * 80)
        
        best_model = max(model_results.keys(), 
                        key=lambda m: sum(r.overall_score for r in model_results[m]) / len(model_results[m]))
        
        report.append(f"\nBest Performing Model: {best_model}")
        report.append(f"Recommendation: Use {best_model} for production with identified improvements")
        
        return "\n".join(report)

def main():
    """Run comprehensive testing framework."""
    print("Starting Comprehensive Model Testing Framework...")
    
    tester = ComprehensiveModelTester()
    
    # Test current model (Nous-Hermes-2-Mistral-7B-DPO)
    results = tester.run_comprehensive_test_suite("Nous-Hermes-2-Mistral-7B-DPO")
    
    # Generate report
    report = tester.generate_comprehensive_report()
    print(report)
    
    # Save results
    with open("comprehensive_test_results.json", "w") as f:
        json.dump([{
            "model_name": r.model_name,
            "test_name": r.test_name,
            "overall_score": r.overall_score,
            "response_time": r.response_time,
            "prompt_injection_score": r.prompt_injection_score,
            "roleplay_quality_score": r.roleplay_quality_score,
            "context_accuracy_score": r.context_accuracy_score,
            "issues": r.issues,
            "recommendations": r.recommendations
        } for r in results], f, indent=2)

if __name__ == "__main__":
    main() 