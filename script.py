import RPi.GPIO as GPIO
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime

cred = credentials.Certificate("/usr/src/app/plantas-dc918-firebase-adminsdk-dcwmf-394c1c400a.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()

class Planta:
    def __init__(self, id, pinIn, pinOut):
        self.id = id
        self.pinIn = pinIn
        self.pinOut = pinOut

GPIO.setmode(GPIO.BCM)

planta1 = Planta("AEVuWwfwto4BhQeRKApT", 16, 13)
planta2 = Planta("IqQBBZYPNO2m9gar86r4", 20, 19)
planta3 = Planta("bNUOBb0StFx3AmefMeKf", 21, 26)

GPIO.setup(planta1.pinIn, GPIO.IN)
GPIO.setup(planta1.pinOut, GPIO.OUT)

GPIO.setup(planta2.pinIn, GPIO.IN)
GPIO.setup(planta2.pinOut, GPIO.OUT)

GPIO.setup(planta3.pinIn, GPIO.IN)
GPIO.setup(planta3.pinOut, GPIO.OUT)

def mandarCorreo(correo):
    # create message object instance
    msg = MIMEMultipart()
    message = "Se ha regado su planta hoy: " + datetime.datetime.now()
 
    # setup the parameters of the message
    password = "70,Verde"
    msg['From'] = "losmascorales@gmail.com"
    msg['To'] = correo
    msg['Subject'] = "Estado de su planta"
 
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
 
    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
 
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
 
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

def callbackA(entrada):
    if (GPIO.input(entrada)):
        print("No se ha detectado agua en la planta: " + planta1.id)
        GPIO.output(planta1.pinOut, GPIO.HIGH)
    else:
        print("Se ha detectado agua en la planta: " + planta1.id)
            #Manda correo
        try:
            doc = db.collection(u'usuarios').document(planta1.id).get()
            correo = doc.to_dict()[u'correo']
            print("Se enviara correo a: "+correo)
            mandarCorreo(correo)
        except google.cloud.exceptions.NotFound:
            print('Missing data')
        GPIO.output(planta1.pinOut, GPIO.LOW)

def callbackB(entrada):
    if (GPIO.input(entrada)):
        print("No se ha detectado agua en la planta: " + planta2.id)
        GPIO.output(planta2.pinOut, GPIO.HIGH)
    else:
        print("Se ha detectado agua en la planta: " + planta2.id)
        #Manda correo
        try:
            doc = db.collection(u'usuarios').document(planta2.id).get()
            correo = doc.to_dict()[u'correo']
            print("Se enviara correo a: "+correo)
            mandarCorreo(correo)
        except google.cloud.exceptions.NotFound:
            print('Missing data')
        GPIO.output(planta2.pinOut, GPIO.LOW)

def callbackC(entrada):
    if (GPIO.input(entrada)):
        print("No se ha detectado agua en la planta: " + planta3.id)
        GPIO.output(planta3.pinOut, GPIO.HIGH)
    else:
        print("Se ha detectado agua en la planta: " + planta3.id)
        #Manda correo
        try:
            doc = db.collection(u'usuarios').document(planta1.id).get()
            correo = doc.to_dict()[u'correo']
            print("Se enviara correo a: "+correo)
            mandarCorreo(correo)
        except google.cloud.exceptions.NotFound:
            print('Missing data')
        GPIO.output(planta3.pinOut, GPIO.LOW)

GPIO.add_event_detect(planta1.pinIn, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(planta1.pinIn, callbackA)

GPIO.add_event_detect(planta2.pinIn, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(planta2.pinIn, callbackB)

GPIO.add_event_detect(planta3.pinIn, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(planta3.pinIn, callbackC)

while True:
    time.sleep(1)
