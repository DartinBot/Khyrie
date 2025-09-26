#!/usr/bin/env python3
"""
Khyrie3.0 Integration Assessment
Analyzes what components are integrated vs what's missing
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional

def check_file_exists(path: str) -> Dict:
    """Check if a file exists and get its size"""
    file_path = Path(path)
    if file_path.exists():
        return {
            "exists": True,
            "size": file_path.stat().st_size,
            "modified": file_path.stat().st_mtime
        }
    return {"exists": False}

def analyze_integration_status() -> Dict:
    """Analyze what Khyrie3.0 components are integrated"""
    
    workspace = Path.cwd()
    print(f"📍 Analyzing workspace: {workspace}")
    
    # Core backend components
    backend_components = {
        "unified_backend.py": "Main unified backend server",
        "backend_family_api.py": "Family & Friends API",
        "ai_backend_simple.py": "Simple AI backend",
        "comprehensive_fitness_api.py": "Comprehensive API",
        "subscription_api.py": "Subscription management API"
    }
    
    # AI & ML components
    ai_components = {
        "ai_workout_engine.py": "AI workout generation engine",
        "adaptive_program_engine.py": "Adaptive program engine", 
        "intelligent_exercise_selector.py": "Smart exercise selection",
        "premium_ai_features.py": "Premium AI features"
    }
    
    # Database components
    database_components = {
        "database_models.py": "Core database models",
        "subscription_models.py": "Subscription database models",
        "comprehensive_fitness_models.py": "Comprehensive fitness models",
        "main_database.py": "Main database integration"
    }
    
    # Frontend components
    frontend_components = {
        "dashboard.html": "Main dashboard interface",
        "ai_dashboard.html": "AI dashboard interface",
        "subscription_test.html": "Subscription test interface",
        "mobile.html": "Mobile interface",
        "enhanced_group_workouts.html": "Group workouts interface"
    }
    
    # Integration & utility components
    integration_components = {
        "integration_utility.py": "Integration testing utility",
        "stripe_integration.py": "Payment processing",
        "khyrie_integration.sh": "Integration shell script"
    }
    
    # Configuration files
    config_components = {
        "requirements.txt": "Python dependencies",
        "package.json": "Node.js/frontend dependencies", 
        "manifest.json": "PWA manifest",
        ".env.example": "Environment configuration template",
        "vercel.json": "Vercel deployment config"
    }
    
    results = {
        "workspace": str(workspace),
        "analysis": {
            "backend_components": {},
            "ai_components": {},
            "database_components": {},
            "frontend_components": {},
            "integration_components": {},
            "config_components": {}
        },
        "summary": {
            "total_files": 0,
            "existing_files": 0,
            "missing_files": 0
        }
    }
    
    # Check each category
    categories = [
        ("backend_components", backend_components),
        ("ai_components", ai_components), 
        ("database_components", database_components),
        ("frontend_components", frontend_components),
        ("integration_components", integration_components),
        ("config_components", config_components)
    ]
    
    for category_name, components in categories:
        print(f"\n🔍 Checking {category_name.replace('_', ' ').title()}...")
        
        for filename, description in components.items():
            file_info = check_file_exists(filename)
            results["analysis"][category_name][filename] = {
                "description": description,
                "status": file_info
            }
            
            results["summary"]["total_files"] += 1
            if file_info["exists"]:
                results["summary"]["existing_files"] += 1
                print(f"  ✅ {filename} - {description}")
            else:
                results["summary"]["missing_files"] += 1
                print(f"  ❌ {filename} - {description} [MISSING]")
    
    # Check for additional important files
    print(f"\n🔍 Checking Additional Components...")
    additional_files = list(workspace.glob("*.py")) + list(workspace.glob("*.html")) + list(workspace.glob("*.js"))
    additional_count = len([f for f in additional_files if f.is_file()])
    print(f"  📄 Total Python files: {len(list(workspace.glob('*.py')))}")
    print(f"  📄 Total HTML files: {len(list(workspace.glob('*.html')))}")
    print(f"  📄 Total JS files: {len(list(workspace.glob('*.js')))}")
    print(f"  📄 Total CSS files: {len(list(workspace.glob('*.css')))}")
    
    # Calculate completion percentage
    completion_percentage = (results["summary"]["existing_files"] / results["summary"]["total_files"]) * 100
    results["summary"]["completion_percentage"] = completion_percentage
    
    return results

def generate_integration_report(results: Dict):
    """Generate a detailed integration report"""
    
    print(f"\n" + "="*60)
    print(f"📊 KHYRIE3.0 INTEGRATION STATUS REPORT")
    print(f"="*60)
    
    print(f"\n📍 Workspace: {results['workspace']}")
    print(f"📈 Integration Completion: {results['summary']['completion_percentage']:.1f}%")
    print(f"✅ Files Present: {results['summary']['existing_files']}")
    print(f"❌ Files Missing: {results['summary']['missing_files']}")
    print(f"📊 Total Tracked: {results['summary']['total_files']}")
    
    # Detailed breakdown by category
    for category_name, components in results["analysis"].items():
        category_title = category_name.replace('_', ' ').title()
        existing = sum(1 for comp in components.values() if comp["status"]["exists"])
        total = len(components)
        
        print(f"\n🔧 {category_title}: {existing}/{total} ({existing/total*100:.0f}%)")
        
        for filename, info in components.items():
            status = "✅" if info["status"]["exists"] else "❌"
            size_info = f" ({info['status']['size']} bytes)" if info["status"]["exists"] else ""
            print(f"   {status} {filename}{size_info}")
    
    # Missing components summary
    missing_components = []
    for category_name, components in results["analysis"].items():
        for filename, info in components.items():
            if not info["status"]["exists"]:
                missing_components.append(f"{filename} ({info['description']})")
    
    if missing_components:
        print(f"\n❌ MISSING COMPONENTS ({len(missing_components)}):")
        for component in missing_components:
            print(f"   • {component}")
    else:
        print(f"\n🎉 ALL TRACKED COMPONENTS ARE PRESENT!")
    
    # Integration recommendations
    print(f"\n🚀 INTEGRATION RECOMMENDATIONS:")
    
    if results["summary"]["completion_percentage"] >= 90:
        print("   ✅ Integration is nearly complete!")
        print("   🔧 Focus on fixing import errors and testing")
        print("   🚀 Ready for production deployment")
    elif results["summary"]["completion_percentage"] >= 70:
        print("   📈 Good integration progress")
        print("   🔧 Install missing dependencies (numpy, etc.)")
        print("   🔗 Fix remaining import issues")
    else:
        print("   ⚠️  Significant components missing")
        print("   📥 Need to move additional files from broader Khyrie3.0 project")
        print("   🔧 Run khyrie_integration.sh for automated integration")

def main():
    """Main integration assessment function"""
    print("🏋️‍♀️ Khyrie3.0 Integration Assessment")
    print("="*40)
    
    results = analyze_integration_status()
    generate_integration_report(results)
    
    # Save results
    output_file = "khyrie_integration_assessment.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Assessment saved to: {output_file}")
    print(f"🔍 For detailed integration help, see: KHYRIE_INTEGRATION_STRATEGY.md")

if __name__ == "__main__":
    main()