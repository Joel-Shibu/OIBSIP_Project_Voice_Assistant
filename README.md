# Voice Assistant (Beginner Level)

## Overview
A simple voice-controlled assistant that responds to greetings, tells the current time and date, and performs web searches based on your voice commands.

## Features
- Responds to basic greetings (e.g., "Hello")
- Tells the current time and date
- Searches the web for queries (e.g., "Search Python tutorials")

## Requirements
- Python 3.x
- Libraries listed in `requirements.txt`

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the assistant:
   ```bash
   python main.py
   ```

## Security Notes
- Use a `.env` file for any API keys or credentials (not needed for this beginner phase)
- Do not store personal data unless encrypted
- Implement access control for sensitive tasks (future phases)

## Folder Structure
```
voice-assistant/
│
├── main.py                # Core voice assistant logic
├── requirements.txt       # List of libraries
└── README.md              # Project overview and instructions
```