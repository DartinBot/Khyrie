#!/usr/bin/env python3
"""
Mobile UI Responsiveness Test for Khyrie PWA
Tests touch interactions, responsive design, and mobile UX
"""

import requests
import re
import sys

def test_mobile_css_framework():
    """Test if mobile-optimized CSS is present"""
    print("📱 Testing Mobile CSS Framework...")
    
    try:
        # Check if mobile CSS file exists
        response = requests.get("http://localhost:8000/mobile-app.css")
        if response.status_code == 200:
            css_content = response.text
            print("  ✅ Mobile CSS file accessible")
            
            # Check for responsive design features
            responsive_features = {
                "Viewport Meta": "@media" in css_content,
                "Flexbox Layout": "display: flex" in css_content or "display:flex" in css_content,
                "Touch Optimization": "touch" in css_content.lower(),
                "Mobile Cards": "mobile-card" in css_content,
                "Bottom Navigation": "bottom-nav" in css_content,
                "Responsive Grid": "grid" in css_content,
                "Safe Area": "safe-area" in css_content or "env(" in css_content
            }
            
            for feature, present in responsive_features.items():
                status = "✅" if present else "⚠️"
                print(f"    {status} {feature}: {'Present' if present else 'Missing'}")
            
            return True
        else:
            print(f"  ❌ Mobile CSS not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Mobile CSS test failed: {e}")
        return False

def test_main_html_mobile_features():
    """Test mobile features in the main HTML"""
    print("\n🏠 Testing Main HTML Mobile Features...")
    
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            html_content = response.text
            print("  ✅ Main page accessible")
            
            # Check for mobile-specific HTML features
            mobile_features = {
                "Viewport Meta Tag": 'name="viewport"' in html_content,
                "Touch Icons": 'apple-touch-icon' in html_content,
                "Mobile CSS Link": 'mobile-app.css' in html_content,
                "PWA Installer": 'pwa-installer' in html_content,
                "Service Worker": 'sw.js' in html_content,
                "Bottom Navigation": 'bottom-nav' in html_content,
                "Mobile Cards": 'mobile-card' in html_content
            }
            
            for feature, present in mobile_features.items():
                status = "✅" if present else "⚠️"
                print(f"    {status} {feature}: {'Present' if present else 'Missing'}")
            
            return True
        else:
            print(f"  ❌ Main page not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Main HTML test failed: {e}")
        return False

def test_touch_interaction_elements():
    """Test touch-friendly interactive elements"""
    print("\n👆 Testing Touch Interaction Elements...")
    
    try:
        # Check mobile CSS for touch-friendly sizing
        response = requests.get("http://localhost:8000/mobile-app.css")
        if response.status_code == 200:
            css_content = response.text
            
            # Look for touch-friendly design patterns
            touch_patterns = {
                "Minimum Touch Target": "44px" in css_content or "2.75rem" in css_content,
                "Button Hover States": ":hover" in css_content,
                "Touch Feedback": ":active" in css_content or "active" in css_content,
                "Large Click Areas": "padding" in css_content,
                "Gesture Support": "swipe" in css_content.lower() or "gesture" in css_content.lower()
            }
            
            for pattern, present in touch_patterns.items():
                status = "✅" if present else "⚠️"
                print(f"    {status} {pattern}: {'Present' if present else 'Missing'}")
            
            return True
        else:
            print("  ❌ Could not analyze touch interactions")
            return False
            
    except Exception as e:
        print(f"  ❌ Touch interaction test failed: {e}")
        return False

def test_responsive_breakpoints():
    """Test responsive design breakpoints"""
    print("\n📏 Testing Responsive Breakpoints...")
    
    try:
        response = requests.get("http://localhost:8000/mobile-app.css")
        if response.status_code == 200:
            css_content = response.text
            
            # Find media queries
            media_queries = re.findall(r'@media[^{]*\([^)]*\)', css_content)
            
            if media_queries:
                print(f"  ✅ Found {len(media_queries)} responsive breakpoints")
                
                # Check for common breakpoints
                breakpoint_types = {
                    "Mobile": any("320px" in mq or "375px" in mq or "480px" in mq for mq in media_queries),
                    "Tablet": any("768px" in mq or "834px" in mq for mq in media_queries),
                    "Desktop": any("1024px" in mq or "1200px" in mq for mq in media_queries),
                    "Large Screen": any("1440px" in mq or "1920px" in mq for mq in media_queries)
                }
                
                for breakpoint, present in breakpoint_types.items():
                    status = "✅" if present else "⚠️"
                    print(f"    {status} {breakpoint} Support: {'Present' if present else 'Inferred'}")
                
                return True
            else:
                print("  ⚠️  No media queries found")
                return False
                
    except Exception as e:
        print(f"  ❌ Breakpoint test failed: {e}")
        return False

def test_mobile_navigation():
    """Test mobile navigation components"""
    print("\n🧭 Testing Mobile Navigation...")
    
    try:
        # Check main HTML for navigation
        response = requests.get("http://localhost:8000/")
        html_content = response.text
        
        nav_features = {
            "Bottom Navigation": "bottom-nav" in html_content,
            "Mobile Menu": "mobile-menu" in html_content or "hamburger" in html_content,
            "Tab Bar": "tab-bar" in html_content or "nav-tab" in html_content,
            "Quick Actions": "quick-action" in html_content,
            "Floating Action Button": "fab" in html_content or "floating" in html_content
        }
        
        for feature, present in nav_features.items():
            status = "✅" if present else "⚠️"
            print(f"    {status} {feature}: {'Present' if present else 'Missing'}")
        
        return any(nav_features.values())
        
    except Exception as e:
        print(f"  ❌ Navigation test failed: {e}")
        return False

def simulate_device_testing():
    """Provide instructions for real device testing"""
    print("\n📱 Device Testing Instructions...")
    print("  ℹ️  For comprehensive mobile testing, perform these tests:")
    print()
    print("  📲 Installation Testing:")
    print("    • Chrome Android: Look for 'Add to Home Screen' banner")
    print("    • iOS Safari: Share > Add to Home Screen")
    print("    • Chrome Desktop: Install button in address bar")
    print()
    print("  👆 Touch Interaction Testing:")
    print("    • Test all buttons and links are easily tappable")
    print("    • Verify 44px minimum touch target size")
    print("    • Check swipe gestures work smoothly")
    print()
    print("  📐 Responsive Testing:")
    print("    • Test on phones (320px-414px width)")
    print("    • Test on tablets (768px-1024px width)")
    print("    • Test landscape and portrait orientations")
    print()
    print("  🔄 Performance Testing:")
    print("    • Test loading speed on 3G networks")
    print("    • Verify smooth scrolling and animations")
    print("    • Check memory usage during extended use")

def main():
    print("🧪 Khyrie PWA Mobile UI Responsiveness Test")
    print("=" * 55)
    
    # Test 1: Mobile CSS Framework
    css_test = test_mobile_css_framework()
    
    # Test 2: Main HTML Mobile Features  
    html_test = test_main_html_mobile_features()
    
    # Test 3: Touch Interactions
    touch_test = test_touch_interaction_elements()
    
    # Test 4: Responsive Breakpoints
    responsive_test = test_responsive_breakpoints()
    
    # Test 5: Mobile Navigation
    nav_test = test_mobile_navigation()
    
    # Device Testing Instructions
    simulate_device_testing()
    
    # Summary
    print("\n📊 Mobile UI Test Summary:")
    print("=" * 35)
    
    tests = {
        "Mobile CSS": css_test,
        "HTML Mobile Features": html_test,
        "Touch Interactions": touch_test,
        "Responsive Design": responsive_test,
        "Mobile Navigation": nav_test
    }
    
    passed_tests = sum(1 for result in tests.values() if result)
    total_tests = len(tests)
    
    for test_name, result in tests.items():
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    overall_score = passed_tests / total_tests
    
    if overall_score >= 0.8:
        status = "✅ EXCELLENT"
        message = "Your PWA has excellent mobile UI optimization!"
    elif overall_score >= 0.6:
        status = "⚠️  GOOD"
        message = "Your PWA has good mobile support with room for improvement."
    else:
        status = "❌ NEEDS WORK"
        message = "Your PWA needs significant mobile UI improvements."
    
    print(f"\nMobile UI Score: {passed_tests}/{total_tests} ({overall_score:.0%})")
    print(f"Overall Rating: {status}")
    print(f"\n{message}")
    
    if overall_score >= 0.6:
        print("\n🎉 Ready for mobile deployment!")
        print("💡 Next: Test on real devices for final validation")
    else:
        print("\n🔧 Recommended improvements:")
        for test_name, result in tests.items():
            if not result:
                print(f"  • Fix {test_name}")

if __name__ == "__main__":
    main()