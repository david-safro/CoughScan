import json
import pickle
import torch
from torch import nn
import sys
sys.path.append('/root/CoughScan/server/ai/symptoms')
from server.ai.symptoms.model import CovidNet
def symptom_predict(input_json, model_path='covid_model.pkl'):
    feature_columns = [
        'breathing', 'fever', 'dry-cough', 'sore-throat', 'running-nose',
        'asthma', 'chronic-lung', 'headache', 'heart-disease', 'diabetes',
        'fatigue', 'gastrointestinal', 'abroad-travel', 'contact-covid',
        'large-gathering', 'public-places', 'family-public', 'masks', 'sanitization', 'Hyper Tension'
    ]
    loaded_model = torch.load(model_path, map_location=torch.device('cpu'))
    input_dict = input_json
    input_dict['sanitization'] = 1
    input_dict['Hyper Tension'] = 1
    input_values = [input_dict.get(col, 0) for col in feature_columns]
    input_tensor = torch.tensor(input_values, dtype=torch.float32).unsqueeze(0)

    loaded_model.eval()
    with torch.no_grad():
        output = loaded_model(input_tensor)
        _, predicted = torch.max(output.data, 1)
        confidence = torch.nn.functional.softmax(output, dim=1)[0][predicted].item()

    prediction = bool(predicted.item())
    return prediction, round(confidence*100, 2)
