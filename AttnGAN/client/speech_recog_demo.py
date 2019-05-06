import speech_recognition as sr
import subprocess
import sys
import os
import os.path
import threading
from multiprocessing import Process #TODO: use threading instead of multiprocessing on mac
from urllib.parse import quote_plus #urllib.parse import quote_plus for python3+
import tkinter as tk #Tkinter for python2, with the capital T

from time import sleep
from PIL import Image, ImageTk

#TODO: convert code to python2.7 for rasberrypi on TJBot

# recognize speech using IBM Speech to Text
# "url": "https://stream.watsonplatform.net/speech-to-text/api"
IBM_USERNAME = "8aa84e85-ad57-46f7-b44c-b6f11b543b17" #speech to text
IBM_PASSWORD = "Y6eqKFPVxv6J" #speech to text
IBM_USERNAME1 = "7b9c08de-f56d-42c4-8e85-6d548bae949e"
IBM_PASSWORD1 = "nkEXXzx1sPvy"
"""
curl -X POST -u 8aa84e85-ad57-46f7-b44c-b6f11b543b17:Y6eqKFPVxv6J --header "Content-Type: audio/flac" --data-binary @Downloads/audio-file.flac "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize"
"""
# obtain audio from the microphone
r = sr.Recognizer()

FNULL = open(os.devnull,'w')

# show the figure
def show(f):
    f=f[0]
    print(f)
    img = Image.open(f)
    w,h = img.size

    if w > 1800:
        w = w/3*2
        h = h/3*2
        img=img.resize((w,h),Image.ANTIALIAS)
        
    root = tk.Tk()
    canvas = tk.Canvas(root, width=w, height=h)
    canvas.pack()

    tk_img = ImageTk.PhotoImage(img)

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    x = ws/2 - w/2
    y = hs/2 - h/2
    # root.geometry("+{}+{}".format(x,y)) #TODO: problem with this line: "TclError: bad geometry specifier "+405.0+273.0" "
    canvas.create_image(w/2, h/2, image=tk_img)
    root.mainloop()
# text to speech by Watson API
def t2s(t):
    t = quote_plus(t)
    if os.path.exists("./speech/{}.wav".format(t)):
        subprocess.call("afplay speech/{}.mp3".format(t),shell=True)
        return
    curl = 'curl -X GET -u {}:{} --output ./speech/{}.mp3 "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize?accept=audio/mp3&text={}&voice=en-US_AllisonVoice"'.format(IBM_USERNAME1, IBM_PASSWORD1, t,t)
    # print(curl)
    subprocess.call(curl,shell=True)
    #sleep(1)
    subprocess.call("afplay speech/{}.mp3".format(t),shell=True)

eval_bird = False
eval_coco = False
with sr.Microphone(device_index=0) as source: #0 for built in microphone: ['Built-in Microphone', 'Built-in Output', 'HDMI'] when hdmi was connected
    t = "Hello world, I am text imager. Would you like to draw a bird or something else?"
    t2s(t)

    audio = r.listen(source)

try:
    #speech recognition by Watson API
    query = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)

    print(query)

    # COCO_KEYWORDS = ["something","general","random","crazy","else","other","different","image","some","thing"] #hasn't been used
    BIRD_KEYWORDS = ["bird", "birds", "wing", "fowl", "third", "thirds"]
    for key in BIRD_KEYWORDS:
        if key in query:
            eval_bird = True
            message = "Sounds like you'd like to draw a bird... What sort of bird would you like to draw?"
            break
    if not eval_bird:
        eval_coco = True
        message = "Okay... What would you like to draw"

    sleep(3)
    t2s(message)
    #message_0 = "IBM Watson heard _" + "What do you see"

    #TODO: REPLACE TEXT TO SPEECH with PYTHON INBUILT t2s library called pyttsx3 -- this works offline and has no limit on usage
    #UPDATE: "error: no module named Foundation"

    with sr.Microphone(device_index=0) as source:
        audio = r.listen(source)
    query = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)     #google speech recognition works better for general queries
    # query = r.recognize_google(audio) #not reliable to use google either, default key is for testing purposes only, even with valid key limited to 50 requests a day. 
    print('\n' + query + '\n')
    with open("example_captions.txt", 'w') as f:
        f.write(query + '\n')
    
    t = "IBM Watson heard _" + query

    t2s(t)
    t2s("Please wait while watson finishes creating your image...")

    s = ["img.jpg"]
    # t1 = Process(target=show, args=(s,))
    # t1.start()
    show(s)
    #TODO: write to example_captions.txt file, then call a subprocess for running the attngan 
    #      on just the queried caption rather than the entire file of captions. measure the
    #      measure the time taken and output this as well through t2s()

    if eval_bird:
        subprocess.call("curl -X POST -F 'type=1' http://10.0.2.9:3000/getbirdimg/ > example_captions.txt", shell=True)
    else: #general image being created
        subprocess.call("curl -X POST -F 'type=1' http://10.0.2.9:3000/getcocoimg/ > example_captions.txt", shell=True)

except sr.UnknownValueError:
    message_2 = "IBM Speech to Text could not understand audio, please try again"
    t2s(message_2)
    print(message_2)
    exit(0)
    
except sr.RequestError as e:
    message_3 = "Could not request results from IBM Speech to Text service; {0}".format(e)
    t2s(message_3)
    print(message_3)
    exit(0)

except:
    t = "Something wrong happened, and I could not generate the image, please try again"
    t2s(t)
    print(t)
    exit(0)



"""
File structure:
AttnGAN 
    code, data, server, models, ...
        code: main.py, model.py, pretrain_DAMSM.py, etc
        server: run_tjserver.sh, AttnGAN_server.py
        data: birds, coco
            birds: example_captions.txt, ...
            coco: example_captions.txt, ...
        models: bird_AttnGAN2, coco_AttnGAN2, ...
            bird_AttnGAN2: example_captions folder with images
            coco_AttnGAN2: example_captions folder with images
IP address for requests: 10.0.2.9:3000/
allowing connections: https://askubuntu.com/questions/224392/how-to-allow-remote-connections-to-flask
"""