from flask import Flask, request, jsonify
from pydub import AudioSegment
import numpy as np
import os
import json

app = Flask(__name__)

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://100.14.234.50'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/upload', methods=['POST'])
def upload():
    try:
        audio_data = request.data

        with open('received_audio.webm', 'wb') as audio_file:
            audio_file.write(audio_data)

        audio = AudioSegment.from_file('received_audio.webm', format='webm')
        duration = len(audio)

        audio.play()

        metadata = {
            "duration_ms": duration,
            "channels": audio.channels,
            "frame_rate": audio.frame_rate,
        }

        with open('metadata.json', 'w') as metadata_file:
            json.dump(metadata, metadata_file)

        response = jsonify({"message": "audio worked on ur end"})
        return add_cors_headers(response), 200

    except Exception as e:
        response = jsonify({"error": str(e)})
        return add_cors_headers(response), 500

@app.route('/waveform', methods=['GET'])
def waveform():
    try:
        audio = AudioSegment.from_file('received_audio.webm', format='webm')
        samples = np.array(audio.get_array_of_samples())
        duration = len(audio)
        time_points = np.linspace(0, duration, len(samples))

        waveform_data = [{"time": t, "amplitude": s} for t, s in zip(time_points, samples)]

        response = jsonify({"waveform_data": waveform_data})
        return add_cors_headers(response), 200

    except Exception as e:
        response = jsonify({"error": str(e)})
        return add_cors_headers(response), 500

if __name__ == '__main__':
    app.run(host='143.42.118.185', port=5000)
