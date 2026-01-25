# Quick Kaggle Setup Guide

## Step 1: Get Kaggle API Credentials

1. **Go to Kaggle Settings:**
   - Open: https://www.kaggle.com/settings
   - Make sure you're logged in to your Kaggle account

2. **Create API Token:**
   - Scroll down to the "API" section
   - Click "Create New Token" button
   - This will download a file named `kaggle.json`

3. **Place the credentials file:**
   ```bash
   # Move the downloaded file to the correct location
   mv ~/Downloads/kaggle.json ~/.kaggle/
   
   # Set proper permissions (required by Kaggle)
   chmod 600 ~/.kaggle/kaggle.json
   ```

## Step 2: Verify Setup

```bash
# Check if credentials are in place
ls -la ~/.kaggle/kaggle.json

# Test Kaggle CLI
kaggle datasets list | head -5
```

## Step 3: Download the Dataset

Once credentials are set up, run:

```bash
./scripts/download_dataset.sh
```

Or manually:
```bash
kaggle datasets download -d salader/dogs-vs-cats -p data/raw --unzip
```

## Alternative: Manual Download

If you prefer to download manually:

1. Go to: https://www.kaggle.com/datasets/salader/dogs-vs-cats
2. Click "Download" button
3. Extract the zip file to `data/raw/`
4. Organize images into `cats/` and `dogs/` folders

