#!/usr/bin/env python
# coding: utf-8

# In[1]:
from flask import flash
from flask_app import routes
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from usps import USPSApi, Address
import numpy as np
import json
import pandas as pd
import collections
import cv2

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)

#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
class readdl:
    def __init__(self, path):
        self.path

    def readlicense(path):

        img = cv2.imread(path)


        pix = get_grayscale(img)
        #pix = remove_noise(pix)
        pix = thresholding(pix)
        #pix = dilate(pix)
        #pix = erode(pix)
        #pix = opening(pix)
        #pix = canny(pix)
        pix = deskew(pix)

        filename = "temp.jpeg"
        cv2.imwrite(filename, pix)
        text = pytesseract.image_to_string(Image.open(filename) ,lang='eng')

        return text
class verify:
    def __init__(self, model,fname,mname,lname,street,city,state,Zipcode,age):
        self.model = model
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.street = street
        self.city =  city
        self.state = state
        self.Zip = Zipcode
        self.age = age

    def validate(model,fname,mname,lname,street,city,state,Zip,age):
        ttable = 0
        result = {}
        if age in model:
            #print("True")
            flash("age checks")
            ttable = ttable +1.5
        else:
            flash("age didn't check")
            #print("False")
            pass
        if fname in model:
            flash("First Name checks")
            #print("True")
            ttable = ttable +1.5
        else:
            flash("First Name didn't check")
            #print("False")
            pass
        if mname in model:
            flash("Middle Name checks")
            #print("True")
            ttable = ttable +.5
        else:
            flash("Middle Name didn't check")
            pass
        if lname in model:
            flash("Last Name Checks")
            #print("True")
            ttable = ttable +1.5
        else:
            flash("Last Name didn't check")
            pass
        if street in model:
            #print("True")
            flash("Street Check")
            ttable = ttable +.5
        else:
            flash("Street didn't check")
            pass
        if state in model:
                #print("True")
            flash("State Checks")
            ttable = ttable +1.5
        else:
            flash("State didn't check")
            pass
        if city in model:
            flash("City Checks")

            ttable = ttable +1.5
        else:
            flash("City didn't check")
            pass
        if Zip in model:
            flash("Zip Chcks")
            #print("True")
            ttable = ttable +1.5
        else:
            flash("Zip didn't check")
            pass


        count =  ttable/8

        if (count > .8) == True:
            address = Address(
            name=(fname+" "+mname+" "+lname),
            address_1=street,
            city=city,
            state=state,
            zipcode=Zip
            )
            usps = USPSApi('062SWIFT5933', test=True)
            validation = usps.validate_address(address)

            result = validation.result
            flash("Close enough!  It doesn't have to be perfect")

            return str("ID works")
        else:


            return str("Take another picture")


# In[ ]:





# In[ ]:





# In[9]:




# In[ ]:





# In[ ]:





# In[ ]:
