import pandas as pd
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from ..ai.symptoms.main import predict
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


#ROUTE TO RECEIVE SYMPTOM DATA AND RETURN PREDICTION (0-3)
@app.route('/predict_symptoms', methods=['POST'])
def predict():
    try:
        data = request.json
        input_data = [
                    data['fever'],
                    data['tiredness'],
                    data['dryCough'],
                    data['difficultyInBreathing'],
                    data['soreThroat'],
                    data['pains'],
                    data['nasalCongestion'],
                    data['runnyNose'],
                    data['diarrhea'],
                    data['noneSymptom'],
                    data['noneExperiencing'],
                    1 if data['ageGroup'] == "0-9" else 0,
                    1 if data['ageGroup'] == "10-19" else 0,
                    1 if data['ageGroup'] == "20-24" else 0,
                    1 if data['ageGroup'] == "25-59" else 0,
                    1 if data['ageGroup'] == "60+" else 0,
                    1 if data['gender'] == "male" else 0,
                    1 if data['gender'] == "female" else 0,
                    1 if data['gender'] == "transgender" else 0,
                    1 if data['contactHistory'] == "dont-know" else 0,
                    1 if data['contactHistory'] == "no" else 0,
                    1 if data['contactHistory'] == "yes" else 0
                ]
        input_tensor = torch.FloatTensor([input_data])
        response = predict(input_tensor)
        return response, 200

    except Exception as e:
        response = jsonify({"error": str(e)})
        return response, 500
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
