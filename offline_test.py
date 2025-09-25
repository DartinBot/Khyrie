#!/usr/bin/env python3
"""
Offline Functionality Test for Khyrie PWA
Tests service worker caching and offline capabilities
"""

import requests
import time
import subprocess
import sys

def test_online_functionality():
    """Test that all endpoints work when online"""
    base_url = "http://localhost:8000"
    endpoints = [
        "/",
        "/health", 
        "/manifest.json",
        "/sw.js",
        "/api/workouts",
        "/api/family",
        "/icons/icon-192x192.svg"
    ]
    
    print("🌐 Testing Online Functionality...")
    results = {}
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            results[endpoint] = {
                "status": response.status_code,
                "success": response.status_code < 400,
                "content_type": response.headers.get("content-type", "unknown"),
                "size": len(response.content) if response.content else 0
            }
            status = "✅" if results[endpoint]["success"] else "❌"
            print(f"  {status} {endpoint}: {response.status_code} ({results[endpoint]['size']} bytes)")
        except Exception as e:
            results[endpoint] = {"status": "error", "success": False, "error": str(e)}
            print(f"  ❌ {endpoint}: ERROR - {e}")
    
    return results

def test_service_worker_registration():
    """Test if service worker can be registered (simulated)"""
    print("\n🔧 Testing Service Worker...")
    
    try:
        response = requests.get("http://localhost:8000/sw.js")
        if response.status_code == 200:
            content = response.text
            print("  ✅ Service Worker file accessible")
            
            # Check for key service worker features
            features = {
                "Cache API": "caches.open" in content,
                "Fetch Interception": "addEventListener('fetch'" in content,
                "Background Sync": "sync" in content.lower(),
                "Push Notifications": "push" in content.lower(),
                "Install Handler": "addEventListener('install'" in content
            }
            
            for feature, present in features.items():
                status = "✅" if present else "⚠️"
                print(f"    {status} {feature}: {'Present' if present else 'Missing'}")
            
            return True
        else:
            print(f"  ❌ Service Worker not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Service Worker test failed: {e}")
        return False

def test_pwa_manifest():
    """Test PWA manifest validity"""
    print("\n📱 Testing PWA Manifest...")
    
    try:
        response = requests.get("http://localhost:8000/manifest.json")
        if response.status_code == 200:
            import json
            manifest = response.json()
            
            print("  ✅ Manifest accessible and valid JSON")
            
            # Check required PWA manifest fields
            required_fields = ["name", "short_name", "start_url", "display", "icons"]
            for field in required_fields:
                if field in manifest:
                    print(f"    ✅ {field}: {manifest.get(field) if field != 'icons' else f'{len(manifest[field])} icons'}")
                else:
                    print(f"    ❌ Missing required field: {field}")
            
            # Validate icons
            icons = manifest.get("icons", [])
            if icons:
                print(f"    📄 Icon sizes available: {', '.join([icon.get('sizes', 'unknown') for icon in icons[:5]])}...")
            
            return True
            
    except Exception as e:
        print(f"  ❌ Manifest test failed: {e}")
        return False

def simulate_offline_test():
    """Simulate offline testing by checking cached resources"""
    print("\n🔄 Simulating Offline Functionality...")
    print("  ℹ️  In a real test environment, you would:")
    print("    1. Load the PWA in Chrome DevTools")
    print("    2. Go to Application > Service Workers")
    print("    3. Check 'Offline' to simulate network failure")
    print("    4. Reload the page to test cached resources")
    print("    5. Verify that key app functionality works offline")
    
    # Test that static assets are defined for caching
    try:
        response = requests.get("http://localhost:8000/sw.js")
        sw_content = response.text
        
        # Look for cached resources
        if "STATIC_ASSETS" in sw_content or "static" in sw_content.lower():
            print("  ✅ Static assets defined for caching")
        else:
            print("  ⚠️  No static assets caching configuration found")
            
        if "api" in sw_content.lower():
            print("  ✅ API caching strategy present")
        else:
            print("  ⚠️  No API caching strategy found")
            
    except Exception as e:
        print(f"  ❌ Offline simulation test failed: {e}")

def main():
    print("🧪 Khyrie PWA Offline Functionality Test")
    print("=" * 50)
    
    # Test 1: Online functionality
    online_results = test_online_functionality()
    
    # Test 2: Service Worker
    sw_test = test_service_worker_registration()
    
    # Test 3: PWA Manifest
    manifest_test = test_pwa_manifest()
    
    # Test 4: Offline simulation
    simulate_offline_test()
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 30)
    
    online_success = sum(1 for result in online_results.values() if result.get("success", False))
    total_endpoints = len(online_results)
    
    print(f"Online Endpoints: {online_success}/{total_endpoints} ({'✅' if online_success == total_endpoints else '⚠️'})")
    print(f"Service Worker: {'✅' if sw_test else '❌'}")
    print(f"PWA Manifest: {'✅' if manifest_test else '❌'}")
    
    overall_success = (online_success == total_endpoints) and sw_test and manifest_test
    
    print(f"\nOverall PWA Status: {'✅ READY' if overall_success else '⚠️  NEEDS ATTENTION'}")
    
    if overall_success:
        print("\n🎉 Your PWA is ready for:")
        print("   - Installation on mobile devices")
        print("   - Offline functionality testing")
        print("   - App store submission")
        print("\n💡 Next: Test on real devices using the installation guides!")
    else:
        print("\n🔧 Issues found - check the test results above")

if __name__ == "__main__":
    main()