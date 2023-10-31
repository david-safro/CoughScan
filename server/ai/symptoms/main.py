import torch
from torch.utils.data import DataLoader
from torch import nn
from data_preprocessing import load_and_preprocess_data
from dataset import CovidDataset
from model import CovidNet
from sklearn.metrics import accuracy_score
import pickle

# Load and preprocess data
X_train, X_test, y_train, y_test = load_and_preprocess_data()

# Hyperparameters
input_size = X_train.shape[1]
hidden_size = 50
num_classes = 2
num_epochs = 100
batch_size = 32
learning_rate = 0.001

# Create datasets and data loaders
train_dataset = CovidDataset(X_train, y_train)
test_dataset = CovidDataset(X_test, y_test)
train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

# Initialize the neural network, loss function, and optimizer
model = CovidNet(input_size, hidden_size, num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
for epoch in range(num_epochs):
    for i, (features, labels) in enumerate(train_loader):
        # Forward pass
        outputs = model(features)
        loss = criterion(outputs, labels)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (i + 1) % 100 == 0:
            print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{len(train_loader)}], Loss: {loss.item():.4f}')

# Test the model
model.eval()
with torch.no_grad():
    y_pred = []
    y_true = []
    for features, labels in test_loader:
        outputs = model(features)
        _, predicted = torch.max(outputs.data, 1)
        y_pred.extend(predicted.numpy())
        y_true.extend(labels.numpy())
    accuracy = accuracy_score(y_true, y_pred)
    print(f'Accuracy: {accuracy * 100:.2f}%')

# Save the model
with open('covid_model.pkl', 'wb') as file:
    pickle.dump(model, file)
