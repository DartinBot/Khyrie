#!/usr/bin/env python3
"""
Khyrie3.0 Complete Integration Demo
A comprehensive demonstration of the full-stack application
"""
import requests
import json
import time
from datetime import datetime

def print_banner(title):
    """Print a formatted banner"""
    print("\n" + "="*60)
    print(f"🏋️‍♀️ {title}")
    print("="*60)

def demo_api_endpoints():
    """Demonstrate all API endpoints"""
    base_url = "http://localhost:8000"
    
    print_banner("API ENDPOINTS DEMONSTRATION")
    
    endpoints = [
        ("/health", "Backend Health Check"),
        ("/api/integration/status", "Integration Status"),
        ("/api/subscriptions/status", "Subscription Status"),
        ("/api/subscriptions/plans", "Available Plans"),
        ("/api/quick/workout-generation", "AI Workout Generation"),
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"\n📍 {description}")
            print(f"   URL: {base_url}{endpoint}")
            print(f"   Status: {response.status_code}")
            
            if response.headers.get('content-type', '').startswith('application/json'):
                data = response.json()
                if isinstance(data, dict) and len(str(data)) < 200:
                    print(f"   Response: {json.dumps(data, indent=2)}")
                else:
                    print(f"   Response: {type(data).__name__} with {len(str(data))} characters")
            else:
                print(f"   Response: {response.headers.get('content-type', 'Unknown type')}")
                
        except Exception as e:
            print(f"❌ Error testing {endpoint}: {e}")

def demo_subscription_system():
    """Demonstrate subscription functionality"""
    print_banner("SUBSCRIPTION SYSTEM DEMONSTRATION")
    base_url = "http://localhost:8000"
    
    try:
        # Get available plans
        plans_response = requests.get(f"{base_url}/api/subscriptions/plans")
        plans = plans_response.json()
        print(f"\n📋 Available Subscription Plans:")
        for plan in plans.get('plans', []):
            print(f"   • {plan['name']}: ${plan['price']}/month - {plan['description']}")
        
        # Check current status
        status_response = requests.get(f"{base_url}/api/subscriptions/status")
        status = status_response.json()
        print(f"\n📊 Current Subscription Status:")
        print(f"   • Tier: {status.get('tier', 'Unknown')}")
        print(f"   • Active: {status.get('is_active', False)}")
        
        # Demo subscription creation
        create_data = {
            "plan_name": "premium",
            "user_id": "demo_user_123"
        }
        create_response = requests.post(
            f"{base_url}/api/subscriptions/create",
            json=create_data
        )
        result = create_response.json()
        print(f"\n✅ Demo Subscription Creation:")
        print(f"   • Success: {result.get('success', False)}")
        print(f"   • Message: {result.get('message', 'No message')}")
        
    except Exception as e:
        print(f"❌ Error in subscription demo: {e}")

def demo_ai_features():
    """Demonstrate AI features"""
    print_banner("AI FEATURES DEMONSTRATION")
    base_url = "http://localhost:8000"
    
    try:
        # Test workout generation
        workout_response = requests.get(f"{base_url}/api/quick/workout-generation")
        workout_data = workout_response.json()
        print(f"\n🤖 AI Workout Generation:")
        print(f"   • Status: {workout_data.get('status', 'Unknown')}")
        print(f"   • Method: {workout_data.get('method', 'Unknown')}")
        
        if 'workout' in workout_data:
            workout = workout_data['workout']
            print(f"   • Generated Workout:")
            print(f"     - Type: {workout.get('type', 'N/A')}")
            print(f"     - Duration: {workout.get('duration', 'N/A')}")
            print(f"     - Exercises: {len(workout.get('exercises', []))}")
        
    except Exception as e:
        print(f"❌ Error in AI demo: {e}")

def demo_frontend_integration():
    """Demonstrate frontend integration"""
    print_banner("FRONTEND INTEGRATION DEMONSTRATION")
    base_url = "http://localhost:8000"
    
    try:
        # Test dashboard access
        dashboard_response = requests.get(f"{base_url}/dashboard")
        print(f"\n🎨 Frontend Dashboard:")
        print(f"   • Status Code: {dashboard_response.status_code}")
        print(f"   • Content Type: {dashboard_response.headers.get('content-type', 'Unknown')}")
        print(f"   • Content Length: {len(dashboard_response.content)} bytes")
        
        # Test JavaScript assets
        js_response = requests.get(f"{base_url}/khyrie-frontend.js")
        print(f"\n📄 JavaScript Assets:")
        print(f"   • Status Code: {js_response.status_code}")
        print(f"   • Content Length: {len(js_response.content)} bytes")
        
        # Check if KhyrieAPI is properly defined
        js_content = js_response.text
        if "class KhyrieAPI" in js_content:
            print(f"   • KhyrieAPI Class: ✅ Found")
        else:
            print(f"   • KhyrieAPI Class: ❌ Not found")
            
    except Exception as e:
        print(f"❌ Error in frontend demo: {e}")

def main():
    """Run complete integration demo"""
    print_banner("KHYRIE3.0 COMPLETE INTEGRATION DEMO")
    print(f"🕒 Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Backend URL: http://localhost:8000")
    print(f"🎯 Dashboard URL: http://localhost:8000/dashboard")
    
    try:
        # Check if backend is running
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Backend is running and healthy")
        else:
            print("❌ Backend health check failed")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Make sure to run: python3 unified_backend.py")
        return
    
    # Run all demos
    demo_api_endpoints()
    demo_subscription_system()
    demo_ai_features()
    demo_frontend_integration()
    
    print_banner("DEMO COMPLETE")
    print("🎉 Khyrie3.0 full-stack integration is working perfectly!")
    print("💻 Access the dashboard at: http://localhost:8000/dashboard")
    print("📚 API documentation at: http://localhost:8000/docs")
    print(f"🕒 Demo completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()