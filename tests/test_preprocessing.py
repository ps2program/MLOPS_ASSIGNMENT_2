"""
Unit tests for data preprocessing functions.
"""

import pytest
import numpy as np
from pathlib import Path
import tempfile
import shutil
from PIL import Image

from src.data.preprocessing import (
    load_image_paths,
    preprocess_images,
    get_data_transforms,
    CatsDogsDataset
)


@pytest.fixture
def temp_data_dir():
    """Create a temporary directory with sample images."""
    temp_dir = tempfile.mkdtemp()
    
    # Create directory structure
    cats_dir = Path(temp_dir) / "cats"
    dogs_dir = Path(temp_dir) / "dogs"
    cats_dir.mkdir(parents=True)
    dogs_dir.mkdir(parents=True)
    
    # Create sample images
    for i in range(5):
        # Create cat image
        img = Image.new('RGB', (100, 100), color='red')
        img.save(cats_dir / f"cat_{i}.jpg")
        
        # Create dog image
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(dogs_dir / f"dog_{i}.jpg")
    
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)


def test_load_image_paths(temp_data_dir):
    """Test loading image paths from directory."""
    image_paths, labels = load_image_paths(temp_data_dir)
    
    assert len(image_paths) == 10  # 5 cats + 5 dogs
    assert len(labels) == 10
    
    # Check labels
    cat_count = sum(1 for l in labels if l == 0)
    dog_count = sum(1 for l in labels if l == 1)
    
    assert cat_count == 5
    assert dog_count == 5
    
    # Check paths
    cat_paths = [p for p, l in zip(image_paths, labels) if l == 0]
    dog_paths = [p for p, l in zip(image_paths, labels) if l == 1]
    
    assert all('cats' in p for p in cat_paths)
    assert all('dogs' in p for p in dog_paths)


def test_load_image_paths_empty_dir():
    """Test loading from empty directory."""
    temp_dir = tempfile.mkdtemp()
    try:
        image_paths, labels = load_image_paths(temp_dir)
        assert len(image_paths) == 0
        assert len(labels) == 0
    finally:
        shutil.rmtree(temp_dir)


def test_preprocess_images(temp_data_dir):
    """Test image preprocessing and splitting."""
    temp_processed = tempfile.mkdtemp()
    
    try:
        # Create more samples for proper splitting
        cats_dir = Path(temp_data_dir) / "cats"
        dogs_dir = Path(temp_data_dir) / "dogs"
        for i in range(5, 15):  # Add more samples
            img = Image.new('RGB', (100, 100), color='red')
            img.save(cats_dir / f"cat_{i}.jpg")
            img = Image.new('RGB', (100, 100), color='blue')
            img.save(dogs_dir / f"dog_{i}.jpg")
        
        train_paths, val_paths, test_paths = preprocess_images(
            raw_data_dir=temp_data_dir,
            processed_data_dir=temp_processed,
            target_size=(224, 224),
            train_ratio=0.8,
            val_ratio=0.1,
            test_ratio=0.1
        )
        
        # Check that images were created
        assert len(train_paths) > 0
        assert len(val_paths) > 0
        assert len(test_paths) > 0
        
        # Check total count (should be 30: 15 cats + 15 dogs)
        total = len(train_paths) + len(val_paths) + len(test_paths)
        assert total == 30
        
        # Check image sizes
        for path in train_paths[:2]:  # Check first 2
            img = Image.open(path)
            assert img.size == (224, 224)
        
    finally:
        shutil.rmtree(temp_processed)


def test_preprocess_images_ratios():
    """Test that ratio validation works."""
    temp_dir = tempfile.mkdtemp()
    temp_processed = tempfile.mkdtemp()
    
    try:
        # Create minimal data
        (Path(temp_dir) / "cats").mkdir(parents=True)
        img = Image.new('RGB', (100, 100))
        img.save(Path(temp_dir) / "cats" / "cat.jpg")
        
        # Test invalid ratios
        with pytest.raises(AssertionError):
            preprocess_images(
                raw_data_dir=temp_dir,
                processed_data_dir=temp_processed,
                train_ratio=0.5,
                val_ratio=0.3,
                test_ratio=0.3  # Sums to 1.1
            )
    finally:
        shutil.rmtree(temp_dir)
        shutil.rmtree(temp_processed)


def test_get_data_transforms():
    """Test data transformation pipelines."""
    train_transform, val_transform = get_data_transforms(augment=True)
    
    assert train_transform is not None
    assert val_transform is not None
    
    # Test with augment=False
    train_transform_no_aug, val_transform_no_aug = get_data_transforms(augment=False)
    assert train_transform_no_aug is not None
    assert val_transform_no_aug is not None


def test_cats_dogs_dataset(temp_data_dir):
    """Test CatsDogsDataset class."""
    image_paths, labels = load_image_paths(temp_data_dir)
    
    # Get transforms
    _, val_transform = get_data_transforms(augment=False)
    
    # Create dataset
    dataset = CatsDogsDataset(image_paths, labels, transform=val_transform)
    
    assert len(dataset) == 10
    
    # Test getting an item
    image, label = dataset[0]
    
    assert image is not None
    assert label in [0, 1]
    
    # Check image tensor shape
    assert image.shape == (3, 224, 224)  # C, H, W


def test_preprocess_images_no_data():
    """Test preprocessing with no data."""
    temp_dir = tempfile.mkdtemp()
    temp_processed = tempfile.mkdtemp()
    
    try:
        with pytest.raises(ValueError, match="No images found"):
            preprocess_images(
                raw_data_dir=temp_dir,
                processed_data_dir=temp_processed
            )
    finally:
        shutil.rmtree(temp_dir)
        shutil.rmtree(temp_processed)

