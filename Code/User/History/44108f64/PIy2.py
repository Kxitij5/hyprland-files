import speech_recognition as sr
import datetime
import torch
import random
import wikipedia
import webbrowser
import time
from gtts import gTTS
import os
from nltk_utils import bag_of_words, tokenize
from model import NeuralNet

import pygame

wikipedia.set_lang('en')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

torch.load("data.pth")

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


def speak(audio):
    tts = gTTS(text=audio, lang='en')
    tts.save("temp.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def get_user_input():
    r=sr.Recognizer()
    r.pause_threshold = 1
    r.energy_threshold = 290
    while True:
        with sr.Microphone()as mic:
            print("Listening....")        
            audio = r.listen(mic)
            
        try:
            query = r.recognize_google(audio, language='en-in')
            return query
        except Exception as e :
            speak("Sorry!! I did not understand that. Could you please reapeat?")
    

def intent_recognition(user_input):
    sentence = tokenize(user_input)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["name"]:
                if intent['responses'] is not None:
                    response = (f"{random.choice(intent['responses'])}")
                else:
                    response = ("Sorry! I don't know how to reply to it!")
    else:
        response = ("Sorry! I don't know how to reply to it!")

    return response

def stop_Evio():
    speak('Shutting down Evio!')
    os.remove('./temp.mp3')
    global stop_flag
    stop_flag = True


def sleep_Evio():
    global is_sleeping
    is_sleeping = True
    speak("Going to sleep! Wake me up by calling my name!")



def wake_Evio():
    global is_sleeping
    r = sr.Recognizer()
    r.pause_threshold = 1
    r.energy_threshold = 290
    
    while is_sleeping:
        with sr.Microphone() as mic:
            
            audio = r.listen(mic)
            
            query = r.recognize_google(audio, language='en-in')
            
        
        try:
            query = r.recognize_google(audio, language='en-in')
            
            # wake-word is evo as the recognizer is not recognising evio, after the wake-word
            #being renamed to evo it responds to evio.
            if "evo" in query.lower():
                is_sleeping = False
                speak("Hey! I am up. What can I do for you?")
        except Exception as e:
            pass


def search_wikipedia():
    speak("What do you want me to search?")
    query = get_user_input()
    speak("Searching Wikipedia...")
    query = query.replace("on wikipedia", "")
    
    try:
        result = wikipedia.summary(query, sentences=3)
        speak("According to Wikipedia")
        speak(result)
        pass
    
    except wikipedia.exceptions.PageError as e:
        speak("I couldn't find any information on Wikipedia for that query.")
        


def search_youtube():
    speak("What do you want me to search?")
    query = get_user_input()
    youtube_url = f"https://www.youtube.com/results?search_query={query}"
    
    
    try:
        webbrowser.open(youtube_url)
        
        pass
    
    except webbrowser.Error as e:
        speak("I couldn't search it on YouTube.")
        



def search_google():
    speak("What do you want me to search?")
    query = get_user_input()
    google_url = f"https://www.google.com/search?q={query}"
    
    try:
        webbrowser.open(google_url)
        
        pass
    
    except webbrowser.Error as e:
        speak("I couldn't connect to Google.")
        

    

    
    
def get_time():
    strTime = datetime.datetime.now().strftime("%H:%M")
    speak(f"The time is {strTime}")


def set_timer():
    speak("Sure! Please specify the duration for the timer in seconds, minutes, or hours.")

    try:
        user_input = get_user_input().lower()
        

        duration = 0
        

        words = user_input.split()
        for i in range(0, len(words), 2):
            value = int(words[i])
            unit = words[i + 1]

            if "minute" in unit:
                duration += value * 60
                
            elif "hour" in unit:
                duration += value * 3600
                
            elif "second" in unit:
                duration += value

        if duration > 0:
            speak(f"Timer set for {user_input}. I will notify you when it's time.")
            
            time.sleep(duration)
            speak("Timer has ended. Time's up!")
        else:
            speak("Could not set a timer. Please specify a valid duration.")

    except Exception as e:
        speak("Could not set a timer!")
