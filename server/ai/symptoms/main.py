import torch
import torch.nn as nn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import BorderlineSMOTE
import pickle
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

with open('modelv1ADAM.pkl', 'rb') as file:
    model = pickle.load(file)

model.eval()

with torch.no_grad():
    predictions = model(X_test_tensor)
    _, predicted = torch.max(predictions, 1)
    accuracy = accuracy_score(y_test_tensor, predicted)
    report = classification_report(y_test_tensor, predicted)
    conf_matrix = confusion_matrix(y_test_tensor, predicted)

print(f"Accuracy: {accuracy}")
print(f"Classification Report: \n{report}")
print(f"Confusion Matrix: \n{conf_matrix}")


def predict(input_data):
    model = pickle.load('modelv1ADAM.pkl')
    input_tensor = torch.FloatTensor([input_data])
    model.eval()
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted_class = torch.max(output, 1)

    return predicted_class.item()

# sample data cuz too lazy to read from data
input_data = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
predicted_severity = predict(input_data)
print(f"Predicted Severity: {predicted_severity}")



