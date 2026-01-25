"""
Training script for Cats vs Dogs classification model.
Includes MLflow experiment tracking.
"""

import argparse
import os
from pathlib import Path
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import mlflow
import mlflow.pytorch
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np

from src.models.cnn_model import create_model
from src.data.preprocessing import (
    load_image_paths, 
    preprocess_images, 
    create_data_loaders
)


def train_epoch(model, train_loader, criterion, optimizer, device):
    """Train for one epoch."""
    model.train()
    running_loss = 0.0
    all_preds = []
    all_labels = []
    
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        
        # Forward pass
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        # Statistics
        running_loss += loss.item()
        _, preds = torch.max(outputs, 1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
    
    epoch_loss = running_loss / len(train_loader)
    epoch_acc = accuracy_score(all_labels, all_preds)
    
    return epoch_loss, epoch_acc


def validate(model, val_loader, criterion, device):
    """Validate the model."""
    model.eval()
    running_loss = 0.0
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    epoch_loss = running_loss / len(val_loader)
    epoch_acc = accuracy_score(all_labels, all_preds)
    precision = precision_score(all_labels, all_preds, average='weighted')
    recall = recall_score(all_labels, all_preds, average='weighted')
    f1 = f1_score(all_labels, all_preds, average='weighted')
    cm = confusion_matrix(all_labels, all_preds)
    
    return epoch_loss, epoch_acc, precision, recall, f1, cm


def train(
    raw_data_dir: str,
    processed_data_dir: str,
    model_save_dir: str,
    num_epochs: int = 10,
    batch_size: int = 32,
    learning_rate: float = 0.001,
    experiment_name: str = "cats_dogs_classification"
):
    """
    Main training function with MLflow tracking.
    
    Args:
        raw_data_dir: Directory containing raw images
        processed_data_dir: Directory for processed images
        model_save_dir: Directory to save trained model
        num_epochs: Number of training epochs
        batch_size: Batch size
        learning_rate: Learning rate
        experiment_name: MLflow experiment name
    """
    # Setup device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Create directories
    Path(processed_data_dir).mkdir(parents=True, exist_ok=True)
    Path(model_save_dir).mkdir(parents=True, exist_ok=True)
    
    # Preprocess data
    print("Preprocessing images...")
    train_paths, val_paths, test_paths = preprocess_images(
        raw_data_dir=raw_data_dir,
        processed_data_dir=processed_data_dir,
        target_size=(224, 224)
    )
    
    # Load labels
    train_labels = [0 if 'cats' in p else 1 for p in train_paths]
    val_labels = [0 if 'cats' in p else 1 for p in val_paths]
    test_labels = [0 if 'cats' in p else 1 for p in test_paths]
    
    # Create data loaders
    print("Creating data loaders...")
    train_loader, val_loader, test_loader = create_data_loaders(
        train_paths, val_paths, test_paths,
        train_labels, val_labels, test_labels,
        batch_size=batch_size
    )
    
    # Create model
    model = create_model(num_classes=2)
    model.to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # MLflow setup
    mlflow.set_experiment(experiment_name)
    
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("num_epochs", num_epochs)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("model_type", "SimpleCNN")
        mlflow.log_param("train_samples", len(train_paths))
        mlflow.log_param("val_samples", len(val_paths))
        mlflow.log_param("test_samples", len(test_paths))
        
        # Training loop
        best_val_acc = 0.0
        train_losses = []
        val_losses = []
        train_accs = []
        val_accs = []
        
        print("Starting training...")
        for epoch in range(num_epochs):
            # Train
            train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
            
            # Validate
            val_loss, val_acc, val_precision, val_recall, val_f1, val_cm = validate(
                model, val_loader, criterion, device
            )
            
            train_losses.append(train_loss)
            val_losses.append(val_loss)
            train_accs.append(train_acc)
            val_accs.append(val_acc)
            
            # Log metrics
            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("train_accuracy", train_acc, step=epoch)
            mlflow.log_metric("val_loss", val_loss, step=epoch)
            mlflow.log_metric("val_accuracy", val_acc, step=epoch)
            mlflow.log_metric("val_precision", val_precision, step=epoch)
            mlflow.log_metric("val_recall", val_recall, step=epoch)
            mlflow.log_metric("val_f1", val_f1, step=epoch)
            
            print(f"Epoch [{epoch+1}/{num_epochs}]")
            print(f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
            print(f"  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
            
            # Save best model
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                model_path = Path(model_save_dir) / "best_model.pt"
                torch.save(model.state_dict(), model_path)
                mlflow.log_artifact(str(model_path), "model")
                print(f"  Saved best model with val_acc: {val_acc:.4f}")
        
        # Log confusion matrix
        import matplotlib.pyplot as plt
        plt.figure(figsize=(8, 6))
        plt.imshow(val_cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Validation Confusion Matrix')
        plt.colorbar()
        tick_marks = np.arange(2)
        plt.xticks(tick_marks, ['Cat', 'Dog'])
        plt.yticks(tick_marks, ['Cat', 'Dog'])
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        
        # Add text annotations
        thresh = val_cm.max() / 2.
        for i, j in np.ndindex(val_cm.shape):
            plt.text(j, i, format(val_cm[i, j], 'd'),
                    horizontalalignment="center",
                    color="white" if val_cm[i, j] > thresh else "black")
        
        cm_path = Path(model_save_dir) / "confusion_matrix.png"
        plt.savefig(cm_path)
        plt.close()
        mlflow.log_artifact(str(cm_path), "artifacts")
        
        # Test evaluation
        print("Evaluating on test set...")
        test_loss, test_acc, test_precision, test_recall, test_f1, test_cm = validate(
            model, test_loader, criterion, device
        )
        
        mlflow.log_metric("test_accuracy", test_acc)
        mlflow.log_metric("test_precision", test_precision)
        mlflow.log_metric("test_recall", test_recall)
        mlflow.log_metric("test_f1", test_f1)
        
        print(f"Test Results:")
        print(f"  Accuracy: {test_acc:.4f}")
        print(f"  Precision: {test_precision:.4f}")
        print(f"  Recall: {test_recall:.4f}")
        print(f"  F1: {test_f1:.4f}")
        
        # Log model
        mlflow.pytorch.log_model(model, "model")
        
        print(f"\nTraining complete! Best validation accuracy: {best_val_acc:.4f}")
        print(f"Model saved to: {model_save_dir}/best_model.pt")
        print(f"MLflow run: {mlflow.active_run().info.run_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Cats vs Dogs classifier")
    parser.add_argument("--raw_data_dir", type=str, default="data/raw",
                        help="Directory containing raw images")
    parser.add_argument("--processed_data_dir", type=str, default="data/processed",
                        help="Directory for processed images")
    parser.add_argument("--model_save_dir", type=str, default="models",
                        help="Directory to save trained model")
    parser.add_argument("--num_epochs", type=int, default=10,
                        help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=32,
                        help="Batch size")
    parser.add_argument("--learning_rate", type=float, default=0.001,
                        help="Learning rate")
    parser.add_argument("--experiment_name", type=str, default="cats_dogs_classification",
                        help="MLflow experiment name")
    
    args = parser.parse_args()
    
    train(
        raw_data_dir=args.raw_data_dir,
        processed_data_dir=args.processed_data_dir,
        model_save_dir=args.model_save_dir,
        num_epochs=args.num_epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        experiment_name=args.experiment_name
    )

