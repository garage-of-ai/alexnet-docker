import argparse
import torch
from sklearn.metrics import classification_report, accuracy_score
from src.model import AlexNet
from src.data import get_data_loaders


def evaluate_model(checkpoint_path, batch_size=64):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    model = AlexNet(num_classes=10).to(device)
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()
    print(f"Model loaded from {checkpoint_path}")

    _, test_loader = get_data_loaders(batch_size=batch_size)

    all_predictions = []
    all_labels = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            all_predictions.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())

    accuracy = accuracy_score(all_labels, all_predictions)
    print(f"\nOverall Accuracy: {accuracy * 100:.2f}%")

    print("\nClassification Report:")
    print(classification_report(all_labels, all_predictions,
                              target_names=[str(i) for i in range(10)]))


def main():
    parser = argparse.ArgumentParser(description="Evaluate CNN on MNIST test set")
    parser.add_argument("--checkpoint", type=str, required=True,
                       help="Path to model checkpoint")
    parser.add_argument("--batch_size", type=int, default=64,
                       help="Batch size for evaluation")
    args = parser.parse_args()

    evaluate_model(checkpoint_path=args.checkpoint, batch_size=args.batch_size)


if __name__ == "__main__":
    main()
