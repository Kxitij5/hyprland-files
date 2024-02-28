import json
import speech_recognition as sr
import datetime
import random
import wikipedia
import webbrowser
import time
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
