import tempfile
import pandas as pd
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from server.ai.symptoms.predict import predict
from server.ai.cough.prediction import cough_predict
app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        print("Received audio data")
        audio_data = request.data

        with tempfile.NamedTemporaryFile(delete=True) as temp_audio_file:
            temp_audio_file.write(audio_data)
            temp_audio_file.flush()
            predicted_class, confidence = cough_predict(temp_audio_file.name, "../ai/cough/sounddr_data/output/covid_model_fold0.pkl")
            response = jsonify({
                "prediction": predicted_class,
                "confidence": f"{confidence * 100:.2f}%"
            })
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
        response = predict(input_tensor, "../ai/symptoms/modelv1ADAM.pkl")
        return response, 200

    except Exception as e:
        response = jsonify({"error": str(e)})
        return response, 500
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
