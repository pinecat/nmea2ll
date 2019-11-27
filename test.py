import RPi.GPIO as GPIO
import time

def forward():
	pwm3.ChangeDutyCycle(0)
	pwm4.ChangeDutyCycle(0)

	pwm1.ChangeDutyCycle(90)
	pwm2.ChangeDutyCycle(90)

def reverse():
	pwm1.ChangeDutyCycle(0)
	pwm2.ChangeDutyCycle(0)

	pwm3.ChangeDutyCycle(75)
	pwm4.ChangeDutyCycle(75)

def stop():
	pwm1.stop()
	pwm2.stop()
	pwm3.stop()
	pwm4.stop()

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

GPIO.setup(20, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

GPIO.setup(16, GPIO.IN)

state = GPIO.input(16)

pwm1 = GPIO.PWM(21, 100)
pwm2 = GPIO.PWM(26, 100)

pwm3 = GPIO.PWM(20, 100)
pwm4 = GPIO.PWM(19, 100)

pwm1.start(0)
pwm2.start(0)

pwm3.start(0)
pwm4.start(0)

while 1:
	state = GPIO.input(16)
	if not state:
		break
time.sleep(1)

while 1:
	forward()
	state = GPIO.input(16)
	print(state)

	if not state:
		reverse()
		time.sleep(2)
		break

stop()

GPIO.cleanup()

