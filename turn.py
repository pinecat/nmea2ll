import RPi.GPIO as GPIO
import time

mode = GPIO.getmode()

GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

def left():
	GPIO.output(27, GPIO.LOW)
	GPIO.output(22, GPIO.HIGH)
	time.sleep(0.25)
	GPIO.output(22, GPIO.LOW)
	GPIO.output(27, GPIO.LOW)

def right():
	GPIO.output(22, GPIO.LOW)
	GPIO.output(27, GPIO.HIGH)
	GPIO.output(22, GPIO.HIGH)
	time.sleep(0.25)
	GPIO.output(27, GPIO.LOW)
	GPIO.output(22, GPIO.LOW)


right()
