import pickle
import torch
from server.ai.symptoms.symptom_model import SymNet
from torch.nn.functional import softmax


def predict_symptoms(input_data, filename):
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    input_tensor = torch.FloatTensor([input_data])
    model.eval()
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = softmax(output, dim=1)
        _, predicted_class = torch.max(probabilities, 1)
        confidence = round(probabilities[0, predicted_class.item()].item() * 100, 2)
    predicted_class = 0 if predicted_class.item() == 0 else 1
    return predicted_class, confidence
# sample data cuz too lazy to read from data
#input_data = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
#predicted_severity = predict(input_data,"modelv1ADAM.pkl")
#print(f"Predicted Severity: {predicted_severity}")
