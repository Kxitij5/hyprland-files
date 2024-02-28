import json
import speech_recognition as sr
import datetime
import random
import wikipedia
import webbrowser
import time
import subprocess
from gtts import gTTS
import os
import pyttsx3
import pygame
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('./intents.json', 'r') as json_data:
    intents = json.load(json_data)

fileName = "data.pth"
if  os.path.exists(fileName):
    
    data = torch.load(fileName)
else:
    subprocess.run(["python", "train.py"])
    data = torch.load("data.pth")

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
