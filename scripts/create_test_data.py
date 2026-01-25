#!/usr/bin/env python3
"""
Create a minimal test dataset for demonstration purposes.
This creates a few sample images to test the pipeline.
"""

import os
from pathlib import Path
from PIL import Image
import numpy as np

def create_test_dataset(output_dir="data/raw", num_samples=10):
    """Create a minimal test dataset."""
    output_path = Path(output_dir)
    cats_dir = output_path / "cats"
    dogs_dir = output_path / "dogs"
    
    cats_dir.mkdir(parents=True, exist_ok=True)
    dogs_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating test dataset in {output_dir}...")
    
    # Create cat images (red tint)
    for i in range(num_samples):
        img = Image.new('RGB', (224, 224), color=(200 + i*2, 100, 100))
        img.save(cats_dir / f"cat_{i:03d}.jpg")
    
    # Create dog images (blue tint)
    for i in range(num_samples):
        img = Image.new('RGB', (224, 224), color=(100, 100, 200 + i*2))
        img.save(dogs_dir / f"dog_{i:03d}.jpg")
    
    print(f"Created {num_samples} cat images and {num_samples} dog images")
    print(f"Total: {num_samples * 2} images")

if __name__ == "__main__":
    import sys
    num_samples = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    create_test_dataset(num_samples=num_samples)


