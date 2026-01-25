"""
Unit tests for inference functions.
"""

import pytest
import torch
import numpy as np
from PIL import Image
import io
from pathlib import Path
from unittest.mock import Mock, patch

from src.inference.app import preprocess_image, predict
from src.models.cnn_model import create_model, load_model


@pytest.fixture
def sample_image_bytes():
    """Create sample image bytes."""
    img = Image.new('RGB', (224, 224), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.read()


@pytest.fixture
def mock_model():
    """Create a mock model for testing."""
    model = create_model(num_classes=2)
    model.eval()
    return model


def test_preprocess_image(sample_image_bytes):
    """Test image preprocessing function."""
    image_tensor = preprocess_image(sample_image_bytes)
    
    # Check tensor properties
    assert isinstance(image_tensor, torch.Tensor)
    assert image_tensor.shape[0] == 1  # Batch dimension
    assert image_tensor.shape[1] == 3  # RGB channels
    assert image_tensor.shape[2] == 224  # Height
    assert image_tensor.shape[3] == 224  # Width


def test_preprocess_image_invalid():
    """Test preprocessing with invalid image data."""
    invalid_bytes = b"not an image"
    
    with pytest.raises(Exception):  # Should raise HTTPException or similar
        preprocess_image(invalid_bytes)


@patch('src.inference.app.model')
@patch('src.inference.app.device', torch.device('cpu'))
def test_predict(mock_model_global, mock_model, sample_image_bytes):
    """Test prediction function."""
    # Setup mock model
    mock_model_global.eval = Mock()
    mock_model_global.return_value = torch.tensor([[2.0, 1.0]])  # Mock output
    
    # Preprocess image
    image_tensor = preprocess_image(sample_image_bytes)
    
    # Mock the model to return expected output
    with patch('torch.nn.functional.softmax') as mock_softmax:
        mock_softmax.return_value = torch.tensor([[0.7, 0.3]])
        
        # This will fail if model is None, so we need to set it
        from src.inference.app import model, device
        if model is None:
            pytest.skip("Model not loaded - requires trained model")
        
        result = predict(image_tensor)
        
        # Check result structure
        assert 'prediction' in result
        assert 'class_probabilities' in result
        assert 'confidence' in result
        assert result['prediction'] in ['cat', 'dog']
        assert 'cat' in result['class_probabilities']
        assert 'dog' in result['class_probabilities']
        assert 0 <= result['confidence'] <= 1


def test_model_creation():
    """Test model creation."""
    model = create_model(num_classes=2)
    
    assert model is not None
    assert isinstance(model, torch.nn.Module)
    
    # Test forward pass
    dummy_input = torch.randn(1, 3, 224, 224)
    output = model(dummy_input)
    
    assert output.shape == (1, 2)  # Batch size 1, 2 classes


def test_model_output_shape():
    """Test that model outputs correct shape."""
    model = create_model(num_classes=2)
    model.eval()
    
    # Create dummy input
    dummy_input = torch.randn(2, 3, 224, 224)  # Batch of 2
    
    with torch.no_grad():
        output = model(dummy_input)
    
    assert output.shape == (2, 2)  # Batch size 2, 2 classes


def test_model_classes():
    """Test model class probabilities sum to 1."""
    model = create_model(num_classes=2)
    model.eval()
    
    dummy_input = torch.randn(1, 3, 224, 224)
    
    with torch.no_grad():
        output = model(dummy_input)
        probabilities = torch.nn.functional.softmax(output, dim=1)
    
    # Check probabilities sum to approximately 1
    prob_sum = probabilities.sum().item()
    assert abs(prob_sum - 1.0) < 1e-5


@pytest.mark.skipif(not Path("models/best_model.pt").exists(), 
                    reason="Model file not found")
def test_load_model():
    """Test loading a saved model."""
    model_path = "models/best_model.pt"
    
    if not Path(model_path).exists():
        pytest.skip("Model file not found")
    
    model = load_model(model_path, device='cpu')
    
    assert model is not None
    assert isinstance(model, torch.nn.Module)
    
    # Test inference
    dummy_input = torch.randn(1, 3, 224, 224)
    model.eval()
    with torch.no_grad():
        output = model(dummy_input)
    
    assert output.shape == (1, 2)

