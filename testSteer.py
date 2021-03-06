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

#PWM frequentie in herz
PWMFreq = 100

#Delay voor PWM opbouw/afbraak in ms
PWMDelay = 1000
PWMDelayCounter = 0;

#Boolean of de opbouw curve al is uitgevoerd
buildupPWM = false

#Variabele voor de waarde van de X-as op de acceleratie meter
xVar = 0

#Initialiseer de wii afstandsbediening
wiimote = cwiid.Wiimote()

#Boolean om het script te stoppen als er een wii remote error voorkomt
NoError = true

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

#Maak er PWM objecten van met een 
p1 = GPIO.PWM(Motor1F, PWMFreq)
p2 = GPIO.PWM(Motor1R, PWMFreq)
p3 = GPIO.PWM(Motor2F, PWMFreq)
p4 = GPIO.PWM(Motor2R, PWMFreq)

#Blanco PWM waarden voor de motors
p1_val = 0
p2_val = 0
p3_val = 0
p4_val = 0


#Start het PWM signaal op een Duty cycle van 0%
p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)

#Functie om alle pins op een Duty c. van 0% te zetten
def allOff():
  p1.ChangeDutyCycle(0)
  p2.ChangeDutyCycle(0)
  p3.ChangeDutyCycle(0)
  p4.ChangeDutyCycle(0)
  
def writeMotors(m1, m2, m3, m4):
  p1.ChangeDutyCycle(m1)
  p2.ChangeDutyCycle(m2)
  p3.ChangeDutyCycle(m3)
  p4.ChangeDutyCycle(m4)
  
#Ga van 0 naar 100% in in lineair verband
def workTowardsPWMUp(totalDelay, currentPWM):
  #initialiseer return variabele
  ret = 0
  
  #kijk of we nog een keer moeten optellen
  if PWMDelayCounter < totalDelay:
    #Tel er een stapje bij op, rond het af en geef het mee aan ret
    extraOptellen = totalPerc / totalDelay
	ret = round(currentPWM + extraOptellen, 1)
  else:
    #Zo niet, return meteen de huidige PWM
    ret = currentPWM
  return ret

#Ga van 0 naar 100% met een boogje. Naarmate de 100% genaderd wordt elke iteratie minder optellen
def workTowardsPWMUpCurve(totalDelay, currentPWM):
  #initialiseer return variabele
  ret = 0
  
  #Bereken het percentage dat we nog te gaan hebben
  basePerc = 100 - currentPWM

  #Als de timer nog niet over is
  if PWMDelayCounter < totalDelay:
    #Bereken wat we moeten optellen, tel dat op en rond het af
    #Geef het vervolgens mee aan ret
    extraOptellen = basePerc / totalDelay
	ret = round(currentPWM + extraOptellen, 1)
  else:
    #Zo niet, return dan gelijk de huidige PWM
    ret = currentPWM
  return ret


#Zolang er geen errors ontstaan, doe loopen
while NoError == True:
  #Lees de knoppen van de remote uit
  btnVar = wiimote.state['buttons']

  print("X: " + str(wiimote.state['acc'][1]) + " b: " + str(wiimote.state['buttons']))
  
  #Sla de waarden van de X-as op en maak er een percentage van
  #Waardes liggen tussen ~98 en ~150. dat geeft 50 graden om mee te werken
  xVar = wiimote.state['acc'][1] - 98
  xPerc = xVar * 2
  
  #Percentage wordt soms >100 of <0. Uitvlakken dus
  if xPerc > 100:
    xPerc = 100
  elif xPerc < 0:
    xPerc = 0
	
  #initialiseer variabelen
  x1 = 0
  x2 = 0
  
  if xPerc > 0 and xPerc < 50:
    #Als de remote naar rechts is gedraaid
	#linker motor 100%, rechter de helft van xPerc
    x1 = 100
    x2 = round(xPerc/2)
  elif xPerc > 50 and xPerc < 100:
    #Als de remote naar links is gedraaid
	#linker motor de helft van xPerc, rechter 100%
    x1 = 100-xPerc
    x2 = 100
  if btnVar == 1:
    #Als de 2-knop is ingedrukt : FORWARD
	
	#Reverse motors UIT, x1 en x2 op de forward motors
	writeMotors(x1, 0, x2, 0)
    print("xPerc - 1 is "+str(xPerc))
  elif btnVar == 2:
    #als de 1-knop is ingedrukt: REVERSE
	
	#x1 en x2 op de reverse motors en forward motors UIT
	writeMotors(0, x1, 0, x2)
  elif btnVar == 0:
    #Als geen enkele knop is ingedrukt: STOP
    allOff()
  else:
    #In elk ander geval: STOP 
    allOff()