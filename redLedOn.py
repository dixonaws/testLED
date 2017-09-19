import RPi.GPIO as GPIO
import time

def LEDon(intPIN):
	GPIO.output(intPIN, GPIO.HIGH)

def LEDoff(intPIN):
	GPIO.output(intPIN, GPIO.LOW)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)

redLEDPin=21

print "Red LED on"
LEDon(redLEDPin)

