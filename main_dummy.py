import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer=sr.Recognizer()
engine=pyttsx3.init()
newsapi = "61b387cbd2014b1da9657ac468a1d2c4"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    

    # Initialize Pygame
    pygame.init()

    # Initialize the mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running so the music can play
    # You can use a loop, input, or any other method to keep the program running
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    client = OpenAI(
    api_key="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",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant Jarvis.Give a short responses please."},
        {
            "role": "user",
            "content": command
        }
        ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://whatsapp.com")
    elif "open swiggy" in c.lower():
        webbrowser.open("https://swiggy.com")
    elif "open gpt" in c.lower():
        webbrowser.open("https://chatgpt.com")
    elif c.lower().startswith("play"):
        songs = c.lower().split(" ")[1]
        link=musicLibrary.music[songs]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=61b387cbd2014b1da9657ac468a1d2c4")
        if r.status_code ==200:
            data=r.json()

            articles=data.get('articles',[])

            for article in articles:
                speak(article['title'])

    else:
        #let openai handle the situation
        output = aiProcess(c)
        speak(output)
            

if __name__=="__main__":
    speak("Initializing jarvis......")
    while True:
        r = sr.Recognizer()
        

        

        print("Recognizing....")
        try:
            with sr.Microphone() as source:    
                print("Listening.....")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)
            word=r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("yes sir")
                #listen for command
                with sr.Microphone() as source:    
                    print("jarvis active.....")
                    audio = r.listen(source)
                    command=r.recognize_google(audio)
                    
                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))

