import os
import tempfile
import traceback

import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from server.ai.symptoms.predict import predict_symptoms
from server.ai.cough.prediction import cough_predict
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
print("STARTED")
@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        print("Received audio data")
        audio_data = request.data

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_data)
            temp_audio_file.flush()
            temp_audio_file.seek(0)  # Rewind the file pointer

            print("tempfile created")
            predicted_class, confidence = cough_predict(temp_audio_file.name, "server/ai/cough/sounddr_data/output/covid_model_fold0.pkl")
            print("response received")

            # Explicitly close the temporary audio file
            temp_audio_file.close()

            # Clean up the temporary audio file
            os.remove(temp_audio_file.name)
            print(predicted_class, confidence)
            response = jsonify({
                "diagnosis": bool(predicted_class),
                "certainty": round(confidence * 100, 2)
            })
            print("sent")
            print("response sent: ",response)
            return response, 200

    except Exception as e:
        response = jsonify({"error": str(e)})
        print(traceback.format_exc())
        print(str(e))
        return response, 500
#ROUTE TO RECEIVE SYMPTOM DATA AND RETURN PREDICTION (0-3)
@app.route('/api/predict_symptoms', methods=['POST'])
def predict():
    try:
        data = request.json

        symptom_prediction = predict_symptoms(data, "server/ai/symptoms/covid_model.pkl")
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
    app.run(host='0.0.0.0', port=5000, debug=False, ssl_context=('/etc/letsencrypt/live/coughscan.net/fullchain.pem', '/etc/letsencrypt/live/coughscan.net/privkey.pem'))

