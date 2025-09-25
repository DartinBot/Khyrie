#!/bin/bash

# 🚀 Khyrie3.0 Production Deployment Script
# Copyright (C) 2025 Darnell Roy

set -e  # Exit on any error

echo "🚀 Starting Khyrie3.0 Production Deployment..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Step 1: Verify Prerequisites
print_step "Checking prerequisites..."

if ! command -v git &> /dev/null; then
    print_error "Git is not installed"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    print_error "Python3 is not installed"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    print_warning "npm is not installed - you'll need it for Vercel CLI"
fi

print_success "Prerequisites check completed"

# Step 2: Test Application Locally
print_step "Testing application locally..."

# Compile Python files
python3 -m py_compile main.py
if [ $? -eq 0 ]; then
    print_success "Python syntax validation passed"
else
    print_error "Python syntax errors found"
    exit 1
fi

# Step 3: Prepare Production Files
print_step "Preparing production configuration..."

# Check if required files exist
required_files=("vercel.json" ".env.production" "requirements.txt" "manifest.json" "sw.js")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "$file exists"
    else
        print_error "$file is missing"
        exit 1
    fi
done

# Step 4: Git Operations
print_step "Preparing Git repository..."

# Add all production files
git add .
git status

# Check if there are changes to commit
if git diff --staged --quiet; then
    print_warning "No changes to commit"
else
    print_step "Committing production deployment files..."
    git commit -m "🚀 Production deployment configuration

    - Add Vercel deployment configuration
    - Update FastAPI for production environment
    - Add security headers and logging
    - Configure environment variables
    - Add health check endpoint"
    
    print_success "Changes committed successfully"
fi

# Step 5: Push to GitHub
print_step "Pushing to GitHub repository..."
git push origin master
print_success "Code pushed to GitHub successfully"

# Step 6: Deployment Instructions
print_step "Deployment Instructions:"

echo ""
echo "🌐 OPTION 1: Deploy with Vercel (Recommended)"
echo "1. Install Vercel CLI: npm install -g vercel"
echo "2. Login: vercel login"
echo "3. Deploy: vercel --prod"
echo "4. Set environment variables:"
echo "   vercel env add ENVIRONMENT production"
echo "   vercel env add DEBUG false"
echo "   vercel env add SECRET_KEY your-secret-key"
echo ""

echo "🌐 OPTION 2: Deploy with Railway"
echo "1. Visit railway.app"
echo "2. Connect your GitHub repository"
echo "3. Configure environment variables"
echo "4. Deploy with one click"
echo ""

echo "🌐 OPTION 3: Deploy with Render"
echo "1. Visit render.com"
echo "2. Connect your GitHub repository"
echo "3. Configure build and start commands"
echo "4. Set environment variables"
echo ""

print_success "Deployment preparation completed!"

echo ""
echo "🎯 Next Steps:"
echo "1. Choose a deployment platform (Vercel recommended)"
echo "2. Set up custom domain (optional but recommended)"
echo "3. Configure SSL certificate (automatic with most platforms)"
echo "4. Set up analytics and monitoring"
echo "5. Test PWA installation on mobile devices"

echo ""
echo "📊 Monitor your deployment:"
echo "- Health check: https://your-domain.com/health"
echo "- PWA manifest: https://your-domain.com/manifest.json"
echo "- Service worker: https://your-domain.com/sw.js"

print_success "🚀 Khyrie3.0 is ready for production deployment!"