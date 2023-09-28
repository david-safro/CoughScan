from flask import Flask, request, jsonify
from flask_cors import CORS

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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
