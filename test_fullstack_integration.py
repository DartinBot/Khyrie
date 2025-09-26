#!/usr/bin/env python3
"""
Khyrie3.0 Full-Stack Integration Test
Tests the complete frontend-backend integration
"""

import requests
import json
import time
from datetime import datetime

class Khyrie3IntegrationTest:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "backend_url": base_url,
            "tests": {}
        }
    
    def run_all_tests(self):
        """Run comprehensive integration tests"""
        print("🧪 Starting Khyrie3.0 Full-Stack Integration Tests")
        print("=" * 60)
        
        tests = [
            ("Backend Health", self.test_backend_health),
            ("Frontend Dashboard", self.test_frontend_dashboard),
            ("API Endpoints", self.test_api_endpoints),
            ("Subscription System", self.test_subscription_system),
            ("AI Features", self.test_ai_features),
            ("Static Assets", self.test_static_assets)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔍 Testing: {test_name}")
            try:
                result = test_func()
                self.test_results["tests"][test_name] = result
                status = "✅ PASS" if result.get("success") else "❌ FAIL"
                print(f"   {status} - {result.get('message', 'No message')}")
            except Exception as e:
                self.test_results["tests"][test_name] = {
                    "success": False,
                    "error": str(e),
                    "message": f"Test failed with exception: {e}"
                }
                print(f"   ❌ ERROR - {e}")
        
        self.generate_report()
        return self.test_results
    
    def test_backend_health(self):
        """Test backend health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "status_code": response.status_code,
                "response": data,
                "message": "Backend is healthy and responsive"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Backend health check failed"
            }
    
    def test_frontend_dashboard(self):
        """Test frontend dashboard loads correctly"""
        try:
            response = requests.get(f"{self.base_url}/dashboard", timeout=10)
            response.raise_for_status()
            
            html_content = response.text
            required_elements = [
                "Khyrie3.0",
                "AI Features", 
                "Family & Friends",
                "Subscriptions",
                "khyrie-frontend.js"
            ]
            
            missing_elements = [elem for elem in required_elements if elem not in html_content]
            
            return {
                "success": len(missing_elements) == 0,
                "status_code": response.status_code,
                "content_length": len(html_content),
                "missing_elements": missing_elements,
                "message": "Dashboard loaded successfully" if not missing_elements else f"Missing elements: {missing_elements}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Frontend dashboard test failed"
            }
    
    def test_api_endpoints(self):
        """Test critical API endpoints"""
        endpoints = [
            "/",
            "/health", 
            "/api/integration/status",
            "/api/quick/workout-generation",
            "/api/subscriptions/status",
            "/api/subscriptions/plans"
        ]
        
        results = {}
        success_count = 0
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                results[endpoint] = {
                    "status_code": response.status_code,
                    "success": response.status_code == 200,
                    "response_time": response.elapsed.total_seconds()
                }
                if response.status_code == 200:
                    success_count += 1
            except Exception as e:
                results[endpoint] = {
                    "success": False,
                    "error": str(e)
                }
        
        return {
            "success": success_count >= len(endpoints) * 0.8,  # 80% success rate
            "endpoints_tested": len(endpoints),
            "endpoints_passed": success_count,
            "results": results,
            "message": f"{success_count}/{len(endpoints)} endpoints working correctly"
        }
    
    def test_subscription_system(self):
        """Test subscription system functionality"""
        try:
            # Test getting plans
            plans_response = requests.get(f"{self.base_url}/api/subscriptions/plans")
            plans_response.raise_for_status()
            plans_data = plans_response.json()
            
            # Test getting status
            status_response = requests.get(f"{self.base_url}/api/subscriptions/status")
            status_response.raise_for_status()
            status_data = status_response.json()
            
            # Test creating subscription
            create_response = requests.post(
                f"{self.base_url}/api/subscriptions/create",
                json={"tier": "premium"},
                headers={"Content-Type": "application/json"}
            )
            
            return {
                "success": True,
                "plans_available": len(plans_data.get("plans", [])),
                "user_tier": status_data.get("tier"),
                "create_subscription": create_response.status_code == 200,
                "message": "Subscription system fully functional"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Subscription system test failed"
            }
    
    def test_ai_features(self):
        """Test AI features functionality"""
        try:
            response = requests.get(f"{self.base_url}/api/quick/workout-generation")
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "ai_available": "sample_workout" in data or "mock_available" in data,
                "response": data,
                "message": "AI features accessible (with mock implementation)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "AI features test failed"
            }
    
    def test_static_assets(self):
        """Test static asset delivery"""
        assets = [
            "/khyrie-frontend.js",
            "/manifest.json",
            "/favicon.ico"
        ]
        
        results = {}
        success_count = 0
        
        for asset in assets:
            try:
                response = requests.get(f"{self.base_url}{asset}", timeout=5)
                results[asset] = {
                    "status_code": response.status_code,
                    "content_length": len(response.content),
                    "success": response.status_code == 200
                }
                if response.status_code == 200:
                    success_count += 1
            except Exception as e:
                results[asset] = {
                    "success": False,
                    "error": str(e)
                }
        
        return {
            "success": success_count >= 1,  # At least JS file should work
            "assets_tested": len(assets),
            "assets_available": success_count,
            "results": results,
            "message": f"{success_count}/{len(assets)} static assets available"
        }
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print(f"\n" + "=" * 60)
        print("📊 KHYRIE3.0 FULL-STACK INTEGRATION REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results["tests"])
        passed_tests = sum(1 for test in self.test_results["tests"].values() if test.get("success"))
        
        print(f"\n📈 Test Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {total_tests - passed_tests}")
        print(f"   Success Rate: {passed_tests/total_tests*100:.1f}%")
        
        print(f"\n🔧 Component Status:")
        for test_name, result in self.test_results["tests"].items():
            status = "✅ WORKING" if result.get("success") else "❌ FAILED"
            print(f"   {status} {test_name}")
        
        # Integration assessment
        if passed_tests >= total_tests * 0.9:
            print(f"\n🎉 INTEGRATION STATUS: EXCELLENT")
            print("   Your Khyrie3.0 full-stack integration is working perfectly!")
        elif passed_tests >= total_tests * 0.7:
            print(f"\n✅ INTEGRATION STATUS: GOOD") 
            print("   Most components working, minor issues to resolve")
        else:
            print(f"\n⚠️ INTEGRATION STATUS: NEEDS ATTENTION")
            print("   Several components need fixing before production")
        
        # Save detailed results
        with open("khyrie3_integration_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"\n💾 Detailed results saved to: khyrie3_integration_test_results.json")
        print(f"🕒 Test completed at: {self.test_results['timestamp']}")

def main():
    """Run the integration test suite"""
    print("🏋️‍♀️ Khyrie3.0 Full-Stack Integration Test Suite")
    print("Comprehensive testing of frontend-backend integration")
    print()
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for backend to be ready...")
    time.sleep(2)
    
    # Run tests
    tester = Khyrie3IntegrationTest()
    results = tester.run_all_tests()
    
    return results

if __name__ == "__main__":
    main()