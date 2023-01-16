from flask import Flask, request, abort, Response, redirect, url_for, flash, Blueprint, send_from_directory, render_template_string
from flask.templating import render_template
from flask_security.decorators import roles_required, login_required, auth_required
from flask_security import current_user
from flask_security.utils import login_user, user_authenticated
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from flask_wtf import FlaskForm
from regex import R
from wtforms import StringField, SubmitField
import base64
from io import BytesIO
import sys
import os
import numpy as np
import cv2
import pytesseract as pt
import pandas as pd
from PIL import Image, ImageGrab
import os

from werkzeug.utils import secure_filename
from wtforms import FileField

UPLOAD_FOLDER = '/Users/aaronl/eclipse-workspace/radio-detox/RadioDetox/src/python/enferno/enferno/datadir'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
from code.public.forms import init_Register


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
bp_public = Blueprint('public',__name__, static_folder='../static',template_folder="../templates")
@bp_public.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=10800'
    return response


@bp_public.route("/", methods=['GET'])
def home():
    if request.method == 'GET':
        
        return render_template("initial_login.html")
@bp_public.route("/upload", methods=["POST"])  
def upload():
    if request.method =='POST': 
        name = request.form.get('name')

        f = request.files['file']
        f.save(secure_filename(f.filename))
        flash("File saved successfully")

        string = imToString(f)
        
        print(string, sys.stderr)
        
        if name in string:
            return redirect("/register")
        else: 
            return render_template("500.html")


@bp_public.route("/index",methods=['GET','POST'])
def index():
    return render_template("index.html")

def imToString(picture):
    pt.pytesseract.tesseract_cmd = r"/opt/homebrew/Cellar/tesseract/5.2.0/bin/tesseract"
    # read the image using OpenCV 
    # from the command line first argument
    #src = cv2.imread(picture)
    # or you can use Pillow
    src = Image.open(picture)
    im_data = np.asarray(src)
    img = cv2.resize(im_data, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(im_data, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    # get the string
    string = pt.image_to_string(img)
    # print it
    
    
    #define special characters list
    special_characters = ['!','#','$','%', '&','@','[',']',' ',']','_']
    string = ''.join(filter(lambda i:i not in special_characters, string))
    # get all data
    #data = pt.image_to_data(image)
    print(string)
    #print(data)
    return string
@bp_public.route('/robots.txt')
def static_from_root():
    return send_from_directory(bp_public.static_folder, request.path[1:])