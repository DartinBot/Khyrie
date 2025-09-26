#!/usr/bin/env python3
"""
TogetherFit Brand Availability Research Tool
Comprehensive check for domain, social media, app store, and trademark availability
"""

import requests
import json
import time
from datetime import datetime

def print_banner(title):
    """Print a formatted banner"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def check_domain_availability():
    """Check domain availability for TogetherFit"""
    print_banner("DOMAIN AVAILABILITY RESEARCH")
    
    domains_to_check = [
        "togetherfit.com",
        "togetherfit.app", 
        "togetherfit.io",
        "togetherfit.net",
        "togetherfit.org",
        "together-fit.com",
        "togetherfitness.com"
    ]
    
    print("🌐 Checking Domain Availability:")
    
    for domain in domains_to_check:
        try:
            # Using a simple HTTP request to check if domain resolves
            response = requests.get(f"http://{domain}", timeout=5)
            status = f"❌ TAKEN (Status: {response.status_code})"
        except requests.exceptions.ConnectionError:
            status = "✅ POTENTIALLY AVAILABLE (No response)"
        except requests.exceptions.Timeout:
            status = "⚠️  TIMEOUT (May be available)"
        except Exception as e:
            status = f"❓ UNKNOWN ({str(e)[:30]}...)"
        
        print(f"   • {domain:<25} - {status}")

def check_social_media_handles():
    """Check social media handle availability"""
    print_banner("SOCIAL MEDIA HANDLE RESEARCH")
    
    handles = [
        "@TogetherFit",
        "@Together_Fit", 
        "@TogetherFitApp",
        "@TogetherFitness"
    ]
    
    platforms = {
        "Instagram": "https://www.instagram.com/",
        "Twitter/X": "https://twitter.com/", 
        "TikTok": "https://www.tiktok.com/@",
        "YouTube": "https://www.youtube.com/@",
        "Facebook": "https://www.facebook.com/"
    }
    
    print("📱 Social Media Handle Research:")
    print("   (Note: Manual verification recommended)")
    
    for handle in handles:
        print(f"\n   Handle: {handle}")
        for platform, base_url in platforms.items():
            clean_handle = handle.replace("@", "")
            full_url = f"{base_url}{clean_handle}"
            print(f"      {platform:<12} - {full_url}")

def check_app_store_availability():
    """Research app store name conflicts"""
    print_banner("APP STORE RESEARCH")
    
    print("📱 App Store Name Conflict Check:")
    print("   Search terms to manually verify:")
    
    search_terms = [
        "TogetherFit",
        "Together Fit", 
        "Together Fitness",
        "Family Fitness Together"
    ]
    
    app_stores = {
        "iOS App Store": "https://apps.apple.com/search?term=",
        "Google Play": "https://play.google.com/store/search?q=",
        "Microsoft Store": "https://www.microsoft.com/en-us/search/shop/apps?q="
    }
    
    for term in search_terms:
        print(f"\n   📋 Search Term: '{term}'")
        for store, base_url in app_stores.items():
            search_url = base_url + term.replace(" ", "%20")
            print(f"      {store:<18} - {search_url}")

def check_trademark_resources():
    """Provide trademark research resources"""
    print_banner("TRADEMARK RESEARCH RESOURCES")
    
    print("⚖️  Trademark Databases to Check:")
    
    trademark_resources = {
        "USPTO (US)": "https://www.uspto.gov/trademarks/search",
        "EUIPO (EU)": "https://euipo.europa.eu/eSearch/",
        "WIPO Global": "https://www.wipo.int/branddb/en/",
        "Trademarkia": "https://www.trademarkia.com/",
        "TMView": "https://www.tmdn.org/tmview/"
    }
    
    for resource, url in trademark_resources.items():
        print(f"   • {resource:<15} - {url}")
    
    print(f"\n   🔍 Search Terms to Use:")
    search_terms = [
        "TogetherFit",
        "Together Fit", 
        "TOGETHERFIT",
        "Together Fitness"
    ]
    
    for term in search_terms:
        print(f"      • '{term}'")
    
    print(f"\n   📋 Trademark Classes to Check:")
    relevant_classes = [
        "Class 09: Mobile apps, software",
        "Class 35: Business services, advertising", 
        "Class 41: Education, fitness training",
        "Class 42: Software services, SaaS",
        "Class 44: Medical, health services"
    ]
    
    for tm_class in relevant_classes:
        print(f"      • {tm_class}")

def generate_availability_report():
    """Generate comprehensive availability report"""
    print_banner("TOGETHERFIT BRAND AVAILABILITY REPORT")
    
    report_data = {
        "brand_name": "TogetherFit",
        "research_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "status": "Research Required",
        "priority_actions": [
            "1. Manual domain check via registrar (GoDaddy, Namecheap)",
            "2. Social media handle verification",
            "3. App store search for conflicts", 
            "4. USPTO trademark database search",
            "5. Google search for existing businesses"
        ],
        "risk_assessment": {
            "domain_risk": "Medium - Common fitness terminology",
            "trademark_risk": "Medium - Need professional search",
            "social_risk": "Low - Can use variations if needed",
            "app_store_risk": "Medium - Popular fitness term"
        }
    }
    
    print("📊 Research Summary:")
    print(f"   Brand Name: {report_data['brand_name']}")
    print(f"   Research Date: {report_data['research_date']}")
    
    print(f"\n   🎯 Priority Actions:")
    for action in report_data['priority_actions']:
        print(f"      {action}")
    
    print(f"\n   ⚠️  Risk Assessment:")
    for risk_type, risk_level in report_data['risk_assessment'].items():
        print(f"      {risk_type.replace('_', ' ').title():<18} - {risk_level}")
    
    # Save report to file
    with open('togetherfit_availability_research.json', 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n   💾 Detailed report saved to: togetherfit_availability_research.json")

def professional_recommendations():
    """Provide professional recommendations"""
    print_banner("PROFESSIONAL RECOMMENDATIONS")
    
    print("💡 Next Steps for TogetherFit Brand Research:")
    
    recommendations = [
        {
            "step": "1. Domain Registration Check",
            "action": "Use GoDaddy, Namecheap, or Google Domains to check availability",
            "cost": "$10-15/year per domain",
            "priority": "HIGH"
        },
        {
            "step": "2. Trademark Professional Search", 
            "action": "Hire trademark attorney or use LegalZoom for comprehensive search",
            "cost": "$300-800 for professional search",
            "priority": "HIGH"
        },
        {
            "step": "3. Social Media Handle Audit",
            "action": "Manually check all major platforms, consider variations",
            "cost": "Free (time investment)",
            "priority": "MEDIUM"
        },
        {
            "step": "4. Competitive Analysis",
            "action": "Google search, fitness industry research for existing 'TogetherFit' brands",
            "cost": "Free (time investment)", 
            "priority": "MEDIUM"
        },
        {
            "step": "5. Backup Name Strategy",
            "action": "Prepare 2-3 alternative names in case TogetherFit is unavailable",
            "cost": "Free (creative time)",
            "priority": "LOW"
        }
    ]
    
    for rec in recommendations:
        print(f"\n   📋 {rec['step']}")
        print(f"      Action: {rec['action']}")
        print(f"      Cost: {rec['cost']}")
        print(f"      Priority: {rec['priority']}")

def main():
    """Run complete TogetherFit availability research"""
    print_banner("TOGETHERFIT BRAND AVAILABILITY RESEARCH")
    print(f"🕒 Research started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target Brand: 'TogetherFit'")
    print(f"🔍 Research Scope: Domains, Social Media, App Stores, Trademarks")
    
    # Run all research functions
    check_domain_availability()
    check_social_media_handles() 
    check_app_store_availability()
    check_trademark_resources()
    generate_availability_report()
    professional_recommendations()
    
    print_banner("RESEARCH COMPLETE")
    print("🎉 TogetherFit brand research completed!")
    print("💡 Review the results above and take recommended actions")
    print("⚠️  Remember: This is preliminary research - professional verification recommended")
    print(f"🕒 Research completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()