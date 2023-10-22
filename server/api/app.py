import os
import tempfile
import traceback

import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from server.ai.symptoms.predict import predict_symptoms
from server.ai.cough.prediction import cough_predict
app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        print("Received audio data")
        audio_data = request.data

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_data)
            temp_audio_file.flush()
            temp_audio_file.seek(0)  # Rewind the file pointer

            print("tempfile created")
            predicted_class, confidence = cough_predict(temp_audio_file.name, "../ai/cough/sounddr_data/output/covid_model_fold0.pkl")
            print("response received")

            # Explicitly close the temporary audio file
            temp_audio_file.close()

            # Clean up the temporary audio file
            os.remove(temp_audio_file.name)

            response = jsonify({
                "prediction": predicted_class,
                "confidence": f"{confidence * 100:.2f}%"
            })
            print("sent")
            return response, 200

    except Exception as e:
        response = jsonify({"error": str(e)})
        print(traceback.format_exc())
        print(str(e))
        return response, 500
#ROUTE TO RECEIVE SYMPTOM DATA AND RETURN PREDICTION (0-3)
@app.route('/predict_symptoms', methods=['POST'])
def predict():
    try:
        data = request.json
        print(data)
        input_data = [
                    data['fever'],
                    data['tiredness'],
                    data['dryCough'],
                    data['breathingDifficulty'],
                    data['soreThroat'],
                    data['pains'],
                    data['nasalCongestion'],
                    data['runnyNose'],
                    data['diarrhea'],
                    data['noSymptoms'],
                    data['noneExperiencing'],
                    1 if data['ageRange'] == "0-9" else 0,
                    1 if data['ageRange'] == "10-19" else 0,
                    1 if data['ageRange'] == "20-24" else 0,
                    1 if data['ageRange'] == "25-59" else 0,
                    1 if data['ageRange'] == "60+" else 0,
                    1 if data['gender'] == "male" else 0,
                    1 if data['gender'] == "female" else 0,
                    1 if data['gender'] == "other" else 0,
                    1 if data['history'] == "dont-know" else 0,
                    1 if data['history'] == "no" else 0,
                    1 if data['history'] == "yes" else 0
                ]
        print(input_data)
        symptom_prediction = predict_symptoms(input_data, "../ai/symptoms/modelv1ADAM.pkl")
        response = jsonify({
            "diagnosis": symptom_prediction[0],
            "certainty":symptom_prediction[1]
        })
        print("success")
        return response, 200

    except Exception as e:
        response = jsonify({"error": str(e)})
        print(traceback.format_exc())
        print(str(e))
        return response, 500
if __name__ == ('__main__'):
    app.run(host='127.0.0.1', port=5000)
