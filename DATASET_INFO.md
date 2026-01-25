# Dataset Information

## Dataset Details

**Source:** [bhavikjikadara/dog-and-cat-classification-dataset](https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset)

**Statistics:**
- **Total Images:** 25,038
- **Cat Images:** 12,519
- **Dog Images:** 12,519
- **Dataset Size:** ~775MB (compressed)
- **Uncompressed Size:** ~1.2GB

## Dataset Structure

```
data/raw/
├── cats/
│   ├── 0.jpg
│   ├── 1.jpg
│   └── ... (12,519 images)
└── dogs/
    ├── 0.jpg
    ├── 1.jpg
    └── ... (12,519 images)
```

## Preprocessing

The dataset is preprocessed as follows:

1. **Resize:** All images resized to 224x224 RGB (standard CNN input size)
2. **Split:** 
   - Training: 80% (~20,030 images)
   - Validation: 10% (~2,504 images)
   - Test: 10% (~2,504 images)
3. **Data Augmentation (Training only):**
   - Random horizontal flip (50% probability)
   - Random rotation (±15 degrees)
   - Random crop (256→224)
   - Color jitter (brightness, contrast)

## Version Control

The dataset is tracked using DVC (Data Version Control):
- **DVC File:** `data/raw.dvc`
- **Cache:** `.dvc/cache/` (excluded from Git)
- **Actual data:** Excluded from Git via `.gitignore`

## Download Instructions

### Using Kaggle CLI

```bash
# Install Kaggle CLI
pip install kaggle

# Set up credentials (download from https://www.kaggle.com/settings)
mkdir -p ~/.kaggle
cp ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Download dataset
kaggle datasets download -d bhavikjikadara/dog-and-cat-classification-dataset -p data/raw --unzip

# Organize (if needed)
find data/raw/PetImages/Cat -type f -name "*.jpg" -exec mv {} data/raw/cats/ \;
find data/raw/PetImages/Dog -type f -name "*.jpg" -exec mv {} data/raw/dogs/ \;
rm -rf data/raw/PetImages

# Track with DVC
dvc add data/raw
git add data/raw.dvc .gitignore
git commit -m "Add dataset with DVC"
```

### Using Download Script

```bash
./scripts/download_dataset.sh
dvc add data/raw
```

## Verification

After downloading, verify the dataset:

```bash
# Count images
echo "Cats: $(ls data/raw/cats/ | wc -l)"
echo "Dogs: $(ls data/raw/dogs/ | wc -l)"
echo "Total: $(find data/raw -type f | wc -l)"
```

Expected output:
- Cats: 12,519
- Dogs: 12,519
- Total: 25,038

## Notes

- The dataset is large (~1.2GB uncompressed) and should be tracked with DVC, not Git
- DVC handles versioning and storage efficiently
- The dataset is already downloaded and organized in this repository
- To retrieve the dataset on a new machine: `dvc pull`

