# encoding: utf-8
import RPi.GPIO as GPIO
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime

# Obtener las creddenciales del archivo json para usar un proyecto de firebase.
cred = credentials.Certificate("/usr/src/app/plantas-dc918-firebase-adminsdk-dcwmf-394c1c400a.json")
# Iniciar una aplicación.
app = firebase_admin.initialize_app(cred)
# Obtener el cliente firestore.
db = firestore.client()

# Creación de la clase planta
class Planta:
    def __init__(self, id, pinIn, pinOut):
        self.id = id            # Id con el que obtendra datos de la base de datos.
        self.pinIn = pinIn      # Pin que será asignado como entrada de datos para la planta.
        self.pinOut = pinOut    # Pin que será asignado como salida de datos para la planta.

# Asignar el modo de operación de los pines GPIO.
GPIO.setmode(GPIO.BCM)

# Crear las instancias de las plantas.
planta1 = Planta("AEVuWwfwto4BhQeRKApT", 16, 13)
planta2 = Planta("IqQBBZYPNO2m9gar86r4", 20, 19)
planta3 = Planta("bNUOBb0StFx3AmefMeKf", 21, 26)

# Asignar el modo de funcionamiento a los pines GPIO por cada planta.
GPIO.setup(planta1.pinIn, GPIO.IN)
GPIO.setup(planta1.pinOut, GPIO.OUT)

GPIO.setup(planta2.pinIn, GPIO.IN)
GPIO.setup(planta2.pinOut, GPIO.OUT)

GPIO.setup(planta3.pinIn, GPIO.IN)
GPIO.setup(planta3.pinOut, GPIO.OUT)

def mandarCorreo(correo):
    # Crear una instancia para el mensaje
    msg = MIMEMultipart()
    message = "Se ha regado su planta hoy: " + datetime.datetime.now()
 
    # Asignar los parametros del mensaje.
    password = "70,Verde"
    msg['From'] = "losmascorales@gmail.com"
    msg['To'] = correo
    msg['Subject'] = "Estado de su planta"
 
    # Añadir dentro el cuerpo del mensaje.
    msg.attach(MIMEText(message, 'plain'))
 
    #Crear el servidor
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
 
    # Credenciales de acceso para enviar el correo.
    server.login(msg['From'], password)
 
    # Enviar el mensaje por el servidor.
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
            print("Se enviará correo a: "+correo)
            mandarCorreo(correo)
        except google.cloud.exceptions.NotFound:
            print('Missing data')
        GPIO.output(planta1.pinOut, GPIO.LOW)

def callbackB(entrada):
    if (GPIO.input(entrada)):
        print(u"No se ha detectado agua en la planta: " + planta2.id)
        GPIO.output(planta2.pinOut, GPIO.HIGH)
    else:
        print(u"Se ha detectado agua en la planta: " + planta2.id)
        #Manda correo
        try:
            doc = db.collection(u'usuarios').document(planta2.id).get()
            correo = doc.to_dict()[u'correo']
            print(u"Se enviará correo a: "+correo)
            mandarCorreo(correo)
        except google.cloud.exceptions.NotFound:
            print(u'Missing data')
        GPIO.output(planta2.pinOut, GPIO.LOW)

def callbackC(entrada):
    if (GPIO.input(entrada)):
        print(u"No se ha detectado agua en la planta: " + planta3.id)
        GPIO.output(planta3.pinOut, GPIO.HIGH)
    else:
        print(u"Se ha detectado agua en la planta: " + planta3.id)
        #Manda correo
        try:
            doc = db.collection(u'usuarios').document(planta1.id).get()
            correo = doc.to_dict()[u'correo']
            print(u"Se enviará correo a: "+correo)
            mandarCorreo(correo)
        except google.cloud.exceptions.NotFound:
            print(u'Missing data')
        GPIO.output(planta3.pinOut, GPIO.LOW)

# Añadir un detecto de eventos por cada una de las plantas.
GPIO.add_event_detect(planta1.pinIn, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(planta1.pinIn, callbackA)

GPIO.add_event_detect(planta2.pinIn, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(planta2.pinIn, callbackB)

GPIO.add_event_detect(planta3.pinIn, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(planta3.pinIn, callbackC)

while True:
    time.sleep(1)