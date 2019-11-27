#!/bin/python3
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)

x = 0

while(x < 1):
	GPIO.output(20, True)
	time.sleep(1.0)
	GPIO.output(20, False)
	time.sleep(1.0)
	x = x + 1	
