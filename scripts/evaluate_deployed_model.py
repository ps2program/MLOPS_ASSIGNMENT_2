"""
Post-deployment model performance evaluation script.

Sends a batch of test images (with known labels) to the deployed API
and reports accuracy, precision, recall, F1, and a confusion matrix.

Uses real images from data/raw/ if available, otherwise generates
simulated test images.

Usage:
    python scripts/evaluate_deployed_model.py [--url http://localhost:8000] [--num-samples 50]
"""

import argparse
import io
import os
import random
import sys
from pathlib import Path

import requests
from PIL import Image


def get_real_test_images(data_dir, num_samples):
    """
    Load real test images with known labels from data/raw/.

    Args:
        data_dir: Path to raw data directory containing cats/ and dogs/ subdirectories.
        num_samples: Number of samples to collect (split evenly between classes).

    Returns:
        List of (image_path, true_label) tuples, or empty list if data not found.
    """
    cats_dir = Path(data_dir) / "cats"
    dogs_dir = Path(data_dir) / "dogs"

    if not cats_dir.exists() or not dogs_dir.exists():
        return []

    cat_images = list(cats_dir.glob("*.jpg"))
    dog_images = list(dogs_dir.glob("*.jpg"))

    if not cat_images or not dog_images:
        return []

    per_class = num_samples // 2
    selected_cats = random.sample(cat_images, min(per_class, len(cat_images)))
    selected_dogs = random.sample(dog_images, min(per_class, len(dog_images)))

    samples = [(str(p), "cat") for p in selected_cats] + [
        (str(p), "dog") for p in selected_dogs
    ]
    random.shuffle(samples)
    return samples


def generate_simulated_images(num_samples):
    """
    Generate simulated test images with known labels.

    Cats are represented by reddish images, dogs by bluish images.

    Args:
        num_samples: Number of samples to generate.

    Returns:
        List of (image_bytes, true_label) tuples.
    """
    samples = []
    per_class = num_samples // 2

    for i in range(per_class):
        # Simulated cat image (reddish)
        img = Image.new("RGB", (224, 224), color=(200 + random.randint(0, 55), 80, 80))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        samples.append((buf.getvalue(), "cat"))

    for i in range(per_class):
        # Simulated dog image (bluish)
        img = Image.new("RGB", (224, 224), color=(80, 80, 200 + random.randint(0, 55)))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        samples.append((buf.getvalue(), "dog"))

    random.shuffle(samples)
    return samples


def send_prediction_request(api_url, image_data, filename="test.jpg"):
    """
    Send an image to the prediction API.

    Args:
        api_url: Base URL of the deployed API.
        image_data: Image bytes.
        filename: Filename for the upload.

    Returns:
        Prediction result dict or None on failure.
    """
    try:
        response = requests.post(
            f"{api_url}/predict",
            files={"file": (filename, image_data, "image/jpeg")},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"  Error sending request: {e}")
        return None


def compute_metrics(true_labels, predicted_labels):
    """
    Compute classification metrics.

    Args:
        true_labels: List of true labels.
        predicted_labels: List of predicted labels.

    Returns:
        Dict with accuracy, precision, recall, f1, and confusion matrix.
    """
    classes = ["cat", "dog"]
    tp = {c: 0 for c in classes}
    fp = {c: 0 for c in classes}
    fn = {c: 0 for c in classes}

    correct = 0
    total = len(true_labels)

    for true, pred in zip(true_labels, predicted_labels):
        if true == pred:
            correct += 1
            tp[true] += 1
        else:
            fp[pred] += 1
            fn[true] += 1

    accuracy = correct / total if total > 0 else 0.0

    # Compute per-class and weighted metrics
    precision_vals = []
    recall_vals = []
    weights = []

    for c in classes:
        p = tp[c] / (tp[c] + fp[c]) if (tp[c] + fp[c]) > 0 else 0.0
        r = tp[c] / (tp[c] + fn[c]) if (tp[c] + fn[c]) > 0 else 0.0
        precision_vals.append(p)
        recall_vals.append(r)
        weights.append(tp[c] + fn[c])

    total_weight = sum(weights) if sum(weights) > 0 else 1
    precision = sum(p * w for p, w in zip(precision_vals, weights)) / total_weight
    recall = sum(r * w for r, w in zip(recall_vals, weights)) / total_weight
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    # Confusion matrix: rows = true, cols = predicted
    cm = {
        "cat": {"cat": tp["cat"], "dog": fn["cat"]},
        "dog": {"cat": fn["dog"], "dog": tp["dog"]},
    }

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": cm,
        "total_samples": total,
        "correct": correct,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate deployed Cats vs Dogs classifier"
    )
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8000",
        help="Base URL of the deployed API",
    )
    parser.add_argument(
        "--num-samples",
        type=int,
        default=50,
        help="Number of test samples to evaluate",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data/raw",
        help="Directory containing raw images (cats/ and dogs/ subdirectories)",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Post-Deployment Model Performance Evaluation")
    print("=" * 60)
    print(f"API URL: {args.url}")
    print(f"Requested samples: {args.num_samples}")

    # Step 1: Check API health
    print("\n[1/4] Checking API health...")
    try:
        health = requests.get(f"{args.url}/health", timeout=10)
        health.raise_for_status()
        health_data = health.json()
        print(f"  Status: {health_data.get('status', 'unknown')}")
        print(f"  Model loaded: {health_data.get('model_loaded', False)}")
        if not health_data.get("model_loaded", False):
            print("  ERROR: Model is not loaded. Cannot evaluate.")
            sys.exit(1)
    except requests.RequestException as e:
        print(f"  ERROR: Cannot reach API at {args.url}: {e}")
        sys.exit(1)

    # Step 2: Load test images
    print("\n[2/4] Loading test images...")
    use_real = False
    real_samples = get_real_test_images(args.data_dir, args.num_samples)

    if real_samples:
        print(f"  Using {len(real_samples)} real images from {args.data_dir}")
        use_real = True
    else:
        print(f"  No real images found in {args.data_dir}, generating simulated images")
        simulated = generate_simulated_images(args.num_samples)
        print(f"  Generated {len(simulated)} simulated test images")

    # Step 3: Send predictions
    print("\n[3/4] Sending prediction requests...")
    true_labels = []
    predicted_labels = []
    confidences = []

    if use_real:
        samples_to_process = real_samples
    else:
        samples_to_process = simulated

    for i, sample in enumerate(samples_to_process):
        if use_real:
            image_path, true_label = sample
            with open(image_path, "rb") as f:
                image_data = f.read()
            filename = os.path.basename(image_path)
        else:
            image_data, true_label = sample
            filename = f"simulated_{i}.jpg"

        result = send_prediction_request(args.url, image_data, filename)

        if result is not None:
            pred = result.get("prediction", "unknown")
            conf = result.get("confidence", 0.0)
            true_labels.append(true_label)
            predicted_labels.append(pred)
            confidences.append(conf)

            status = "correct" if pred == true_label else "WRONG"
            if (i + 1) % 10 == 0 or i == 0:
                print(
                    f"  [{i+1}/{len(samples_to_process)}] "
                    f"True: {true_label}, Pred: {pred}, "
                    f"Conf: {conf:.4f} ({status})"
                )

    if not true_labels:
        print("  ERROR: No successful predictions. Cannot compute metrics.")
        sys.exit(1)

    # Step 4: Compute and report metrics
    print(f"\n[4/4] Computing metrics ({len(true_labels)} successful predictions)...")
    metrics = compute_metrics(true_labels, predicted_labels)

    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    print(f"  Total samples evaluated: {metrics['total_samples']}")
    print(f"  Correct predictions:     {metrics['correct']}")
    print(f"  Accuracy:                {metrics['accuracy']:.4f}")
    print(f"  Precision (weighted):    {metrics['precision']:.4f}")
    print(f"  Recall (weighted):       {metrics['recall']:.4f}")
    print(f"  F1 Score (weighted):     {metrics['f1']:.4f}")
    print(f"  Average confidence:      {sum(confidences)/len(confidences):.4f}")

    print("\nConfusion Matrix:")
    print("                Predicted Cat  Predicted Dog")
    cm = metrics["confusion_matrix"]
    print(f"  Actual Cat       {cm['cat']['cat']:>5}          {cm['cat']['dog']:>5}")
    print(f"  Actual Dog       {cm['dog']['cat']:>5}          {cm['dog']['dog']:>5}")

    print("\n" + "=" * 60)
    data_source = "real images" if use_real else "simulated images"
    print(f"Evaluation complete using {data_source}.")
    print("=" * 60)


if __name__ == "__main__":
    main()
