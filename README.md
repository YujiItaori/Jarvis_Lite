Jarvis AI Assistant
====================

A voice-controlled personal assistant with web interface, combining speech recognition, natural language processing and web automation capabilities.

Features
--------
- Voice Commands: Speak naturally to interact with Jarvis
- Web Interface: Modern UI with dark/light mode
- Smart Features:
  * Wikipedia searches
  * Calculator
  * Jokes
  * Time/date information
  * Application launcher
  * Web browser control
- Fuzzy Matching: Understands variations of commands
- Conversation History: Keeps track of interactions
- Cross-platform: Works on Windows, macOS, and Linux

Installation
------------
1. Clone the repository:
   git clone https://github.com/YujiItaori/Jarvis_Lite.git
   cd Jarvis_Lite


2. Install dependencies:
   pip install -r requirements.txt

3. Install additional system dependencies:
   - For speech recognition: pyaudio (Windows/macOS) or python3-pyaudio (Linux)
   - For text-to-speech: espeak (Linux) or system voices (Windows/macOS)

Usage
-----
Run the application:
python app.py

Then open your browser to:
http://localhost:5000

Voice Commands Examples:
- "What time is it?"
- "Tell me a joke"
- "Open YouTube"
- "Search Wikipedia for artificial intelligence"
- "Calculate 45 times 3"

Keyboard Shortcuts:
- Ctrl+Space: Toggle voice listening
- Ctrl+D: Toggle dark mode
- Esc: Close settings panel

Project Structure
----------------
jarvis-ai/
├── app.py                # Flask web application
├── jarvis.py             # Core AI functionality
├── static/               # Web assets
│   └── style.css         # Stylesheet
├── templates/            # HTML templates
│   └── index.html        # Main interface
└── README.txt            # This file

Technologies Used
----------------
- Python 3.7+
- Flask (web framework)
- pyttsx3 (text-to-speech)
- SpeechRecognition (speech-to-text)
- FuzzyWuzzy (command matching)
- Wikipedia API (information lookup)

Contributing
------------
Contributions are welcome! Please open an issue or submit a pull request.

License
-------
This project is licensed under the MIT License.

Notes
-----
- For optimal performance, use Chrome browser and quality microphone
- Some features may require additional API keys (like weather services)
- Tested on Windows 10/11, macOS Big Sur+, and Ubuntu 20.04+


![Screenshot 2025-06-02 124615](https://github.com/user-attachments/assets/c04099a4-1dd3-4219-a95f-4666b5c246a6)
![Screenshot 2025-06-02 124642](https://github.com/user-attachments/assets/052986e9-995a-4567-a311-440bf76df63b)
![Screenshot 2025-06-02 124119](https://github.com/user-attachments/assets/f9f1fe2c-f985-44be-adc0-153d85b15e0e)
