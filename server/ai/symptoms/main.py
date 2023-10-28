import json
import pickle

import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the CSV file into a DataFrame
file_path = 'covid.csv'
covid_data = pd.read_csv(file_path)

# Rename columns
new_column_names = {
    'Breathing Problem': 'breathing',
    'Fever': 'fever',
    'Dry Cough': 'dry-cough',
    'Sore throat': 'sore-throat',
    'Running Nose': 'running-nose',
    'Asthma': 'asthma',
    'Chronic Lung Disease': 'chronic-lung',
    'Headache': 'headache',
    'Heart Disease': 'heart-disease',
    'Diabetes': 'diabetes',
    'Fatigue ': 'fatigue',
    'Gastrointestinal ': 'gastrointestinal',
    'Abroad travel': 'abroad-travel',
    'Contact with COVID Patient': 'contact-covid',
    'Attended Large Gathering': 'large-gathering',
    'Visited Public Exposed Places': 'public-places',
    'Family working in Public Exposed Places': 'family-public',
    'Wearing Masks': 'masks',
    'Sanitization from Market': 'sanitization',
    'COVID-19': 'covid-19'
}
covid_data = covid_data.rename(columns=new_column_names)

# Convert categorical values to numerical values
covid_data = covid_data.replace({'Yes': 1, 'No': 0})

# Set target label and features
y = covid_data['covid-19']
X = covid_data.drop('covid-19', axis=1)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Check for and handle missing values
X_train = X_train.fillna(0)
X_test = X_test.fillna(0)

print(X_train.columns)
# Custom dataset class
class CovidDataset(Dataset):
    def __init__(self, features, labels):
        self.features = torch.tensor(features.values, dtype=torch.float32)
        self.labels = torch.tensor(labels.values, dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        return self.features[index], self.labels[index]


# Neural network class
class CovidNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(CovidNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.softmax(out)
        return out


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
#with open('covid_model.pkl', 'wb') as file:
 #   pickle.dump(model, file)


# Load the trained model from the .pkl file


# Define the predict function
def predict_symptoms(input_json, pkl):
    with open(pkl, 'rb') as file:
        loaded_model = pickle.load(file)
    # Convert input JSON to PyTorch tensor
    input_dict = json.loads(input_json)
    input_dict['sanitization'] = 1  # Add 'sanitization' feature with value 1
    input_values = [input_dict[col] for col in X_train.columns]
    input_tensor = torch.tensor(input_values, dtype=torch.float32).unsqueeze(0)

    # Make a prediction with the trained model
    loaded_model.eval()
    with torch.no_grad():
        output = loaded_model(input_tensor)
        _, predicted = torch.max(output.data, 1)
        confidence = torch.nn.functional.softmax(output, dim=1)[0][predicted].item()

    # Convert prediction to boolean and return with confidence
    prediction = bool(predicted.item())
    return prediction, confidence