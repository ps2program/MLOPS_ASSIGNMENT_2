#!/bin/bash
# Helper script to set up Kaggle credentials

echo "=== Kaggle Credentials Setup ==="
echo ""

# Check if kaggle.json exists in Downloads
if [ -f ~/Downloads/kaggle.json ]; then
    echo "✅ Found kaggle.json in Downloads folder"
    mkdir -p ~/.kaggle
    cp ~/Downloads/kaggle.json ~/.kaggle/
    chmod 600 ~/.kaggle/kaggle.json
    echo "✅ Credentials set up successfully!"
    echo ""
    echo "Testing Kaggle API..."
    kaggle datasets list | head -3
else
    echo "❌ kaggle.json not found in Downloads folder"
    echo ""
    echo "Please:"
    echo "1. Go to https://www.kaggle.com/settings"
    echo "2. Click 'Create New Token'"
    echo "3. Download kaggle.json"
    echo "4. Place it in ~/Downloads/ or run this script again"
fi
