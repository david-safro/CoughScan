import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from ..ai.symptoms.covidSymptoms import NeuralNetwork
relevant_features = ['Breathing Problem', 'Fever', 'Dry Cough', 'Sore throat', 'Abroad travel',
                     'Contact with COVID Patient', 'Visited Public Exposed Places', 'Wearing Masks',
                     'Sanitization from Market', 'Fatigue ']
nn = NeuralNetwork(relevant_features)

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        print("Received audio data")
        audio_data = request.data
        with open('received_audio.webm', 'wb') as audio_file:
            audio_file.write(audio_data)

        response = jsonify({"message": "Audio data received and saved successfully."})
        return response, 200
    except Exception as e:
        response = jsonify({"error": str(e)})
        return response, 500
@app.route('/predict_symptoms', methods=['POST'])
def predict():
    data = request.get_json()
    symptoms = {
        'Breathing Problem': data.get('Breathing Problem', 0),
        'Fever': data.get('Fever', 0),
        'Dry Cough': data.get('Dry Cough', 0),
        'Sore throat': data.get('Sore throat', 0),
        'Abroad travel': data.get('Abroad travel', 0),
        'Contact with COVID Patient': data.get('Contact with COVID Patient', 0),
        'Visited Public Exposed Places': data.get('Visited Public Exposed Places', 0),
        'Wearing Masks': data.get('Wearing Masks', 0),
        'Sanitization from Market': data.get('Sanitization from Market', 0),
        'Fatigue ': data.get('Fatigue ', 0)
    }

    prediction_proba = nn.predict_proba(pd.DataFrame([symptoms]))
    confidence = float(prediction_proba[0][1])
    prediction = {
        'prediction': prediction_proba[0][1] > 0.5,
        'confidence': confidence
    }

    return jsonify(prediction)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
