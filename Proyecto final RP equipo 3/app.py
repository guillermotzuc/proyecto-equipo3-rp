from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import requests
import os

app = Flask(__name__)

# Configuración de la API de Bing
BING_API_KEY = '5b8b39d079e54f54bf4f48c8ca6cdf9c'
BING_ENDPOINT = 'https://api.bing.microsoft.com/v7.0/images/search'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio']
    audio_path = os.path.join('static/uploads', audio_file.filename)
    audio_file.save(audio_path)

    # Convertir el audio a un formato compatible si es necesario
    audio = AudioSegment.from_file(audio_path)
    audio.export("static/uploads/converted_audio.wav", format="wav")

    # Reconocimiento de voz
    recognizer = sr.Recognizer()
    with sr.AudioFile("static/uploads/converted_audio.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language='es-ES')

    # Buscar imagen en Bing
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {"q": text, "license": "public", "imageType": "photo"}
    response = requests.get(BING_ENDPOINT, headers=headers, params=params)
    image_url = response.json()['value'][0]['contentUrl'] if response.json()['value'] else ""

    return jsonify({"text": text, "audio_path": audio_path, "image_url": image_url})

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    app.run(debug=True)
