from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from six.moves import xrange  # pylint: disable=redefined-builtin

from os.path import join, dirname
# from watson_developer_cloud import VisualRecognitionV3

import io
# from google.cloud import vision
# from google.cloud.vision import types

import numpy as np
import subprocess

import sys
print(sys.version)

from flask import Flask, redirect, request, url_for, render_template, flash, send_file
from werkzeug import secure_filename
import os

app = Flask('Show Text')
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='this_is_a_dev_key'
))
# app.debug = True





@app.route('/getbirdimg/', methods=['POST'])
def get_bird_img():
    # send generated image (with recognized text) back to TJBot 
    print('Sending image back to TJBot...')
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
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

@app.route('/getcocoimg/', methods=['POST'])
def get_coco_img():
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


if __name__ == "__main__":

    app.run(debug=True)
