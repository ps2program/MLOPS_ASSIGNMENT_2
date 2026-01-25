"""
Data preprocessing utilities for Cats vs Dogs classification.
Handles image loading, resizing, augmentation, and dataset splitting.
"""

import os
import shutil
from pathlib import Path
from typing import Tuple, List
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from sklearn.model_selection import train_test_split


class CatsDogsDataset(Dataset):
    """Custom dataset for Cats vs Dogs images."""
    
    def __init__(self, image_paths: List[str], labels: List[int], transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        image = Image.open(image_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label


def load_image_paths(data_dir: str) -> Tuple[List[str], List[int]]:
    """
    Load image paths and labels from directory structure.
    
    Expected structure:
    data_dir/
        cats/
            *.jpg
        dogs/
            *.jpg
    
    Args:
        data_dir: Root directory containing cat and dog subdirectories
    
    Returns:
        Tuple of (image_paths, labels) where labels: 0=cat, 1=dog
    """
    image_paths = []
    labels = []
    
    data_path = Path(data_dir)
    
    # Load cat images (label 0)
    cats_dir = data_path / 'cats'
    if cats_dir.exists():
        for img_file in cats_dir.glob('*.jpg'):
            image_paths.append(str(img_file))
            labels.append(0)
        for img_file in cats_dir.glob('*.png'):
            image_paths.append(str(img_file))
            labels.append(0)
    
    # Load dog images (label 1)
    dogs_dir = data_path / 'dogs'
    if dogs_dir.exists():
        for img_file in dogs_dir.glob('*.jpg'):
            image_paths.append(str(img_file))
            labels.append(1)
        for img_file in dogs_dir.glob('*.png'):
            image_paths.append(str(img_file))
            labels.append(1)
    
    return image_paths, labels


def preprocess_images(
    raw_data_dir: str,
    processed_data_dir: str,
    target_size: Tuple[int, int] = (224, 224),
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    test_ratio: float = 0.1
) -> Tuple[List[str], List[str], List[str]]:
    """
    Preprocess images and split into train/val/test sets.
    
    Args:
        raw_data_dir: Directory containing raw images
        processed_data_dir: Directory to save processed images
        target_size: Target image size (height, width)
        train_ratio: Proportion of data for training
        val_ratio: Proportion of data for validation
        test_ratio: Proportion of data for testing
    
    Returns:
        Tuple of (train_paths, val_paths, test_paths)
    """
    # Validate ratios
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, \
        "Ratios must sum to 1.0"
    
    # Load image paths and labels
    image_paths, labels = load_image_paths(raw_data_dir)
    
    if len(image_paths) == 0:
        raise ValueError(f"No images found in {raw_data_dir}")
    
    # Split data
    # First split: train vs (val + test)
    train_paths, temp_paths, train_labels, temp_labels = train_test_split(
        image_paths, labels,
        test_size=(val_ratio + test_ratio),
        stratify=labels,
        random_state=42
    )
    
    # Second split: val vs test
    val_size = val_ratio / (val_ratio + test_ratio)
    val_paths, test_paths, val_labels, test_labels = train_test_split(
        temp_paths, temp_labels,
        test_size=(1 - val_size),
        stratify=temp_labels,
        random_state=42
    )
    
    # Create processed data directory structure
    processed_path = Path(processed_data_dir)
    for split, paths in [('train', train_paths), ('val', val_paths), ('test', test_paths)]:
        (processed_path / split / 'cats').mkdir(parents=True, exist_ok=True)
        (processed_path / split / 'dogs').mkdir(parents=True, exist_ok=True)
    
    # Copy and resize images
    splits = {
        'train': (train_paths, train_labels),
        'val': (val_paths, val_labels),
        'test': (test_paths, test_labels)
    }
    
    processed_paths = {'train': [], 'val': [], 'test': []}
    
    for split_name, (paths, split_labels) in splits.items():
        for img_path, label in zip(paths, split_labels):
            # Load and resize image
            img = Image.open(img_path).convert('RGB')
            img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
            
            # Determine class name
            class_name = 'cats' if label == 0 else 'dogs'
            
            # Save processed image
            filename = Path(img_path).name
            output_path = processed_path / split_name / class_name / filename
            img_resized.save(output_path)
            
            processed_paths[split_name].append(str(output_path))
    
    return processed_paths['train'], processed_paths['val'], processed_paths['test']


def get_data_transforms(augment: bool = True) -> Tuple[transforms.Compose, transforms.Compose]:
    """
    Get data transformation pipelines for training and validation.
    
    Args:
        augment: Whether to apply data augmentation for training
    
    Returns:
        Tuple of (train_transform, val_transform)
    """
    if augment:
        train_transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomCrop(224),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    else:
        train_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_transform


def create_data_loaders(
    train_paths: List[str],
    val_paths: List[str],
    test_paths: List[str],
    train_labels: List[int],
    val_labels: List[int],
    test_labels: List[int],
    batch_size: int = 32,
    num_workers: int = 4
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Create PyTorch data loaders for train, validation, and test sets.
    
    Args:
        train_paths: List of training image paths
        val_paths: List of validation image paths
        test_paths: List of test image paths
        train_labels: List of training labels
        val_labels: List of validation labels
        test_labels: List of test labels
        batch_size: Batch size for data loaders
        num_workers: Number of worker processes
    
    Returns:
        Tuple of (train_loader, val_loader, test_loader)
    """
    train_transform, val_transform = get_data_transforms(augment=True)
    
    train_dataset = CatsDogsDataset(train_paths, train_labels, transform=train_transform)
    val_dataset = CatsDogsDataset(val_paths, val_labels, transform=val_transform)
    test_dataset = CatsDogsDataset(test_paths, test_labels, transform=val_transform)
    
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers
    )
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )
    
    return train_loader, val_loader, test_loader

