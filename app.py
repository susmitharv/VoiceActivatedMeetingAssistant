# Voice-Activated Meeting Assistant (Flask + spaCy + Vosk STT)

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import json
import spacy
import wave
import subprocess
from vosk import Model, KaldiRecognizer
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Load Vosk model
MODEL_PATH = "model"
if not os.path.exists(MODEL_PATH):
    raise EnvironmentError("Please download a Vosk model from https://alphacephei.com/vosk/models and unzip it to a folder named 'model'")

vosk_model = Model(MODEL_PATH)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# NLP: Extract action items and decisions
def extract_key_points(text):
    doc = nlp(text)
    action_items = []
    decisions = []
    for sent in doc.sents:
        if any(w.lemma_ in ["assign", "complete", "submit", "schedule"] for w in sent):
            action_items.append(sent.text)
        elif any(w.lemma_ in ["agree", "approve", "decide"] for w in sent):
            decisions.append(sent.text)
    return action_items, decisions

# Transcribe using Vosk
def transcribe_audio(audio_path):
    wf = wave.open(audio_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 44100]:
        raise ValueError("Audio must be WAV format, mono PCM, and 16-bit")

    rec = KaldiRecognizer(vosk_model, wf.getframerate())
    rec.SetWords(True)

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            results.append(res.get("text", ""))
    final_res = json.loads(rec.FinalResult())
    results.append(final_res.get("text", ""))

    return " ".join(results)

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        transcript = transcribe_audio(filepath)
        action_items, decisions = extract_key_points(transcript)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return render_template_string(RESULT_TEMPLATE,
                                  transcript=transcript,
                                  action_items=action_items,
                                  decisions=decisions)

@app.route("/")
def home():
    return render_template_string(UPLOAD_TEMPLATE)

UPLOAD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Meeting Assistant</title></head>
<body>
<h2>Upload WAV File</h2>
<form action="/upload" method="post" enctype="multipart/form-data">
    <input type="file" name="file" accept="audio/wav" required>
    <button type="submit">Upload and Transcribe</button>
</form>
</body>
</html>
'''

RESULT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Transcription Result</title></head>
<body>
<h2>Transcript</h2>
<p>{{ transcript }}</p>
<h3>Action Items</h3>
<ul>
  {% for item in action_items %}<li>{{ item }}</li>{% endfor %}
</ul>
<h3>Decisions</h3>
<ul>
  {% for decision in decisions %}<li>{{ decision }}</li>{% endfor %}
</ul>
<a href="/">Back to Upload</a>
</body>
</html>
'''

if __name__ == "__main__":
    app.run(debug=True)
