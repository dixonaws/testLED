import RPi.GPIO as GPIO
import time

def LEDoff(intPIN):
	GPIO.output(intPIN, GPIO.LOW)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

greenLEDPin=18

print "Green LED off"
LEDoff(greenLEDPin)

