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




stop_flag = False
is_sleeping = False

mapping = {
    "search_wikipedia": search_wikipedia,
    "get_time": get_time,
    "stop_Evio": stop_Evio,
    "search_google": search_google,
    "search_youtube": search_youtube,
    "sleep_Evio": sleep_Evio,
    "set_timer": set_timer,
    
}