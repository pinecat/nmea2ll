import RPi.GPIO as GPIO
import time

mode = GPIO.getmode()

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

pwm1=GPIO.PWM(21, 100)
pwm2=GPIO.PWM(26, 100)

pwm1.start(80)
pwm2.start(80)

time.sleep(5)

pwm1.ChangeDutyCycle(50)
pwm2.ChangeDutyCycle(50)

time.sleep(5)

pwm1.stop()
pwm2.stop()

#GPIO.output(21, GPIO.HIGH)
#GPIO.output(26, GPIO.HIGH)
#time.sleep(3)
#GPIO.output(21, GPIO.LOW)
#GPIO.output(26, GPIO.LOW)

GPIO.cleanup()
