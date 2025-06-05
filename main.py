import os
import requests
from dotenv import load_dotenv
import openai
from google.oauth2 import service_account
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
import json
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Load environment variables
load_dotenv()
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Path to your downloaded credentials.json
GMAIL_CREDENTIALS_FILE = 'credentials.json'
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
openai.api_key = OPENAI_API_KEY

def get_weather(city):
    if not OPENWEATHER_API_KEY:
        return "Weather API key not set."
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        desc = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"The weather in {city} is {desc} with a temperature of {temp}°C."
    else:
        return "Sorry, I couldn't fetch the weather."

def get_news(api_key, query="latest"):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&pageSize=3"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        if not articles:
            return "No news articles found."
        return '\n'.join([f"- {a['title']}" for a in articles])
    else:
        return "Sorry, I couldn't fetch the news."

def send_email(to, subject, body):
    """
    Send an email using the Gmail API. Requires credentials.json (OAuth 2.0 client ID) in the project directory.
    """
    try:
        credentials = service_account.Credentials.from_service_account_file(
            GMAIL_CREDENTIALS_FILE, scopes=GMAIL_SCOPES)
        service = build('gmail', 'v1', credentials=credentials)
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        service.users().messages().send(userId='me', body=raw_message).execute()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def ask_gpt(prompt):
    if not OPENAI_API_KEY:
        return "OpenAI API key not set."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, my speech service is down.")
        return ""

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning!"
    elif hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

def get_datetime():
    now = datetime.datetime.now()
    return f"Current date and time is {now.strftime('%A, %d %B %Y, %I:%M %p')}"

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Here are the search results for {query}."

if __name__ == "__main__":
    speak(greet_user())
    while True:
        command = listen()
        if not command:
            continue
        if "weather" in command:
            # Try to extract city name after the word 'in', e.g. 'weather in Paris'
            import re
            match = re.search(r"weather(?: in)? ([a-zA-Z\s]+)", command)
            if match:
                city = match.group(1).strip()
            else:
                # fallback: remove 'weather' and use the rest as city
                city = command.replace("weather", "").replace("in", "").strip()
            if not city:
                city = "London"
            response = get_weather(city)
            print(response)
            speak(response)
        elif "news" in command:
            response = get_news(NEWSAPI_KEY, "technology")
            print(response)
            speak(response)
        elif "email" in command:
            send_email("recipient@example.com", "Test Subject", "Test Body")
            speak("Email sent.")
        elif "gpt" in command or "joke" in command:
            prompt = command.replace("gpt", "").replace("joke", "Tell me a joke.").strip() or "Tell me a joke."
            response = ask_gpt(prompt)
            print(response)
            speak(response)
        elif "date" in command or "time" in command:
            dt = get_datetime()
            print(dt)
            speak(dt)
        elif "search" in command:
            query = command.replace("search", "").strip()
            result = search_web(query)
            print(result)
            speak(result)
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I can't help with that.")
            speak("Sorry, I can't help with that.")
    # Weather
    print(get_weather("London"))
    # News
    if NEWSAPI_KEY:
        print(get_news(NEWSAPI_KEY, "technology"))
    else:
        print("NewsAPI key not set.")
    # Email
    # send_email("recipient@example.com", "Test Subject", "Test Body")
    # GPT
    print(ask_gpt("Tell me a joke."))