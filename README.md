# Voice Assistant

A professional, voice-controlled assistant built with Python, featuring advanced natural language processing, email integration, weather and news updates, and GPT-powered responses. This project is designed for easy setup and extensibility, making it ideal for both personal productivity and as a learning resource.

## Features

- **Voice Command Recognition:** Interact with the assistant using natural spoken language.
- **Weather Updates:** Get real-time weather information for any city using the OpenWeatherMap API.
- **News Headlines:** Hear the latest world news headlines via NewsAPI.
- **Email Integration:** Send emails and check your Gmail inbox using the Gmail API.
- **GPT Integration:** Ask questions or request jokes powered by OpenAI's GPT-3.5 Turbo.
- **Date & Time:** Ask for the current date and time.
- **Web Search:** Perform Google searches directly from your voice commands.
- **Text-to-Speech:** All responses are spoken back to you using text-to-speech.

## Demo

![Voice Assistant Demo](demo.gif)

## Getting Started

### Prerequisites
- Python 3.8+
- Microphone and speakers
- Google Cloud account for Gmail API
- API keys for OpenWeatherMap, NewsAPI, and OpenAI

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/voice-assistant.git
   cd OIBSIP_Task1
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Download PyAudio wheel (Windows only):**
   - If you encounter issues installing PyAudio, download a pre-built wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it with pip.

4. **Set up API keys:**
   - Copy `.env.example` to `.env` and fill in your API keys and credentials.
   - For Gmail, follow the steps below to obtain `credentials.json`.

### Gmail API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the Gmail API for your project.
4. Go to **APIs & Services > Credentials**.
5. Click **Create Credentials > OAuth client ID** (choose Desktop app).
6. Download the `credentials.json` file and place it in your project directory.
7. The assistant will use this file to authenticate and send/check emails via the Gmail API.

### Environment Variables

Create a `.env` file in the project root with the following keys:

```
OPENWEATHER_API_KEY=your_openweather_api_key
NEWSAPI_KEY=your_newsapi_key
OPENAI_API_KEY=your_openai_api_key
SENDER_EMAIL=your_gmail_address
DEFAULT_SUBJECT=Voice Assistant Email
```

## Usage

Run the assistant:
```bash
python main.py
```

Speak commands such as:
- "What's the weather in London?"
- "Send an email"
- "Check my inbox"
- "Tell me a joke"
- "What's the latest news?"
- "Search for Python tutorials"

## Project Structure

```
voice-assistant/
├── main.py           # Core assistant logic
├── requirements.txt  # Python dependencies
├── .env.example      # Example environment variables
├── README.md         # Project documentation
```

## Security Notes
- Never commit your `.env` file or API keys to version control.
- Keep your credentials private.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements or new features.

## License

This project is licensed under the MIT License.

## Acknowledgements
- [OpenWeatherMap](https://openweathermap.org/)
- [NewsAPI](https://newsapi.org/)
- [OpenAI](https://openai.com/)
- [Google Cloud Platform](https://cloud.google.com/)
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)