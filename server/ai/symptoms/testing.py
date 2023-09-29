import pandas as pd

from covidSymptoms import NeuralNetwork

relevant_features = ['Breathing Problem', 'Fever', 'Dry Cough', 'Sore throat', 'Abroad travel',
                     'Contact with COVID Patient', 'Visited Public Exposed Places', 'Wearing Masks',
                     'Sanitization from Market', 'Fatigue ']
nn = NeuralNetwork(relevant_features)

sample_datasets = [
    {
        'Breathing Problem': 1,
        'Fever': 1,
        'Dry Cough': 1,
        'Sore throat': 0,
        'Abroad travel': 1,
        'Contact with COVID Patient': 1,
        'Visited Public Exposed Places': 1,
        'Wearing Masks': 1,
        'Sanitization from Market': 1,
        'Fatigue ': 1
    },
    {
        'Breathing Problem': 0,
        'Fever': 1,
        'Dry Cough': 1,
        'Sore throat': 1,
        'Abroad travel': 0,
        'Contact with COVID Patient': 0,
        'Visited Public Exposed Places': 1,
        'Wearing Masks': 0,
        'Sanitization from Market': 1,
        'Fatigue ': 1
    },
]

for idx, dataset in enumerate(sample_datasets, start=1):
    print(f"Testing dataset {idx}:")
    print("Symptoms:", dataset)
    prediction_proba = nn.predict_proba(pd.DataFrame([dataset]))
    confidence = prediction_proba[0][1] * 100

    print('Prediction:', 'Yes' if prediction_proba[0][1] > 0.5 else 'No')
    print('Confidence Percentage:', confidence)
    print()
