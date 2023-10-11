import pickle

import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import BorderlineSMOTE
from model import Net
df = pd.read_csv('data/Cleaned-Data.csv')
df = df.drop(columns=['Country'])

df['Severity'] = df['Severity_None'] * 0 + df['Severity_Mild'] * 1 + df['Severity_Moderate'] * 2 + df[
    'Severity_Severe'] * 3
df = df.drop(columns=['Severity_None', 'Severity_Mild', 'Severity_Moderate', 'Severity_Severe'])

X = df.drop(columns=['Severity']).values
y = df['Severity'].values

scaler = StandardScaler()
X = scaler.fit_transform(X)

smote = BorderlineSMOTE(random_state=42)
X, y = smote.fit_resample(X, y)

X_train, X_val_test, y_train, y_val_test = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_val_test, y_val_test, test_size=0.5, random_state=42)

X_train_tensor = torch.FloatTensor(X_train)
y_train_tensor = torch.LongTensor(y_train)
X_val_tensor = torch.FloatTensor(X_val)
y_val_tensor = torch.LongTensor(y_val)
X_test_tensor = torch.FloatTensor(X_test)
y_test_tensor = torch.LongTensor(y_test)



model = Net(X_train)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=10, factor=0.5)

clip_value = 1
for p in model.parameters():
    p.register_hook(lambda grad: torch.clamp(grad, -clip_value, clip_value))

patience = 20
best_val_loss = float('inf')
counter = 0

epochs = 300
for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()

    val_outputs = model(X_val_tensor)
    val_loss = criterion(val_outputs, y_val_tensor)

    scheduler.step(val_loss)

    print(f"Epoch {epoch + 1}/{epochs}, Training Loss: {loss.item()}, Validation Loss: {val_loss.item()}")

    if val_loss < best_val_loss:
        best_val_loss = val_loss
        counter = 0
    else:
        counter += 1
        if counter >= patience:
            print("Early stopping triggered.")
            break
accuracy = 0
model.eval()
with torch.no_grad():
    predictions = model(X_test_tensor)
    _, predicted = torch.max(predictions, 1)
    accuracy += accuracy_score(y_test_tensor, predicted)
    report = classification_report(y_test_tensor, predicted)
    conf_matrix = confusion_matrix(y_test_tensor, predicted)

print(f"Accuracy: {accuracy}")
print(f"Classification Report: \n{report}")
print(f"Confusion Matrix: \n{conf_matrix}")
#for saving wnb stuff
#with open('modelv1ADAM.pkl', 'wb') as file:
#    pickle.dump(model, file)

print("Model saved to trained_model.pkl")