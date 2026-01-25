"""
Monitoring utilities for the inference service.
"""

import logging
import time
from functools import wraps
from typing import Callable, Any
import json

logger = logging.getLogger(__name__)


def log_request_response(func: Callable) -> Callable:
    """
    Decorator to log request and response (excluding sensitive data).
    
    Args:
        func: Function to decorate
    
    Returns:
        Decorated function
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # Log request (without file content)
        logger.info(f"Request: {func.__name__}")
        
        try:
            result = await func(*args, **kwargs)
            latency = time.time() - start_time
            
            # Log response summary (without sensitive data)
            if hasattr(result, 'dict'):
                result_dict = result.dict()
                # Remove or mask sensitive fields
                safe_result = {
                    'prediction': result_dict.get('prediction'),
                    'confidence': result_dict.get('confidence'),
                    'latency_seconds': round(latency, 4)
                }
                logger.info(f"Response: {json.dumps(safe_result)}")
            else:
                logger.info(f"Response: {type(result).__name__}, Latency: {latency:.4f}s")
            
            return result
        
        except Exception as e:
            latency = time.time() - start_time
            logger.error(f"Error in {func.__name__}: {str(e)}, Latency: {latency:.4f}s")
            raise
    
    return wrapper


class MetricsCollector:
    """Simple in-app metrics collector."""
    
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.total_latency = 0.0
        self.prediction_counts = {'cat': 0, 'dog': 0}
    
    def record_request(self, latency: float, success: bool = True):
        """Record a request."""
        self.request_count += 1
        self.total_latency += latency
        if not success:
            self.error_count += 1
    
    def record_prediction(self, prediction: str):
        """Record a prediction."""
        if prediction in self.prediction_counts:
            self.prediction_counts[prediction] += 1
    
    def get_stats(self) -> dict:
        """Get current statistics."""
        avg_latency = self.total_latency / self.request_count if self.request_count > 0 else 0.0
        error_rate = self.error_count / self.request_count if self.request_count > 0 else 0.0
        
        return {
            'total_requests': self.request_count,
            'error_count': self.error_count,
            'error_rate': error_rate,
            'average_latency_seconds': avg_latency,
            'prediction_counts': self.prediction_counts.copy()
        }


# Global metrics collector instance
metrics_collector = MetricsCollector()

