import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#echo-grey pin 17
#echo-blue pin 6
#trigger-purple pin 18
#trigger-green pin 12

GPIO_ECHO1 = 17
GPIO_ECHO2 = 6
GPIO_TRIGGER1 = 18
GPIO_TRIGGER2 = 12

GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)

def distance():
	GPIO.output(GPIO_TRIGGER1, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER1, False)
	
	StartTime = time.time()
	StopTime = time.time()

	while GPIO.input(GPIO_ECHO1) == 0:
		StartTime = time.time()

	while GPIO.input(GPIO_ECHO1) == 1:
		StopTime = time.time()

	TimeElapsed = StartTime - StopTime

	distance = (TimeElapsed * 34300) / 2

	return distance

def distance2():
	GPIO.output(GPIO_TRIGGER2, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER2, False)

	StartTime = time.time()
	StopTime = time.time()

	while GPIO.input(GPIO_ECHO2) == 0:
		StartTime = time.time()	

	while GPIO.input(GPIO_ECHO2) == 1:
		StopTime = time.time()

	TimeElapsed = StartTime - StopTime

	distance = (TimeElapsed * 34300) / 2

	return distance

if __name__ == '__main__':
	try:
		while True:
			dist1 = distance()
			dist2 = distance2()
			print("Measured distance1 = %.1f cm" % dist1)
			print("Measured distance2 = %.1f cm" % dist2) 
			time.sleep(0.5)

	except KeyboardInterrupt:
		print("Stopped")
		GPIO.cleanup()
