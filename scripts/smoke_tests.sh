#!/bin/bash

# Smoke tests for Cats vs Dogs Classifier API
# Usage: ./smoke_tests.sh <base_url>
# Example: ./smoke_tests.sh http://localhost:8000

set -e

BASE_URL=${1:-http://localhost:8000}
MAX_RETRIES=5
RETRY_DELAY=2

echo "Running smoke tests against: $BASE_URL"

# Function to retry a command
retry() {
    local retries=0
    while [ $retries -lt $MAX_RETRIES ]; do
        if "$@"; then
            return 0
        fi
        retries=$((retries + 1))
        echo "Retry $retries/$MAX_RETRIES: Waiting $RETRY_DELAY seconds..."
        sleep $RETRY_DELAY
    done
    echo "Failed after $MAX_RETRIES retries"
    return 1
}

# Test 1: Health check
echo "Test 1: Health check endpoint"
HEALTH_RESPONSE=$(retry curl -s -f "${BASE_URL}/health")
if [ $? -eq 0 ]; then
    echo "✓ Health check passed"
    echo "Response: $HEALTH_RESPONSE"
else
    echo "✗ Health check failed"
    exit 1
fi

# Verify health response contains expected fields
if echo "$HEALTH_RESPONSE" | grep -q "status"; then
    echo "✓ Health response format is correct"
else
    echo "✗ Health response format is incorrect"
    exit 1
fi

# Test 2: Metrics endpoint
echo ""
echo "Test 2: Metrics endpoint"
METRICS_RESPONSE=$(retry curl -s -f "${BASE_URL}/metrics")
if [ $? -eq 0 ]; then
    echo "✓ Metrics endpoint accessible"
    if echo "$METRICS_RESPONSE" | grep -q "inference_requests_total"; then
        echo "✓ Metrics contain expected data"
    else
        echo "⚠ Metrics endpoint accessible but may not have data yet"
    fi
else
    echo "✗ Metrics endpoint failed"
    exit 1
fi

# Test 3: Prediction endpoint (requires a test image)
echo ""
echo "Test 3: Prediction endpoint"

# Create a simple test image if it doesn't exist
TEST_IMAGE="test_image.jpg"
if [ ! -f "$TEST_IMAGE" ]; then
    echo "Creating test image..."
    # Use ImageMagick or Python to create a test image
    if command -v convert &> /dev/null; then
        convert -size 224x224 xc:red "$TEST_IMAGE"
    elif command -v python3 &> /dev/null; then
        python3 << EOF
from PIL import Image
img = Image.new('RGB', (224, 224), color='red')
img.save('$TEST_IMAGE')
EOF
    else
        echo "⚠ Cannot create test image. Skipping prediction test."
        echo "✓ Smoke tests completed (health and metrics passed)"
        exit 0
    fi
fi

PREDICTION_RESPONSE=$(retry curl -s -f -X POST \
    -F "file=@${TEST_IMAGE}" \
    "${BASE_URL}/predict")

if [ $? -eq 0 ]; then
    echo "✓ Prediction endpoint accessible"
    echo "Response: $PREDICTION_RESPONSE"
    
    # Verify response contains expected fields
    if echo "$PREDICTION_RESPONSE" | grep -q "prediction"; then
        echo "✓ Prediction response format is correct"
    else
        echo "✗ Prediction response format is incorrect"
        exit 1
    fi
    
    if echo "$PREDICTION_RESPONSE" | grep -q "confidence"; then
        echo "✓ Prediction includes confidence score"
    fi
else
    echo "✗ Prediction endpoint failed"
    exit 1
fi

# Cleanup
if [ -f "$TEST_IMAGE" ] && [ "$TEST_IMAGE" != "test_image.jpg" ]; then
    rm -f "$TEST_IMAGE"
fi

echo ""
echo "✓ All smoke tests passed!"

