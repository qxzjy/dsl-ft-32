import os
import tempfile
import torch
from ray import train, tune
from ray.tune.search.optuna import OptunaSearch
from torchvision.datasets import MNIST
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.nn import CrossEntropyLoss
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision.models import resnet18
from torchvision.transforms import ToTensor, Normalize, Compose


def objective(config):  # ①
    # Data
    transform = Compose([ToTensor(), Normalize((0.5,), (0.5,))])
    data_dir = os.path.join(tempfile.gettempdir(), "data")
    train_data = MNIST(root=data_dir, train=True, download=True, transform=transform)
    train_loader = DataLoader(train_data, batch_size=128, shuffle=True)
    test_data = MNIST(root=data_dir, train=False, download=True, transform=transform)
    test_loader = DataLoader(test_data, batch_size=128, shuffle=True)

    # MODEL
    # Define the CNN architecture
    class CNN(nn.Module):
        def __init__(self, units):
            super(CNN, self).__init__()
            # First convolutional layer: 1 input channel (grayscale), 32 output channels, 3x3 kernel
            self.conv1 = nn.Conv2d(1, units, kernel_size=3, stride=1, padding=1)
            # Second convolutional layer: 32 input channels, 64 output channels, 3x3 kernel
            self.conv2 = nn.Conv2d(units, units*2, kernel_size=3, stride=1, padding=1)
            # Fully connected layer 1 (after flattening): input 7*7*64, output 128
            self.fc1 = nn.Linear(units*2 * 7 * 7, 128)
            # Fully connected layer 2: input 128, output 10 (for 10 classes)
            self.fc2 = nn.Linear(128, 10)
            # Max pooling layer
            self.pool = nn.MaxPool2d(2, 2)
            # Dropout layer to prevent overfitting
            self.dropout = nn.Dropout(0.25)

        def forward(self, x):
            # Apply first conv layer + ReLU + max pool
            x = self.pool(F.relu(self.conv1(x)))
            # Apply second conv layer + ReLU + max pool
            x = self.pool(F.relu(self.conv2(x)))
            # Flatten the output for the fully connected layers
            x = x.view(-1, self.conv2.out_channels * 7 * 7)
            # Apply dropout, first fully connected layer + ReLU
            x = F.relu(self.fc1(x))
            x = self.dropout(x)
            # Output layer (no activation function for the output, since we'll apply CrossEntropyLoss)
            x = self.fc2(x)
            return x

    # Initialize the model, loss function, and optimizer
    model = CNN(units=config["units"]).to("cpu")  # Create a PyTorch conv net
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())

    # Training the model
    def train_model(num_epochs):
        model.train()
        for epoch in range(num_epochs):
            running_loss = 0.0
            for images, labels in train_loader:
                # Zero the gradients
                optimizer.zero_grad()
                # Forward pass
                outputs = model(images)
                # Compute the loss
                loss = criterion(outputs, labels)
                # Backpropagation
                loss.backward()
                # Opt imize
                optimizer.step()
                running_loss += loss.item()
            
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}')

    # Testing the model
    def test_model():
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in test_loader:
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        return correct / total
    
        print(f'Test Accuracy: {100 * correct / total:.2f}%')

    while True:
        train_model(1)  # Train the model
        acc = test_model()  # Compute test accuracy
        train.report({"mean_accuracy": acc})  # Report to Tune


search_space = {"units": tune.grid_search([8, 22, 64])}
#algo = OptunaSearch()  # ②

tuner = tune.Tuner(  # ③
    objective,
    tune_config=tune.TuneConfig(
        metric="mean_accuracy",
        mode="max",
        #search_alg=algo
    ),
    run_config=train.RunConfig(
        stop={"training_iteration": 100},
    ),
    param_space=search_space,
)
results = tuner.fit()
print("Best config is:", results.get_best_result().config)