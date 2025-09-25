#!/bin/bash

# Khyrie3.0 Integration Script
# Automates the integration of your fitness app with the broader Khyrie3.0 project

echo "🏋️‍♂️ Khyrie3.0 Integration Script"
echo "=================================="
echo

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project paths
KHYRIE_ROOT="/Users/darnellamcguire/Khyrie3.0"
CURRENT_WORKSPACE="$KHYRIE_ROOT/src/fitness_mcp/fitness app/fitness app2.0/fitness app 3.0"
BACKEND_DIR="$KHYRIE_ROOT/backend"
FRONTEND_DIR="$KHYRIE_ROOT/frontend"

echo -e "${BLUE}📍 Project Locations:${NC}"
echo "   Khyrie3.0 Root: $KHYRIE_ROOT"
echo "   Current Workspace: $CURRENT_WORKSPACE"
echo "   Backend Directory: $BACKEND_DIR" 
echo "   Frontend Directory: $FRONTEND_DIR"
echo

# Function to check if directory exists
check_directory() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅ Found: $1${NC}"
        return 0
    else
        echo -e "${RED}❌ Missing: $1${NC}"
        return 1
    fi
}

# Function to backup directory
backup_directory() {
    if [ -d "$1" ]; then
        backup_name="${1}_backup_$(date +%Y%m%d_%H%M%S)"
        echo -e "${YELLOW}💾 Backing up $1 to $backup_name${NC}"
        cp -r "$1" "$backup_name"
        echo -e "${GREEN}✅ Backup created: $backup_name${NC}"
    fi
}

# Step 1: Environment Check
echo -e "${BLUE}🔍 Step 1: Environment Check${NC}"
echo "----------------------------------------"

check_directory "$KHYRIE_ROOT"
check_directory "$CURRENT_WORKSPACE"

backend_exists=false
frontend_exists=false

if check_directory "$BACKEND_DIR"; then
    backend_exists=true
fi

if check_directory "$FRONTEND_DIR"; then
    frontend_exists=true
fi

# Check for Python
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✅ Python3 is installed${NC}"
    python3 --version
else
    echo -e "${RED}❌ Python3 is not installed${NC}"
fi

# Check for Node.js
if command -v node &> /dev/null; then
    echo -e "${GREEN}✅ Node.js is installed${NC}"
    node --version
    npm --version
else
    echo -e "${YELLOW}⚠️ Node.js is not installed (needed for React frontend)${NC}"
    echo "   Install with: brew install node"
fi

echo

# Step 2: Backend Integration
echo -e "${BLUE}🔧 Step 2: Backend Integration${NC}"
echo "----------------------------------------"

if [ "$backend_exists" = true ]; then
    echo -e "${YELLOW}Found existing backend directory${NC}"
    
    # Ask user if they want to integrate
    read -p "Do you want to move backend files to current workspace? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Create backup
        backup_directory "$BACKEND_DIR"
        
        # Move backend files
        echo -e "${YELLOW}📦 Moving backend files to workspace...${NC}"
        
        # Create a list of files to move
        for file in "$BACKEND_DIR"/*; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                destination="$CURRENT_WORKSPACE/$filename"
                
                # Check if file already exists in workspace
                if [ -f "$destination" ]; then
                    echo -e "${YELLOW}⚠️ File $filename already exists in workspace${NC}"
                    read -p "Overwrite $filename? (y/n): " -n 1 -r
                    echo
                    if [[ $REPLY =~ ^[Yy]$ ]]; then
                        cp "$file" "$destination"
                        echo -e "${GREEN}✅ Updated: $filename${NC}"
                    else
                        echo -e "${BLUE}⏭️ Skipped: $filename${NC}"
                    fi
                else
                    cp "$file" "$destination"
                    echo -e "${GREEN}✅ Moved: $filename${NC}"
                fi
            fi
        done
        
        echo -e "${GREEN}✅ Backend integration completed!${NC}"
    else
        echo -e "${BLUE}⏭️ Skipping backend integration${NC}"
    fi
else
    echo -e "${BLUE}ℹ️ No existing backend directory found${NC}"
fi

echo

# Step 3: Install Dependencies
echo -e "${BLUE}📦 Step 3: Install Dependencies${NC}"
echo "----------------------------------------"

# Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
cd "$CURRENT_WORKSPACE"

if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️ No requirements.txt found, installing basic dependencies...${NC}"
    pip3 install fastapi uvicorn numpy
fi

# Node.js dependencies (if frontend exists)
if [ "$frontend_exists" = true ] && command -v npm &> /dev/null; then
    echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
    cd "$FRONTEND_DIR"
    npm install
    echo -e "${GREEN}✅ Node.js dependencies installed${NC}"
    cd "$CURRENT_WORKSPACE"
elif [ "$frontend_exists" = true ]; then
    echo -e "${YELLOW}⚠️ Frontend found but Node.js not installed${NC}"
    echo "   Install Node.js to set up React frontend"
else
    echo -e "${BLUE}ℹ️ No frontend directory found${NC}"
fi

echo

# Step 4: Test Integration
echo -e "${BLUE}🧪 Step 4: Test Integration${NC}"
echo "----------------------------------------"

echo -e "${YELLOW}Testing unified backend...${NC}"

# Check if unified_backend.py exists
if [ -f "unified_backend.py" ]; then
    echo -e "${GREEN}✅ Unified backend file found${NC}"
    
    # Test import
    if python3 -c "import unified_backend" 2>/dev/null; then
        echo -e "${GREEN}✅ Backend imports successful${NC}"
    else
        echo -e "${YELLOW}⚠️ Some imports may need fixing${NC}"
        echo "   See IMPORT_FIX_GUIDE.md for solutions"
    fi
else
    echo -e "${RED}❌ unified_backend.py not found${NC}"
fi

echo

# Step 5: Setup Instructions
echo -e "${BLUE}🚀 Step 5: Next Steps${NC}"
echo "----------------------------------------"

echo -e "${GREEN}Integration setup completed!${NC}"
echo
echo -e "${BLUE}To start your Khyrie3.0 application:${NC}"
echo
echo "1. Start the unified backend:"
echo -e "   ${YELLOW}cd '$CURRENT_WORKSPACE'${NC}"
echo -e "   ${YELLOW}python3 unified_backend.py${NC}"
echo
echo "2. Access your application:"
echo -e "   ${YELLOW}Dashboard: http://localhost:8000/dashboard${NC}"
echo -e "   ${YELLOW}API Docs: http://localhost:8000/docs${NC}"
echo -e "   ${YELLOW}Integration Status: http://localhost:8000/api/integration/status${NC}"
echo

if [ "$frontend_exists" = true ] && command -v npm &> /dev/null; then
    echo "3. Start the React frontend (in new terminal):"
    echo -e "   ${YELLOW}cd '$FRONTEND_DIR'${NC}"
    echo -e "   ${YELLOW}npm start${NC}"
    echo -e "   ${YELLOW}Frontend: http://localhost:3000${NC}"
    echo
fi

echo -e "${BLUE}📚 Additional Resources:${NC}"
echo "   • KHYRIE_INTEGRATION_STRATEGY.md - Complete integration guide"
echo "   • IMPORT_FIX_GUIDE.md - Fix any remaining import issues"
echo "   • README.md - Project documentation"
echo

echo -e "${GREEN}🎉 Welcome to Khyrie3.0 - Your unified fitness platform is ready!${NC}"