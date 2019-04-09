#!/usr/bin/python
import cwiid
import time
import array
import RPi.GPIO as GPIO
#Imports om de elementen te laten werken

#ser = serial.Serial('/dev/ttyUSB0')

#Initialiseer de GPIO pins op de Raspberry
Motor1F = 2   #Motor 1 forward
Motor1R = 3   #Motor 1 reverse
Motor2F = 4   #Motor 2 forward
Motor2R = 14  #Motor 2 reverse

#Initialiseer de wii afstandsbediening
wiimote = cwiid.Wiimote()

#stel de report modus in op Acceleratie en op buttons
wiimote.rpt_mode = cwiid.RPT_ACC | cwiid.RPT_BTN

#Pins setup
#gebruik standaard Broadcom GPIO layout
#(Dus zoals elke afbeelding op Google de layout weergeeft)
GPIO.setmode(GPIO.BCM)

#foutmeldingen wegdrukken
GPIO.setwarnings(False)

#Initialiseer de pins als output
GPIO.setup(Motor1F,GPIO.OUT)
GPIO.setup(Motor1R,GPIO.OUT)
GPIO.setup(Motor2F,GPIO.OUT)
GPIO.setup(Motor2R,GPIO.OUT)

#Functie om alle pins op low te zetten
def allOff():
  GPIO.output(Motor1F,GPIO.LOW)
  GPIO.output(Motor1R,GPIO.LOW)
  GPIO.output(Motor2F,GPIO.LOW)
  GPIO.output(Motor2R,GPIO.LOW)


while True:
  #Lees de knoppen van de remote uit
  btnVar = wiimote.state['buttons']
  
  #print(wiimote.state['acc'][1])
  print("X: " + str(wiimote.state['acc'][1]) + " b: " + str(wiimote.state['buttons']))
  
  if btnVar == 2048:
	#Links
    allOff()
    GPIO.output(Motor1F,GPIO.HIGH)
    GPIO.output(Motor2R,GPIO.HIGH)
  elif btnVar == 1024:
    #Rechts
    allOff()
    GPIO.output(Motor2F,GPIO.HIGH)
    GPIO.output(Motor1R,GPIO.HIGH)
  elif btnVar == 1:
    #Achteruit
    allOff()
    GPIO.output(Motor1F,GPIO.HIGH)
    GPIO.output(Motor2F,GPIO.HIGH)
  elif btnVar == 2:
    #Vooruit
    allOff()
    GPIO.output(Motor1R,GPIO.HIGH)
    GPIO.output(Motor2R,GPIO.HIGH)
  elif btnVar == 0:
	#Geen enkele knop
	allOff()
  else:
    #Anders
    allOff()
    