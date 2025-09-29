#!/bin/bash
# Setup PostgreSQL PATH configuration for FitFriendsClub

echo "🔧 PostgreSQL PATH Configuration Setup"
echo "======================================"

# Common PostgreSQL installation paths on macOS
PG_PATHS=(
    "/opt/homebrew/bin"
    "/usr/local/bin" 
    "/usr/local/pgsql/bin"
    "/Applications/Postgres.app/Contents/Versions/*/bin"
    "/Library/PostgreSQL/*/bin"
)

echo ""
echo "🔍 Searching for PostgreSQL installations..."
echo "--------------------------------------------"

FOUND_PATHS=()

for path in "${PG_PATHS[@]}"; do
    if [ -f "$path/pg_config" ]; then
        FOUND_PATHS+=("$path")
        PG_VERSION=$("$path/pg_config" --version 2>/dev/null || echo "unknown")
        echo "✅ Found: $path (PostgreSQL: $PG_VERSION)"
    elif ls $path/pg_config 2>/dev/null >/dev/null; then
        for pg_path in $path; do
            if [ -f "$pg_path/pg_config" ]; then
                FOUND_PATHS+=("$pg_path")
                PG_VERSION=$("$pg_path/pg_config" --version 2>/dev/null || echo "unknown")
                echo "✅ Found: $pg_path (PostgreSQL: $PG_VERSION)"
            fi
        done
    fi
done

if [ ${#FOUND_PATHS[@]} -eq 0 ]; then
    echo "❌ No PostgreSQL installations found"
    echo ""
    echo "💡 Install PostgreSQL first:"
    echo "   Homebrew: brew install postgresql"
    echo "   Postgres.app: Download from https://postgresapp.com/"
    echo "   Official: Download from https://www.postgresql.org/download/"
    exit 1
fi

echo ""
echo "📝 PATH Configuration Options:"
echo "------------------------------"

# Determine shell configuration file
SHELL_CONFIG=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [ -n "$BASH_VERSION" ]; then
    if [ -f "$HOME/.bash_profile" ]; then
        SHELL_CONFIG="$HOME/.bash_profile"
    else
        SHELL_CONFIG="$HOME/.bashrc"
    fi
    SHELL_NAME="bash"
else
    echo "⚠️  Unable to detect shell type"
    SHELL_CONFIG="$HOME/.profile"
    SHELL_NAME="shell"
fi

echo "Detected shell: $SHELL_NAME"
echo "Config file: $SHELL_CONFIG"

# Choose the best PostgreSQL path
RECOMMENDED_PATH="${FOUND_PATHS[0]}"
echo ""
echo "🎯 Recommended PostgreSQL path: $RECOMMENDED_PATH"

# Create PATH export command
PATH_COMMAND="export PATH=\"$RECOMMENDED_PATH:\$PATH\""

echo ""
echo "🔧 To add PostgreSQL to your PATH permanently:"
echo "----------------------------------------------"
echo ""
echo "1. Add this line to your $SHELL_CONFIG:"
echo "   $PATH_COMMAND"
echo ""
echo "2. Reload your shell configuration:"
echo "   source $SHELL_CONFIG"
echo ""
echo "3. Or restart your terminal"
echo ""

# Offer to add automatically
echo "❓ Would you like to add this to your $SHELL_CONFIG automatically? (y/N)"
read -r RESPONSE

if [[ "$RESPONSE" =~ ^[Yy]$ ]]; then
    # Check if already exists
    if grep -q "export PATH.*pg_config" "$SHELL_CONFIG" 2>/dev/null; then
        echo "⚠️  PostgreSQL PATH entry already exists in $SHELL_CONFIG"
    else
        echo "" >> "$SHELL_CONFIG"
        echo "# PostgreSQL PATH (added by FitFriendsClub setup)" >> "$SHELL_CONFIG"
        echo "$PATH_COMMAND" >> "$SHELL_CONFIG"
        echo "✅ Added PostgreSQL PATH to $SHELL_CONFIG"
        echo ""
        echo "🔄 Run this command to apply changes:"
        echo "   source $SHELL_CONFIG"
    fi
else
    echo "📋 Manual setup instructions saved above ☝️"
fi

echo ""
echo "🧪 Test PostgreSQL PATH:"
echo "------------------------"
echo "After updating your PATH, verify with:"
echo "   which pg_config"
echo "   pg_config --version"

echo ""
echo "🐘 Then install PostgreSQL support:"
echo "   ./install-postgresql.sh"