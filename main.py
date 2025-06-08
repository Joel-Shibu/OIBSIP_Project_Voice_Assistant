import os
from dotenv import load_dotenv
import openai
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
from email.mime.text import MIMEText
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import pickle
import re

# Load environment variables
load_dotenv()
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GMAIL_CREDENTIALS_FILE = 'credentials.json'
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
sender = os.getenv("SENDER_EMAIL")
subject = os.getenv("DEFAULT_SUBJECT", "Voice Assistant Email")
openai.api_key = OPENAI_API_KEY

# =====================
# Weather Function
# =====================
def get_weather(city):
    if not OPENWEATHER_API_KEY:
        return "Weather API key not set."
    import requests
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        desc = data['weather'][0]['description']
        temp = data['main']['temp']
        city_name = data.get('name', city)
        country = data.get('sys', {}).get('country', '')
        return f"Current weather in {city_name}, {country}: {desc}, {temp}°C."
    except requests.RequestException:
        return f"Sorry, I couldn't fetch the weather for '{city}'. Please check the city name and try again."

# =====================
# News Function
# =====================
def get_news(api_key):
    import requests
    url = f"https://newsapi.org/v2/everything?q=world&sortBy=publishedAt&language=en&apiKey={api_key}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        headlines = [article["title"] for article in articles if article.get("title") and article.get("publishedAt")]
        if not headlines:
            return "Sorry, I couldn't find any up-to-date world news articles right now."
        return "; ".join(headlines[:5])
    except requests.RequestException:
        return "Sorry, I couldn't fetch the news right now. Please try again later."

# =====================
# Email Function
# =====================
def authenticate_gmail():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_FILE, GMAIL_SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def format_email_input(raw_input):
    email = raw_input.lower()
    email = email.replace(" at ", "@")
    email = email.replace(" dot ", ".")
    email = email.replace(" underscore ", "_")
    email = email.replace(" ", "")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("❌ You said: email address is wrong")
        return None
    return email

def send_email(body_text, receiver):
    if not receiver or '@' not in receiver:
        print("Invalid receiver email format.")
        return
    try:
        creds = Credentials.from_authorized_user_file('token.json') if os.path.exists('token.json') else None
        if not creds or not creds.valid:
            creds = authenticate_gmail()._http.credentials
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText(body_text)
        message['to'] = receiver
        message['from'] = sender
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_result = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        print(f"✅ Email sent to {receiver}. Message ID: {send_result['id']}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def read_latest_emails():
    service = authenticate_gmail()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
    messages = results.get('messages', [])
    if not messages:
        print("No new messages.")
        return
    print("Latest Emails:")
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = msg_data['snippet']
        headers = msg_data['payload']['headers']
        subject = [h['value'] for h in headers if h['name'] == 'Subject']
        from_ = [h['value'] for h in headers if h['name'] == 'From']
        print(f"\nFrom: {from_[0] if from_ else 'Unknown'}")
        print(f"Subject: {subject[0] if subject else 'No Subject'}")
        print(f"Snippet: {snippet}")

# =====================
# GPT Function
# =====================
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

# =====================
# Text-to-Speech Function
# =====================
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# =====================
# Speech Recognition Function
# =====================
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=5)
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

# =====================
# Greeting Function
# =====================
def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning! How can I assist you today?"
    elif hour < 18:
        return "Good afternoon! How can I assist you today?"
    else:
        return "Good evening! How can I assist you today?"

# =====================
# Date and Time Function
# =====================
def get_datetime():
    now = datetime.datetime.now()
    return f"Current date and time is {now.strftime('%A, %d %B %Y, %I:%M %p')}"

# =====================
# Web Search Function
# =====================
def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Here are the search results for {query}."

if __name__ == "__main__":
    speak(greet_user())
    JOKE_PROMPT = "Tell me a joke."
    while True:
        command = listen()
        if not command:
            continue
        if "weather" in command:
            city = ""
            match = re.search(r"weather(?: in)? ([a-zA-Z\s]+)", command)
            if match:
                city = match.group(1).strip()
            else:
                match2 = re.search(r"in ([a-zA-Z\s]+)", command)
                if match2:
                    city = match2.group(1).strip()
            while not city:
                speak("Which city do you want the weather for?")
                city = listen()
                if not city:
                    speak("Sorry, I need a city name to get the weather.")
            response = get_weather(city)
            print(response)
            speak(response)
        elif "news" in command:
            response = get_news(NEWSAPI_KEY)
            print(response)
            speak(response)
        elif "email" in command:
            speak("Please say the receiver's email address.")
            receiver = listen()
            receiver = format_email_input(receiver)
            if not receiver:
                speak("Receiver email not captured or invalid. Email not sent.")
                continue
            speak("Please say the message you want to send.")
            body = listen()
            if not body:
                speak("Message body not captured. Email not sent.")
                continue
            try:
                send_email(body_text=body, receiver=receiver)
                speak("Email sent.")
            except Exception as e:
                print(f"Failed to send email: {e}")
                speak("Sorry, I couldn't send the email. Please try again.")
        elif "gpt" in command or "joke" in command:
            prompt = command.replace("gpt", "").replace("joke", JOKE_PROMPT).strip() or JOKE_PROMPT
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
        elif "check inbox" in command or "check email" in command or "inbox" in command:
            try:
                speak("Checking your inbox.")
                service = authenticate_gmail()
                results = service.users().messages().list(userId="me", maxResults=1).execute()
                messages = results.get("messages", [])
                if not messages:
                    speak("Your inbox is empty.")
                else:
                    msg = service.users().messages().get(userId="me", id=messages[0]["id"]).execute()
                    headers = msg["payload"]["headers"]
                    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
                    sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")
                    speak(f"Your latest email is from {sender} with subject: {subject}")
            except Exception as e:
                speak(f"Sorry, I couldn't check your inbox. {str(e)}")
                print(f"Failed to check inbox: {e}")
        elif "exit" in command or "quit" in command or "goodbye" in command or "farewell" in command or "take care" in command or "until next time" in command or "it was a pleasure" in command:
            exit_message = "It was a pleasure assisting you. Wishing you a wonderful day ahead. Farewell!"
            print(exit_message)
            speak(exit_message)
            break
        else:
            speak("Sorry, I can't help with that.")