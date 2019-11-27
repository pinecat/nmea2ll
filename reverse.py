import RPi.GPIO as GPIO
import time

mode = GPIO.getmode()

GPIO.setmode(GPIO.BCM)

GPIO.setup(20, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

GPIO.output(20, GPIO.HIGH)
GPIO.output(19, GPIO.HIGH)
time.sleep(3)
GPIO.output(20, GPIO.LOW)
GPIO.output(19, GPIO.LOW)

GPIO.cleanup()
