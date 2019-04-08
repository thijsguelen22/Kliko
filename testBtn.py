#!/usr/bin/python
import cwiid
import time
import array
import RPi.GPIO as GPIO

#ser = serial.Serial('/dev/ttyUSB0')

Motor1F = 2
Motor1R = 3
Motor2F = 4
Motor2R = 14

wiimote = cwiid.Wiimote()
wiimote.rpt_mode = cwiid.RPT_ACC | cwiid.RPT_BTN

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Motor1F,GPIO.OUT)
GPIO.setup(Motor1R,GPIO.OUT)
GPIO.setup(Motor2F,GPIO.OUT)
GPIO.setup(Motor2R,GPIO.OUT)

def allOff():
  GPIO.output(Motor1F,GPIO.LOW)
  GPIO.output(Motor1R,GPIO.LOW)
  GPIO.output(Motor2F,GPIO.LOW)
  GPIO.output(Motor2R,GPIO.LOW)


while True:
  btnVar = wiimote.state['buttons']
  #print(wiimote.state['acc'][1])
  print("X: " + str(wiimote.state['acc'][1]) + " b: " + str(wiimote.state['buttons']))
  if btnVar == 2048:
    allOff()
    GPIO.output(Motor1F,GPIO.HIGH)
    GPIO.output(Motor2R,GPIO.HIGH)
  elif btnVar == 1024:
    allOff()
    GPIO.output(Motor2F,GPIO.HIGH)
    GPIO.output(Motor1R,GPIO.HIGH)
  elif btnVar == 1:
    allOff()
    GPIO.output(Motor1F,GPIO.HIGH)
    GPIO.output(Motor2F,GPIO.HIGH)
  elif btnVar == 2:
    allOff()
    GPIO.output(Motor1R,GPIO.HIGH)
    GPIO.output(Motor2R,GPIO.HIGH)
  elif btnVar == 0:
    