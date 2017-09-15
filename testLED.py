import RPi.GPIO as GPIO
import time

def LEDon(intPIN):
	GPIO.output(intPIN, GPIO.HIGH)

def LEDoff(intPIN):
	GPIO.output(intPIN, GPIO.LOW)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

greenLEDPin=18
redLEDPin=21

print "Green LED on"
LEDon(greenLEDPin)
time.sleep(1)
print "Green LED off"
LEDoff(greenLEDPin)

print "Red LED on"
LEDon(redLEDPin)
time.sleep(1)
print "Red LED off"
LEDoff(redLEDPin)

