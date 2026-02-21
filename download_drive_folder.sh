#!/usr/bin/env bash
#
# download_drive_folder.sh
#
# Downloads all files from a shared Google Drive folder
# into the current directory.
#
# Usage:
#   chmod +x download_drive_folder.sh
#   ./download_drive_folder.sh

set -e

# Google Drive folder ID (from your link)
FOLDER_ID="1f7zWKwjIZIZBcxh5VCwZQ39foE-5HgDJ"

# Check for gdown
if ! command -v gdown &> /dev/null; then
    echo "gdown not found. Installing..."
    pip install --user gdown
fi

# Create temporary directory
TEMP_JSON="$(mktemp --suffix .json)"

echo "Fetching file list from Google Drive folder..."

# Use gdown to list files
gdown --folder "https://drive.google.com/drive/folders/$FOLDER_ID" --print-json > "$TEMP_JSON"

echo "Parsing file list..."

# Extract file IDs and names
FILE_COUNT=$(jq '.[] | select(.id and .name) | length' "$TEMP_JSON" 2>/dev/null || true)
if [ -z "$FILE_COUNT" ]; then
    echo "No files found or failed to fetch folder contents."
    exit 1
fi

# Loop through each file
jq -c '.[] | select(.id and .name)' "$TEMP_JSON" | while read -r file; do
    FILE_ID=$(echo "$file" | jq -r '.id')
    FILE_NAME=$(echo "$file" | jq -r '.name')

    echo "Downloading: $FILE_NAME ..."
    gdown "https://drive.google.com/uc?id=$FILE_ID" -O "$FILE_NAME"
done

# Clean up
rm -f "$TEMP_JSON"

echo "Download complete!"