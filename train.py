import argparse
import torch
import torch.optim as optim
from src.model import AlexNet
from src.data import get_data_loaders
from src.trainer import Trainer


def main():
    parser = argparse.ArgumentParser(description="Train CNN on MNIST")
    parser.add_argument("--output_dir", type=str, default="./checkpoints",
                       help="Directory to save model checkpoints")
    parser.add_argument("--epochs", type=int, default=5,
                       help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=64,
                       help="Batch size for training")
    parser.add_argument("--lr", type=float, default=0.001,
                       help="Learning rate")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    model = AlexNet(num_classes=10).to(device)
    print("Model loaded: AlexNet")

    train_loader, test_loader = get_data_loaders(batch_size=args.batch_size)
    print(f"Data loaded with batch size: {args.batch_size}")

    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        test_loader=test_loader,
        optimizer=optimizer,
        device=device,
        output_dir=args.output_dir
    )

    print(f"Starting training for {args.epochs} epochs...")
    trainer.train(num_epochs=args.epochs)


if __name__ == "__main__":
    main()
