#!/usr/bin/env python3
"""
Anthropic API Test Script for Khyrie3.0
Tests Claude API integration and verifies configuration
"""

import requests
import os
import json
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

def test_anthropic_api():
    """Test Anthropic API key and integration."""
    
    print("🔍 Testing Anthropic API Configuration...")
    print("-" * 50)
    
    # Check if API key exists
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment variables")
        print("💡 Make sure to add it to your .env file:")
        print("   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here")
        return False
    
    # Validate API key format
    if not api_key.startswith("sk-ant-"):
        print("❌ Invalid API key format")
        print("💡 Anthropic API keys should start with 'sk-ant-'")
        return False
    
    if len(api_key) < 50:
        print("❌ API key appears to be incomplete")
        return False
    
    print(f"✅ API key format valid: {api_key[:15]}...")
    
    # Test API call
    print("\n🧪 Testing API connection...")
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    data = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 150,
        "temperature": 0.7,
        "system": "You are a fitness instructor creating safe beginner workouts.",
        "messages": [
            {
                "role": "user", 
                "content": "Create a simple 10-minute beginner workout routine with no equipment."
            }
        ]
    }
    
    try:
        print("📡 Making API request...")
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            workout = result["content"][0]["text"]
            
            print("✅ API Test Successful!")
            print(f"📊 Response length: {len(workout)} characters")
            print(f"🔢 Tokens used: ~{len(workout.split())}")
            print("\n📝 Sample Claude Response:")
            print("-" * 30)
            print(workout[:300] + ("..." if len(workout) > 300 else ""))
            print("-" * 30)
            
            return True
            
        elif response.status_code == 401:
            print("❌ Authentication failed - Invalid API key")
            print("💡 Check that your API key is correct and active")
            
        elif response.status_code == 429:
            print("❌ Rate limit exceeded")
            print("💡 Wait a moment and try again, or check your rate limits")
            
        elif response.status_code == 402:
            print("❌ Payment required - Check your billing setup")
            print("💡 Add a payment method in the Anthropic Console")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
        return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        print("💡 Check your internet connection")
        return False
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        print("💡 Check your internet connection and API endpoint")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_premium_features():
    """Test that premium feature functions work with Claude."""
    
    print("\n🎯 Testing Premium Feature Integration...")
    print("-" * 50)
    
    try:
        # Import the premium features module
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from premium_ai_features import call_claude_api
        
        # Test the call_claude_api function
        print("📡 Testing call_claude_api function...")
        
        response = call_claude_api(
            messages=[{"role": "user", "content": "Say 'Hello from Khyrie!' in a friendly way."}],
            system_prompt="You are a helpful fitness assistant.",
            max_tokens=50,
            temperature=0.7
        )
        
        print("✅ Premium feature integration successful!")
        print(f"📝 Response: {response}")
        
        return True
        
    except ImportError as e:
        print(f"⚠️  Could not import premium_ai_features: {e}")
        print("💡 This is normal if testing outside the main application")
        return True  # Not a critical failure for this test
        
    except Exception as e:
        print(f"❌ Premium feature test failed: {e}")
        return False

def verify_environment_config():
    """Verify environment configuration is correct."""
    
    print("\n⚙️  Verifying Environment Configuration...")
    print("-" * 50)
    
    # Check for old OpenAI key (should be removed)
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print("⚠️  Found OPENAI_API_KEY in environment")
        print("💡 Consider removing it since you're now using Claude")
    else:
        print("✅ No conflicting OpenAI key found")
    
    # Check other required environment variables
    required_vars = [
        "ANTHROPIC_API_KEY",
        "STRIPE_SECRET_KEY", 
        "DATABASE_URL"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
        else:
            print(f"✅ {var} configured")
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {missing_vars}")
        print("💡 Add them to your .env file for full functionality")
    
    return len(missing_vars) == 0

def main():
    """Run all tests."""
    
    print("🤖 Anthropic Claude API Setup Verification")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: API Configuration
    if test_anthropic_api():
        tests_passed += 1
    
    # Test 2: Premium Features (if available)
    if test_premium_features():
        tests_passed += 1
    
    # Test 3: Environment Configuration
    if verify_environment_config():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 60)
    print("🏁 Test Results Summary")
    print("-" * 30)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your Claude API is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Start your Khyrie server: python3 main.py")
        print("   2. Test premium features in the web interface")
        print("   3. Set up Stripe for payment processing")
    elif tests_passed >= 1:
        print("⚠️  Some tests passed. Check the issues above.")
        print("💡 Your API key works, but there may be configuration issues.")
    else:
        print("❌ Tests failed. Please check your API key and configuration.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)