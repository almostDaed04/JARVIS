# JARVIS

JARVIS is a Python-based personal assistant capable of speech recognition, text-to-speech, AI responses, and performing simple tasks like opening applications and searching the web.

---

## Installation

Follow these steps to set up JARVIS:

1. **Clone the repository:**
```bash
git clone https://github.com/almostDaed04/JARVIS.git
cd JARVIS
```

2. **Create a virtual environment:**
```bash
python3 -m venv venv
```

3. **Activate the virtual environment:**
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. **Install all required Python modules and libraries:**
```bash
pip install -r requirements.txt
```

---

## Dependencies

All dependencies are installed via `requirements.txt`. Major external libraries include:

- **SpeechRecognition** – for recognizing voice commands
- **pygame** – for audio playback
- **gTTS** – Google Text-to-Speech
- **pyautogui** – GUI automation
- **requests** – making HTTP requests
- **wikipedia** – searching and retrieving info from Wikipedia

Standard Python libraries like `os`, `sys`, `datetime`, `threading`, `time`, `queue`, `subprocess`, `tempfile`, and `webbrowser` are built-in and do not require installation.

### requirements.txt
```
SpeechRecognition>=3.11.0
pygame>=2.4.0
gTTS>=2.4.0
pyautogui>=0.9.55
requests>=2.31.0
wikipedia>=1.4.0
```

---

## Usage

After setting up the environment and installing dependencies, run the main program:

```bash
python main.py
```

Activation
To activate JARVIS, first say:
```
Wake up JARVIS
```

### Example Commands

You can give JARVIS commands like:
- "Hey JARVIS, what's the weather?"
- "Play song on YouTube"
- "Tell me a joke"
- "Search Google for AI news"

---

## Features

- 🎤 Speech recognition for interactive commands
- 🗣️ Text-to-speech output
- 🤖 Basic AI responses
- 🚀 Open applications and websites
- 🔧 Modular and easily extendable

---

## License

This project is licensed under the MIT License.

---

## Author

**almostDaed04**

⭐ Star this repo if you find it helpful!
