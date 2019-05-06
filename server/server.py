from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from six.moves import xrange  # pylint: disable=redefined-builtin

from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

import io
from google.cloud import vision
from google.cloud.vision import types

import numpy as np
import subprocess

import sys
print(sys.version)

from flask import Flask, redirect, request, url_for, render_template, flash, send_file
import os

app = Flask('Show Text')
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='this_is_a_dev_key'
))
# app.debug = True

visual_recognition = VisualRecognitionV3('2016-05-20', api_key='f5a7e83ebe0ee1a90ba06a7fad6e35629c657ab0')
mywords = ''

# text detector based on Watson OCR
def textDetection(file_path):
    '''text detection'''
    with open(file_path, 'rb') as image_file:    
        text_results = visual_recognition.recognize_text(images_file=image_file)
        try:
            words = text_results['images'][0]['text']
            symbols = ['[',']']
            for sym in symbols:               
                words = words.replace(sym,'')
            words = words.replace('\n',' ')
        except:
            words = []
    return words

# text detector based on Google OCR
def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    words = texts[0].description
    words = words.replace('\n',' ')
    words = words[:-1]
    return words


@app.route('/post/<id>', methods=['POST'])
def get_cap(id):
    print('ID: ', id)

    img = request.files['file']
    
    img.save('/home/ubuntu/tjbot/server/input.jpg')

    print('Text received, generating images...')

    #send photo to Bluemix for text recognition
    #words = textDetection('/home/ubuntu/tjbot/server/input.jpg')
    words = detect_text('/home/ubuntu/tjbot/server/input.jpg')
    print(words)

    global mywords
    mywords = words

    #receive text for generating images
    if "bird" in mywords:
      type = 1
    elif "flower" in mywords:
      type = 2
    else: 
      type = 0

    # example class labels for demo video (can support up to 1000 different classes of ImageNet)
    # 1000 class list here: https://gist.github.com/yrevar/942d3a0ac09ec9e5eb3a
    if type == 0:
        if words == 'turtle':
            num=35
        elif words == 'elephant':
            num=101
        elif words == 'crab':
            num=118
        elif words == 'dog':
            num=152
        elif words == 'lipstick':
            num=629
        elif words == 'tent':
            num=672
        elif words == 'guitar':
            num=546
        elif words == 'backpack':
            num=414
        elif words == 'beer':
            num=440
        elif words == 'broom':
            num=462
        elif words == 'jean':
            num=608
        elif words == 'iron':
            num=606
        elif words == 'lamp':
            num=619
        elif words == 'ship':
            num=625
        elif words == 'tent':
            num=672
        elif words == 'bridge':
            num=718
        else:
            print("Text not recognized.")

    if type==0:  # PPGN model for 1000-class object generation 
        os.chdir("/home/ubuntu/tjbot/PPGN")
        cap = num
        subprocess.call("chmod +x /home/ubuntu/tjbot/PPGN/1_class_conditional_sampling.sh", shell=True)
        subprocess.call("/home/ubuntu/tjbot/PPGN/1_class_conditional_sampling.sh {}".format(cap), shell=True)
        return send_file('/home/ubuntu/tjbot/PPGN/output/output.jpg', mimetype='image/jpg')
    elif type==1:  # StackGAN model for bird generation
        os.chdir("/home/ubuntu/tjbot/StackGAN")
        with open('/home/ubuntu/tjbot/StackGAN/Data/birds/caption.txt', 'w') as f:
            f.write(words)
        subprocess.call("chmod +x /home/ubuntu/tjbot/StackGAN/demo/birds_demo.sh", shell=True)   
        subprocess.call("/home/ubuntu/tjbot/StackGAN/demo/birds_demo.sh", shell=True)
        return send_file('/home/ubuntu/tjbot/StackGAN/Data/birds/caption/sentence0.jpg', mimetype='image/jpg')
    elif type==2:  # StackGAN model for flower generation
        os.chdir("/home/ubuntu/tjbot/StackGAN")
        print(os.getcwd())
        with open('/home/ubuntu/tjbot/StackGAN/Data/flowers/caption.txt', 'w') as f:
            f.write(words)
        subprocess.call("chmod +x /home/ubuntu/tjbot/StackGAN/demo/flowers_demo.sh", shell=True) 
        subprocess.call("/home/ubuntu/tjbot/StackGAN/demo/flowers_demo.sh", shell=True)   
        return send_file('/home/ubuntu/tjbot/StackGAN/Data/flowers/caption/sentence0.jpg', mimetype='image/jpg')
    else:
        print("Input type not supported")
    return 'Image generated!'


@app.route('/getimg/', methods=['POST'])
def get_img():
    # send generated image (with recognized text) back to TJBot 
    print('Sending image back to TJBot...')

    global mywords
    if "bird" in mywords:
      type = 1
    elif "flower" in mywords:
      type = 2
    else: 
      type = 0

    if type==0:
        os.chdir("/home/ubuntu/tjbot/PPGN")
        
        return mywords
        return send_file('/home/ubuntu/tjbot/PPGN/output/output.jpg', mimetype='image/jpg')
    elif type==1:
        os.chdir("/home/ubuntu/tjbot/StackGAN")
        return mywords
        return send_file('/home/ubuntu/tjbot/StackGAN/Data/birds/caption/sentence0.jpg', mimetype='image/jpg')
    elif type==2:
        os.chdir("/home/ubuntu/tjbot/StackGAN")
        return mywords
        return send_file('/home/ubuntu/tjbot/StackGAN/Data/flowers/caption/sentence0.jpg', mimetype='image/jpg')
    else:
        print("Input type not supported")
    return 'Generated image has been sent.'


@app.route('/post_test/', methods=['POST'])
def post_test():
    # return "111"
    return send_file('./bird.png', mimetype='image/png')
    return send_file('/home/ubuntu/tjbot/StackGAN/Data/birds/caption/sentence0.jpg', mimetype='image/jpg')


if __name__ == "__main__":

    app.run(debug=True)
