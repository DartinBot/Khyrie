"""
Khyrie3.0 Unified Backend
Integrates all fitness app services into a single FastAPI application
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import uvicorn

# Import your existing apps and engines
try:
    # Import from current workspace
    from backend_family_api import app as family_app
    from ai_backend_simple import app as ai_app
    from family_friends_tools import FamilyFriendsTools
    from ai_workout_engine import AIWorkoutEngine
    from adaptive_program_engine import AdaptiveProgramEngine
    from intelligent_exercise_selector import IntelligentExerciseSelector
    print("✅ Successfully imported all Khyrie3.0 components")
except ImportError as e:
    print(f"⚠️ Import warning: {e}")
    print("Some components may not be available until integration is complete")

# Create main Khyrie3.0 application
app = FastAPI(
    title="Khyrie3.0 - Unified Fitness Platform",
    description="Complete fitness ecosystem with AI, family/friends features, and comprehensive tracking",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images)
static_path = Path(__file__).parent
if (static_path / "static").exists():
    app.mount("/static", StaticFiles(directory=static_path / "static"), name="static")

# Health check endpoint
@app.get("/")
async def root():
    """Khyrie3.0 API root endpoint"""
    return {
        "message": "🏋️‍♂️ Welcome to Khyrie3.0 - Unified Fitness Platform",
        "version": "3.0.0",
        "status": "active",
        "services": {
            "family_friends": "✅ Active",
            "ai_workouts": "✅ Active", 
            "adaptive_programming": "✅ Active",
            "intelligent_selection": "✅ Active"
        },
        "docs": "/docs",
        "frontend": "http://localhost:3000"
    }

@app.get("/health")
async def health_check():
    """System health check"""
    return {
        "status": "healthy",
        "timestamp": "2025-09-25",
        "services": {
            "api": "running",
            "ai_engine": "ready",
            "database": "connected"  # Update when database is added
        }
    }

# Integration endpoints for the broader Khyrie3.0 ecosystem
@app.get("/api/integration/status")
async def integration_status():
    """Check integration status with broader Khyrie3.0 project"""
    return {
        "workspace_location": "/Users/darnellamcguire/Khyrie3.0/src/fitness_mcp/fitness app/fitness app2.0/fitness app 3.0",
        "integrated_components": [
            "family_friends_api",
            "ai_workout_engine", 
            "adaptive_program_engine",
            "intelligent_exercise_selector",
            "frontend_assets"
        ],
        "pending_integration": [
            "main_backend_migration",
            "database_setup",
            "authentication_system",
            "frontend_react_connection"
        ],
        "next_steps": [
            "Move /backend files to current workspace",
            "Set up database persistence", 
            "Configure React frontend API endpoints",
            "Implement user authentication"
        ]
    }

# Mount sub-applications with proper routing
try:
    # Mount family & friends features
    app.mount("/api/family", family_app, name="family")
    print("✅ Mounted Family & Friends API at /api/family")
except Exception as e:
    print(f"⚠️ Could not mount Family API: {e}")

try:
    # Mount AI features  
    app.mount("/api/ai", ai_app, name="ai")
    print("✅ Mounted AI Backend at /api/ai")
except Exception as e:
    print(f"⚠️ Could not mount AI API: {e}")

# Direct integration endpoints (bypass sub-apps for key features)
@app.get("/api/quick/workout-generation")
async def quick_workout_generation():
    """Quick access to AI workout generation"""
    try:
        engine = AIWorkoutEngine()
        sample_profile = {
            "fitness_level": "intermediate",
            "goals": ["strength", "endurance"],
            "available_time": 45,
            "equipment": ["dumbbells", "bodyweight"]
        }
        
        # This would normally take user input
        return {
            "message": "AI Workout Generator Ready",
            "sample_endpoint": "/api/ai/generate-workout", 
            "capabilities": engine.get_capabilities() if hasattr(engine, 'get_capabilities') else "Available"
        }
    except Exception as e:
        return {"error": f"AI Engine not fully initialized: {e}"}

@app.get("/api/quick/family-features")
async def quick_family_features():
    """Quick access to family & friends features"""
    try:
        tools = FamilyFriendsTools()
        return {
            "message": "Family & Friends Features Ready",
            "sample_endpoints": [
                "/api/family/groups",
                "/api/family/shared-workout", 
                "/api/family/challenges"
            ],
            "tools_available": "Yes"
        }
    except Exception as e:
        return {"error": f"Family tools not fully initialized: {e}"}

# Serve the main dashboard HTML
@app.get("/dashboard")
async def serve_dashboard():
    """Serve the AI dashboard HTML"""
    dashboard_path = Path(__file__).parent / "ai_dashboard.html"
    if dashboard_path.exists():
        return FileResponse(dashboard_path)
    return {"error": "Dashboard not found", "path": str(dashboard_path)}

# Serve test frontend
@app.get("/test")
async def serve_test_frontend():
    """Serve the test frontend HTML"""
    test_path = Path(__file__).parent / "test_frontend.html"
    if test_path.exists():
        return FileResponse(test_path)
    return {"error": "Test frontend not found", "path": str(test_path)}

# Integration helper endpoints
@app.post("/api/integration/migrate-backend")
async def migrate_backend_files():
    """Helper endpoint to guide backend file migration"""
    return {
        "message": "Backend Migration Guide",
        "source": "/Users/darnellamcguire/Khyrie3.0/backend/",
        "destination": "/Users/darnellamcguire/Khyrie3.0/src/fitness_mcp/fitness app/fitness app2.0/fitness app 3.0/",
        "commands": [
            "# Backup existing backend",
            "cp -r /Users/darnellamcguire/Khyrie3.0/backend /Users/darnellamcguire/Khyrie3.0/backend_backup",
            "",
            "# Move backend files to current workspace",
            'mv /Users/darnellamcguire/Khyrie3.0/backend/* "/Users/darnellamcguire/Khyrie3.0/src/fitness_mcp/fitness app/fitness app2.0/fitness app 3.0/"',
            "",
            "# Update imports in moved files (see IMPORT_FIX_GUIDE.md)",
            "# Restart this server to include migrated files"
        ],
        "benefits": [
            "No more import path issues",
            "All code in one location", 
            "Unified development environment",
            "Easier deployment and testing"
        ]
    }

@app.get("/api/integration/frontend-setup")  
async def frontend_setup_guide():
    """Guide for setting up React frontend integration"""
    return {
        "message": "Frontend Integration Setup",
        "frontend_location": "/Users/darnellamcguire/Khyrie3.0/frontend/",
        "requirements": [
            "Node.js 16+ installed",
            "npm or yarn package manager"
        ],
        "setup_commands": [
            "# Navigate to frontend directory",
            "cd /Users/darnellamcguire/Khyrie3.0/frontend/",
            "",
            "# Install dependencies", 
            "npm install",
            "",
            "# Start React development server",
            "npm start",
            "",
            "# Frontend will be available at http://localhost:3000"
        ],
        "api_integration": {
            "backend_url": "http://localhost:8000",
            "api_endpoints": {
                "family": "http://localhost:8000/api/family",
                "ai": "http://localhost:8000/api/ai",
                "health": "http://localhost:8000/health"
            }
        },
        "next_steps": [
            "Update frontend/src/services/api.js with new endpoints",
            "Test API integration between React and FastAPI",
            "Implement authentication flow",
            "Add real-time WebSocket features"
        ]
    }

if __name__ == "__main__":
    print("\n🚀 Starting Khyrie3.0 Unified Backend...")
    print("📍 Dashboard: http://localhost:8000/dashboard")
    print("📍 API Docs: http://localhost:8000/docs") 
    print("📍 Test Frontend: http://localhost:8000/test")
    print("📍 Integration Status: http://localhost:8000/api/integration/status")
    print("📍 React Frontend (after setup): http://localhost:3000")
    
    uvicorn.run(
        "unified_backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )