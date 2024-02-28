import speech_recognition as sr
import subprocess

r=sr.Recognizer()
r.pause_threshold = 1
r.energy_threshold = 290

while True:
    with sr.Microphone()as mic:
        r.adjust_for_ambient_noise(mic, 1)
        print("Listening....")        
        audio = r.listen(mic)
        
    try:
        print("try")
        query = r.recognize_google(audio, language='en-in')
        subprocess(["espeak", query]) 
        print(query)
    except Exception as e :
        print("exception")