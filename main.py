import speech_recognition as sr
import webbrowser 
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import datetime
import random
import subprocess

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "b9f9519348a8483c91f8c09b682a45cc"

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    try:
        client = OpenAI(api_key="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")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis. Give short, helpful answers."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return "Sorry, I couldn't reach OpenAI services."

def tell_time():
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {time}")

def tell_date():
    date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today is {date}")

def calculate(expression):
    try:
        result = eval(expression)
        speak(f"The result is {result}")
    except:
        speak("Sorry, I couldn't calculate that.")

def tell_joke():
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything.",
        "Why did the computer get cold? Because it forgot to close its Windows.",
        "Why was the math book sad? Because it had too many problems."
    ]
    speak(random.choice(jokes))

def open_app(app_name):
    if app_name == "notepad":
        subprocess.Popen(["notepad.exe"])
    elif app_name == "vscode":
        subprocess.Popen(["code"])
    else:
        speak(f"I can't open {app_name} right now.")

def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.split(" ")[1]
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song}")
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            for i, article in enumerate(articles[:5]):
                speak(f"Headline {i+1}")
                speak(article['title'])
    elif "time" in c:
        tell_time()
    elif "date" in c:
        tell_date()
    elif "calculate" in c:
        expr = c.replace("calculate", "").strip()
        calculate(expr)
    elif "joke" in c:
        tell_joke()
    elif "open notepad" in c:
        open_app("notepad")
    elif "open vs code" in c:
        open_app("vscode")
    elif c in ["exit", "quit", "stop"]:
        speak("Goodbye malik")
        exit()
    elif "most beautiful girl" in c:
        speak("Sara is the most beautiful girl")
    else:
        response = aiProcess(c)
        speak(response)

if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
            word = recognizer.recognize_google(audio)
            print("Wake word:", word)

            if word.lower() == "jarvis":
                speak("Yes Malik, I'm listening")
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print("Command:", command)
                    processCommand(command)

        except Exception as e:
            print("Could not understand audio.")
