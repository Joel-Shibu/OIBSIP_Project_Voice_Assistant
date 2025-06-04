import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, I am unable to access the speech service.")
            return ""

def get_time():
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")

def get_date():
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y")

def process_command(command):
    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you today?")
    elif "time" in command:
        current_time = get_time()
        speak(f"The current time is {current_time}.")
    elif "date" in command:
        current_date = get_date()
        speak(f"Today's date is {current_date}.")
    elif command.startswith("search"):
        query = command.replace("search", "", 1).strip()
        if query:
            speak(f"Searching for {query}.")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("Please specify what you want to search for.")
    elif command:
        speak("Sorry, I can only respond to greetings, tell the time or date, or search the web.")

def main():
    speak("Voice assistant activated. How can I help you?")
    while True:
        command = listen()
        if command:
            if "exit" in command or "quit" in command or "stop" in command:
                speak("Goodbye!")
                break
            process_command(command)

if __name__ == "__main__":
    main()