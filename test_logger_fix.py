#!/usr/bin/env python3
"""
Test script to validate the logger fix in premium_ai_features.py
"""

import sys
import traceback

def test_logger_fix():
    """Test that the logger is properly configured"""
    print("🧪 Testing Premium AI Features Logger Fix...")
    
    try:
        # Test 1: Import the module
        print("1. Testing module import...")
        import premium_ai_features
        print("   ✅ Module imported successfully")
        
        # Test 2: Check logger exists
        print("2. Testing logger configuration...")
        if hasattr(premium_ai_features, 'logger'):
            print("   ✅ Logger found")
            
            # Test 3: Test logger functionality
            print("3. Testing logger functionality...")
            premium_ai_features.logger.info("Test log message")
            print("   ✅ Logger is functional")
        else:
            print("   ❌ Logger not found")
            return False
            
        # Test 4: Check premium_ai instance
        print("4. Testing premium_ai instance...")
        if hasattr(premium_ai_features, 'premium_ai'):
            print("   ✅ premium_ai instance found")
            print(f"   📊 Type: {type(premium_ai_features.premium_ai)}")
        else:
            print("   ❌ premium_ai instance not found")
            return False
            
        # Test 5: Test PremiumAIFeatures class
        print("5. Testing PremiumAIFeatures class...")
        ai_features = premium_ai_features.PremiumAIFeatures()
        print("   ✅ PremiumAIFeatures class instantiated successfully")
        
        # Test 6: Check available methods
        methods = [method for method in dir(ai_features) if not method.startswith('_')]
        print(f"   📋 Available methods: {len(methods)}")
        for method in methods[:3]:  # Show first 3 methods
            print(f"      - {method}")
        
        print("\n🎉 All tests passed! Logger fix is successful.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_logger_fix()
    sys.exit(0 if success else 1)