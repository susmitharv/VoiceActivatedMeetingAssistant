# VoiceActivatedMeetingAssistant

An AI-powered meeting assistant built with **Flask**, **spaCy**, and **Vosk** to automatically transcribe `.wav` meeting audio files, extract action items and decisions, and present the results via a simple web UI.

---

## 🚀 Features

- 🎙️ Offline speech-to-text with [Vosk](https://alphacephei.com/vosk/)
- 🧠 NLP using spaCy to extract:
  - **Action Items** (e.g., “assign”, “submit”)
  - **Decisions** (e.g., “approve”, “agree”)
- 🌐 Simple browser-based file upload interface
- 📄 Transcription results shown instantly after upload

---

## 🧰 Requirements

- Python 3.8 or above
- Virtual environment (recommended)
- [Vosk model](https://alphacephei.com/vosk/models)
- FFmpeg (optional, for MP3 → WAV conversion)

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/voice-meeting-assistant.git
cd voice-meeting-assistant
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate    # On Windows
# source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Download Vosk Model

Go to: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)

- Download: `vosk-model-small-en-us-0.15`
- Extract it and rename the folder to `model`
- Place it inside your project root:
  ```
  voice-meeting-assistant/
  ├── app.py
  ├── model/
  ```

---

## 🧪 Running the App

```bash
python app.py
```

Then open your browser and go to:

📍 `http://127.0.0.1:5000`

---

## 🎧 Upload Requirements

- Upload a **mono, 16-bit PCM WAV** file (recommended format for Vosk).
- You can use [Audacity](https://www.audacityteam.org/) or `ffmpeg` to convert if needed:

```bash
ffmpeg -i input.mp3 -ac 1 -ar 16000 -c:a pcm_s16le output.wav
```

---

## 📁 Project Structure

```
voice-meeting-assistant/
├── app.py                 # Flask + Vosk + spaCy backend
├── model/                 # Vosk model files (not committed)
├── uploads/               # Uploaded audio files
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 🙋 Support

If you encounter errors with `ffmpeg`, make sure it's added to your system PATH or configured in your script.

---

## 📜 License

MIT License
