import speech_recognition as sr
import subprocess
import sys
import os
import os.path
import PIL
from PIL import Image
from urllib import quote_plus #urllib.parse import quote_plus for python3+
from PIL import Image, ImageTk
import Tkinter as tk #Tkinter for python2, with the capital T
import threading
from multiprocessing import Process

from picamera import PiCamera
from time import sleep


sleep(5)

# recognize speech using IBM Speech to Text
IBM_USERNAME = "insert username"
IBM_PASSWORD = "insert password"

# obtain audio from the microphone
r = sr.Recognizer()

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
    root.geometry("+{}+{}".format(x,y))
    canvas.create_image(w/2, h/2, image=tk_img)
    root.mainloop()

# test to speech by Watson API
def t2s(t):
    t = quote_plus(t)
    if os.path.exists("./speech/{}.wav".format(t)):
        subprocess.call("aplay ./speech/{}.wav".format(t),shell=True)
        return
    curl = 'curl -X GET -u "7ea4ce16-5a8b-4574-a76f-f417b28c6d65":"873eOA3ZDbkR" --output ./speech/{}.wav "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize?accept=audio/wav&text={}&voice=en-US_AllisonVoice"'.format(t,t)
    #print(curl)
    subprocess.call(curl,shell=True)
    #sleep(1)
    subprocess.call("aplay ./speech/{}.wav".format(t),shell=True)

FNULL = open(os.devnull,'w')

with sr.Microphone(device_index=2) as source:
    t = "Hello world, I am text imager. How can I help you?"
    t2s(t)
    
    print("I am ready to paint")
    audio = r.listen(source)
try:
    #speech recognition by Watson API
    message_0 = "IBM Watson heard _" + r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
    #sleep(2)
    #message_0 = "IBM Watson heard _" + "What do you see"

    t = message_0
    t2s(t)
    
    keyword = ["see","sea","c","what","are","do","you","draw","this","image","can"]
    for key in keyword:
      if key in message_0: #or True:
    
        t = "Let me take a look"
        t2s(t)
        #open camera
        with PiCamera() as cam:
            cam.start_preview(fullscreen=False, window = (200, 150, 1440, 960))
            sleep(4)
            with open('img.jpg', 'wb') as f:
                cam.capture(f)

        s = ["./img.jpg"]
        t1 = Process(target=show, args=(s,))
        t1.start()
        
        waitmsg = "OK, I am painting now"
        t = waitmsg
        t2s(t)

        # send input photo and retrieve generated image
        subprocess.call("curl -X POST -F 'file=@./img.jpg' -F 'type=1' http://9.3.158.223:5000/post/666 > output.jpg" , shell=True)
        introread="This is what I just painted"
        t2s(introread)

        s = ["./output.jpg"]
        t2 = Process(target=show, args=(s,))    
        t2.start()
        
        subprocess.call("curl -X POST -F 'type=1' http://9.3.158.223:5000/getimg/ > text.txt", shell=True)
        
        textfile=open("text.txt","r")
           
        textread=textfile.read()
        print(len(textread))
        
        if textread!='':
            #introread="This is what I just painted"
            #t2s(introread)
            #print(introread)
            t2s(textread)
            print(textread)
        else:
            errmsg="Input text was not recognized, please try again"
            t2s(errmsg)
            print(errmsg)
            exit(0)

        try:
           im=Image.open("output.jpg")
           t = "How do you like it?"
           t2s(t)
        except IOError:
           t = "Something wrong happened, and I could not generate the image, please try again"
           t2s(t)
           print(t)           
        break
    
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

