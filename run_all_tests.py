"""
Master Test Runner for PersonaForge
Executes all testing frameworks and generates comprehensive reports
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, List

# Import our testing frameworks
from improved_testing_framework import ComprehensiveModelTester
from automated_test_suite import AutomatedTestSuite
from baseline_testing import BaselineTestingFramework

class MasterTestRunner:
    def __init__(self):
        self.test_results = {}
        self.start_time = None
        self.end_time = None
        
    def run_comprehensive_tests(self) -> Dict:
        """Run comprehensive testing framework."""
        print("\n" + "="*80)
        print("RUNNING COMPREHENSIVE TESTING FRAMEWORK")
        print("="*80)
        
        tester = ComprehensiveModelTester()
        results = tester.run_comprehensive_test_suite("Nous-Hermes-2-Mistral-7B-DPO")
        
        # Convert results to dict format
        comprehensive_results = {
            "framework": "comprehensive",
            "timestamp": datetime.now().isoformat(),
            "model_results": {}
        }
        
        # Group results by model
        model_results = {}
        for result in results:
            model_name = result.model_name
            if model_name not in model_results:
                model_results[model_name] = []
            model_results[model_name].append({
                "test_name": result.test_name,
                "overall_score": result.overall_score,
                "response_time": result.response_time,
                "prompt_injection_score": result.prompt_injection_score,
                "roleplay_quality_score": result.roleplay_quality_score,
                "context_accuracy_score": result.context_accuracy_score,
                "issues": result.issues,
                "recommendations": result.recommendations
            })
        
        comprehensive_results["model_results"] = model_results
        return comprehensive_results
    
    def run_automated_tests(self) -> Dict:
        """Run automated test suite."""
        print("\n" + "="*80)
        print("RUNNING AUTOMATED TEST SUITE")
        print("="*80)
        
        test_suite = AutomatedTestSuite()
        results = test_suite.run_full_test_suite()
        
        # Add framework identifier
        results["framework"] = "automated"
        results["timestamp"] = datetime.now().isoformat()
        
        return results
    
    def run_baseline_tests(self) -> Dict:
        """Run baseline testing framework."""
        print("\n" + "="*80)
        print("RUNNING BASELINE TESTING FRAMEWORK")
        print("="*80)
        
        baseline_framework = BaselineTestingFramework()
        results = baseline_framework.run_baseline_comparison()
        
        # Add framework identifier
        results["framework"] = "baseline"
        results["timestamp"] = datetime.now().isoformat()
        
        return results
    
    def run_all_tests(self) -> Dict:
        """Run all testing frameworks."""
        self.start_time = datetime.now()
        print(f"Starting Master Test Runner at {self.start_time}")
        
        all_results = {
            "master_test_run": {
                "start_time": self.start_time.isoformat(),
                "frameworks": []
            },
            "results": {}
        }
        
        # Run all testing frameworks
        frameworks = [
            ("comprehensive", self.run_comprehensive_tests),
            ("automated", self.run_automated_tests),
            ("baseline", self.run_baseline_tests)
        ]
        
        for framework_name, framework_func in frameworks:
            try:
                print(f"\n{'='*20} {framework_name.upper()} {'='*20}")
                results = framework_func()
                all_results["results"][framework_name] = results
                all_results["master_test_run"]["frameworks"].append(framework_name)
                print(f"✅ {framework_name} completed successfully")
            except Exception as e:
                print(f"❌ {framework_name} failed: {str(e)}")
                all_results["results"][framework_name] = {
                    "error": str(e),
                    "framework": framework_name,
                    "timestamp": datetime.now().isoformat()
                }
        
        self.end_time = datetime.now()
        all_results["master_test_run"]["end_time"] = self.end_time.isoformat()
        all_results["master_test_run"]["duration"] = (self.end_time - self.start_time).total_seconds()
        
        return all_results
    
    def generate_master_report(self, results: Dict) -> str:
        """Generate comprehensive master report."""
        report_lines = []
        report_lines.append("=" * 100)
        report_lines.append("PERSONAFORGE MASTER TESTING REPORT")
        report_lines.append("=" * 100)
        
        # Test run summary
        master_run = results["master_test_run"]
        report_lines.append(f"\n📊 TEST RUN SUMMARY")
        report_lines.append(f"Start Time: {master_run['start_time']}")
        report_lines.append(f"End Time: {master_run['end_time']}")
        report_lines.append(f"Duration: {master_run['duration']:.2f} seconds")
        report_lines.append(f"Frameworks Run: {', '.join(master_run['frameworks'])}")
        
        # Framework results
        for framework_name, framework_results in results["results"].items():
            if "error" in framework_results:
                report_lines.append(f"\n❌ {framework_name.upper()} - FAILED")
                report_lines.append(f"Error: {framework_results['error']}")
                continue
            
            report_lines.append(f"\n✅ {framework_name.upper()} - COMPLETED")
            
            if framework_name == "comprehensive":
                self._add_comprehensive_summary(report_lines, framework_results)
            elif framework_name == "automated":
                self._add_automated_summary(report_lines, framework_results)
            elif framework_name == "baseline":
                self._add_baseline_summary(report_lines, framework_results)
        
        # Overall recommendations
        report_lines.append(f"\n" + "=" * 100)
        report_lines.append("OVERALL RECOMMENDATIONS")
        report_lines.append("=" * 100)
        
        recommendations = self._generate_overall_recommendations(results)
        for rec in recommendations:
            report_lines.append(f"• {rec}")
        
        return "\n".join(report_lines)
    
    def _add_comprehensive_summary(self, report_lines: List[str], results: Dict):
        """Add comprehensive testing summary to report."""
        for model_name, model_results in results["model_results"].items():
            report_lines.append(f"\n🔹 {model_name}")
            
            # Calculate averages
            scores = [r["overall_score"] for r in model_results]
            times = [r["response_time"] for r in model_results]
            
            avg_score = sum(scores) / len(scores) if scores else 0
            avg_time = sum(times) / len(times) if times else 0
            
            report_lines.append(f"  Average Score: {avg_score:.2f}/1.0")
            report_lines.append(f"  Average Response Time: {avg_time:.2f}s")
            
            # Test breakdown
            for result in model_results:
                report_lines.append(f"    {result['test_name']}: {result['overall_score']:.2f}")
    
    def _add_automated_summary(self, report_lines: List[str], results: Dict):
        """Add automated testing summary to report."""
        for model_name, model_data in results["model_results"].items():
            report_lines.append(f"\n🔹 {model_name}")
            report_lines.append(f"  Success Rate: {model_data['success_rate']:.1%}")
            report_lines.append(f"  Overall Score: {model_data['avg_overall_score']:.2f}/1.0")
            report_lines.append(f"  Avg Response Time: {model_data['avg_response_time']:.2f}s")
            
            # Category scores
            if model_data.get("category_scores"):
                for category, score in model_data["category_scores"].items():
                    report_lines.append(f"    {category.capitalize()}: {score:.2f}")
    
    def _add_baseline_summary(self, report_lines: List[str], results: Dict):
        """Add baseline testing summary to report."""
        for model_name, model_data in results["model_results"].items():
            report_lines.append(f"\n🔹 {model_name}")
            report_lines.append(f"  Success Rate: {model_data['success_rate']:.1%}")
            report_lines.append(f"  Baseline Score: {model_data['avg_baseline_score']:.2f}/1.0")
            report_lines.append(f"  Avg Response Time: {model_data['avg_response_time']:.2f}s")
            
            # Category scores
            if model_data.get("category_scores"):
                for category, score in model_data["category_scores"].items():
                    report_lines.append(f"    {category.capitalize()}: {score:.2f}")
    
    def _generate_overall_recommendations(self, results: Dict) -> List[str]:
        """Generate overall recommendations based on all test results."""
        recommendations = []
        
        # Check for framework failures
        failed_frameworks = []
        for framework_name, framework_results in results["results"].items():
            if "error" in framework_results:
                failed_frameworks.append(framework_name)
        
        if failed_frameworks:
            recommendations.append(f"Fix failed frameworks: {', '.join(failed_frameworks)}")
        
        # Check for performance issues
        for framework_name, framework_results in results["results"].items():
            if "error" in framework_results:
                continue
                
            if framework_name == "automated":
                for model_name, model_data in framework_results["model_results"].items():
                    if model_data["avg_response_time"] > 10:
                        recommendations.append(f"{model_name}: Optimize response time (currently {model_data['avg_response_time']:.2f}s)")
            
            elif framework_name == "baseline":
                for model_name, model_data in framework_results["model_results"].items():
                    if model_data["avg_response_time"] > 10:
                        recommendations.append(f"{model_name}: Optimize baseline response time (currently {model_data['avg_response_time']:.2f}s)")
        
        # Check for quality issues
        for framework_name, framework_results in results["results"].items():
            if "error" in framework_results:
                continue
                
            if framework_name == "automated":
                for model_name, model_data in framework_results["model_results"].items():
                    if model_data["avg_overall_score"] < 0.6:
                        recommendations.append(f"{model_name}: Improve overall performance (score: {model_data['avg_overall_score']:.2f})")
            
            elif framework_name == "baseline":
                for model_name, model_data in framework_results["model_results"].items():
                    if model_data["avg_baseline_score"] < 0.6:
                        recommendations.append(f"{model_name}: Improve baseline performance (score: {model_data['avg_baseline_score']:.2f})")
        
        # General recommendations
        recommendations.append("Consider testing with additional models when endpoints become available")
        recommendations.append("Implement continuous testing in CI/CD pipeline")
        recommendations.append("Add more edge case scenarios to test suites")
        
        return recommendations
    
    def save_master_results(self, results: Dict, filename: str = "master_test_results.json"):
        """Save master test results to file."""
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nMaster results saved to {filename}")
    
    def save_master_report(self, report: str, filename: str = "master_test_report.md"):
        """Save master report to markdown file."""
        with open(filename, "w") as f:
            f.write(report)
        print(f"Master report saved to {filename}")

def main():
    """Run the master test runner."""
    print("🚀 Starting PersonaForge Master Test Runner...")
    
    runner = MasterTestRunner()
    
    try:
        # Run all tests
        results = runner.run_all_tests()
        
        # Generate and save reports
        report = runner.generate_master_report(results)
        runner.save_master_results(results)
        runner.save_master_report(report)
        
        # Print summary
        print("\n" + "="*100)
        print("MASTER TEST RUN COMPLETED")
        print("="*100)
        print(f"Duration: {results['master_test_run']['duration']:.2f} seconds")
        print(f"Frameworks: {', '.join(results['master_test_run']['frameworks'])}")
        print("\nCheck the generated files for detailed results:")
        print("• master_test_results.json - Raw test data")
        print("• master_test_report.md - Formatted report")
        
    except Exception as e:
        print(f"❌ Master test run failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 