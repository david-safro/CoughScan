import pickle
import torch
from server.ai.symptoms.symptom_model import SymNet


def predict(input_data, filename):
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    input_tensor = torch.FloatTensor([input_data])
    model.eval()
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted_class = torch.max(output, 1)
    return predicted_class.item()

# sample data cuz too lazy to read from data
#input_data = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
#predicted_severity = predict(input_data,"modelv1ADAM.pkl")
#print(f"Predicted Severity: {predicted_severity}")
