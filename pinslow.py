import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

GPIO.output(20, GPIO.LOW)
GPIO.output(21, GPIO.LOW)
GPIO.output(26, GPIO.LOW)
GPIO.output(19, GPIO.LOW)

GPIO.cleanup()
