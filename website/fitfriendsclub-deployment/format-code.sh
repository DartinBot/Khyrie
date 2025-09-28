#!/bin/bash
# Format FitFriendsClub Python code with Black

echo "🎨 Formatting Python code with Black..."

# Activate virtual environment
source .venv/bin/activate

# Format all Python files
black backend/ --line-length 88

# Check if formatting was successful
if [ $? -eq 0 ]; then
    echo "✅ Code formatting complete!"
else
    echo "❌ Code formatting failed!"
    exit 1
fi

echo "📋 To check code without formatting, run: black backend/ --check --diff"