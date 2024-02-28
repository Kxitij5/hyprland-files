import json
import os
import subprocess
import random
import datetime
import torch

from functions import  speak, get_user_input, intent_recognition, stop_Evio, wake_Evio, sleep_Evio, search_google,search_wikipedia,search_youtube,set_timer, get_time


with open('./intents.json', 'r') as json_data:
    intents = json.load(json_data)

fileName = "data.pth"
if  os.path.exists(fileName):
    
    data = torch.load(fileName)
else:
    speak("Please wait for a while, I am getting trained. It might take some time.")
    subprocess.run(["python", "train.py"])
    data = torch.load("data.pth")






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

if __name__ == "__main__":
   
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<17:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    
    speak("I am Evio, your voice assistant! How can i help you today?")
    
    while not stop_flag:
        if not is_sleeping:
            user_input = get_user_input()
            print(user_input)
            recognized_intent = intent_recognition(user_input)
            print(recognized_intent)
            if recognized_intent:
            
                if "responses" in recognized_intent:
                    responses = recognized_intent['responses']
                    respond = random.choice(responses) 
                    speak(respond)
                if "action" in recognized_intent:
                    action = recognized_intent["action"]
                    
                    if action in mapping:
                        mapping[action]()
                        
                        if action != "stop_Evio" and action != "sleep_Evio":
                            sleep_Evio()
                            
                    else:
                        speak("I dont know how to do this!")
                        sleep_Evio()
                       
        else: 
            wake_Evio()
        