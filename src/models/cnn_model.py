"""
CNN model for Cats vs Dogs binary classification.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleCNN(nn.Module):
    """
    Simple CNN model for binary image classification.
    
    Architecture:
    - Conv layers with ReLU and MaxPool
    - Fully connected layers
    - Binary classification output
    """
    
    def __init__(self, num_classes: int = 2):
        super(SimpleCNN, self).__init__()
        
        # Convolutional layers
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(256)
        
        # Pooling layer
        self.pool = nn.MaxPool2d(2, 2)
        
        # Dropout
        self.dropout = nn.Dropout(0.5)
        
        # Fully connected layers
        # After 4 pooling operations: 224 -> 112 -> 56 -> 28 -> 14
        self.fc1 = nn.Linear(256 * 14 * 14, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, num_classes)
    
    def forward(self, x):
        # Conv block 1
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        
        # Conv block 2
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        
        # Conv block 3
        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        
        # Conv block 4
        x = self.pool(F.relu(self.bn4(self.conv4(x))))
        
        # Flatten
        x = x.view(-1, 256 * 14 * 14)
        
        # Fully connected layers
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        
        return x


def create_model(num_classes: int = 2, pretrained: bool = False) -> nn.Module:
    """
    Create a CNN model for binary classification.
    
    Args:
        num_classes: Number of output classes (default: 2 for binary)
        pretrained: Whether to use pretrained weights (not implemented for SimpleCNN)
    
    Returns:
        PyTorch model
    """
    model = SimpleCNN(num_classes=num_classes)
    return model


def load_model(model_path: str, device: str = 'cpu') -> nn.Module:
    """
    Load a trained model from file.
    
    Args:
        model_path: Path to saved model file (.pt or .pth)
        device: Device to load model on ('cpu' or 'cuda')
    
    Returns:
        Loaded PyTorch model
    """
    model = create_model()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model

