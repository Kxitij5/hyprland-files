import speech_recognition as sr
import subprocess

r=sr.Recognizer()
r.pause_threshold = 1
r.energy_threshold = 290
while True:
    with sr.Microphone()as mic:
        print("Listening....")        
        audio = r.listen(mic)
        
    try:
        query = r.recognize_google(audio, language='en-in')
        subprocess(["espeak", query]) 
        print(query)
    except Exception as e :
        subprocess(["espeak","Sorry!! I did not understand that. Could you please reapeat?"])