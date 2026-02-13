"""
FastAPI inference service for Cats vs Dogs classification.
Includes health check and prediction endpoints with monitoring.
"""

import os
import time
import logging
from pathlib import Path
from typing import Optional
import torch
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image
import io
import numpy as np
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response

from src.models.cnn_model import load_model
from src.data.preprocessing import get_data_transforms

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
request_count = Counter('inference_requests_total', 'Total number of inference requests')
request_latency = Histogram('inference_request_duration_seconds', 'Inference request latency')
prediction_count = Counter('predictions_total', 'Total predictions', ['class'])

app = FastAPI(title="Cats vs Dogs Classifier API", version="1.0.0")

# Global model variable
model = None
device = None
transform = None


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


class PredictionResponse(BaseModel):
    prediction: str
    class_probabilities: dict
    confidence: float


def load_model_once():
    """Load the model once at startup."""
    global model, device, transform
    
    model_path = os.getenv("MODEL_PATH", "models/best_model.pt")
    
    if not Path(model_path).exists():
        logger.warning(f"Model file not found at {model_path}. Please train the model first.")
        return False
    
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Loading model from {model_path} on device: {device}")
        
        model = load_model(model_path, device=device)
        logger.info("Model loaded successfully")
        
        # Get validation transform (no augmentation for inference)
        _, transform = get_data_transforms(augment=False)
        
        return True
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False


@app.on_event("startup")
async def startup_event():
    """Load model on application startup."""
    load_model_once()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Returns the status of the service and whether the model is loaded.
    """
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None
    )


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type="text/plain")


def preprocess_image(image_bytes: bytes) -> torch.Tensor:
    """
    Preprocess image bytes for model inference.
    
    Args:
        image_bytes: Raw image bytes
    
    Returns:
        Preprocessed image tensor
    """
    try:
        # Load image
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Apply transforms
        if transform:
            image_tensor = transform(image)
        else:
            # Fallback transform
            from torchvision import transforms
            transform_fallback = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            image_tensor = transform_fallback(image)
        
        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0)
        
        return image_tensor
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")


def predict(image_tensor: torch.Tensor) -> dict:
    """
    Run model inference.
    
    Args:
        image_tensor: Preprocessed image tensor
    
    Returns:
        Dictionary with prediction results
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    model.eval()
    with torch.no_grad():
        image_tensor = image_tensor.to(device)
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
    
    # Get class probabilities
    probs = probabilities[0].cpu().numpy()
    class_probs = {
        "cat": float(probs[0]),
        "dog": float(probs[1])
    }
    
    # Get prediction
    predicted_class = "cat" if predicted.item() == 0 else "dog"
    confidence_score = confidence.item()
    
    # Update metrics
    prediction_count.labels(**{'class': predicted_class}).inc()
    
    return {
        "prediction": predicted_class,
        "class_probabilities": class_probs,
        "confidence": confidence_score
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_image(file: UploadFile = File(...)):
    """
    Predict the class of an uploaded image (cat or dog).
    
    Args:
        file: Image file to classify
    
    Returns:
        Prediction result with class probabilities
    """
    start_time = time.time()
    request_count.inc()
    
    # Enhanced logging for better monitoring (M5 requirement)
    logger.info(f"Processing prediction request - timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image bytes
        image_bytes = await file.read()
        
        # Preprocess
        image_tensor = preprocess_image(image_bytes)
        
        # Predict
        result = predict(image_tensor)
        
        # Log request (excluding sensitive data)
        latency = time.time() - start_time
        request_latency.observe(latency)
        
        logger.info(
            f"Prediction: {result['prediction']}, "
            f"Confidence: {result['confidence']:.4f}, "
            f"Latency: {latency:.4f}s"
        )
        
        return PredictionResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/batch")
async def predict_batch(files: list[UploadFile] = File(...)):
    """
    Predict classes for multiple images.
    
    Args:
        files: List of image files to classify
    
    Returns:
        List of prediction results
    """
    results = []
    
    for file in files:
        try:
            image_bytes = await file.read()
            image_tensor = preprocess_image(image_bytes)
            result = predict(image_tensor)
            results.append({
                "filename": file.filename,
                **result
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {"results": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

