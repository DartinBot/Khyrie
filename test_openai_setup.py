#!/usr/bin/env python3
"""
OpenAI API Test Script for Khyrie3.0
Tests GPT-4 API integration and verifies configuration
"""

import openai
import os
import json
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

def test_openai_api():
    """Test OpenAI API key and integration."""
    
    print("🔍 Testing OpenAI API Configuration...")
    print("-" * 50)
    
    # Check if API key exists
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("💡 Make sure to add it to your .env file:")
        print("   OPENAI_API_KEY=sk-your-openai-key-here")
        return False
    
    # Validate API key format
    if not api_key.startswith("sk-"):
        print("❌ Invalid API key format")
        print("💡 OpenAI API keys should start with 'sk-'")
        return False
    
    if len(api_key) < 45:
        print("❌ API key appears to be incomplete")
        return False
    
    print(f"✅ API key format valid: {api_key[:15]}...")
    
    # Configure OpenAI
    openai.api_key = api_key
    
    # Test API call
    print("\n🧪 Testing API connection...")
    
    try:
        print("📡 Making API request to GPT-4...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a fitness instructor creating safe beginner workouts."
                },
                {
                    "role": "user", 
                    "content": "Create a simple 10-minute beginner workout routine with no equipment."
                }
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        workout = response.choices[0].message.content
        
        print("✅ API Test Successful!")
        print(f"📊 Response length: {len(workout)} characters")
        print(f"🔢 Tokens used: {response.usage.total_tokens}")
        print(f"💰 Estimated cost: ${response.usage.total_tokens * 0.00003:.4f}")
        print("\n📝 Sample GPT-4 Response:")
        print("-" * 30)
        print(workout[:300] + ("..." if len(workout) > 300 else ""))
        print("-" * 30)
        
        return True
        
    except openai.error.AuthenticationError:
        print("❌ Authentication failed - Invalid API key")
        print("💡 Check that your API key is correct and active")
        
    except openai.error.RateLimitError:
        print("❌ Rate limit exceeded")
        print("💡 Wait a moment and try again, or check your rate limits")
        
    except openai.error.InsufficientQuotaError:
        print("❌ Insufficient quota - Check your billing setup")
        print("💡 Add a payment method in your OpenAI account")
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        
    return False

def verify_environment_config():
    """Verify environment configuration is correct."""
    
    print("\n⚙️  Verifying Environment Configuration...")
    print("-" * 50)
    
    # Check for Anthropic key (should be removed)
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        print("⚠️  Found ANTHROPIC_API_KEY in environment")
        print("💡 You can remove it since you're now using OpenAI")
    else:
        print("✅ No conflicting Anthropic key found")
    
    # Check other required environment variables
    required_vars = [
        "OPENAI_API_KEY",
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
    
    print("🤖 OpenAI GPT-4 API Setup Verification")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: API Configuration
    if test_openai_api():
        tests_passed += 1
    
    # Test 2: Environment Configuration
    if verify_environment_config():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 60)
    print("🏁 Test Results Summary")
    print("-" * 30)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your OpenAI GPT-4 API is ready to use.")
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