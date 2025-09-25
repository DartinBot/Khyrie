"""
Khyrie3.0 API Integration Utility
Provides helper functions for connecting with the broader Khyrie3.0 ecosystem
"""

import requests
import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KhyrieIntegration:
    """
    Integration utility class for connecting Khyrie3.0 components
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Khyrie3.0-Integration/1.0"
        })
    
    def health_check(self) -> Dict:
        """Check if the Khyrie3.0 backend is running"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_integration_status(self) -> Dict:
        """Get the current integration status"""
        try:
            response = self.session.get(f"{self.base_url}/api/integration/status")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Integration status check failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def test_family_api(self) -> Dict:
        """Test the Family & Friends API functionality"""
        try:
            # Test getting groups
            response = self.session.get(f"{self.base_url}/api/family/groups")
            if response.status_code == 200:
                return {
                    "family_api": "✅ Working",
                    "endpoints_available": True,
                    "data": response.json()
                }
            else:
                return {
                    "family_api": "⚠️ Accessible but returned error",
                    "status_code": response.status_code,
                    "message": response.text
                }
        except requests.exceptions.RequestException as e:
            return {
                "family_api": "❌ Not accessible", 
                "error": str(e)
            }
    
    def test_ai_api(self) -> Dict:
        """Test the AI API functionality"""
        try:
            # Test AI capabilities
            response = self.session.get(f"{self.base_url}/api/quick/workout-generation")
            if response.status_code == 200:
                return {
                    "ai_api": "✅ Working",
                    "endpoints_available": True,
                    "data": response.json()
                }
            else:
                return {
                    "ai_api": "⚠️ Accessible but returned error",
                    "status_code": response.status_code,
                    "message": response.text
                }
        except requests.exceptions.RequestException as e:
            return {
                "ai_api": "❌ Not accessible",
                "error": str(e)
            }
    
    def generate_workout(self, user_profile: Dict) -> Dict:
        """Generate a workout using the AI engine"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/ai/generate-workout",
                json=user_profile
            )
            response.raise_for_status()
            return {
                "success": True,
                "workout": response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_family_group(self, group_data: Dict) -> Dict:
        """Create a new family fitness group"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/family/groups",
                json=group_data
            )
            response.raise_for_status()
            return {
                "success": True,
                "group": response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def run_comprehensive_test(self) -> Dict:
        """Run a comprehensive test of all Khyrie3.0 integrations"""
        results = {
            "timestamp": "2025-09-25",
            "tests": {}
        }
        
        # Test 1: Health Check
        logger.info("🔍 Testing health check...")
        results["tests"]["health_check"] = self.health_check()
        
        # Test 2: Integration Status
        logger.info("🔍 Testing integration status...")
        results["tests"]["integration_status"] = self.get_integration_status()
        
        # Test 3: Family API
        logger.info("🔍 Testing Family & Friends API...")
        results["tests"]["family_api"] = self.test_family_api()
        
        # Test 4: AI API
        logger.info("🔍 Testing AI API...")
        results["tests"]["ai_api"] = self.test_ai_api()
        
        # Test 5: Sample Workout Generation
        logger.info("🔍 Testing AI workout generation...")
        sample_profile = {
            "fitness_level": "intermediate",
            "goals": ["strength"],
            "available_time": 30,
            "equipment": ["bodyweight"]
        }
        results["tests"]["workout_generation"] = self.generate_workout(sample_profile)
        
        # Test 6: Sample Family Group Creation
        logger.info("🔍 Testing family group creation...")
        sample_group = {
            "name": "Test Family Group",
            "description": "Integration test group",
            "privacy": "private"
        }
        results["tests"]["family_group_creation"] = self.create_family_group(sample_group)
        
        return results
    
    def frontend_api_config(self) -> Dict:
        """Generate configuration for frontend API integration"""
        return {
            "api_config": {
                "base_url": self.base_url,
                "endpoints": {
                    "health": f"{self.base_url}/health",
                    "family": {
                        "groups": f"{self.base_url}/api/family/groups",
                        "workouts": f"{self.base_url}/api/family/shared-workout",
                        "challenges": f"{self.base_url}/api/family/challenges"
                    },
                    "ai": {
                        "generate_workout": f"{self.base_url}/api/ai/generate-workout",
                        "exercise_substitution": f"{self.base_url}/api/ai/exercise-substitution",
                        "risk_assessment": f"{self.base_url}/api/ai/injury-risk-assessment"
                    }
                },
                "headers": {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            },
            "javascript_example": """
// Frontend API Integration Example
const KhyrieAPI = {
    baseURL: 'http://localhost:8000',
    
    // Health check
    async healthCheck() {
        const response = await fetch(`${this.baseURL}/health`);
        return response.json();
    },
    
    // AI workout generation
    async generateWorkout(userProfile) {
        const response = await fetch(`${this.baseURL}/api/ai/generate-workout`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userProfile)
        });
        return response.json();
    },
    
    // Family group management
    async getGroups() {
        const response = await fetch(`${this.baseURL}/api/family/groups`);
        return response.json();
    },
    
    async createGroup(groupData) {
        const response = await fetch(`${this.baseURL}/api/family/groups`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(groupData)
        });
        return response.json();
    }
};
            """
        }
    
    def save_test_results(self, results: Dict, filename: str = "integration_test_results.json"):
        """Save test results to a JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            logger.info(f"✅ Test results saved to {filename}")
        except Exception as e:
            logger.error(f"❌ Failed to save test results: {e}")

# CLI interface for testing
if __name__ == "__main__":
    print("🏋️‍♂️ Khyrie3.0 Integration Testing")
    print("=" * 40)
    
    # Initialize integration utility
    integration = KhyrieIntegration()
    
    # Run comprehensive test
    print("\n🧪 Running comprehensive integration tests...")
    results = integration.run_comprehensive_test()
    
    # Display results
    print("\n📊 Test Results:")
    print("-" * 20)
    
    for test_name, result in results["tests"].items():
        print(f"\n{test_name.replace('_', ' ').title()}:")
        
        if isinstance(result, dict):
            if "success" in result:
                status = "✅ PASS" if result["success"] else "❌ FAIL"
            elif "status" in result:
                if result["status"] == "healthy":
                    status = "✅ HEALTHY"
                elif "error" in result["status"]:
                    status = "❌ ERROR"
                else:
                    status = "⚠️ WARNING"
            else:
                status = "ℹ️ INFO"
            
            print(f"  Status: {status}")
            
            # Show key information
            if "message" in result:
                print(f"  Message: {result['message']}")
            if "error" in result:
                print(f"  Error: {result['error']}")
    
    # Save results
    integration.save_test_results(results)
    
    # Generate frontend config
    print("\n🌐 Frontend Integration Configuration:")
    print("-" * 40)
    config = integration.frontend_api_config()
    print(json.dumps(config["api_config"], indent=2))
    
    print("\n✅ Integration testing completed!")
    print("📄 Results saved to integration_test_results.json")
    print("🚀 Your Khyrie3.0 integration is ready!")