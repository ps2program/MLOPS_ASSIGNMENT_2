# Dataset Setup Guide

## Current Status

**Test Dataset (Current):**
- 40 images total (20 cats, 20 dogs)
- Created using `scripts/create_test_data.py`
- Used for quick testing and development

**Full Dataset (Required for Assignment):**
- Full Kaggle Cats vs Dogs dataset
- Typically contains 25,000 images (12,500 cats, 12,500 dogs)
- Required for proper model training as per assignment

## Download Full Dataset

### Option 1: Using Kaggle CLI (Recommended)

1. **Install Kaggle CLI:**
   ```bash
   pip install kaggle
   ```

2. **Get Kaggle API Credentials:**
   - Go to https://www.kaggle.com/settings
   - Scroll to "API" section
   - Click "Create New Token"
   - Download `kaggle.json`

3. **Set up credentials:**
   ```bash
   mkdir -p ~/.kaggle
   cp ~/Downloads/kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```

4. **Download the dataset:**
   ```bash
   ./scripts/download_dataset.sh
   ```

   Or manually:
   ```bash
   kaggle datasets download -d salader/dogs-vs-cats -p data/raw --unzip
   ```

5. **Organize the dataset:**
   The script will organize images into:
   ```
   data/raw/
     cats/
       *.jpg
     dogs/
       *.jpg
   ```

6. **Track with DVC:**
   ```bash
   dvc add data/raw
   git add data/raw.dvc .gitignore
   git commit -m "Add full Cats vs Dogs dataset with DVC"
   ```

### Option 2: Manual Download

1. **Download from Kaggle:**
   - Go to: https://www.kaggle.com/datasets/salader/dogs-vs-cats
   - Click "Download" button
   - Extract the zip file

2. **Organize the dataset:**
   ```bash
   # Extract to data/raw/
   unzip dogs-vs-cats.zip -d data/raw/
   
   # Organize into cats/ and dogs/ folders
   mkdir -p data/raw/cats data/raw/dogs
   
   # Move cat images
   find data/raw/train -name "cat.*" -exec mv {} data/raw/cats/ \;
   
   # Move dog images
   find data/raw/train -name "dog.*" -exec mv {} data/raw/dogs/ \;
   ```

3. **Track with DVC:**
   ```bash
   dvc add data/raw
   git add data/raw.dvc .gitignore
   git commit -m "Add full Cats vs Dogs dataset with DVC"
   ```

## Dataset Information

**Expected Structure:**
```
data/raw/
  cats/
    cat.0.jpg
    cat.1.jpg
    ... (12,500 images)
  dogs/
    dog.0.jpg
    dog.1.jpg
    ... (12,500 images)
```

**Total Size:** ~800MB - 1GB (compressed)

## After Downloading

1. **Verify dataset:**
   ```bash
   ls data/raw/cats/ | wc -l  # Should show ~12,500
   ls data/raw/dogs/ | wc -l  # Should show ~12,500
   ```

2. **Retrain the model with full dataset:**
   ```bash
   python src/training/train.py \
       --raw_data_dir data/raw \
       --processed_data_dir data/processed \
       --model_save_dir models \
       --num_epochs 10 \
       --batch_size 32
   ```

3. **Note:** Training with full dataset will take significantly longer (30-60 minutes depending on hardware)

## Important Notes

- The full dataset is large (~1GB) and should be tracked with DVC, not Git
- The test dataset (40 images) was only for quick testing
- For assignment submission, use the full dataset for proper model training
- DVC will handle versioning of the large dataset files

