import json
import pickle
import torch
from server.ai.symptoms.main import *


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