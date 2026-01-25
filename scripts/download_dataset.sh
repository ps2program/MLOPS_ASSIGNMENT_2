#!/bin/bash

# Script to download Cats vs Dogs dataset
# Note: This requires Kaggle API credentials

set -e

DATA_DIR="data/raw"

echo "Setting up data directory..."
mkdir -p "$DATA_DIR/cats"
mkdir -p "$DATA_DIR/dogs"

# Check if kaggle is installed
if ! command -v kaggle &> /dev/null; then
    echo "Kaggle CLI not found. Installing..."
    pip install kaggle
fi

# Check for Kaggle credentials
if [ ! -f ~/.kaggle/kaggle.json ]; then
    echo "Error: Kaggle credentials not found."
    echo "Please download your kaggle.json from https://www.kaggle.com/settings and place it in ~/.kaggle/"
    exit 1
fi

echo "Downloading Cats vs Dogs dataset..."
kaggle datasets download -d salader/dogs-vs-cats -p "$DATA_DIR" --unzip

# The dataset structure may vary, adjust paths as needed
# If images are in a single folder, organize them
if [ -d "$DATA_DIR/train" ]; then
    echo "Organizing dataset..."
    find "$DATA_DIR/train" -name "cat.*" -exec mv {} "$DATA_DIR/cats/" \;
    find "$DATA_DIR/train" -name "dog.*" -exec mv {} "$DATA_DIR/dogs/" \;
fi

echo "Dataset downloaded and organized in $DATA_DIR"
echo "Run 'dvc add data/raw' to track with DVC"

