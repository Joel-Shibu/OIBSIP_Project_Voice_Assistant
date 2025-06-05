# Voice Assistant (Advanced Level)

## Overview
A voice-controlled assistant with advanced features including NLP-based command interpretation, email sending, reminders, weather updates, smart home control, and integration with GPT-4.1 for general knowledge questions.

## Features
- Weather updates (OpenWeatherMap API)
- News updates (NewsAPI, optional; set `NEWSAPI_KEY` in `.env` and it will be used automatically in `main.py`)
- Send emails (Gmail API via google-auth and google-api-python-client)

## Gmail API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Enable the Gmail API for your project.
4. Go to **APIs & Services > Credentials**.
5. Click **Create Credentials** > **OAuth client ID** (choose Desktop app or Web app as appropriate).
6. Download the `credentials.json` file and place it in your project directory.
7. Install the required libraries:
   ```bash
   pip install google-auth google-api-python-client
   ```
8. The assistant will use this file to authenticate and send emails via the Gmail API.
- GPT responses (OpenAI API)

## Requirements
- Python 3.x
- Libraries listed in `requirements.txt`

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Download spaCy English model (if using spaCy):
   ```bash
   python -m spacy download en_core_web_sm
   ```
3. Create a `.env` file for API keys and credentials (see Security Notes).
4. Run the assistant:
   ```bash
   python main.py
   ```

## Security Notes
- Always store all API keys and credentials in a `.env` file (never commit this file)
- Keep your API keys private and never share them publicly

## Folder Structure
```
voice-assistant/
│
├── main.py                # Core voice assistant logic
├── requirements.txt       # List of libraries
└── README.md              # Project overview and instructions
```

## Additional Notes
- For PyAudio installation issues on Windows, use a pre-built wheel from [https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- For OpenWeatherMap and OpenAI, obtain API keys and add them to your `.env` file