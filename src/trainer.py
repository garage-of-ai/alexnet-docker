import os
import torch
import torch.nn as nn
from tqdm import tqdm


class Trainer:
    def __init__(self, model, train_loader, test_loader, optimizer, device, output_dir):
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.optimizer = optimizer
        self.device = device
        self.output_dir = output_dir
        self.criterion = nn.CrossEntropyLoss()

        os.makedirs(output_dir, exist_ok=True)

    def train_epoch(self):
        self.model.train()
        total_loss = 0
        total_correct = 0
        total_samples = 0

        for images, labels in tqdm(self.train_loader, desc="Training"):
            images = images.to(self.device)
            labels = labels.to(self.device)

            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()

            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total_correct += (predicted == labels).sum().item()
            total_samples += labels.size(0)

        avg_loss = total_loss / len(self.train_loader)
        accuracy = 100 * total_correct / total_samples
        return avg_loss, accuracy

    def evaluate(self):
        self.model.eval()
        total_correct = 0
        total_samples = 0

        with torch.no_grad():
            for images, labels in tqdm(self.test_loader, desc="Evaluating"):
                images = images.to(self.device)
                labels = labels.to(self.device)

                outputs = self.model(images)
                _, predicted = torch.max(outputs.data, 1)
                total_correct += (predicted == labels).sum().item()
                total_samples += labels.size(0)

        accuracy = 100 * total_correct / total_samples
        return accuracy

    def train(self, num_epochs):
        for epoch in range(num_epochs):
            train_loss, train_acc = self.train_epoch()
            test_acc = self.evaluate()

            print(f"Epoch {epoch+1}/{num_epochs}")
            print(f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
            print(f"  Test Acc: {test_acc:.2f}%")

            checkpoint_path = os.path.join(self.output_dir, f"model_epoch_{epoch+1}.pt")
            torch.save(self.model.state_dict(), checkpoint_path)

        final_checkpoint = os.path.join(self.output_dir, "model.pt")
        torch.save(self.model.state_dict(), final_checkpoint)
        print(f"\nTraining complete. Model saved to {final_checkpoint}")
