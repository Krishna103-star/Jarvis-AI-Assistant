import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
from fuzzywuzzy import fuzz

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "61b387cbd2014b1da9657ac468a1d2c4"

# Function to calibrate microphone noise levels
def calibrate_noise():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

# Text-to-speech function using gTTS
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# Function to process AI responses
def ai_process(command):
    client = OpenAI(
        api_key="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",
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant Jarvis. Give short responses."},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

# Process commands

def process_command(c):
    c = c.lower()
    if "open" in c:
        if "google" in c:
            webbrowser.open("https://google.com")
        elif "facebook" in c:
            webbrowser.open("https://facebook.com")
        elif "youtube" in c:
            webbrowser.open("https://youtube.com")
        elif "linkedin" in c:
            webbrowser.open("https://linkedin.com")
        elif "whatsapp" in c:
            webbrowser.open("https://web.whatsapp.com")
        elif "swiggy" in c:
            webbrowser.open("https://swiggy.com")
        elif "gpt" in c:
            webbrowser.open("https://chatgpt.com")
    elif c.startswith("play"):
        song = c.split(" ", 1)[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find the song.")
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # Limit to 5 articles
                speak(article['title'])
        else:
            speak("Failed to fetch news.")
    else:
        output = ai_process(c)
        speak(output)

# Main function
if __name__ == "__main__":
    speak("Initializing Jarvis. Please wait.")
    calibrate_noise()

    while True:
        try:
            print("Listening for wake word...")
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            word = recognizer.recognize_google(audio)

            if fuzz.ratio(word.lower(), "jarvis") > 80:  # Fuzzy matching for wake word
                speak("Yes, sir.")
                print("Jarvis activated.")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = recognizer.recognize_google(audio)
                process_command(command)

        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error: {e}")
